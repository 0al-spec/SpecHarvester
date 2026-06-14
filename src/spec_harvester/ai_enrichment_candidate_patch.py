from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.producer_receipt import digest_record, sha256_file

AI_ENRICHMENT_CANDIDATE_PATCH_API_VERSION = "spec-harvester.ai-enrichment-candidate-patch/v0"
AI_ENRICHMENT_CANDIDATE_PATCH_KIND = "SpecHarvesterAIEnrichmentCandidatePatch"
AI_ENRICHMENT_CANDIDATE_PATCH_FILENAME = "ai-enrichment-candidate-patch.json"

NON_AUTHORITY = [
    "This patch is producer-side review evidence only.",
    "It applies a clean AI enrichment proposal into a copied preview candidate.",
    "It is not SpecPM registry acceptance.",
    "It is not maintainer approval.",
    "It is not upstream project endorsement.",
    "It must not remove preview_only or publish registry metadata.",
]


@dataclass(frozen=True)
class AIEnrichmentCandidatePatchOptions:
    proposal: Path
    candidate: Path
    output: Path
    package_id: str | None = None
    report: Path | None = None


def build_ai_enrichment_candidate_patch(
    options: AIEnrichmentCandidatePatchOptions,
) -> dict[str, Any]:
    source = options.candidate.resolve()
    output = options.output.resolve()
    if not source.is_dir():
        raise ValueError(f"Candidate directory does not exist: {source}")
    if output.exists():
        raise ValueError(f"Output directory already exists: {output}")
    if output == source or path_is_relative_to(output, source):
        raise ValueError("Output directory must not be inside the source candidate.")
    if options.report and path_is_relative_to(options.report.resolve(), source):
        raise ValueError("Report path must not be inside the source candidate.")

    proposal = read_json_object(options.proposal)
    selected = selected_proposal(proposal, options.package_id)
    package_id = string_value(selected.get("packageId"))
    validate_proposal(proposal, selected, package_id)
    source_manifest = read_yaml_object(source / "specpm.yaml")
    candidate_package_id = string_value(mapping_value(source_manifest.get("metadata")).get("id"))
    if candidate_package_id != package_id:
        raise ValueError(
            f"Candidate package id {candidate_package_id!r} does not match proposal "
            f"package id {package_id!r}."
        )

    before = candidate_digests(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, output)

    manifest_path = output / "specpm.yaml"
    manifest = read_yaml_object(manifest_path)
    spec_relative = first_spec_path(manifest)
    spec_path = output / spec_relative
    spec = read_yaml_object(spec_path)

    applied: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    apply_summary(manifest, spec, selected, applied, skipped)
    apply_capabilities(manifest, spec, selected, applied, skipped)
    apply_interfaces(spec, selected, applied, skipped)

    write_yaml_object(manifest_path, manifest)
    write_yaml_object(spec_path, spec)
    refresh_receipt(output)

    after = candidate_digests(output)
    report = {
        "apiVersion": AI_ENRICHMENT_CANDIDATE_PATCH_API_VERSION,
        "kind": AI_ENRICHMENT_CANDIDATE_PATCH_KIND,
        "schemaVersion": 1,
        "status": "prepared",
        "authority": "producer_preview_evidence_only",
        "subject": {
            "packageId": package_id,
            "sourceCandidate": str(source),
            "enrichedCandidate": str(output),
            "sourceMutated": False,
            "previewOnly": bool(manifest.get("preview_only")),
        },
        "inputs": [
            {
                "role": "ai_enrichment_proposal",
                "path": str(options.proposal),
                "digest": digest_record(sha256_file(options.proposal)),
            },
            {
                "role": "source_candidate_manifest",
                "path": "specpm.yaml",
                "digest": before.get("specpm.yaml"),
            },
            {
                "role": "source_candidate_boundary_spec",
                "path": spec_relative,
                "digest": before.get(spec_relative),
            },
        ],
        "proposal": proposal_summary(proposal, selected),
        "appliedChanges": applied,
        "skippedChanges": skipped,
        "digests": {
            "before": before,
            "after": after,
        },
        "nonAuthority": NON_AUTHORITY,
    }
    report_path = options.report or output / AI_ENRICHMENT_CANDIDATE_PATCH_FILENAME
    write_json_object(report_path, report)
    return report


def selected_proposal(report: dict[str, Any], package_id: str | None) -> dict[str, Any]:
    proposals = [item for item in list_value(report.get("proposals")) if isinstance(item, dict)]
    if not proposals:
        raise ValueError("AI enrichment proposal does not contain proposals[].")
    if package_id:
        for item in proposals:
            if item.get("packageId") == package_id:
                return item
        raise ValueError(f"AI enrichment proposal does not contain packageId {package_id!r}.")
    if len(proposals) != 1:
        raise ValueError("package_id is required when proposal contains multiple packages.")
    return proposals[0]


def validate_proposal(report: dict[str, Any], proposal: dict[str, Any], package_id: str) -> None:
    expected = {
        "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
        "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
        "schemaVersion": 1,
        "status": "completed",
        "authority": "proposal_only_not_registry_acceptance",
    }
    for key, value in expected.items():
        if report.get(key) != value:
            raise ValueError(f"AI enrichment proposal {key} must be {value!r}.")
    if proposal.get("status") != "proposed":
        raise ValueError(f"{package_id} proposal status must be 'proposed'.")
    if not string_value(proposal.get("refinedSummary")):
        raise ValueError(f"{package_id} proposal refinedSummary is required.")
    package_diagnostics = [
        item
        for item in list_value(report.get("diagnostics"))
        if isinstance(item, dict) and item.get("packageId") == package_id
    ]
    if package_diagnostics:
        codes = ", ".join(sorted({string_value(item.get("code")) for item in package_diagnostics}))
        raise ValueError(f"{package_id} proposal has unresolved diagnostics: {codes}")
    if not list_value(proposal.get("capabilities")):
        raise ValueError(f"{package_id} proposal must include at least one capability.")


def apply_summary(
    manifest: dict[str, Any],
    spec: dict[str, Any],
    proposal: dict[str, Any],
    applied: list[dict[str, Any]],
    _skipped: list[dict[str, Any]],
) -> None:
    refined = string_value(proposal.get("refinedSummary"))
    set_nested(manifest, ["metadata", "summary"], refined)
    set_nested(spec, ["intent", "summary"], refined)
    capabilities = list_value(mapping_value(spec.get("provides")).get("capabilities"))
    for capability in capabilities:
        if isinstance(capability, dict) and capability.get("role") == "primary":
            capability["summary"] = refined
            break
    applied.append({"field": "metadata.summary", "value": refined})
    applied.append({"field": "intent.summary", "value": refined})
    applied.append({"field": "provides.capabilities[primary].summary", "value": refined})


def apply_capabilities(
    manifest: dict[str, Any],
    spec: dict[str, Any],
    proposal: dict[str, Any],
    applied: list[dict[str, Any]],
    skipped: list[dict[str, Any]],
) -> None:
    proposed = [item for item in list_value(proposal.get("capabilities")) if isinstance(item, dict)]
    manifest_capabilities = ensure_list_path(manifest, ["index", "provides", "capabilities"])
    manifest_intents = ensure_list_path(manifest, ["index", "provides", "intents"])
    spec_capabilities = ensure_list_path(spec, ["provides", "capabilities"])
    existing = {
        item.get("id")
        for item in spec_capabilities
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    for capability in proposed:
        capability_id = string_value(capability.get("id"))
        summary = string_value(capability.get("summary"))
        intent_ids = [
            item for item in list_value(capability.get("intentIds")) if isinstance(item, str)
        ]
        evidence_paths = [
            item for item in list_value(capability.get("evidencePaths")) if isinstance(item, str)
        ]
        if not capability_id or not summary or not evidence_paths:
            skipped.append({"field": "capabilities", "id": capability_id, "reason": "incomplete"})
            continue
        if capability_id in existing:
            skipped.append(
                {"field": "capabilities", "id": capability_id, "reason": "already_present"}
            )
            continue
        spec_capabilities.append(
            {
                "id": capability_id,
                "role": "secondary",
                "summary": summary,
                "intentIds": intent_ids,
            }
        )
        append_unique(manifest_capabilities, capability_id)
        for intent_id in intent_ids:
            append_unique(manifest_intents, intent_id)
        add_evidence_support(spec, capability_id)
        existing.add(capability_id)
        applied.append(
            {
                "field": "provides.capabilities",
                "id": capability_id,
                "summary": summary,
                "intentIds": intent_ids,
                "evidencePaths": evidence_paths,
            }
        )


def apply_interfaces(
    spec: dict[str, Any],
    proposal: dict[str, Any],
    applied: list[dict[str, Any]],
    skipped: list[dict[str, Any]],
) -> None:
    proposed = [item for item in list_value(proposal.get("interfaces")) if isinstance(item, dict)]
    inbound = ensure_list_path(spec, ["interfaces", "inbound"])
    existing = {item.get("id"): item for item in inbound if isinstance(item, dict)}
    for interface in proposed:
        interface_id = string_value(interface.get("id"))
        summary = string_value(interface.get("summary"))
        kind = string_value(interface.get("kind"))
        evidence_paths = [
            item for item in list_value(interface.get("evidencePaths")) if isinstance(item, str)
        ]
        if not interface_id or not summary or not evidence_paths:
            skipped.append(
                {"field": "interfaces.inbound", "id": interface_id, "reason": "incomplete"}
            )
            continue
        if interface_id in existing:
            target = existing[interface_id]
            target["summary"] = summary
            if kind:
                target["kind"] = kind
            action = "updated"
        else:
            inbound.append(
                {
                    "id": interface_id,
                    "kind": kind or "library",
                    "summary": summary,
                    "source": "ai_enrichment_proposal",
                }
            )
            action = "added"
        applied.append(
            {
                "field": "interfaces.inbound",
                "id": interface_id,
                "action": action,
                "summary": summary,
                "kind": kind or "library",
                "evidencePaths": evidence_paths,
            }
        )


def add_evidence_support(spec: dict[str, Any], capability_id: str) -> None:
    support = f"provides.capabilities.{capability_id}"
    for evidence in list_value(spec.get("evidence")):
        if not isinstance(evidence, dict):
            continue
        supports = evidence.get("supports")
        if isinstance(supports, list) and "provides.capabilities" in supports:
            append_unique(supports, support)


def refresh_receipt(candidate: Path) -> None:
    path = candidate / "producer-receipt.json"
    if not path.is_file():
        return
    receipt = read_json_object(path)
    outputs = receipt.get("outputs")
    if isinstance(outputs, list):
        for output in outputs:
            if not isinstance(output, dict):
                continue
            relative = string_value(output.get("path"))
            target = candidate / relative
            if relative and target.is_file() and relative != "producer-receipt.json":
                output["digest"] = digest_record(sha256_file(target))
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def candidate_digests(root: Path) -> dict[str, dict[str, str]]:
    paths = ["specpm.yaml"]
    manifest = read_yaml_object(root / "specpm.yaml")
    paths.extend(manifest_spec_paths(manifest))
    if (root / "producer-receipt.json").is_file():
        paths.append("producer-receipt.json")
    return {
        path: digest_record(sha256_file(root / path))
        for path in sorted(set(paths))
        if (root / path).is_file()
    }


def first_spec_path(manifest: dict[str, Any]) -> str:
    paths = manifest_spec_paths(manifest)
    if not paths:
        raise ValueError("Candidate manifest must declare specs[].path.")
    return paths[0]


def manifest_spec_paths(manifest: dict[str, Any]) -> list[str]:
    specs = list_value(manifest.get("specs"))
    return [
        item["path"]
        for item in specs
        if isinstance(item, dict) and isinstance(item.get("path"), str) and item["path"]
    ]


def proposal_summary(report: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    provider = mapping_value(report.get("provider"))
    receipt = mapping_value(proposal.get("providerReceipt"))
    return {
        "packageId": proposal.get("packageId"),
        "refinedSummary": proposal.get("refinedSummary"),
        "capabilityCount": len(list_value(proposal.get("capabilities"))),
        "interfaceCount": len(list_value(proposal.get("interfaces"))),
        "overallConfidence": proposal.get("overallConfidence"),
        "provider": {
            "name": provider.get("name"),
            "model": provider.get("model"),
            "execution": provider.get("execution"),
            "responseDigest": receipt.get("responseDigest"),
        },
    }


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read JSON artifact {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON artifact {path}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return value


def write_json_object(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_yaml_object(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read YAML artifact {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML artifact must be an object: {path}")
    return value


def write_yaml_object(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def ensure_list_path(root: dict[str, Any], path: list[str]) -> list[Any]:
    current: dict[str, Any] = root
    for key in path[:-1]:
        value = current.get(key)
        if not isinstance(value, dict):
            value = {}
            current[key] = value
        current = value
    value = current.get(path[-1])
    if not isinstance(value, list):
        value = []
        current[path[-1]] = value
    return value


def set_nested(root: dict[str, Any], path: list[str], value: Any) -> None:
    current = root
    for key in path[:-1]:
        child = current.get(key)
        if not isinstance(child, dict):
            child = {}
            current[key] = child
        current = child
    current[path[-1]] = value


def append_unique(values: list[Any], value: Any) -> None:
    if value not in values:
        values.append(value)


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True
