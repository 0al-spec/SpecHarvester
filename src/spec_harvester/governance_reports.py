from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.promoter import parse_yaml_scalar
from spec_harvester.report_source_records import (
    ReportSourceIssuePolicy,
    SpecpmReportSourceRecords,
)

GOVERNANCE_DUPLICATE_REPORT_KIND = "SpecHarvesterGovernanceDuplicateClaimReport"
GOVERNANCE_DUPLICATE_REPORT_SCHEMA_VERSION = 1

TRUST_BOUNDARY_NOTES = [
    "Report generation summarizes existing `specpm.yaml` metadata only.",
    "No repository code execution, package installation, network access, or analyzer "
    "execution occurs.",
    "The report is advisory and does not change any package content.",
]


@dataclass(frozen=True)
class PackageClaimRecord:
    path: str
    source: str
    package_id: str
    package_version: str
    intents: tuple[str, ...]
    capabilities: tuple[str, ...]


def build_duplicate_claim_report(
    *,
    accepted_root: Path | None = None,
    candidates_root: Path | None = None,
) -> dict[str, Any]:
    if accepted_root is None and candidates_root is None:
        raise ValueError("At least one of accepted_root or candidates_root must be provided.")

    records, issues = collect_claim_records(accepted_root, candidates_root)
    duplicate_intents = duplicate_claims(records, "intents")
    duplicate_capabilities = duplicate_claims(records, "capabilities")

    return {
        "schemaVersion": GOVERNANCE_DUPLICATE_REPORT_SCHEMA_VERSION,
        "kind": GOVERNANCE_DUPLICATE_REPORT_KIND,
        "status": "partial" if issues else "ok",
        "summary": {
            "records": len(records),
            "duplicateIntentCount": len(duplicate_intents),
            "duplicateCapabilityCount": len(duplicate_capabilities),
            "issueCount": len(issues),
        },
        "records": [claim_record_to_dict(record) for record in records],
        "duplicates": {
            "intent": duplicate_intents,
            "capability": duplicate_capabilities,
        },
        "issues": issues,
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }


def collect_claim_records(
    accepted_root: Path | None,
    candidates_root: Path | None,
) -> tuple[list[PackageClaimRecord], list[dict[str, str]]]:
    return SpecpmReportSourceRecords(
        accepted_root=accepted_root,
        candidates_root=candidates_root,
        parse_manifest=parse_specpm_claims,
        issue_policy=ReportSourceIssuePolicy(
            symlink_message="Skip symlinked specpm.yaml in governance report scan.",
        ),
        sort_key=lambda item: (item.source, item.path),
    ).collect()


def claim_record_to_dict(record: PackageClaimRecord) -> dict[str, Any]:
    return {
        "path": record.path,
        "source": record.source,
        "packageId": record.package_id,
        "packageVersion": record.package_version,
        "intents": list(record.intents),
        "capabilities": list(record.capabilities),
    }


def parse_specpm_claims(manifest_path: Path, source: str) -> PackageClaimRecord:
    metadata: dict[str, str] = {}
    intents: set[str] = set()
    capabilities: set[str] = set()

    parse_state = "root"
    mode = ""
    for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()

        if indent == 0 and text == "metadata:":
            parse_state = "metadata"
            mode = ""
            continue
        if indent == 0 and text == "index:":
            parse_state = "index"
            mode = ""
            continue
        if indent == 0:
            parse_state = "root"
            mode = ""
            continue

        if parse_state == "metadata":
            if indent != 2 or ":" not in text:
                continue
            key, raw_value = text.split(":", 1)
            metadata[key.strip()] = parse_yaml_scalar(raw_value.strip())
            continue

        if parse_state == "index":
            if indent == 2 and text == "provides:":
                mode = "provides"
                continue
            if indent == 2 and text == "intents:":
                mode = "intents"
                continue
            if indent < 2:
                parse_state = "root"
                mode = ""
                continue
            if mode == "intents":
                if indent == 4 and text.startswith("- "):
                    for intent in normalize_scalar_list_item(text):
                        intents.add(intent)
                    continue
                if indent <= 2:
                    mode = ""
            if mode == "provides":
                if indent == 4 and text == "capabilities:":
                    mode = "capabilities"
                    continue
                if indent == 4 and text == "intents:":
                    mode = "provides_intents"
                    continue
                if indent <= 2:
                    mode = ""
            if mode == "capabilities":
                if indent == 6 and text.startswith("- "):
                    for capability in normalize_scalar_list_item(text):
                        capabilities.add(capability)
                    continue
                if indent == 4 and text == "intents:":
                    mode = "provides_intents"
                    continue
                if indent <= 4:
                    mode = "index"
                    parse_state = "index"
            if mode == "provides_intents":
                if indent == 6 and text.startswith("- "):
                    for intent in normalize_scalar_list_item(text):
                        intents.add(intent)
                    continue
                if indent <= 4:
                    mode = "index"
                    parse_state = "index"

    package_id = metadata.get("id", "").strip()
    package_version = metadata.get("version", "").strip()
    if not package_id or not package_version:
        raise ValueError("specpm.yaml must contain metadata.id and metadata.version.")

    return PackageClaimRecord(
        path=str(manifest_path),
        source=source,
        package_id=package_id,
        package_version=package_version,
        intents=tuple(sorted(intents)),
        capabilities=tuple(sorted(capabilities)),
    )


def normalize_scalar_list_item(text: str) -> list[str]:
    value = text[2:].strip()
    parsed = parse_yaml_scalar(value)
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def duplicate_claims(records: list[PackageClaimRecord], claim_key: str) -> list[dict[str, Any]]:
    claim_map: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        for claim in getattr(record, claim_key):
            claim_map.setdefault(claim, []).append(
                {
                    "packageId": record.package_id,
                    "packageVersion": record.package_version,
                    "path": record.path,
                    "source": record.source,
                }
            )

    duplicates: list[dict[str, Any]] = []
    for claim_id, claimants in sorted(claim_map.items(), key=lambda item: item[0]):
        if len(claimants) > 1:
            duplicates.append(
                {
                    "claim": claim_id,
                    "count": len(claimants),
                    "claimants": sorted(
                        claimants,
                        key=lambda item: (item["source"], item["packageId"], item["path"]),
                    ),
                }
            )
    return duplicates


def write_governance_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
