from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.fresh_candidate_refresh_run import (
    FRESH_CANDIDATE_REFRESH_RUN_API_VERSION,
    FRESH_CANDIDATE_REFRESH_RUN_KIND,
    FRESH_CANDIDATE_REFRESH_RUN_SCHEMA_VERSION,
)
from spec_harvester.producer_receipt import digest_record, sha256_file

BASELINE_SUBMISSION_HANDOFF_API_VERSION = "spec-harvester.baseline-submission-handoff/v0"
BASELINE_SUBMISSION_HANDOFF_KIND = "SpecHarvesterBaselineSubmissionHandoff"
BASELINE_SUBMISSION_HANDOFF_SCHEMA_VERSION = 1
MISSING_BASELINE_DIAGNOSTIC = "refresh_decision_prepare_current_contract_files_missing"


@dataclass(frozen=True)
class BaselineSubmissionHandoffOptions:
    fresh_candidate_refresh_run: Path
    specpm_prepare_report: Path | None = None


def build_baseline_submission_handoff(
    options: BaselineSubmissionHandoffOptions,
) -> dict[str, Any]:
    fresh_run = read_json_object(options.fresh_candidate_refresh_run, "fresh candidate refresh run")
    check_fresh_run_identity(fresh_run)

    prepare_report: dict[str, Any] | None = None
    missing_baseline_errors: list[dict[str, Any]] = []
    if options.specpm_prepare_report is not None:
        prepare_report = read_json_object(options.specpm_prepare_report, "SpecPM prepare report")
        missing_baseline_errors = missing_baseline_diagnostics(prepare_report)
        if not missing_baseline_errors:
            raise ValueError(
                f"SpecPM prepare report does not contain {MISSING_BASELINE_DIAGNOSTIC} diagnostics"
            )

    return {
        "apiVersion": BASELINE_SUBMISSION_HANDOFF_API_VERSION,
        "kind": BASELINE_SUBMISSION_HANDOFF_KIND,
        "schemaVersion": BASELINE_SUBMISSION_HANDOFF_SCHEMA_VERSION,
        "status": (
            "first_submission_required" if missing_baseline_errors else "baseline_review_required"
        ),
        "reason": (
            "missing_current_generated_baseline"
            if missing_baseline_errors
            else "specpm_prepare_report_not_provided"
        ),
        "inputs": input_records(options),
        "source": fresh_run.get("source") if isinstance(fresh_run.get("source"), dict) else {},
        "packageSet": package_set_record(fresh_run),
        "freshGeneratedRoot": fresh_run.get("freshGeneratedRoot", {}),
        "specpmPrepareReport": specpm_prepare_report_record(
            prepare_report=prepare_report,
            missing_baseline_errors=missing_baseline_errors,
        ),
        "baselineWorkflow": {
            "blockedRefreshDecision": True,
            "requiredBefore": "specpm_refresh_decision",
            "maintainerActions": [
                {
                    "id": "first_submission_review",
                    "description": (
                        "Review generated candidates as a new package-set submission before "
                        "any refresh decision exists."
                    ),
                },
                {
                    "id": "seed_baseline",
                    "description": (
                        "Create an explicit generated baseline only after maintainer review "
                        "decides the producer output is suitable as baseline evidence."
                    ),
                },
                {
                    "id": "reject_or_request_regeneration",
                    "description": (
                        "Reject the handoff or ask the producer to regenerate when package "
                        "selection, provenance, or evidence quality is insufficient."
                    ),
                },
            ],
        },
        "authority": {
            "producerEvidenceAuthority": "evidence_only",
            "registryAuthority": "SpecPM maintainer review",
            "noRegistryMutation": True,
            "notRefreshDecision": True,
        },
        "nonGoals": [
            "specpm_acceptance",
            "registry_publication",
            "baseline_mutation",
            "refresh_decision_emission",
            "source_repository_execution",
            "package_manager_execution",
        ],
    }


def write_baseline_submission_handoff(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


def input_records(options: BaselineSubmissionHandoffOptions) -> dict[str, Any]:
    records: dict[str, Any] = {
        "freshCandidateRefreshRun": {
            "path": str(options.fresh_candidate_refresh_run),
            "digest": digest_record(sha256_file(options.fresh_candidate_refresh_run)),
            "apiVersion": FRESH_CANDIDATE_REFRESH_RUN_API_VERSION,
            "kind": FRESH_CANDIDATE_REFRESH_RUN_KIND,
        }
    }
    if options.specpm_prepare_report is not None:
        records["specpmPrepareReport"] = {
            "path": str(options.specpm_prepare_report),
            "digest": digest_record(sha256_file(options.specpm_prepare_report)),
        }
    return records


def package_set_record(fresh_run: dict[str, Any]) -> dict[str, Any]:
    package_set = fresh_run.get("packageSet")
    if not isinstance(package_set, dict):
        package_set = {}
    packages = fresh_run.get("packages")
    if not isinstance(packages, list):
        packages = []
    member_ids = [
        str(item.get("packageId"))
        for item in packages
        if isinstance(item, dict) and isinstance(item.get("packageId"), str)
    ]
    return {
        "id": package_set.get("id"),
        "candidateCount": package_set.get("candidateCount", len(member_ids)),
        "memberPackageIds": member_ids,
        "contractFileCount": sum(
            len(item.get("contractFiles", []))
            for item in packages
            if isinstance(item, dict) and isinstance(item.get("contractFiles"), list)
        ),
    }


def specpm_prepare_report_record(
    *,
    prepare_report: dict[str, Any] | None,
    missing_baseline_errors: list[dict[str, Any]],
) -> dict[str, Any]:
    if prepare_report is None:
        return {
            "status": "not_provided",
            "missingBaselineDiagnosticCount": 0,
            "diagnosticCode": MISSING_BASELINE_DIAGNOSTIC,
        }
    decision = prepare_report.get("decision")
    decision_status = ""
    decision_reason = ""
    if isinstance(decision, dict):
        decision_payload = decision.get("decision")
        if isinstance(decision_payload, dict):
            decision_status = str(decision_payload.get("status") or "")
            decision_reason = str(decision_payload.get("reason") or "")
    return {
        "status": "missing_baseline",
        "decisionStatus": decision_status,
        "decisionReason": decision_reason,
        "missingBaselineDiagnosticCount": len(missing_baseline_errors),
        "diagnosticCode": MISSING_BASELINE_DIAGNOSTIC,
        "sampleDiagnostics": missing_baseline_errors[:5],
    }


def missing_baseline_diagnostics(report: dict[str, Any]) -> list[dict[str, Any]]:
    errors = report.get("errors")
    if not isinstance(errors, list):
        return []
    diagnostics: list[dict[str, Any]] = []
    for item in errors:
        if not isinstance(item, dict):
            continue
        if item.get("code") != MISSING_BASELINE_DIAGNOSTIC:
            continue
        diagnostics.append(
            {
                "code": MISSING_BASELINE_DIAGNOSTIC,
                "field": str(item.get("field") or ""),
                "message": str(item.get("message") or ""),
            }
        )
    return diagnostics


def check_fresh_run_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != FRESH_CANDIDATE_REFRESH_RUN_API_VERSION:
        raise ValueError(
            f"Unsupported fresh candidate refresh run apiVersion: {payload.get('apiVersion')!r}"
        )
    if payload.get("kind") != FRESH_CANDIDATE_REFRESH_RUN_KIND:
        raise ValueError(f"Unsupported fresh candidate refresh run kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != FRESH_CANDIDATE_REFRESH_RUN_SCHEMA_VERSION:
        raise ValueError(
            "Unsupported fresh candidate refresh run schemaVersion: "
            f"{payload.get('schemaVersion')!r}"
        )


def read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Cannot read {label}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid {label} JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label.capitalize()} must be a JSON object")
    return payload


def render_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
