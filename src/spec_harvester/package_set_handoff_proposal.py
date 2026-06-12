from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.bundle_set_preflight import (
    BUNDLE_SET_PREFLIGHT_API_VERSION,
    BUNDLE_SET_PREFLIGHT_KIND,
)
from spec_harvester.package_set_drafter import (
    PACKAGE_RELATION_PROPOSALS_API_VERSION,
    PACKAGE_RELATION_PROPOSALS_FILENAME,
    PACKAGE_RELATION_PROPOSALS_KIND,
    PACKAGE_SET_DRAFT_API_VERSION,
    PACKAGE_SET_DRAFT_FILENAME,
    PACKAGE_SET_DRAFT_KIND,
)
from spec_harvester.producer_reports import (
    author_ready_stop_policy_summary,
    author_review_payload,
    read_optional_report_object,
)

PACKAGE_SET_HANDOFF_PROPOSAL_API_VERSION = "spec-harvester.package-set-handoff-proposal/v0"
PACKAGE_SET_HANDOFF_PROPOSAL_KIND = "SpecHarvesterPackageSetHandoffProposal"
PACKAGE_SET_HANDOFF_PROPOSAL_SCHEMA_VERSION = 1
BUNDLE_SET_PREFLIGHT_FILENAME = "bundle-set-preflight.json"

TRUST_BOUNDARY_NOTES = [
    "SpecHarvester package-set handoff is review evidence only.",
    "SpecPM remains the validation, acceptance, relation, and registry authority.",
    "Generated relation proposals remain producer-observed until maintainer review.",
    "The proposal generator reads local JSON/YAML artifacts and does not execute package code.",
]


@dataclass(frozen=True)
class PackageSetHandoffProposalOptions:
    bundle_set: Path
    viewer: Path | None = None


def build_package_set_handoff_proposal(
    options: PackageSetHandoffProposalOptions,
) -> dict[str, Any]:
    bundle_set = options.bundle_set.resolve()
    if not bundle_set.is_dir():
        raise ValueError(f"Package-set directory does not exist: {bundle_set}")

    draft = read_required_json(bundle_set / PACKAGE_SET_DRAFT_FILENAME)
    relations = read_required_json(bundle_set / PACKAGE_RELATION_PROPOSALS_FILENAME)
    check_identity(
        draft,
        expected={
            "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
            "kind": PACKAGE_SET_DRAFT_KIND,
            "schemaVersion": 1,
        },
        artifact=PACKAGE_SET_DRAFT_FILENAME,
    )
    check_identity(
        relations,
        expected={
            "apiVersion": PACKAGE_RELATION_PROPOSALS_API_VERSION,
            "kind": PACKAGE_RELATION_PROPOSALS_KIND,
            "schemaVersion": 1,
        },
        artifact=PACKAGE_RELATION_PROPOSALS_FILENAME,
    )

    preflight = read_optional_json(bundle_set / BUNDLE_SET_PREFLIGHT_FILENAME)
    if preflight is not None:
        check_identity(
            preflight,
            expected={
                "apiVersion": BUNDLE_SET_PREFLIGHT_API_VERSION,
                "kind": BUNDLE_SET_PREFLIGHT_KIND,
                "schemaVersion": 1,
            },
            artifact=BUNDLE_SET_PREFLIGHT_FILENAME,
        )

    viewer = viewer_record(options.viewer)
    members = member_records(bundle_set, draft)
    quality_reports = member_quality_reports(bundle_set, members)
    author_ready_summary = author_ready_stop_policy_summary(quality_reports)
    author_review = author_review_payload(author_ready_summary, quality_reports)
    relation_records_value = relation_records(relations)
    relation_proposals = mapping_value(draft.get("relationProposals"))
    package_set_id = next(
        (member["packageId"] for member in members if member["role"] == "workspace"),
        members[0]["packageId"] if members else "package-set",
    )

    return {
        "apiVersion": PACKAGE_SET_HANDOFF_PROPOSAL_API_VERSION,
        "kind": PACKAGE_SET_HANDOFF_PROPOSAL_KIND,
        "schemaVersion": PACKAGE_SET_HANDOFF_PROPOSAL_SCHEMA_VERSION,
        "status": "ok",
        "packageSet": {
            "id": package_set_id,
            "candidateCount": len(members),
            "relationCount": len(relation_records_value),
            "authority": string_value(draft.get("authority")),
            "reviewStatus": string_value(relation_proposals.get("reviewStatus")),
            "source": mapping_value(draft.get("source")),
            "selectedRoles": list_value(mapping_value(draft.get("selection")).get("roles")),
        },
        "authorReadyDraftSummary": author_ready_summary,
        "authorReview": author_review,
        "members": members,
        "relations": relation_records_value,
        "evidenceLinks": evidence_links(bundle_set, members, relations, preflight, viewer),
        "preflight": preflight_record(preflight),
        "viewer": viewer,
        "registryAcceptanceDecision": registry_acceptance_decision(),
        "trustBoundary": TRUST_BOUNDARY_NOTES,
        "nonGoals": [
            "specpm_acceptance",
            "package_acceptance",
            "relation_acceptance",
            "registry_publication",
            "package_execution",
            "package_manager_execution",
        ],
    }


def build_package_set_handoff_proposal_markdown(report: dict[str, Any]) -> str:
    package_set = report["packageSet"]
    author_review = mapping_value(report.get("authorReview"))
    member_lines = "\n".join(
        f"- `{member['packageId']}` ({member['role']}): `{member['candidatePath']}`"
        for member in report["members"]
    )
    relation_lines = "\n".join(
        (
            f"- `{relation['source']['packageId']}` {relation['type']} "
            f"`{relation['target']['packageId']}` "
            f"({relation['reviewStatus']}, {relation['authority']})"
        )
        for relation in report["relations"]
    )
    evidence_lines = "\n".join(
        (f"- `{link['role']}`: `{link['path']}` ({link['status']}, {link['pathScope']})")
        for link in report["evidenceLinks"]
    )
    boundary_lines = "\n".join(f"- {note}" for note in report["trustBoundary"])

    return "\n".join(
        [
            f"# SpecPM Package-Set Handoff Proposal: {package_set['id']}",
            "",
            "## Summary",
            "",
            f"- Package set: `{package_set['id']}`",
            f"- Candidate packages: {package_set['candidateCount']}",
            f"- Relation proposals: {package_set['relationCount']}",
            f"- Preflight: `{report['preflight']['status']}`",
            (f"- Author-ready stop decision: `{report['authorReadyDraftSummary']['decision']}`"),
            "- Registry acceptance decision: `external_required`",
            "",
            "## Author Review Checklist",
            "",
            review_item_lines(object_list(author_review.get("checklist")))
            or "- _No author review checklist recorded._",
            "",
            "## Weak Claims and Evidence Gaps",
            "",
            "### Weak Claims",
            "",
            weak_claim_lines(object_list(author_review.get("weakClaims")))
            or "- _No weak claims recorded._",
            "",
            "### Evidence Gaps",
            "",
            review_item_lines(object_list(author_review.get("evidenceGaps")))
            or "- _No evidence gaps recorded._",
            "",
            "## Recommended Edits",
            "",
            review_item_lines(object_list(author_review.get("recommendedEdits")))
            or "- _No recommended edits recorded._",
            "",
            "## Member Packages",
            "",
            member_lines or "- _No member packages declared._",
            "",
            "## Relation Proposals",
            "",
            relation_lines or "- _No relation proposals declared._",
            "",
            "## Evidence Links",
            "",
            evidence_lines or "- _No evidence links declared._",
            "",
            "## Review Boundary",
            "",
            boundary_lines,
            "",
            "This proposal does not accept packages, accept relations, publish registry metadata, "
            "or replace SpecPM maintainer review.",
            "",
        ]
    )


def review_item_lines(items: list[dict[str, Any]]) -> str:
    return "\n".join(
        (
            f"- `{string_value(item.get('severity')) or 'info'}` "
            f"`{string_value(item.get('target')) or 'package-set'}`: "
            f"{string_value(item.get('summary'))}"
        )
        for item in items
    )


def weak_claim_lines(items: list[dict[str, Any]]) -> str:
    return "\n".join(
        (
            f"- `{string_value(item.get('id'))}` "
            f"({', '.join(string_list(item.get('packageIds'))) or 'package-set'}): "
            f"{string_value(item.get('summary'))}"
        )
        for item in items
    )


def member_quality_reports(bundle_set: Path, members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reports = []
    for member in members:
        path = string_value(member.get("qualityReportPath"))
        source_path = safe_bundle_path(bundle_set, path)
        if source_path is None:
            quality_report = {
                "status": "blocked",
                "authorReadyDraft": {
                    "status": "blocked",
                    "stopReason": "quality_report_path_rejected",
                },
                "readError": "path_rejected",
            }
        else:
            quality_report = read_optional_report_object(source_path, missing_status="missing")
        reports.append(
            {
                "packageId": string_value(member.get("packageId")),
                "qualityReportPath": path,
                "qualityReport": quality_report,
            }
        )
    return reports


def write_package_set_handoff_proposal(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_package_set_handoff_proposal_markdown(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_package_set_handoff_proposal_markdown(report), encoding="utf-8")


def member_records(bundle_set: Path, draft: dict[str, Any]) -> list[dict[str, Any]]:
    members = []
    for candidate in list_value(draft.get("candidates")):
        if not isinstance(candidate, dict):
            continue
        candidate_path = string_value(candidate.get("candidatePath"))
        members.append(
            {
                "packageId": string_value(candidate.get("packageId")),
                "role": string_value(candidate.get("role")),
                "candidatePath": candidate_path,
                "manifestPath": string_value(candidate.get("manifest")),
                "producerReceiptPath": string_value(candidate.get("producerReceipt")),
                "validationReportPath": string_value(candidate.get("validationReport")),
                "diagnosticsReportPath": string_value(candidate.get("diagnosticsReport")),
                "qualityReportPath": string_value(candidate.get("qualityReport")),
                "sourceTargetPath": string_value(candidate.get("sourceTargetPath")),
                "status": string_value(candidate.get("status")),
                "evidenceLinks": member_evidence_links(candidate, bundle_set),
            }
        )
    return sorted(members, key=lambda item: (item["role"] != "workspace", item["packageId"]))


def member_evidence_links(
    candidate: dict[str, Any],
    bundle_set: Path,
) -> list[dict[str, Any]]:
    links = []
    for role, field in (
        ("member_manifest", "manifest"),
        ("member_boundary_spec", "spec"),
        ("member_producer_receipt", "producerReceipt"),
        ("member_validation_report", "validationReport"),
        ("member_diagnostics", "diagnosticsReport"),
        ("member_quality_report", "qualityReport"),
    ):
        path = string_value(candidate.get(field))
        links.append(
            artifact_link(
                role=role,
                path=path,
                path_scope="bundle_relative",
                source_path=safe_bundle_path(bundle_set, path),
            )
        )
    return links


def relation_records(relations: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for relation in list_value(relations.get("relations")):
        if not isinstance(relation, dict):
            continue
        records.append(
            {
                "id": string_value(relation.get("id")),
                "type": string_value(relation.get("type")),
                "source": mapping_value(relation.get("source")),
                "target": mapping_value(relation.get("target")),
                "reviewStatus": string_value(relation.get("reviewStatus")),
                "authority": string_value(relation.get("authority")),
                "evidenceCount": len(list_value(relation.get("evidence"))),
            }
        )
    return sorted(records, key=lambda item: item["id"])


def evidence_links(
    bundle_set: Path,
    members: list[dict[str, Any]],
    relations: dict[str, Any],
    preflight: dict[str, Any] | None,
    viewer: dict[str, Any],
) -> list[dict[str, Any]]:
    links = [
        artifact_link(
            role="package_set_draft",
            path=PACKAGE_SET_DRAFT_FILENAME,
            path_scope="bundle_relative",
            source_path=safe_bundle_path(bundle_set, PACKAGE_SET_DRAFT_FILENAME),
        ),
        artifact_link(
            role="package_relation_proposals",
            path=PACKAGE_RELATION_PROPOSALS_FILENAME,
            path_scope="bundle_relative",
            source_path=safe_bundle_path(bundle_set, PACKAGE_RELATION_PROPOSALS_FILENAME),
        ),
    ]
    if preflight is not None:
        links.append(
            artifact_link(
                role="bundle_set_preflight",
                path=BUNDLE_SET_PREFLIGHT_FILENAME,
                path_scope="bundle_relative",
                source_path=safe_bundle_path(bundle_set, BUNDLE_SET_PREFLIGHT_FILENAME),
            )
        )
    if viewer["status"] == "present":
        links.append(
            artifact_link(
                role="package_set_viewer",
                path=viewer["indexPath"],
                path_scope="local_path",
                source_path=Path(viewer["indexPath"]),
            )
        )
    for member in members:
        links.append(
            artifact_link(
                role="member_candidate_bundle",
                path=member["candidatePath"],
                path_scope="bundle_relative",
                source_path=safe_bundle_path(bundle_set, member["candidatePath"]),
                package_id=member["packageId"],
            )
        )
    relation_summary = mapping_value(relations.get("summary"))
    links.append(
        {
            "role": "package_relation_summary",
            "path": PACKAGE_RELATION_PROPOSALS_FILENAME,
            "pathScope": "bundle_relative",
            "status": "present",
            "relationCount": integer_value(relation_summary.get("relationCount")),
            "containsCount": integer_value(relation_summary.get("containsCount")),
        }
    )
    return links


def artifact_link(
    *,
    role: str,
    path: str,
    path_scope: str,
    source_path: Path | None,
    package_id: str | None = None,
) -> dict[str, Any]:
    status = (
        "rejected" if source_path is None else "present" if source_path.exists() else "expected"
    )
    link: dict[str, Any] = {
        "role": role,
        "path": path,
        "pathScope": path_scope,
        "status": status,
    }
    if package_id is not None:
        link["packageId"] = package_id
    if source_path is not None and source_path.is_file():
        link["digest"] = f"sha256:{sha256_file(source_path)}"
    return link


def safe_bundle_path(bundle_set: Path, path: str) -> Path | None:
    relative = Path(path)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = (bundle_set / relative).resolve(strict=False)
    try:
        candidate.relative_to(bundle_set.resolve())
    except ValueError:
        return None
    return candidate


def preflight_record(preflight: dict[str, Any] | None) -> dict[str, Any]:
    if preflight is None:
        return {"status": "not_provided", "path": BUNDLE_SET_PREFLIGHT_FILENAME}
    summary = mapping_value(preflight.get("summary"))
    return {
        "status": string_value(preflight.get("status")),
        "path": BUNDLE_SET_PREFLIGHT_FILENAME,
        "candidateCount": integer_value(summary.get("candidateCount")),
        "relationCount": integer_value(summary.get("relationCount")),
        "errorCount": integer_value(summary.get("errorCount")),
        "warningCount": integer_value(summary.get("warningCount")),
    }


def viewer_record(viewer: Path | None) -> dict[str, Any]:
    if viewer is None:
        return {"status": "not_provided"}
    index = viewer / "index.html"
    payload = viewer / "package-set.json"
    return {
        "status": "present" if index.is_file() and payload.is_file() else "missing",
        "indexPath": str(index),
        "payloadPath": str(payload),
        "payloadDigest": f"sha256:{sha256_file(payload)}" if payload.is_file() else None,
    }


def registry_acceptance_decision() -> dict[str, Any]:
    return {
        "status": "external_required",
        "requiredFor": ["public_index_acceptance", "package_relation_acceptance"],
        "recordKind": "SpecPMRegistryAcceptanceDecision",
        "producerAuthority": "evidence_only",
        "acceptanceAuthority": "SpecPM maintainer review",
    }


def check_identity(payload: dict[str, Any], *, expected: dict[str, Any], artifact: str) -> None:
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(f"{artifact} {key} must be {value!r}.")


def read_required_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Required package-set artifact is missing: {path}")
    return read_json_object(path)


def read_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return read_json_object(path)


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str) and item)


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
