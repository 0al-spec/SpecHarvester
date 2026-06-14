from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SELECTED_CANDIDATE_HANDOFF_PROPOSAL_API_VERSION = (
    "spec-harvester.selected-candidate-handoff-proposal/v0"
)
SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND = "SpecHarvesterSelectedCandidateHandoffProposal"
SELECTED_CANDIDATE_HANDOFF_PROPOSAL_SCHEMA_VERSION = 1

SELECTED_HANDOFF_DRY_RUN_API_VERSION = (
    "spec-harvester.limited-popular-library-selected-handoff-dry-run/v0"
)
SELECTED_HANDOFF_DRY_RUN_KIND = "SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun"

REQUIRED_EVIDENCE_ROLES: tuple[dict[str, Any], ...] = (
    {"role": "candidate_bundle", "scope": "selected_candidate", "required": True},
    {
        "role": "manifest",
        "scope": "selected_candidate",
        "path": "specpm.yaml",
        "required": True,
    },
    {
        "role": "boundary_spec",
        "scope": "selected_candidate",
        "path": "specs/*.spec.yaml",
        "required": True,
    },
    {
        "role": "producer_receipt",
        "scope": "selected_candidate",
        "path": "producer-receipt.json",
        "required": True,
    },
    {
        "role": "validation_report",
        "scope": "selected_candidate",
        "path": "validation-report.json",
        "required": True,
    },
    {
        "role": "diagnostics",
        "scope": "selected_candidate",
        "path": "diagnostics.json",
        "required": True,
    },
    {
        "role": "quality_report",
        "scope": "selected_candidate",
        "path": "author-ready-draft-quality-report.json",
        "required": True,
    },
    {
        "role": "producer_preflight",
        "scope": "selected_candidate",
        "path": "preflight/<package_id>.json",
        "required": True,
    },
    {
        "role": "static_viewer",
        "scope": "selected_candidate",
        "path": "viewer/<package_id>/index.html",
        "required": True,
    },
    {
        "role": "static_viewer_payload",
        "scope": "selected_candidate",
        "path": "viewer/<package_id>/spec-package.json",
        "required": True,
    },
    {
        "role": "selected_handoff_dry_run",
        "scope": "proposal",
        "path": (
            "tests/fixtures/limited_popular_library_selected_handoff_dry_run/"
            "p30-t5-limited-popular-libraries.example.json"
        ),
        "required": True,
    },
)

MAINTAINER_CHECKLIST = [
    "Verify selected candidate identity, namespace, and package version before intake.",
    "Verify every required evidence role and digest before trusting the handoff.",
    "Run SpecPM-side validation and preflight before any accepted-source change.",
    (
        "Reject or request regeneration for weak evidence, package identity drift, "
        "or warning-bearing generated claims."
    ),
    "Record the external registry acceptance decision outside producer evidence.",
]

NON_AUTHORITY = [
    "This proposal is review evidence only.",
    "It is not SpecPM registry acceptance.",
    "It does not accept packages.",
    "It does not accept relations.",
    "It does not seed baselines.",
    "It does not remove preview_only.",
    "It does not publish registry metadata.",
    "It does not create a SpecPM pull request.",
    "It does not merge a SpecPM pull request.",
    "It does not replace maintainer review.",
    "It does not run prepare-accepted-entry.",
    "It does not run accepted-package-update-proposal.",
]

NOT_EXECUTED = [
    "prepare-accepted-entry",
    "accepted-package-update-proposal",
    "SpecPM pull request creation",
    "registry mutation",
    "relation acceptance",
    "baseline seeding",
    "preview_only removal",
]


@dataclass(frozen=True)
class SelectedCandidateHandoffProposalOptions:
    selected_handoff_dry_run: Path
    candidate_root: Path | None = None
    preflight_root: Path | None = None
    viewer_root: Path | None = None


def build_selected_candidate_handoff_proposal(
    options: SelectedCandidateHandoffProposalOptions,
) -> dict[str, Any]:
    dry_run_path = options.selected_handoff_dry_run.resolve()
    dry_run_display_path = options.selected_handoff_dry_run
    dry_run = read_required_json(dry_run_path)
    check_identity(
        dry_run,
        expected={
            "apiVersion": SELECTED_HANDOFF_DRY_RUN_API_VERSION,
            "kind": SELECTED_HANDOFF_DRY_RUN_KIND,
            "schemaVersion": 1,
            "authority": "producer_preview_evidence_only",
        },
        artifact=str(options.selected_handoff_dry_run),
    )

    selected = [
        item for item in list_value(dry_run.get("selectedCandidates")) if isinstance(item, dict)
    ]
    deferred = [
        item for item in list_value(dry_run.get("deferredCandidates")) if isinstance(item, dict)
    ]
    selected_records = [
        selected_candidate_record(options, dry_run_display_path, dry_run_path, candidate)
        for candidate in selected
    ]
    deferred_records = [deferred_candidate_record(candidate) for candidate in deferred]

    return {
        "apiVersion": SELECTED_CANDIDATE_HANDOFF_PROPOSAL_API_VERSION,
        "kind": SELECTED_CANDIDATE_HANDOFF_PROPOSAL_KIND,
        "schemaVersion": SELECTED_CANDIDATE_HANDOFF_PROPOSAL_SCHEMA_VERSION,
        "authority": "producer_preview_evidence_only",
        "source": source_record(dry_run, dry_run_display_path, dry_run_path),
        "summary": {
            "selectedCandidateCount": len(selected_records),
            "deferredCandidateCount": len(deferred_records),
            "requiredEvidenceRoleCount": len(REQUIRED_EVIDENCE_ROLES),
            "specpmPullRequestCreated": False,
            "registryMutationCount": 0,
        },
        "requiredEvidenceRoles": [dict(item) for item in REQUIRED_EVIDENCE_ROLES],
        "selectedCandidates": selected_records,
        "deferredCandidates": deferred_records,
        "maintainerChecklist": list(MAINTAINER_CHECKLIST),
        "futureConsumerBoundary": {
            "specpmMayPreflight": True,
            "specpmMayAcceptAfterMaintainerReview": True,
            "producerCanAccept": False,
        },
        "nonAuthority": list(NON_AUTHORITY),
        "notExecuted": list(NOT_EXECUTED),
    }


def build_selected_candidate_handoff_proposal_markdown(report: dict[str, Any]) -> str:
    summary = mapping_value(report.get("summary"))
    selected = object_list(report.get("selectedCandidates"))
    deferred = object_list(report.get("deferredCandidates"))
    selected_lines = "\n".join(
        (
            f"| `{candidate['id']}` | `{candidate['repositoryId']}` | "
            f"`{mapping_value(candidate.get('producerPreflight')).get('status')}` | "
            f"`{mapping_value(candidate.get('staticViewer')).get('status')}` | "
            f"`{mapping_value(candidate.get('registryAcceptanceDecision')).get('status')}` |"
        )
        for candidate in selected
    )
    deferred_lines = "\n".join(
        (f"| `{candidate['id']}` | `{candidate['reason']}` | {candidate['requiredAction']} |")
        for candidate in deferred
    )
    role_lines = "\n".join(
        (f"- `{role['role']}` ({role['scope']}): {role.get('path', 'candidate bundle root')}")
        for role in object_list(report.get("requiredEvidenceRoles"))
    )
    checklist_lines = "\n".join(
        f"- {item}" for item in string_list_unsorted(report.get("maintainerChecklist"))
    )
    boundary_lines = "\n".join(
        f"- {item}" for item in string_list_unsorted(report.get("nonAuthority"))
    )

    return "\n".join(
        [
            "# SpecPM Selected Candidate Handoff Proposal",
            "",
            "## Summary",
            "",
            f"- Selected candidates: {integer_value(summary.get('selectedCandidateCount'))}",
            f"- Deferred candidates: {integer_value(summary.get('deferredCandidateCount'))}",
            f"- Required evidence roles: {integer_value(summary.get('requiredEvidenceRoleCount'))}",
            "- Registry acceptance decision: `external_required`",
            "- Authority: `producer_preview_evidence_only`",
            "",
            "## Selected Candidates",
            "",
            "| Candidate | Repository | Producer preflight | Viewer | Registry acceptance |",
            "| --- | --- | --- | --- | --- |",
            selected_lines or "| _None_ | _None_ | _None_ | _None_ | _None_ |",
            "",
            "## Deferred Candidates",
            "",
            "| Candidate | Reason | Required action |",
            "| --- | --- | --- |",
            deferred_lines or "| _None_ | _None_ | _None_ |",
            "",
            "## Required Evidence Roles",
            "",
            role_lines,
            "",
            "## Maintainer Checklist",
            "",
            checklist_lines,
            "",
            "## Non-Authority Boundary",
            "",
            boundary_lines,
            "",
            (
                "This proposal does not accept packages, accept relations, seed baselines, "
                "remove `preview_only`, publish registry metadata, create a SpecPM pull "
                "request, or replace SpecPM maintainer review."
            ),
            "",
        ]
    )


def write_selected_candidate_handoff_proposal(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_selected_candidate_handoff_proposal_markdown(
    path: Path,
    report: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_selected_candidate_handoff_proposal_markdown(report), encoding="utf-8")


def selected_candidate_record(
    options: SelectedCandidateHandoffProposalOptions,
    dry_run_display_path: Path,
    dry_run_path: Path,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    validate_selected_candidate(candidate)
    candidate_id = string_value(candidate.get("id"))
    candidate_dir = candidate_bundle_path(options, candidate)
    preflight_path = producer_preflight_path(options, candidate)
    viewer_dir = static_viewer_path(options, candidate)
    candidate_display_path = candidate_bundle_display_path(options, candidate)
    preflight_display_path = producer_preflight_display_path(options, candidate)
    viewer_display_dir = static_viewer_display_path(options, candidate)
    candidate_source = candidate_dir if options.candidate_root is not None else None
    preflight_source = preflight_path if options.preflight_root is not None else None
    viewer_source = viewer_dir if options.viewer_root is not None else None
    preflight = producer_preflight_record(candidate, preflight_display_path, preflight_source)
    viewer = static_viewer_record(candidate, viewer_display_dir, viewer_source)
    evidence = evidence_links(
        candidate,
        candidate_display_path,
        candidate_source,
        preflight_display_path,
        preflight_source,
        viewer_display_dir,
        viewer_source,
        dry_run_display_path,
        dry_run_path,
    )

    return {
        "id": candidate_id,
        "repositoryId": string_value(candidate.get("repositoryId")),
        "candidateBundlePath": str(candidate_display_path),
        "previewOnly": True,
        "triageClassification": string_value(candidate.get("triageClassification")),
        "maintainerAction": "review_for_possible_specpm_intake",
        "producerPreflight": preflight,
        "staticViewer": viewer,
        "registryAcceptanceDecision": registry_acceptance_decision(candidate),
        "evidenceLinks": evidence,
    }


def validate_selected_candidate(candidate: dict[str, Any]) -> None:
    candidate_id = string_value(candidate.get("id")) or "<unknown>"
    if candidate.get("previewOnly") is not True:
        raise ValueError(f"{candidate_id} must remain previewOnly: true.")
    preflight = mapping_value(candidate.get("producerPreflight"))
    if preflight.get("status") != "passed":
        raise ValueError(f"{candidate_id} producer preflight must be passed.")
    if integer_value(preflight.get("warningCount")) != 0:
        raise ValueError(f"{candidate_id} producer preflight warningCount must be 0.")
    if integer_value(preflight.get("errorCount")) != 0:
        raise ValueError(f"{candidate_id} producer preflight errorCount must be 0.")
    viewer = mapping_value(candidate.get("viewer"))
    if viewer.get("status") != "ok":
        raise ValueError(f"{candidate_id} static viewer status must be ok.")
    decision = mapping_value(candidate.get("registryAcceptanceDecision"))
    if decision.get("status") != "external_required":
        raise ValueError(
            f"{candidate_id} registryAcceptanceDecision.status must be external_required."
        )
    if decision.get("producerAuthority") != "evidence_only":
        raise ValueError(
            f"{candidate_id} registryAcceptanceDecision.producerAuthority must be evidence_only."
        )


def candidate_bundle_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.candidate_root is None:
        return Path(string_value(candidate.get("sourceCandidatePath")))
    root = options.candidate_root.resolve()
    candidate_path = root / candidate_id / "candidate"
    if candidate_path.exists():
        return candidate_path
    return root / candidate_id


def candidate_bundle_display_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.candidate_root is None:
        return Path(string_value(candidate.get("sourceCandidatePath")))
    candidate_path = options.candidate_root / candidate_id / "candidate"
    if candidate_path.exists():
        return candidate_path
    return options.candidate_root / candidate_id


def producer_preflight_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.preflight_root is not None:
        return options.preflight_root.resolve() / f"{candidate_id}.json"
    return Path(string_value(mapping_value(candidate.get("producerPreflight")).get("reportPath")))


def producer_preflight_display_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.preflight_root is not None:
        return options.preflight_root / f"{candidate_id}.json"
    return Path(string_value(mapping_value(candidate.get("producerPreflight")).get("reportPath")))


def static_viewer_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.viewer_root is not None:
        return options.viewer_root.resolve() / candidate_id
    return Path(string_value(mapping_value(candidate.get("viewer")).get("outputPath")))


def static_viewer_display_path(
    options: SelectedCandidateHandoffProposalOptions,
    candidate: dict[str, Any],
) -> Path:
    candidate_id = string_value(candidate.get("id"))
    if options.viewer_root is not None:
        return options.viewer_root / candidate_id
    return Path(string_value(mapping_value(candidate.get("viewer")).get("outputPath")))


def producer_preflight_record(
    candidate: dict[str, Any],
    display_path: Path,
    source_path: Path | None,
) -> dict[str, Any]:
    declared = mapping_value(candidate.get("producerPreflight"))
    report = read_optional_json(source_path) if source_path is not None else None
    if report is not None:
        validate_preflight_report(string_value(candidate.get("id")), report)
        summary = mapping_value(report.get("summary"))
        return {
            "status": string_value(report.get("status")),
            "warningCount": integer_value(summary.get("warningCount")),
            "errorCount": integer_value(summary.get("errorCount")),
            "diagnosticCount": integer_value(summary.get("diagnosticCount")),
            "reportPath": str(display_path),
            "reportDigest": f"sha256:{sha256_file(source_path)}",
        }
    return {
        "status": string_value(declared.get("status")),
        "warningCount": integer_value(declared.get("warningCount")),
        "errorCount": integer_value(declared.get("errorCount")),
        "diagnosticCount": integer_value(declared.get("diagnosticCount")),
        "reportPath": str(display_path),
        "reportDigest": string_value(declared.get("reportDigest")),
    }


def validate_preflight_report(candidate_id: str, report: dict[str, Any]) -> None:
    expected = {
        "kind": "SpecHarvesterCandidateBundlePreflightReport",
        "schemaVersion": 1,
        "status": "passed",
        "authority": "producer_side_preflight",
    }
    for key, value in expected.items():
        if report.get(key) != value:
            raise ValueError(f"{candidate_id} preflight report {key} must be {value!r}.")
    summary = mapping_value(report.get("summary"))
    if integer_value(summary.get("warningCount")) != 0:
        raise ValueError(f"{candidate_id} preflight report warningCount must be 0.")
    if integer_value(summary.get("errorCount")) != 0:
        raise ValueError(f"{candidate_id} preflight report errorCount must be 0.")


def static_viewer_record(
    candidate: dict[str, Any],
    display_dir: Path,
    source_dir: Path | None,
) -> dict[str, Any]:
    declared = mapping_value(candidate.get("viewer"))
    index = display_dir / "index.html"
    payload = display_dir / "spec-package.json"
    source_index = source_dir / "index.html" if source_dir is not None else None
    source_payload = source_dir / "spec-package.json" if source_dir is not None else None
    return {
        "status": string_value(declared.get("status")),
        "outputPath": str(display_dir),
        "indexPath": str(index),
        "indexDigest": (
            f"sha256:{sha256_file(source_index)}"
            if source_index is not None and source_index.is_file()
            else string_value(declared.get("indexDigest"))
        ),
        "specPackagePath": str(payload),
        "specPackageDigest": (
            f"sha256:{sha256_file(source_payload)}"
            if source_payload is not None and source_payload.is_file()
            else string_value(declared.get("specPackageDigest"))
        ),
    }


def evidence_links(
    candidate: dict[str, Any],
    candidate_display_path: Path,
    candidate_source_path: Path | None,
    preflight_display_path: Path,
    preflight_source_path: Path | None,
    viewer_display_dir: Path,
    viewer_source_dir: Path | None,
    dry_run_display_path: Path,
    dry_run_path: Path,
) -> list[dict[str, Any]]:
    links = [
        artifact_link(
            role="candidate_bundle",
            path=str(candidate_display_path),
            path_scope="local_path",
            source_path=candidate_source_path,
        )
    ]
    for required_file in object_list(candidate.get("requiredFiles")):
        role = string_value(required_file.get("role"))
        relative_path = string_value(required_file.get("path"))
        display_path = safe_candidate_path(candidate_display_path, relative_path)
        source_path = (
            safe_candidate_path(candidate_source_path, relative_path)
            if candidate_source_path is not None
            else None
        )
        links.append(
            artifact_link(
                role=role,
                path=str(display_path) if display_path is not None else relative_path,
                path_scope="local_path",
                source_path=source_path,
                fallback_digest=string_value(required_file.get("digest")),
                missing_status="rejected" if display_path is None else "expected",
            )
        )
    viewer = mapping_value(candidate.get("viewer"))
    preflight = mapping_value(candidate.get("producerPreflight"))
    links.extend(
        [
            artifact_link(
                role="producer_preflight",
                path=str(preflight_display_path),
                path_scope="local_path",
                source_path=preflight_source_path,
                fallback_digest=string_value(preflight.get("reportDigest")),
            ),
            artifact_link(
                role="static_viewer",
                path=str(viewer_display_dir / "index.html"),
                path_scope="local_path",
                source_path=viewer_source_dir / "index.html"
                if viewer_source_dir is not None
                else None,
                fallback_digest=string_value(viewer.get("indexDigest")),
            ),
            artifact_link(
                role="static_viewer_payload",
                path=str(viewer_display_dir / "spec-package.json"),
                path_scope="local_path",
                source_path=viewer_source_dir / "spec-package.json"
                if viewer_source_dir is not None
                else None,
                fallback_digest=string_value(viewer.get("specPackageDigest")),
            ),
            artifact_link(
                role="selected_handoff_dry_run",
                path=str(dry_run_display_path),
                path_scope="local_path",
                source_path=dry_run_path,
            ),
        ]
    )
    return links


def artifact_link(
    *,
    role: str,
    path: str,
    path_scope: str,
    source_path: Path | None,
    fallback_digest: str = "",
    missing_status: str = "expected",
) -> dict[str, Any]:
    if source_path is None:
        status = missing_status
    elif source_path.exists():
        status = "present"
    else:
        status = "expected"
    link: dict[str, Any] = {
        "role": role,
        "path": path,
        "pathScope": path_scope,
        "status": status,
    }
    if source_path is not None and source_path.is_file():
        actual_digest = f"sha256:{sha256_file(source_path)}"
        link["digest"] = actual_digest
        link["digestSource"] = "local_file"
        if fallback_digest and actual_digest != fallback_digest:
            link["status"] = "rejected"
            link["expectedDigest"] = fallback_digest
            link["diagnostic"] = "local_file_digest_mismatch"
    elif fallback_digest:
        link["digest"] = fallback_digest
        link["digestSource"] = "selected_handoff_dry_run"
    return link


def deferred_candidate_record(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": string_value(candidate.get("id")),
        "reason": string_value(candidate.get("reason")),
        "requiredAction": string_value(candidate.get("requiredBeforeHandoff"))
        or "targeted_regeneration_before_selected_handoff",
        "handoffStatus": "excluded_from_selected_handoff",
    }


def registry_acceptance_decision(candidate: dict[str, Any]) -> dict[str, Any]:
    decision = mapping_value(candidate.get("registryAcceptanceDecision"))
    return {
        "status": "external_required",
        "requiredFor": string_value(decision.get("requiredFor")) or "public_index_acceptance",
        "producerAuthority": "evidence_only",
    }


def source_record(
    dry_run: dict[str, Any],
    dry_run_display_path: Path,
    dry_run_path: Path,
) -> dict[str, Any]:
    inputs = mapping_value(dry_run.get("inputs"))
    triage = mapping_value(inputs.get("candidateLayerTriageFixture"))
    product_verdict = mapping_value(dry_run.get("productVerdict"))
    return {
        "corpusId": string_value(mapping_value(dry_run.get("corpus")).get("id")),
        "triageFixture": {
            "kind": string_value(triage.get("kind")),
            "path": string_value(triage.get("path")),
            "status": string_value(triage.get("status")),
        },
        "selectedDryRunFixture": {
            "apiVersion": string_value(dry_run.get("apiVersion")),
            "kind": string_value(dry_run.get("kind")),
            "path": str(dry_run_display_path),
            "digest": f"sha256:{sha256_file(dry_run_path)}",
            "status": string_value(product_verdict.get("status")),
        },
    }


def safe_candidate_path(candidate_dir: Path, relative_path: str) -> Path | None:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidate = candidate_dir / relative
    try:
        candidate.resolve(strict=False).relative_to(candidate_dir.resolve())
    except ValueError:
        return None
    return candidate


def check_identity(payload: dict[str, Any], *, expected: dict[str, Any], artifact: str) -> None:
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(f"{artifact} {key} must be {value!r}.")


def read_required_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Required selected handoff artifact is missing: {path}")
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


def string_list_unsorted(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
