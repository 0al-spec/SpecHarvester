from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from spec_harvester.candidate_review_schema import load_candidate_review_schema
from spec_harvester.local_specpm_intake_bridge import (
    DEFAULT_SPECPM_TIMEOUT_SECONDS,
    MAX_SPECPM_REPORT_BYTES,
    _normalized_specpm_report,
    _run_specpm_validation,
)
from spec_harvester.portable_semantic_proposal import validate_portable_semantic_proposal
from spec_harvester.semantic_review import validate_semantic_reviewer_edit
from spec_harvester.specpm_manifest import SpecPackageManifest

MAX_CANDIDATE_FILES = 64
MAX_CANDIDATE_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class SemanticMaterializationOptions:
    candidate: Path
    semantic_record: Path
    review_decision: Path
    output: Path
    specpm_command: str = "specpm"
    specpm_pythonpath: str | None = None
    specpm_timeout_seconds: int = DEFAULT_SPECPM_TIMEOUT_SECONDS
    max_specpm_report_bytes: int = MAX_SPECPM_REPORT_BYTES


def _json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate_files(root: Path) -> list[Path]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Semantic materialization candidate must be a regular directory")
    resolved_root = root.resolve()
    specs = root / "specs"
    if specs.is_symlink():
        raise ValueError("Semantic materialization candidate contains a symlinked specs directory")
    files = sorted(
        [root / "specpm.yaml", *root.glob("specs/*.spec.yaml")],
        key=lambda path: path.relative_to(root).as_posix(),
    )
    if not files or not files[0].is_file():
        raise ValueError("Semantic materialization candidate has no specpm.yaml")
    if len(files) > MAX_CANDIDATE_FILES:
        raise ValueError("Semantic materialization candidate exceeds file limit")
    total = 0
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValueError("Semantic materialization candidate contains an unsafe file")
        try:
            path.resolve(strict=True).relative_to(resolved_root)
        except (OSError, ValueError) as exc:
            raise ValueError("Semantic materialization candidate file escapes its root") from exc
        total += path.stat().st_size
    if total > MAX_CANDIDATE_BYTES:
        raise ValueError("Semantic materialization candidate exceeds byte limit")
    return files


def _validate_output_boundary(candidate: Path, output: Path) -> None:
    if output.is_symlink():
        raise ValueError("Semantic materialization output must not be a symlink")
    candidate_path = candidate.resolve(strict=False)
    output_path = output.resolve(strict=False)
    if (
        candidate_path == output_path
        or candidate_path in output_path.parents
        or output_path in candidate_path.parents
    ):
        raise ValueError("Semantic materialization output overlaps the source candidate")


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Cannot read candidate YAML: {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Candidate YAML must be an object: {path.name}")
    return value


def _selected_claims(
    record: dict[str, Any], reviewer_edit: dict[str, Any]
) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    accepted = set(reviewer_edit["acceptedOrEditedClaimIds"])
    edits = {item["claimId"]: item["text"] for item in reviewer_edit.get("editedClaims", [])}
    claims: dict[str, list[dict[str, Any]]] = {}
    for source in record["proposal"]["claims"]:
        if source["id"] not in accepted:
            continue
        claim = dict(source)
        claim["text"] = edits.get(source["id"], source["text"])
        claims.setdefault(source["kind"], []).append(claim)
    return claims, sorted(accepted)


def _append_unique(target: list[Any], values: list[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _selected_intents(
    record: dict[str, Any], selected_claim_ids: set[str]
) -> tuple[list[str], list[str]]:
    reused: list[str] = []
    experimental: list[str] = []
    for decision in record["proposal"]["intentDecisions"]:
        if decision["state"] == "proposed_reuse":
            if decision["rationaleClaimId"] in selected_claim_ids:
                reused.append(decision["intentId"])
        elif decision["userNeedClaimId"] in selected_claim_ids:
            experimental.append(decision["intentId"])
    return sorted(set(reused)), sorted(set(experimental))


def _apply_semantics(
    root: Path, record: dict[str, Any], reviewer_edit: dict[str, Any]
) -> dict[str, Any]:
    manifest_path = root / "specpm.yaml"
    manifest = _load_yaml(manifest_path)
    boundaries = [(path, _load_yaml(path)) for path in sorted(root.glob("specs/*.spec.yaml"))]
    claims, selected_ids = _selected_claims(record, reviewer_edit)
    purpose = claims.get("purpose", [])
    capabilities = claims.get("capability", [])
    interfaces = [claim["text"] for claim in claims.get("interface", [])]
    exclusions = [
        claim["text"]
        for kind in ("nearby_intent_difference", "non_goal")
        for claim in claims.get(kind, [])
    ]
    if purpose:
        metadata = manifest.setdefault("metadata", {})
        metadata["summary"] = purpose[0]["text"]

    selected_set = set(selected_ids)
    reused, experimental = _selected_intents(record, selected_set)
    intent_ids = [*reused, *experimental]
    provides = manifest.setdefault("index", {}).setdefault("provides", {})
    manifest_intents = provides.setdefault("intents", [])
    if not isinstance(manifest_intents, list):
        raise ValueError("Candidate manifest intent list is invalid")
    _append_unique(manifest_intents, intent_ids)

    capability_index = 0
    for _path, boundary in boundaries:
        if purpose:
            boundary.setdefault("intent", {})["summary"] = purpose[0]["text"]
        scope = boundary.setdefault("scope", {})
        included = scope.setdefault("includes", [])
        excluded = scope.setdefault("excludes", [])
        if not isinstance(included, list) or not isinstance(excluded, list):
            raise ValueError("Candidate BoundarySpec scope is invalid")
        _append_unique(included, interfaces)
        _append_unique(excluded, exclusions)
        capability_records = boundary.setdefault("provides", {}).setdefault("capabilities", [])
        if not isinstance(capability_records, list):
            raise ValueError("Candidate BoundarySpec capability list is invalid")
        for capability in capability_records:
            if not isinstance(capability, dict):
                raise ValueError("Candidate BoundarySpec capability is invalid")
            if capability_index < len(capabilities):
                capability["summary"] = capabilities[capability_index]["text"]
                capability_index += 1
            bound_intents = capability.setdefault("intentIds", [])
            if not isinstance(bound_intents, list):
                raise ValueError("Candidate capability intent list is invalid")
            _append_unique(bound_intents, intent_ids)

    manifest["preview_only"] = True
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    for path, boundary in boundaries:
        path.write_text(yaml.safe_dump(boundary, sort_keys=False), encoding="utf-8")
    return {
        "selectedClaimIds": selected_ids,
        "editedClaimIds": sorted(item["claimId"] for item in reviewer_edit.get("editedClaims", [])),
        "reusedIntentIds": reused,
        "experimentalIntentIds": experimental,
    }


def materialize_semantic_candidate(options: SemanticMaterializationOptions) -> dict[str, Any]:
    if options.specpm_timeout_seconds < 1:
        raise ValueError("SpecPM validation timeout must be positive")
    if not 1 <= options.max_specpm_report_bytes <= MAX_SPECPM_REPORT_BYTES:
        raise ValueError("SpecPM validation report byte limit is invalid")
    record = _json_object(options.semantic_record, "portable semantic proposal")
    decision = _json_object(options.review_decision, "semantic review decision")
    validate_portable_semantic_proposal(record)
    errors = list(
        Draft202012Validator(
            load_candidate_review_schema(), format_checker=FormatChecker()
        ).iter_errors(decision)
    )
    if errors or decision.get("kind") != "SpecHarvesterCandidateReviewDecision":
        message = errors[0].message if errors else "record kind is invalid"
        raise ValueError(f"Semantic review decision is invalid: {message}")
    reviewer_edit = decision.get("semanticReview")
    if not isinstance(reviewer_edit, dict):
        raise ValueError("Semantic review decision is missing")
    validate_semantic_reviewer_edit(reviewer_edit, record)
    if reviewer_edit["reviewer"] != decision["reviewer"]:
        raise ValueError("Semantic reviewer identity differs from candidate decision")
    if reviewer_edit["decision"] not in {"accepted", "edited"}:
        raise ValueError("Semantic materialization requires an accepted or edited decision")
    if decision["binding"]["candidateId"] != record["candidateId"]:
        raise ValueError("Semantic materialization candidate binding is stale")

    _validate_output_boundary(options.candidate, options.output)
    source_files = _candidate_files(options.candidate)
    source_manifest = SpecPackageManifest.from_path(options.candidate / "specpm.yaml")
    if source_manifest.package_id() != record["candidateId"]:
        raise ValueError("Semantic materialization manifest package identity is stale")
    before = {
        path.relative_to(options.candidate).as_posix(): _file_digest(path) for path in source_files
    }
    options.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".semantic-materialization-", dir=options.output.parent
    ) as temporary:
        revision = Path(temporary) / "candidate"
        revision.mkdir()
        for source in source_files:
            relative = source.relative_to(options.candidate)
            target = revision / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        application = _apply_semantics(revision, record, reviewer_edit)
        revision_manifest = SpecPackageManifest.from_path(revision / "specpm.yaml")
        if revision_manifest.package_id() != record["candidateId"]:
            raise ValueError("Materialized manifest package identity is stale")
        specpm = _normalized_specpm_report(
            _run_specpm_validation(
                revision,
                command=options.specpm_command,
                pythonpath=options.specpm_pythonpath,
                timeout_seconds=options.specpm_timeout_seconds,
                max_report_bytes=options.max_specpm_report_bytes,
            )
        )
        if specpm["status"] not in {"valid", "warning_only"}:
            raise ValueError("Materialized candidate failed read-only SpecPM validation")
        output_files = _candidate_files(revision)
        after = {path.relative_to(revision).as_posix(): _file_digest(path) for path in output_files}
        if before != {
            path.relative_to(options.candidate).as_posix(): _file_digest(path)
            for path in source_files
        }:
            raise ValueError("Semantic materialization modified the source candidate")
        report = {
            "apiVersion": "spec-harvester.semantic-materialization/v0",
            "kind": "SpecHarvesterSemanticMaterialization",
            "authority": "reviewer_controlled_preview_revision_evidence_only",
            "candidateId": record["candidateId"],
            "packetSha256": decision["binding"]["packetSha256"],
            "semanticRecordSha256": record["recordSha256"],
            "proposalSha256": record["proposalSha256"],
            "sourceBundleSha256": record["sourceBundleSha256"],
            "reviewerEditSha256": reviewer_edit["reviewerEditSha256"],
            "reviewer": reviewer_edit["reviewer"],
            "decision": reviewer_edit["decision"],
            "application": application,
            "files": {"before": before, "after": after},
            "validation": {
                "specHarvester": "passed",
                "specPM": specpm,
            },
            "previewOnly": True,
            "isRegistryTruth": False,
            "registryMutationCount": 0,
        }
        (Path(temporary) / "materialization-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if options.output.exists():
            shutil.rmtree(options.output)
        os.replace(temporary, options.output)
    return report
