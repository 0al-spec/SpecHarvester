from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib
import yaml
from jsonschema import Draft202012Validator

from spec_harvester.ai_semantic_author_schema import load_ai_semantic_author_schema
from spec_harvester.interface_index import validate_public_interface_index
from spec_harvester.outcome_purpose_anchors import build_outcome_purpose_anchors
from spec_harvester.relevant_intent_routing import validate_relevant_intent_catalog
from spec_harvester.semantic_product_profile import (
    PROFILE_FILENAME,
    validate_semantic_product_profile,
)

INPUT_PACK_API_VERSION = "spec-harvester.ai-semantic-author-input-pack/v0"
INPUT_PACK_KIND = "SpecHarvesterAISemanticAuthorInputPack"


@dataclass(frozen=True)
class SemanticAuthorInputPackOptions:
    document_paths: tuple[str, ...] = ()
    max_evidence_items: int = 16
    max_total_bytes: int = 96 * 1024
    max_document_bytes: int = 24 * 1024
    max_observed_intents: int = 64


def build_semantic_author_input_pack(
    candidate_workspace: Path,
    observed_intent_catalog: dict[str, Any],
    *,
    options: SemanticAuthorInputPackOptions | None = None,
) -> dict[str, Any]:
    """Build a deterministic, evidence-only P55 request pack from local artifacts."""
    workspace = candidate_workspace.resolve()
    if not workspace.is_dir():
        raise ValueError(f"Candidate workspace does not exist: {candidate_workspace}")
    options = options or SemanticAuthorInputPackOptions()
    _validate_options(options)

    candidate = _read_yaml(workspace, "specpm.yaml")
    if candidate.get("kind") != "SpecPackage" or candidate.get("preview_only") is not True:
        raise ValueError("specpm.yaml must be a preview-only SpecPackage")
    candidate_id = candidate.get("metadata", {}).get("id")
    if not isinstance(candidate_id, str) or not candidate_id:
        raise ValueError("specpm.yaml metadata.id must be non-empty")

    evidence: list[dict[str, Any]] = []
    _append_file(evidence, workspace, "specpm.yaml", "validated_candidate_yaml", options)
    for path in sorted((workspace / "specs").glob("*.spec.yaml")):
        relative = path.relative_to(workspace).as_posix()
        spec = _read_yaml(workspace, relative)
        if spec.get("kind") != "BoundarySpec":
            raise ValueError(f"{relative} must be a BoundarySpec")
        _append_file(evidence, workspace, relative, "validated_candidate_yaml", options)

    harvest = _read_json(workspace, "harvest.json")
    if not isinstance(harvest, dict):
        raise ValueError("harvest.json must be an object")
    _append_file(evidence, workspace, "harvest.json", "harvested_repository_metadata", options)

    interface_path = workspace / "public-interface-index.json"
    if interface_path.exists():
        if interface_path.is_symlink():
            raise ValueError("public-interface-index.json must not be a symlink")
        validate_public_interface_index(_read_json(workspace, "public-interface-index.json"))
        _append_file(
            evidence, workspace, "public-interface-index.json", "public_interface_evidence", options
        )

    profile: dict[str, Any] | None = None
    profile_path = workspace / PROFILE_FILENAME
    if profile_path.exists():
        profile = _read_json(workspace, PROFILE_FILENAME)
        validate_semantic_product_profile(profile)
        _validate_profile_workspace_bindings(workspace, profile)
        _append_file(
            evidence,
            workspace,
            PROFILE_FILENAME,
            "deterministic_semantic_product_profile",
            options,
        )

    if profile is not None and profile["package"].get("manifestSha256"):
        _append_file(
            evidence,
            workspace,
            profile["package"]["manifestPath"],
            "pinned_package_manifest",
            options,
        )
    document_paths = tuple(
        dict.fromkeys(
            (
                *options.document_paths,
                *(document["evidencePath"] for document in (profile or {}).get("documents", [])),
            )
        )
    )
    for path in document_paths:
        _append_file(evidence, workspace, path, "allowlisted_source_documentation", options)

    observed_intents, catalog_binding = _validate_catalog(observed_intent_catalog, options)
    intent_routing = observed_intent_catalog.get("routing")
    if intent_routing is not None:
        if profile is None:
            raise ValueError("relevant observed intent routing requires a semantic product profile")
        validate_relevant_intent_catalog(observed_intent_catalog, profile)
    evidence.append(catalog_binding)
    if len(evidence) > options.max_evidence_items:
        raise ValueError("semantic author input pack evidence item budget exceeded")

    total_bytes = sum(item["byteCount"] for item in evidence)
    if total_bytes > options.max_total_bytes:
        raise ValueError("semantic author input pack byte budget exceeded")
    source_bundle_sha256 = _source_bundle_digest(evidence)
    for item in evidence:
        item["sourceBundleSha256"] = source_bundle_sha256

    request = {
        "apiVersion": "spec-harvester.ai-semantic-author-request/v0",
        "kind": "SpecHarvesterAISemanticAuthorRequest",
        "schemaVersion": 1,
        "authority": "semantic_author_request_evidence_only",
        "candidateId": candidate_id,
        "sourceBundleSha256": source_bundle_sha256,
        "evidence": [_binding(item) for item in evidence],
    }
    schema = load_ai_semantic_author_schema()
    validator = Draft202012Validator(schema)
    validator.validate(request)
    for observed in observed_intents:
        validator.validate(observed)

    result = {
        "apiVersion": INPUT_PACK_API_VERSION,
        "kind": INPUT_PACK_KIND,
        "schemaVersion": 1,
        "authority": "semantic_author_input_pack_evidence_only",
        "candidateId": candidate_id,
        "sourceBundleSha256": source_bundle_sha256,
        "budget": {
            "maxEvidenceItems": options.max_evidence_items,
            "maxTotalBytes": options.max_total_bytes,
            "maxDocumentBytes": options.max_document_bytes,
            "evidenceItemCount": len(evidence),
            "totalBytes": total_bytes,
        },
        "request": request,
        "observedIntents": observed_intents,
        "evidence": evidence,
        "executionBoundary": {
            "providerInvoked": False,
            "repositoryCodeExecuted": False,
            "packageManagerInvoked": False,
            "adapterExecuted": False,
            "materializationPerformed": False,
        },
    }
    if intent_routing is not None:
        result["intentRouting"] = json.loads(json.dumps(intent_routing))
    if profile is not None:
        purpose_anchors = build_outcome_purpose_anchors(
            profile,
            evidence,
            candidate_id=candidate_id,
            source_bundle_sha256=source_bundle_sha256,
        )
        result["outcomePurposeAnchors"] = purpose_anchors
    return result


def _validate_options(options: SemanticAuthorInputPackOptions) -> None:
    if (
        min(
            options.max_evidence_items,
            options.max_total_bytes,
            options.max_document_bytes,
            options.max_observed_intents,
        )
        <= 0
    ):
        raise ValueError("semantic author input pack budgets must be positive")


def validate_semantic_author_input_pack_integrity(pack: dict[str, Any]) -> None:
    """Fail closed when a persisted input pack no longer matches its evidence."""
    evidence = pack.get("evidence")
    source_bundle_sha256 = pack.get("sourceBundleSha256")
    request = pack.get("request")
    if (
        not isinstance(evidence, list)
        or not evidence
        or not isinstance(source_bundle_sha256, str)
        or not isinstance(request, dict)
    ):
        raise ValueError("semantic author input pack integrity is malformed")
    identifiers: set[str] = set()
    bindings: list[dict[str, str]] = []
    for item in evidence:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("id"), str)
            or item["id"] in identifiers
            or not isinstance(item.get("content"), str)
            or not isinstance(item.get("byteCount"), int)
            or item["byteCount"] < 0
            or not isinstance(item.get("sha256"), str)
            or item.get("sourceBundleSha256") != source_bundle_sha256
            or hashlib.sha256(item["content"].encode()).hexdigest() != item["sha256"]
            or len(item["content"].encode()) != item["byteCount"]
        ):
            raise ValueError("semantic author input pack evidence binding is stale")
        identifiers.add(item["id"])
        try:
            bindings.append(_binding(item))
        except KeyError as exc:
            raise ValueError("semantic author input pack evidence binding is malformed") from exc
    if _source_bundle_digest(evidence) != source_bundle_sha256:
        raise ValueError("semantic author input pack source bundle is stale")
    if (
        request.get("candidateId") != pack.get("candidateId")
        or request.get("sourceBundleSha256") != source_bundle_sha256
    ):
        raise ValueError("semantic author input pack request is malformed")
    if request.get("evidence") != bindings:
        raise ValueError("semantic author input pack request evidence is stale")
    _validate_profile_document_authority(pack, evidence)


def _validate_profile_document_authority(
    pack: dict[str, Any], evidence: list[dict[str, Any]]
) -> None:
    profile_records = [
        item for item in evidence if item.get("class") == "deterministic_semantic_product_profile"
    ]
    if not profile_records:
        return
    if len(profile_records) != 1:
        raise ValueError("semantic author input pack product profile is malformed")
    try:
        profile = json.loads(profile_records[0]["content"])
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("semantic author input pack product profile is malformed") from exc
    validate_semantic_product_profile(profile)
    if profile.get("package", {}).get("candidateId") != pack.get("candidateId"):
        raise ValueError("semantic author input pack product profile is stale")
    documentation = {
        (item.get("sourcePath"), item.get("sha256"), item.get("byteCount"))
        for item in evidence
        if item.get("class") == "allowlisted_source_documentation"
    }
    for document in profile["documents"]:
        binding = (
            document.get("evidencePath"),
            document.get("sha256"),
            document.get("byteCount"),
        )
        if binding not in documentation:
            raise ValueError("semantic author input pack product profile document is stale")
    provenance = profile["package"].get("descriptionProvenance")
    if provenance is not None:
        manifest = next(
            (
                item
                for item in evidence
                if item.get("class") == "pinned_package_manifest"
                and item.get("sourcePath") == provenance.get("sourcePath")
                and item.get("sha256") == provenance.get("sha256")
            ),
            None,
        )
        description = profile["package"]["description"].strip()
        if not isinstance(manifest, dict) or _manifest_description(manifest) != description:
            raise ValueError("semantic author input pack product profile manifest is stale")


def _manifest_description(manifest: dict[str, Any]) -> str:
    try:
        path = Path(manifest["sourcePath"])
        content = manifest["content"]
        value = json.loads(content) if path.suffix == ".json" else tomllib.loads(content)
    except (KeyError, TypeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return ""
    if not isinstance(value, dict):
        return ""
    package = value.get("package") if isinstance(value.get("package"), dict) else {}
    project = value.get("project") if isinstance(value.get("project"), dict) else {}
    tool = value.get("tool") if isinstance(value.get("tool"), dict) else {}
    poetry = tool.get("poetry") if isinstance(tool.get("poetry"), dict) else {}
    metadata = next((item for item in (project, package, poetry, value) if item), {})
    description = metadata.get("description")
    return description.strip() if isinstance(description, str) else ""


def _safe_path(path: str) -> str:
    candidate = Path(path)
    if not path or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe evidence path: {path}")
    return candidate.as_posix()


def _workspace_file(workspace: Path, relative: str) -> Path:
    path = workspace
    for component in Path(_safe_path(relative)).parts:
        path /= component
        if path.is_symlink():
            raise ValueError(f"allowlisted evidence file is unavailable: {relative}")
    if not path.is_file() or workspace not in path.resolve().parents:
        raise ValueError(f"allowlisted evidence file is unavailable: {relative}")
    return path


def _read_yaml(workspace: Path, relative: str) -> dict[str, Any]:
    try:
        value = yaml.safe_load(_workspace_file(workspace, relative).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read YAML evidence {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML evidence {relative} must be an object")
    return value


def _read_json(workspace: Path, relative: str) -> Any:
    try:
        return json.loads(_workspace_file(workspace, relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON evidence {relative}: {exc}") from exc


def _append_file(
    evidence: list[dict[str, Any]],
    workspace: Path,
    relative: str,
    evidence_class: str,
    options: SemanticAuthorInputPackOptions,
) -> None:
    path = _workspace_file(workspace, relative)
    file_size = path.stat().st_size
    remaining_bytes = options.max_total_bytes - sum(item["byteCount"] for item in evidence)
    if file_size > remaining_bytes:
        raise ValueError(f"evidence exceeds remaining byte budget: {relative}")
    if (
        evidence_class == "allowlisted_source_documentation"
        and file_size > options.max_document_bytes
    ):
        raise ValueError(f"documentation evidence exceeds byte budget: {relative}")
    raw = path.read_bytes()
    evidence.append(
        {
            "id": f"evidence_{len(evidence) + 1}",
            "class": evidence_class,
            "sourcePath": _safe_path(relative),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "byteCount": len(raw),
            "content": raw.decode("utf-8", errors="strict"),
            "untrusted": evidence_class
            in {
                "allowlisted_source_documentation",
                "deterministic_semantic_product_profile",
            },
        }
    )


def _validate_profile_workspace_bindings(workspace: Path, profile: dict[str, Any]) -> None:
    source_bindings = profile["sourceBindings"]
    harvest_bindings = [
        item for item in source_bindings if item.get("sourcePath") == "harvest.json"
    ]
    if len(harvest_bindings) != 1:
        raise ValueError("semantic product profile harvest binding is malformed")
    _verify_profile_workspace_file(
        workspace,
        "harvest.json",
        harvest_bindings[0]["sha256"],
    )
    for document in profile["documents"]:
        _verify_profile_workspace_file(
            workspace,
            document["evidencePath"],
            document["sha256"],
            expected_byte_count=document["byteCount"],
        )
    manifest_sha256 = profile["package"].get("manifestSha256")
    if manifest_sha256 is not None:
        _verify_profile_workspace_file(
            workspace,
            profile["package"]["manifestPath"],
            manifest_sha256,
        )


def _verify_profile_workspace_file(
    workspace: Path,
    relative: str,
    expected_sha256: str,
    *,
    expected_byte_count: int | None = None,
) -> None:
    raw = _workspace_file(workspace, relative).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256 or (
        expected_byte_count is not None and len(raw) != expected_byte_count
    ):
        raise ValueError(f"semantic product profile evidence binding is stale: {relative}")


def _validate_catalog(
    catalog: dict[str, Any], options: SemanticAuthorInputPackOptions
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path, digest, intents = catalog.get("sourcePath"), catalog.get("sha256"), catalog.get("intents")
    if (
        not isinstance(path, str)
        or not isinstance(digest, str)
        or len(digest) != 64
        or not isinstance(intents, list)
    ):
        raise ValueError("observed intent catalog is malformed")
    if len(intents) > options.max_observed_intents:
        raise ValueError("observed intent catalog item budget exceeded")
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for item in intents:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("intentId"), str)
            or not isinstance(item.get("sha256"), str)
        ):
            raise ValueError("observed intent catalog item is malformed")
        intent_id = item["intentId"]
        if intent_id in seen:
            raise ValueError("observed intent catalog has duplicate intent ID")
        seen.add(intent_id)
        records.append(
            {
                "apiVersion": "spec-harvester.ai-semantic-observed-intent/v0",
                "kind": "SpecHarvesterAISemanticObservedIntent",
                "schemaVersion": 1,
                "state": "observed",
                "intentId": intent_id,
                "observedIntentSha256": item["sha256"],
            }
        )
    catalog_content = {key: value for key, value in catalog.items() if key != "sha256"}
    raw = json.dumps(catalog_content, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError("observed intent catalog digest is stale")
    return records, {
        "id": "observed_intent_catalog",
        "class": "specpm_observed_intent_catalog",
        "sourcePath": _safe_path(path),
        "sha256": digest,
        "byteCount": len(raw),
        "content": raw.decode("utf-8"),
        "untrusted": False,
    }


def _source_bundle_digest(evidence: list[dict[str, Any]]) -> str:
    bindings = [
        {key: item[key] for key in ("id", "class", "sourcePath", "sha256", "byteCount")}
        for item in evidence
    ]
    return hashlib.sha256(
        json.dumps(bindings, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _binding(item: dict[str, Any]) -> dict[str, str]:
    return {key: item[key] for key in ("id", "class", "sourcePath", "sha256", "sourceBundleSha256")}
