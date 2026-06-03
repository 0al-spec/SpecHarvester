from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.accepted_diff import (
    PackageDiffInputRecord,
    build_candidate_comparison,
    collect_package_diff_records,
    latest_accepted_by_package_id,
    parse_specpm_diff_record,
)
from spec_harvester.promoter import read_manifest_identity, reject_symlinks, validate_with_specpm

ACCEPTED_PACKAGE_UPDATE_PROPOSAL_KIND = "SpecHarvesterAcceptedPackageUpdateProposal"
ACCEPTED_PACKAGE_UPDATE_PROPOSAL_SCHEMA_VERSION = 1

VALID_UPDATE_KINDS = {"upstream_revision", "metadata_errata", "correction"}
DEFAULT_MANIFEST_ENTRY_PREFIX = "public-index/generated"

TRUST_BOUNDARY_NOTES = [
    (
        "Report generation reads local candidate/accepted package files for immutable "
        "evidence comparison."
    ),
    "Source revision and evidence digests are derived from local package artifacts.",
    "No candidate or accepted package files are written during report generation.",
    "SpecPM validation is optional and can be explicitly skipped.",
]

PRODUCER_EVIDENCE_FILES = (
    ("manifest", "specpm.yaml", True),
    ("producer_receipt", "producer-receipt.json", True),
    ("validation_report", "validation-report.json", True),
    ("diagnostics", "diagnostics.json", True),
    ("producer_preflight", "preflight-report.json", False),
    ("static_viewer", "static-viewer/index.html", False),
)


@dataclass(frozen=True)
class AcceptedPackageUpdateProposalOptions:
    candidate: Path
    accepted_root: Path
    specpm_command: str = "specpm"
    specpm_pythonpath: str | None = None
    skip_validation: bool = False
    update_kind: str | None = None
    allow_correction: bool = False
    correction_notes: tuple[str, ...] = ()
    reviewer_notes: tuple[str, ...] = ()


def build_accepted_package_update_proposal(
    options: AcceptedPackageUpdateProposalOptions,
) -> dict[str, Any]:
    candidate = options.candidate.resolve()
    if not candidate.is_dir():
        raise ValueError(f"Candidate directory does not exist or is not a directory: {candidate}")

    reject_symlinks(candidate)
    manifest_path = candidate / "specpm.yaml"
    if not manifest_path.is_file():
        raise ValueError(f"Candidate is missing specpm.yaml: {candidate}")

    candidate_record = parse_specpm_diff_record(manifest_path, "candidate")
    candidate_identity = read_manifest_identity(manifest_path)

    accepted_issues: list[dict[str, str]] = []
    accepted_records, accepted_issues = collect_package_diff_records(
        options.accepted_root.resolve(),
        "accepted",
    )
    prior_record = _find_prior_accepted_record(
        candidate_record=candidate_record,
        accepted_records=accepted_records,
        candidate_path=candidate,
    )

    comparison = build_candidate_comparison(candidate_record, prior_record)
    requires_correction = _requires_correction_mode(
        candidate_path=candidate,
        candidate_record=candidate_record,
        prior_record=prior_record,
        comparison=comparison,
    )

    if requires_correction:
        if not options.allow_correction:
            raise ValueError(
                "Accepted package version is immutable. Updates that target an already "
                "accepted package version require explicit correction mode "
                "--allow-correction."
            )
        if not options.correction_notes:
            raise ValueError("Correction mode requires at least one --correction-note.")

    update_kind = _normalize_update_kind(
        provided=options.update_kind,
        comparison=comparison,
        candidate_source_revision=_extract_source_revision(candidate_record),
        prior_source_revision=_extract_source_revision(prior_record) if prior_record else None,
        requires_correction=requires_correction,
    )
    validation_status, validation_issues = _validate_candidate(
        candidate,
        command=options.specpm_command,
        pythonpath=options.specpm_pythonpath,
        skip_validation=options.skip_validation,
    )
    issues = accepted_issues + validation_issues

    comparison_payload = {
        "status": "correction" if requires_correction else comparison["status"],
        "capabilities": {
            "added": comparison["changes"]["capabilities"]["added"],
            "removed": comparison["changes"]["capabilities"]["removed"],
        },
        "intents": {
            "added": comparison["changes"]["intents"]["added"],
            "removed": comparison["changes"]["intents"]["removed"],
        },
    }

    package_id = candidate_identity["id"]
    package_version = candidate_identity["version"]
    package_subdir = f"{package_id}/{package_version}"

    report: dict[str, Any] = {
        "schemaVersion": ACCEPTED_PACKAGE_UPDATE_PROPOSAL_SCHEMA_VERSION,
        "kind": ACCEPTED_PACKAGE_UPDATE_PROPOSAL_KIND,
        "status": "partial" if issues else "ok",
        "packageId": package_id,
        "packageSubdir": package_subdir,
        "manifestEntryPath": f"{DEFAULT_MANIFEST_ENTRY_PREFIX}/{package_subdir}",
        "oldPackageVersion": comparison["oldPackageVersion"],
        "newPackageVersion": comparison["newPackageVersion"],
        "updateKind": update_kind,
        "sourceRevision": _extract_source_revision(candidate_record),
        "evidenceDigests": {
            "harvestJson": _file_digest_if_exists(candidate / "harvest.json"),
            "specpmYaml": _file_digest(candidate / "specpm.yaml"),
        },
        "producerEvidenceLinks": _build_producer_evidence_links(candidate, package_subdir),
        "registryAcceptanceDecision": _registry_acceptance_decision_reference(),
        "changedClaims": _build_changed_claims(comparison["changes"]),
        "validationStatus": validation_status,
        "reviewerNotes": list(options.reviewer_notes),
        "comparison": comparison_payload,
        "candidate": {
            "path": str(candidate),
            "packageId": package_id,
            "packageVersion": package_version,
        },
        "accepted": {
            "packageId": package_id if prior_record else None,
            "packageVersion": comparison["oldPackageVersion"],
            "path": prior_record.path if prior_record else None,
        },
        "issues": sorted(issues, key=lambda issue: (issue["path"], issue["code"])),
        "trustBoundary": TRUST_BOUNDARY_NOTES,
    }

    if requires_correction:
        report["correction"] = {
            "enabled": True,
            "reason": list(options.correction_notes),
            "source": "manual_review",
        }
        report["reviewerNotes"] = list(options.reviewer_notes) + list(options.correction_notes)

    return report


def _find_prior_accepted_record(
    *,
    candidate_record: PackageDiffInputRecord,
    accepted_records: list[PackageDiffInputRecord],
    candidate_path: Path,
) -> PackageDiffInputRecord | None:
    if not accepted_records:
        return None

    candidate_manifest_path = (candidate_path / "specpm.yaml").resolve()
    accepted_for_package = [
        record
        for record in accepted_records
        if record.package_id == candidate_record.package_id
        and Path(record.path).resolve() != candidate_manifest_path
    ]
    if not accepted_for_package:
        return None

    accepted_for_candidate_version = [
        record
        for record in accepted_for_package
        if record.package_version == candidate_record.package_version
    ]
    if accepted_for_candidate_version:
        return latest_accepted_by_package_id(accepted_for_candidate_version).get(
            candidate_record.package_id
        )

    return latest_accepted_by_package_id(accepted_for_package).get(candidate_record.package_id)


def build_accepted_package_update_proposal_markdown(report: dict[str, Any]) -> str:
    changed_claims = report["changedClaims"]
    evidence_digests = report["evidenceDigests"]
    trust_boundary = report["trustBoundary"]
    validation_status = report["validationStatus"]
    comparison = report["comparison"]

    if changed_claims:
        claims_block = "\n".join(f"- {claim}" for claim in changed_claims)
    else:
        claims_block = "- _No changed claims detected._"

    evidence_block = "\n".join(
        f"- {name}: {value}" for name, value in evidence_digests.items() if value is not None
    )
    if not evidence_block:
        evidence_block = "- _No evidence artifacts found._"

    producer_evidence_block = _producer_evidence_markdown(report["producerEvidenceLinks"])
    registry_decision_block = _registry_acceptance_decision_markdown(
        report["registryAcceptanceDecision"]
    )

    notes_block = "\n".join(f"- {note}" for note in report["reviewerNotes"]) or (
        "- _No reviewer notes supplied._"
    )

    validation_block = []
    if "error" in validation_status:
        validation_block.append(f" - error: {validation_status['error']}")
    if "status" in validation_status:
        validation_block.append(f" - status: {validation_status['status']}")
    for key, value in sorted(validation_status.items()):
        if key in {"error", "status"}:
            continue
        validation_block.append(f" - {key}: {value}")
    if not validation_block:
        validation_block.append(" - none")

    correction_block: list[str] = []
    if report.get("correction"):
        correction = report["correction"]
        correction_block = [
            "",
            "## Correction",
            f"- enabled: {str(correction['enabled']).lower()}",
            f"- source: {correction['source']}",
            "- reason:",
            *[f"  - {note}" for note in correction["reason"]],
        ]

    trust_boundary_block = "\n".join(f"- {item}" for item in trust_boundary)
    issue_lines = []
    for issue in report["issues"]:
        issue_lines.append(f"- {issue['code']} in {issue['path']}: {issue['message']}")
    if not issue_lines:
        issue_lines.append("- no blocking issues")

    return (
        "\n".join(
            [
                (
                    f"# Proposal: {report['packageId']} "
                    f"{report['oldPackageVersion']} -> {report['newPackageVersion']}"
                ),
                "",
                "## Summary",
                f"- Update kind: `{report['updateKind']}`",
                f"- Source revision: `{report['sourceRevision'] or 'unknown'}`",
                f"- Manifest path: `{report['manifestEntryPath']}`",
                f"- Candidate status: `{comparison['status']}`",
                f"- Validation (specpm): `{validation_status['specpm']}`",
                "",
                "## Changed Claims",
                claims_block,
                "",
                "## Evidence Digests",
                evidence_block,
                "",
                "## Producer Bundle Evidence",
                producer_evidence_block,
                "",
                "## Registry Acceptance Decision",
                registry_decision_block,
                "",
                "## Capability Changes",
                f"- added: {', '.join(comparison['capabilities']['added']) or 'none'}",
                f"- removed: {', '.join(comparison['capabilities']['removed']) or 'none'}",
                "",
                "## Intent Changes",
                f"- added: {', '.join(comparison['intents']['added']) or 'none'}",
                f"- removed: {', '.join(comparison['intents']['removed']) or 'none'}",
                "",
                "## Validation",
                "```text",
                "- specpm:",
                *validation_block,
                "```",
                *correction_block,
                "",
                "## Reviewer Notes",
                notes_block,
                "",
                "## Issues",
                *issue_lines,
                "",
                "## Trust Boundary",
                trust_boundary_block,
            ]
        )
        + "\n"
    )


def write_accepted_package_update_proposal(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_accepted_package_update_proposal_markdown(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _extract_source_revision(record: PackageDiffInputRecord | None) -> str | None:
    if record is None:
        return None
    for artifact in record.upstream_artifacts:
        if artifact.get("id") == "upstream_repository":
            return artifact.get("revision")
    return None


def _build_changed_claims(changes: dict[str, Any]) -> list[str]:
    claims: set[str] = set()
    for intent in changes["intents"]["added"]:
        claims.add(f"intent:{intent}")
    for intent in changes["intents"]["removed"]:
        claims.add(f"intent:{intent}")
    for capability in changes["capabilities"]["added"]:
        claims.add(f"capability:{capability}")
    for capability in changes["capabilities"]["removed"]:
        claims.add(f"capability:{capability}")
    return sorted(claims)


def _registry_acceptance_decision_reference() -> dict[str, Any]:
    return {
        "status": "external_required",
        "requiredFor": ["public_index_acceptance"],
        "authority": "SpecPM maintainer review",
        "recordKind": "SpecPMRegistryAcceptanceDecision",
        "recordLocation": "SpecPM pull request or accepted-source review record",
        "producerReceiptAuthority": "evidence_only",
    }


def _build_producer_evidence_links(candidate: Path, package_subdir: str) -> list[dict[str, Any]]:
    links: list[dict[str, Any]] = [
        {
            "role": "accepted_source_bundle",
            "path": f"{DEFAULT_MANIFEST_ENTRY_PREFIX}/{package_subdir}",
            "pathScope": "repo_relative",
            "required": True,
            "status": "expected",
        }
    ]
    for role, relative_path, required in PRODUCER_EVIDENCE_FILES:
        path = candidate / relative_path
        link: dict[str, Any] = {
            "role": role,
            "path": relative_path,
            "pathScope": "candidate_bundle",
            "required": required,
            "status": "present" if path.is_file() else "missing",
        }
        if path.is_file():
            link["digest"] = _file_digest(path)
        links.append(link)
    links.append(
        {
            "role": "accepted_source_diff",
            "path": "pull-request-diff",
            "pathScope": "pull_request",
            "required": True,
            "status": "expected",
        }
    )
    return links


def _producer_evidence_markdown(links: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for link in links:
        status = link["status"]
        digest = f" ({link['digest']})" if "digest" in link else ""
        requirement = "required" if link["required"] else "optional"
        lines.append(f"- {link['role']}: `{link['path']}` - {status}, {requirement}{digest}")
    if not lines:
        return "- _No producer bundle evidence links recorded._"
    return "\n".join(lines)


def _registry_acceptance_decision_markdown(decision: dict[str, Any]) -> str:
    required_for = ", ".join(decision["requiredFor"])
    return "\n".join(
        [
            f"- status: `{decision['status']}`",
            f"- required for: `{required_for}`",
            f"- authority: `{decision['authority']}`",
            f"- record kind: `{decision['recordKind']}`",
            f"- producer receipt authority: `{decision['producerReceiptAuthority']}`",
        ]
    )


def _requires_correction_mode(
    *,
    candidate_path: Path,
    candidate_record: PackageDiffInputRecord,
    prior_record: PackageDiffInputRecord | None,
    comparison: dict[str, Any],
) -> bool:
    if prior_record is None:
        return False
    if candidate_record.package_version != prior_record.package_version:
        return False
    if comparison["status"] != "unchanged":
        return True
    return _package_tree_digests(candidate_path) != _package_tree_digests(
        Path(prior_record.path).parent
    )


def _package_tree_digests(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if _is_ignored_package_path(relative):
            continue
        relative_path = relative.as_posix()
        if path.is_symlink():
            files[relative_path] = f"symlink:{path.readlink()}"
            continue
        if path.is_file():
            files[relative_path] = _file_digest(path)
    return files


def _is_ignored_package_path(relative_path: Path) -> bool:
    return ".git" in relative_path.parts or relative_path.name == ".DS_Store"


def _normalize_update_kind(
    *,
    provided: str | None,
    comparison: dict[str, Any],
    candidate_source_revision: str | None,
    prior_source_revision: str | None,
    requires_correction: bool,
) -> str:
    if requires_correction and provided is not None and provided != "correction":
        raise ValueError(
            "Manual correction mode requires --allow-correction and --correction-note."
        )

    if requires_correction:
        return "correction"

    if provided is not None:
        if provided not in VALID_UPDATE_KINDS:
            raise ValueError(f"Unknown update kind: {provided}")
        return provided

    if comparison["status"] == "new_package":
        return "upstream_revision"

    if (
        candidate_source_revision is not None
        and prior_source_revision is not None
        and candidate_source_revision == prior_source_revision
    ):
        return "metadata_errata"

    if comparison["status"] == "unchanged":
        return "metadata_errata"

    return "upstream_revision"


def _validate_candidate(
    candidate: Path,
    *,
    command: str,
    pythonpath: str | None,
    skip_validation: bool,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    if skip_validation:
        return {"specpm": "skipped"}, []

    issues: list[dict[str, str]] = []
    try:
        validation = validate_with_specpm(candidate, command=command, pythonpath=pythonpath)
    except ValueError as exc:
        issues.append(
            {
                "path": str(candidate),
                "code": "specpm_validation_failed",
                "message": str(exc),
            }
        )
        return {"specpm": "failed", "error": str(exc)}, issues

    status = str(validation.get("status", "unknown"))
    if status != "ok":
        issues.append(
            {
                "path": str(candidate),
                "code": "specpm_validation_warning",
                "message": "SpecPM validation status is not ok.",
            }
        )

    return {"specpm": status}, issues


def _file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _file_digest_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return _file_digest(path)
