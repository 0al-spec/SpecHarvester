from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester import __version__
from spec_harvester.producer_receipt import (
    CandidateOutputFile,
    digest_record,
    sha256_file,
)

VALIDATION_REPORT_FILENAME = "validation-report.json"
DIAGNOSTICS_REPORT_FILENAME = "diagnostics.json"
AUTHOR_READY_QUALITY_REPORT_FILENAME = "author-ready-draft-quality-report.json"
AUTHOR_READY_QUALITY_REPORT_API_VERSION = "spec-harvester.author-ready-draft-quality/v0"
AUTHOR_READY_QUALITY_REPORT_KIND = "SpecHarvesterAuthorReadyDraftQualityReport"
AUTHOR_READY_STATUS_READY = "author_ready_draft"
AUTHOR_READY_STATUS_NEEDS_REGENERATION = "needs_regeneration"
AUTHOR_READY_STATUS_BLOCKED = "blocked"
AUTHOR_READY_STOP_DECISION_STOP = "stop_for_author_review"
AUTHOR_READY_STOP_DECISION_CONTINUE = "continue_generation"
AUTHOR_READY_STOP_DECISION_BLOCKED = "blocked_until_inputs_change"
AUTHOR_READY_STOP_POLICY_SUMMARY_VERSION = 1
AUTHOR_REVIEW_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ProducerReportRequest:
    candidate_root: Path
    package_id: str
    package_version: str
    package_api_version: str
    spec_paths: tuple[str, ...]
    output_files: tuple[CandidateOutputFile, ...]
    has_external_inputs: bool = False


class ProducerValidationReport:
    def __init__(self, request: ProducerReportRequest):
        self.request = request

    def payload(self) -> dict[str, Any]:
        checks = [
            self.check_file("specpm.yaml", "manifest"),
            *[self.check_file(path, "boundary_spec") for path in self.request.spec_paths],
        ]
        errors = [check for check in checks if check["status"] != "passed"]
        return {
            "kind": "SpecHarvesterProducerValidationReport",
            "schemaVersion": 1,
            "producer": {"name": "SpecHarvester", "version": __version__},
            "subject": self.subject(),
            "status": "invalid" if errors else "valid",
            "warningCount": 0,
            "errorCount": len(errors),
            "checks": checks,
            "authority": "producer_side_shape_check",
            "notes": [
                "This report records producer-side candidate shape checks only.",
                "SpecPM validation and maintainer review remain separate authority boundaries.",
            ],
        }

    def subject(self) -> dict[str, Any]:
        return {
            "packageId": self.request.package_id,
            "packageVersion": self.request.package_version,
            "packageApiVersion": self.request.package_api_version,
            "packageRoot": ".",
        }

    def check_file(self, path: str, role: str) -> dict[str, Any]:
        file_path = self.request.candidate_root / path
        exists = file_path.is_file()
        check: dict[str, Any] = {
            "id": f"required_{role}_{check_path_suffix(path)}",
            "status": "passed" if exists else "failed",
            "path": path,
            "role": role,
        }
        if exists:
            check["digest"] = digest_record(sha256_file(file_path))
        else:
            check["message"] = f"Required {role} file is missing."
        return check

    def write(self) -> Path:
        path = self.request.candidate_root / VALIDATION_REPORT_FILENAME
        path.write_text(render_report_json(self.payload()), encoding="utf-8")
        return path


class ProducerDiagnosticsReport:
    def __init__(self, request: ProducerReportRequest):
        self.request = request

    def payload(self) -> dict[str, Any]:
        entries = self.entries()
        return {
            "kind": "SpecHarvesterProducerDiagnosticsReport",
            "schemaVersion": 1,
            "producer": {"name": "SpecHarvester", "version": __version__},
            "subject": {
                "packageId": self.request.package_id,
                "packageVersion": self.request.package_version,
                "packageRoot": ".",
            },
            "status": diagnostics_status(entries),
            "entries": entries,
            "privacy": {
                "secretsIncluded": False,
                "rawSourceIncluded": False,
                "privatePromptsIncluded": False,
            },
            "review": {
                "requiredFor": ["public_index_acceptance"],
                "acceptanceAuthority": "maintainer_review",
            },
        }

    def entries(self) -> list[dict[str, str]]:
        entries = [
            {
                "severity": "info",
                "code": "privacy_public_handoff",
                "message": (
                    "Generated diagnostics are path, digest, and summary metadata only; "
                    "raw private source, private prompts, tokens, and credentials are excluded."
                ),
            },
            {
                "severity": "info",
                "code": "human_review_required",
                "message": (
                    "Generated candidates require maintainer review before public index acceptance."
                ),
            },
            {
                "severity": "info",
                "code": "producer_receipt_is_evidence",
                "message": "Producer receipts are evidence and do not imply SpecPM acceptance.",
            },
        ]
        if self.request.has_external_inputs:
            entries.append(
                {
                    "severity": "info",
                    "code": "external_input_reference",
                    "message": (
                        "At least one receipt input is outside the candidate bundle and is marked "
                        "with location: external."
                    ),
                }
            )
        return entries

    def write(self) -> Path:
        path = self.request.candidate_root / DIAGNOSTICS_REPORT_FILENAME
        path.write_text(render_report_json(self.payload()), encoding="utf-8")
        return path


@dataclass(frozen=True)
class AuthorReadyDraftQualityReportRequest:
    report: ProducerReportRequest
    validation_report_path: Path
    diagnostics_report_path: Path


class AuthorReadyDraftQualityReport:
    def __init__(self, request: AuthorReadyDraftQualityReportRequest):
        self.request = request

    def payload(self) -> dict[str, Any]:
        validation = read_optional_report_object(
            self.request.validation_report_path,
            missing_status="missing",
        )
        diagnostics = read_optional_report_object(
            self.request.diagnostics_report_path,
            missing_status="missing",
        )
        gates = self.hard_gates(validation, diagnostics)
        dimensions = self.dimensions(gates, diagnostics)
        action_items = self.action_items(gates, dimensions)
        status = author_ready_status(gates, diagnostics)
        return {
            "apiVersion": AUTHOR_READY_QUALITY_REPORT_API_VERSION,
            "kind": AUTHOR_READY_QUALITY_REPORT_KIND,
            "schemaVersion": 1,
            "producer": {"name": "SpecHarvester", "version": __version__},
            "subject": {
                "packageId": self.request.report.package_id,
                "packageVersion": self.request.report.package_version,
                "packageApiVersion": self.request.report.package_api_version,
                "packageRoot": ".",
                "boundarySpecs": list(self.request.report.spec_paths),
            },
            "status": status,
            "authorReadyDraft": {
                "status": status,
                "summary": author_ready_summary(status),
                "stopReason": author_ready_stop_reason(status),
                "hardGateStatus": hard_gate_rollup(gates),
                "actionItemCount": len(action_items),
            },
            "hardGates": gates,
            "dimensions": dimensions,
            "authorActionItems": action_items,
            "nonAuthority": [
                "This quality report is producer-side review evidence only.",
                "It is not SpecPM registry acceptance.",
                "It is not maintainer approval.",
                "It is not upstream project endorsement.",
            ],
        }

    def hard_gates(
        self,
        validation: dict[str, Any],
        diagnostics: dict[str, Any],
    ) -> list[dict[str, Any]]:
        output_paths = {item.path for item in self.request.report.output_files}
        output_roles = {item.role for item in self.request.report.output_files}
        required_paths = {
            "specpm.yaml",
            *self.request.report.spec_paths,
            VALIDATION_REPORT_FILENAME,
            DIAGNOSTICS_REPORT_FILENAME,
        }
        missing_paths = sorted(
            path
            for path in required_paths
            if not (self.request.report.candidate_root / path).is_file()
        )
        diagnostics_entries = diagnostics_report_entries(diagnostics)
        critical_entries = [
            entry for entry in diagnostics_entries if entry.get("severity") == "error"
        ]
        warning_entries = [
            entry for entry in diagnostics_entries if entry.get("severity") == "warning"
        ]
        evidence_output_count = sum(
            1
            for item in self.request.report.output_files
            if item.role in {"evidence", "foreign_artifact"} and output_file_exists(item)
        )
        return [
            {
                "id": "producer_validation",
                "status": (
                    "passed"
                    if validation.get("status") == "valid"
                    and integer_value(validation.get("errorCount")) == 0
                    else "failed"
                ),
                "source": VALIDATION_REPORT_FILENAME,
                "details": {
                    "validationStatus": string_value(validation.get("status")),
                    "warningCount": integer_value(validation.get("warningCount")),
                    "errorCount": integer_value(validation.get("errorCount")),
                },
            },
            {
                "id": "critical_diagnostics",
                "status": (
                    "passed"
                    if not critical_entries
                    and diagnostics.get("status") not in {"failed", "invalid", "missing"}
                    else "failed"
                ),
                "source": DIAGNOSTICS_REPORT_FILENAME,
                "details": {
                    "diagnosticsStatus": string_value(diagnostics.get("status")),
                    "criticalCount": len(critical_entries),
                    "warningCount": len(warning_entries),
                },
            },
            {
                "id": "required_bundle_files",
                "status": "passed" if not missing_paths else "failed",
                "details": {
                    "required": sorted(required_paths),
                    "missing": missing_paths,
                },
            },
            {
                "id": "producer_receipt_planned",
                "status": "passed" if "producer-receipt.json" not in output_paths else "failed",
                "details": {
                    "reason": "producer-receipt.json must stay outside outputs to avoid self-hash.",
                    "receiptIncludedInOutputs": "producer-receipt.json" in output_paths,
                },
            },
            {
                "id": "evidence_links_present",
                "status": "passed" if evidence_output_count else "review_required",
                "details": {
                    "evidenceOutputCount": evidence_output_count,
                    "outputRoles": sorted(output_roles),
                },
            },
            {
                "id": "authority_boundary",
                "status": "passed",
                "details": {
                    "registryAcceptance": "external_maintainer_review_required",
                    "candidateStatus": "preview_review_material",
                },
            },
        ]

    def dimensions(
        self,
        gates: list[dict[str, Any]],
        diagnostics: dict[str, Any],
    ) -> list[dict[str, Any]]:
        gate_map = {gate["id"]: gate for gate in gates}
        diagnostics_status = string_value(diagnostics.get("status"))
        evidence_gate = gate_map["evidence_links_present"]
        validation_gate = gate_map["producer_validation"]
        diagnostic_gate = gate_map["critical_diagnostics"]
        return [
            dimension_record(
                "validation",
                "strong" if validation_gate["status"] == "passed" else "blocked",
                "Producer validation report is valid and has no errors.",
            ),
            dimension_record(
                "evidenceCoverage",
                "strong" if evidence_gate["status"] == "passed" else "needs_review",
                "Generated claims have at least one bundled evidence output.",
            ),
            dimension_record(
                "repositorySpecificity",
                "needs_review" if evidence_gate["status"] == "review_required" else "reviewable",
                "Static repository evidence is present, but author curation remains required.",
            ),
            dimension_record(
                "packageTopology",
                "reviewable",
                "Single candidate topology is reviewable; "
                "package-set topology is checked separately.",
            ),
            dimension_record(
                "claimConservatism",
                "blocked" if diagnostic_gate["status"] == "failed" else "reviewable",
                "Diagnostics did not report critical overclaiming issues.",
            ),
            dimension_record(
                "authorActionability",
                "strong",
                "The report emits explicit author action items instead of a numeric score.",
            ),
            dimension_record(
                "authorityBoundary",
                "strong" if diagnostics_status != "failed" else "blocked",
                "SpecPM registry acceptance and maintainer approval remain external.",
            ),
        ]

    def action_items(
        self,
        gates: list[dict[str, Any]],
        dimensions: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        items = []
        for gate in gates:
            if gate["status"] == "failed":
                items.append(
                    action_item(
                        f"fix_{gate['id']}",
                        "error",
                        "regenerate_or_repair",
                        gate["id"],
                        f"Resolve failed hard gate `{gate['id']}` before author review.",
                    )
                )
            elif gate["status"] == "review_required":
                items.append(
                    action_item(
                        f"review_{gate['id']}",
                        "warning",
                        "author_review",
                        gate["id"],
                        f"Review `{gate['id']}` before treating this as an author-ready draft.",
                    )
                )
        items.extend(
            [
                action_item(
                    "review_package_identity_and_summary",
                    "info",
                    "author_review",
                    "specpm.yaml",
                    "Confirm package id, name, summary, license, keywords, and version.",
                ),
                action_item(
                    "review_capabilities_and_intents",
                    "info",
                    "author_review",
                    "specs/*.spec.yaml",
                    "Confirm capabilities, intents, constraints, and evidence support.",
                ),
                action_item(
                    "run_specpm_validation_before_submission",
                    "info",
                    "handoff",
                    "SpecPM",
                    "Run downstream SpecPM validation before requesting public index acceptance.",
                ),
            ]
        )
        critical_diagnostics_gate = next(
            (gate for gate in gates if gate["id"] == "critical_diagnostics"),
            {},
        )
        critical_diagnostics_details = mapping_value(critical_diagnostics_gate.get("details"))
        if (
            critical_diagnostics_details.get("diagnosticsStatus") == "warnings"
            or integer_value(critical_diagnostics_details.get("warningCount")) > 0
        ):
            items.append(
                action_item(
                    "review_diagnostics_warnings",
                    "warning",
                    "author_review",
                    DIAGNOSTICS_REPORT_FILENAME,
                    "Review diagnostics warnings before rerunning or handing off the draft.",
                )
            )
        if any(dimension["rating"] == "needs_review" for dimension in dimensions):
            items.append(
                action_item(
                    "complete_evidence_review",
                    "warning",
                    "author_review",
                    "evidence",
                    "Add or confirm evidence links for claims that are still weak or generic.",
                )
            )
        return items

    def write(self) -> Path:
        path = self.request.report.candidate_root / AUTHOR_READY_QUALITY_REPORT_FILENAME
        path.write_text(render_report_json(self.payload()), encoding="utf-8")
        return path


def diagnostics_status(entries: list[dict[str, str]]) -> str:
    severities = {entry.get("severity") for entry in entries}
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warnings"
    return "clean"


def check_path_suffix(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", path).strip("_").lower()


def author_ready_status(
    gates: list[dict[str, Any]],
    diagnostics: dict[str, Any],
) -> str:
    if any(gate["status"] == "failed" for gate in gates):
        return AUTHOR_READY_STATUS_BLOCKED
    if string_value(diagnostics.get("status")) == "warnings":
        return AUTHOR_READY_STATUS_NEEDS_REGENERATION
    if any(gate["status"] == "review_required" for gate in gates):
        return AUTHOR_READY_STATUS_NEEDS_REGENERATION
    return AUTHOR_READY_STATUS_READY


def author_ready_summary(status: str) -> str:
    if status == AUTHOR_READY_STATUS_READY:
        return "Valid starter package is ready for author review and curation."
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION:
        return "Draft is structurally usable, but generator or evidence gaps should be reviewed."
    return "Draft is blocked by failed hard gates and should not be handed to authors yet."


def author_ready_stop_reason(status: str) -> str:
    if status == AUTHOR_READY_STATUS_READY:
        return "remaining_work_is_author_reviewable"
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION:
        return "review_or_regeneration_needed_before_author_handoff"
    return "hard_gate_failed"


def author_ready_stop_decision(status: str) -> str:
    if status == AUTHOR_READY_STATUS_READY:
        return AUTHOR_READY_STOP_DECISION_STOP
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION:
        return AUTHOR_READY_STOP_DECISION_CONTINUE
    return AUTHOR_READY_STOP_DECISION_BLOCKED


def author_ready_stop_policy_summary(
    member_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    normalized = [
        normalize_author_ready_member_report(member, index)
        for index, member in enumerate(member_reports)
    ]
    counts = {
        "total": len(normalized),
        AUTHOR_READY_STATUS_READY: 0,
        AUTHOR_READY_STATUS_NEEDS_REGENERATION: 0,
        AUTHOR_READY_STATUS_BLOCKED: 0,
    }
    for member in normalized:
        counts[member["status"]] += 1
    status = aggregate_author_ready_status(counts)
    return {
        "schemaVersion": AUTHOR_READY_STOP_POLICY_SUMMARY_VERSION,
        "status": status,
        "decision": author_ready_stop_decision(status),
        "summary": aggregate_author_ready_summary(status, counts),
        "memberCounts": counts,
        "members": [
            {
                "packageId": member["packageId"],
                "status": member["status"],
                "decision": author_ready_stop_decision(member["status"]),
                "qualityReportPath": member["qualityReportPath"],
                "stopReason": member["stopReason"],
                "actionItemCount": member["actionItemCount"],
            }
            for member in normalized
        ],
        "blockingReasons": blocking_reasons(normalized),
        "reviewableDimensions": reviewable_dimensions(normalized),
        "topAuthorActionItems": top_author_action_items(normalized),
        "nonAuthority": [
            "The stop-policy summary is producer-side review evidence only.",
            "It is not SpecPM registry acceptance.",
            "It is not maintainer approval.",
            "It is not upstream project endorsement.",
        ],
    }


def author_review_payload(
    author_ready_summary: dict[str, Any],
    member_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    normalized = [
        normalize_author_ready_member_report(member, index)
        for index, member in enumerate(member_reports)
    ]
    return {
        "schemaVersion": AUTHOR_REVIEW_SCHEMA_VERSION,
        "status": string_value(author_ready_summary.get("status")),
        "decision": string_value(author_ready_summary.get("decision")),
        "summary": string_value(author_ready_summary.get("summary")),
        "checklist": author_review_checklist(author_ready_summary),
        "weakClaims": author_review_weak_claims(author_ready_summary),
        "evidenceGaps": author_review_evidence_gaps(author_ready_summary, normalized),
        "recommendedEdits": author_review_recommended_edits(author_ready_summary),
        "memberActions": [author_review_member_action(member) for member in normalized],
        "nonAuthority": [
            "The author review surface is producer-side review evidence only.",
            "It is not SpecPM registry acceptance.",
            "It is not maintainer approval.",
            "It is not upstream project endorsement.",
        ],
    }


def author_review_checklist(author_ready_summary: dict[str, Any]) -> list[dict[str, str]]:
    decision = string_value(author_ready_summary.get("decision"))
    first_item = {
        AUTHOR_READY_STOP_DECISION_STOP: review_item(
            "stop_generation",
            "info",
            "handoff",
            "package-set",
            "Stop generation and hand the valid starter package set to the author for review.",
        ),
        AUTHOR_READY_STOP_DECISION_CONTINUE: review_item(
            "review_or_regenerate",
            "warning",
            "generator_review",
            "package-set",
            "Review warning-level gaps before treating this package set as author-ready.",
        ),
        AUTHOR_READY_STOP_DECISION_BLOCKED: review_item(
            "repair_blockers",
            "error",
            "repair",
            "package-set",
            "Do not hand off until blocked member reports or inputs are repaired.",
        ),
    }.get(
        decision,
        review_item(
            "review_unknown_decision",
            "warning",
            "author_review",
            "package-set",
            "Review the package-set stop decision before handoff.",
        ),
    )
    return [
        first_item,
        review_item(
            "confirm_identity",
            "info",
            "author_review",
            "specpm.yaml",
            "Confirm package IDs, names, summaries, license, keywords, and versions.",
        ),
        review_item(
            "review_capabilities",
            "info",
            "author_review",
            "specs/*.spec.yaml",
            "Review capabilities, intents, constraints, and public interface claims.",
        ),
        review_item(
            "verify_evidence",
            "info",
            "author_review",
            "evidence",
            "Verify that every important claim has enough repository-specific evidence.",
        ),
        review_item(
            "decide_outcome",
            "info",
            "author_review",
            "handoff",
            "Decide whether to keep, edit, reject, or regenerate each member package.",
        ),
    ]


def author_review_weak_claims(author_ready_summary: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for dimension in object_list(author_ready_summary.get("reviewableDimensions")):
        identifier = string_value(dimension.get("id"))
        if not identifier:
            continue
        package_ids = string_list(dimension.get("packageIds"))
        records.append(
            {
                "id": identifier,
                "severity": "warning",
                "packageIds": package_ids,
                "ratings": string_list(dimension.get("ratings")),
                "summary": (
                    f"Review {identifier} for "
                    f"{', '.join(package_ids) if package_ids else 'package-set members'}."
                ),
            }
        )
    return records


def author_review_evidence_gaps(
    author_ready_summary: dict[str, Any],
    members: list[dict[str, Any]],
) -> list[dict[str, str]]:
    gaps = []
    for item in object_list(author_ready_summary.get("topAuthorActionItems")):
        if action_item_mentions_evidence(item):
            gaps.append(author_review_action_item(item, fallback_severity="warning"))
    for member in members:
        for dimension in object_list(mapping_value(member["qualityReport"]).get("dimensions")):
            if string_value(dimension.get("id")) == "evidenceCoverage" and string_value(
                dimension.get("rating")
            ) in {"needs_review", "reviewable"}:
                gaps.append(
                    review_item(
                        f"review_evidence_coverage_{member['packageId']}",
                        "warning",
                        "author_review",
                        member["packageId"],
                        (
                            "Review evidence coverage for "
                            f"{member['packageId']} before accepting its claims."
                        ),
                    )
                )
    return dedupe_review_items(gaps)


def author_review_recommended_edits(
    author_ready_summary: dict[str, Any],
) -> list[dict[str, str]]:
    return [
        author_review_action_item(item)
        for item in object_list(author_ready_summary.get("topAuthorActionItems"))
    ]


def author_review_member_action(member: dict[str, Any]) -> dict[str, Any]:
    quality_report = mapping_value(member["qualityReport"])
    action_items = [
        author_review_action_item(item)
        for item in object_list(quality_report.get("authorActionItems"))
    ]
    reviewable_dimensions = [
        {
            "id": string_value(dimension.get("id")),
            "rating": string_value(dimension.get("rating")),
            "summary": string_value(dimension.get("summary")),
        }
        for dimension in object_list(quality_report.get("dimensions"))
        if string_value(dimension.get("rating")) in {"needs_review", "reviewable"}
    ]
    return {
        "packageId": member["packageId"],
        "status": member["status"],
        "decision": author_ready_stop_decision(member["status"]),
        "qualityReportPath": member["qualityReportPath"],
        "actionItems": action_items,
        "reviewableDimensions": reviewable_dimensions,
        "evidenceGaps": [item for item in action_items if action_item_mentions_evidence(item)],
    }


def stop_policy_summary_from_diagnostics(
    *,
    source_status: str,
    error_count: int,
    warning_count: int,
    subject_count: int,
) -> dict[str, Any]:
    status = stop_policy_status_from_diagnostics(source_status, error_count, warning_count)
    if status == AUTHOR_READY_STATUS_READY and subject_count <= 0:
        status = AUTHOR_READY_STATUS_NEEDS_REGENERATION
    return {
        "schemaVersion": AUTHOR_READY_STOP_POLICY_SUMMARY_VERSION,
        "status": status,
        "decision": author_ready_stop_decision(status),
        "sourceStatus": source_status,
        "subjectCount": subject_count,
        "diagnosticCounts": {
            "errorCount": error_count,
            "warningCount": warning_count,
        },
        "reason": stop_policy_reason(status, subject_count),
        "summary": proposal_stop_policy_summary(status),
        "nonAuthority": [
            "The stop-policy summary is producer-side review evidence only.",
            "It is not SpecPM registry acceptance.",
            "It is not maintainer approval.",
            "It is not upstream project endorsement.",
        ],
    }


def stop_policy_status_from_diagnostics(
    source_status: str,
    error_count: int,
    warning_count: int,
) -> str:
    if error_count > 0 or source_status in {"failed", "invalid", "missing"}:
        return AUTHOR_READY_STATUS_BLOCKED
    if warning_count > 0 or source_status in {"warning", "warnings"}:
        return AUTHOR_READY_STATUS_NEEDS_REGENERATION
    return AUTHOR_READY_STATUS_READY


def proposal_stop_policy_summary(status: str) -> str:
    if status == AUTHOR_READY_STATUS_READY:
        return "Proposal diagnostics are clean; stop model iteration and hand off for review."
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION:
        return (
            "Proposal has warning-level gaps; continue generation or review evidence "
            "before handoff."
        )
    return "Proposal has blocking diagnostics; do not hand off until inputs or model output change."


def stop_policy_reason(status: str, subject_count: int) -> str:
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION and subject_count <= 0:
        return "no_proposal_subjects"
    return author_ready_stop_reason(status)


def review_item(
    identifier: str,
    severity: str,
    category: str,
    target: str,
    summary: str,
) -> dict[str, str]:
    return {
        "id": identifier,
        "severity": severity,
        "category": category,
        "target": target,
        "summary": summary,
    }


def author_review_action_item(
    item: dict[str, Any],
    *,
    fallback_severity: str = "info",
) -> dict[str, str]:
    package_id = string_value(item.get("packageId"))
    target = string_value(item.get("target"))
    if package_id and target and target != package_id:
        target = f"{package_id}:{target}"
    elif package_id:
        target = package_id
    return review_item(
        string_value(item.get("id")) or "review_item",
        string_value(item.get("severity")) or fallback_severity,
        string_value(item.get("category")) or "author_review",
        target,
        string_value(item.get("summary")),
    )


def action_item_mentions_evidence(item: dict[str, Any]) -> bool:
    haystack = " ".join(
        string_value(item.get(key)) for key in ("id", "category", "target", "summary")
    ).lower()
    return "evidence" in haystack


def dedupe_review_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        key = (item["id"], item["target"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def normalize_author_ready_member_report(
    member: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    package_id = string_value(member.get("packageId")) or f"member-{index + 1}"
    quality_report_path = string_value(member.get("qualityReportPath"))
    report = mapping_value(member.get("qualityReport"))
    author_ready = mapping_value(report.get("authorReadyDraft"))
    status = string_value(author_ready.get("status")) or string_value(report.get("status"))
    if status not in {
        AUTHOR_READY_STATUS_READY,
        AUTHOR_READY_STATUS_NEEDS_REGENERATION,
        AUTHOR_READY_STATUS_BLOCKED,
    }:
        status = AUTHOR_READY_STATUS_BLOCKED
    read_error = string_value(report.get("readError"))
    stop_reason = string_value(author_ready.get("stopReason"))
    if not stop_reason and read_error:
        stop_reason = f"quality_report_unreadable:{read_error}"
    return {
        "packageId": package_id,
        "qualityReportPath": quality_report_path,
        "qualityReport": report,
        "status": status,
        "stopReason": stop_reason or author_ready_stop_reason(status),
        "actionItemCount": integer_value(author_ready.get("actionItemCount")),
        "readError": read_error,
    }


def aggregate_author_ready_status(counts: dict[str, int]) -> str:
    if counts["total"] == 0:
        return AUTHOR_READY_STATUS_BLOCKED
    if counts[AUTHOR_READY_STATUS_BLOCKED] > 0:
        return AUTHOR_READY_STATUS_BLOCKED
    if counts[AUTHOR_READY_STATUS_NEEDS_REGENERATION] > 0:
        return AUTHOR_READY_STATUS_NEEDS_REGENERATION
    return AUTHOR_READY_STATUS_READY


def aggregate_author_ready_summary(status: str, counts: dict[str, int]) -> str:
    if status == AUTHOR_READY_STATUS_READY:
        return "All member candidates are valid starter packages ready for author review."
    if status == AUTHOR_READY_STATUS_NEEDS_REGENERATION:
        return (
            "At least one member candidate needs regeneration or evidence review before "
            "author handoff."
        )
    if counts["total"] == 0:
        return "No member quality reports were available; package-set handoff is blocked."
    return "At least one member candidate is blocked by failed hard gates."


def blocking_reasons(members: list[dict[str, Any]]) -> list[dict[str, str]]:
    reasons = []
    for member in members:
        if member["status"] != AUTHOR_READY_STATUS_BLOCKED:
            continue
        reason = member["stopReason"] or author_ready_stop_reason(member["status"])
        if member["readError"]:
            reason = f"quality_report_unreadable:{member['readError']}"
        reasons.append(
            {
                "packageId": member["packageId"],
                "qualityReportPath": member["qualityReportPath"],
                "reason": reason,
            }
        )
    return sorted(reasons, key=lambda item: item["packageId"])


def reviewable_dimensions(members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dimensions: dict[str, dict[str, Any]] = {}
    for member in members:
        for dimension in object_list(mapping_value(member["qualityReport"]).get("dimensions")):
            rating = string_value(dimension.get("rating"))
            if rating not in {"needs_review", "reviewable"}:
                continue
            identifier = string_value(dimension.get("id"))
            if not identifier:
                continue
            record = dimensions.setdefault(
                identifier,
                {
                    "id": identifier,
                    "ratings": set(),
                    "packageIds": [],
                    "count": 0,
                },
            )
            record["ratings"].add(rating)
            record["packageIds"].append(member["packageId"])
            record["count"] += 1
    return [
        {
            "id": identifier,
            "ratings": sorted(record["ratings"]),
            "packageIds": sorted(set(record["packageIds"])),
            "count": record["count"],
        }
        for identifier, record in sorted(dimensions.items())
    ]


def top_author_action_items(
    members: list[dict[str, Any]],
    *,
    limit: int = 8,
) -> list[dict[str, str]]:
    severity_rank = {"error": 0, "warning": 1, "info": 2}
    records = []
    seen: set[tuple[str, str]] = set()
    for member in members:
        for item in object_list(mapping_value(member["qualityReport"]).get("authorActionItems")):
            identifier = string_value(item.get("id"))
            key = (member["packageId"], identifier)
            if not identifier or key in seen:
                continue
            seen.add(key)
            records.append(
                {
                    "packageId": member["packageId"],
                    "id": identifier,
                    "severity": string_value(item.get("severity")),
                    "category": string_value(item.get("category")),
                    "target": string_value(item.get("target")),
                    "summary": string_value(item.get("summary")),
                }
            )
    return sorted(
        records,
        key=lambda item: (
            severity_rank.get(item["severity"], 9),
            item["packageId"],
            item["id"],
        ),
    )[:limit]


def hard_gate_rollup(gates: list[dict[str, Any]]) -> str:
    statuses = {gate["status"] for gate in gates}
    if "failed" in statuses:
        return "failed"
    if "review_required" in statuses:
        return "review_required"
    return "passed"


def diagnostics_report_entries(diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    entries = diagnostics.get("entries")
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def read_optional_report_object(path: Path, *, missing_status: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"status": missing_status, "entries": [], "readError": "missing"}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        return {"status": "invalid", "entries": [], "readError": str(exc)}
    if not isinstance(value, dict):
        return {"status": "invalid", "entries": [], "readError": "report_not_object"}
    return value


def output_file_exists(item: CandidateOutputFile) -> bool:
    relative = Path(item.path)
    if relative.is_absolute() or ".." in relative.parts:
        return False
    return (item.root / relative).is_file()


def dimension_record(identifier: str, rating: str, summary: str) -> dict[str, Any]:
    return {
        "id": identifier,
        "rating": rating,
        "advisory": True,
        "summary": summary,
    }


def action_item(
    identifier: str,
    severity: str,
    category: str,
    target: str,
    summary: str,
) -> dict[str, str]:
    return {
        "id": identifier,
        "severity": severity,
        "category": category,
        "target": target,
        "summary": summary,
    }


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str) and item)


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) else 0


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def render_report_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
