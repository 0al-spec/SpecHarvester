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
    read_json_object,
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
    diagnostics_entries: tuple[dict[str, Any], ...] = ()


class AuthorReadyDraftQualityReport:
    def __init__(self, request: AuthorReadyDraftQualityReportRequest):
        self.request = request

    def payload(self) -> dict[str, Any]:
        validation = read_json_object(self.request.validation_report_path)
        diagnostics = read_json_object(self.request.diagnostics_report_path)
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
        has_evidence = bool({"evidence", "foreign_artifact"} & output_roles)
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
                "status": "passed" if not critical_entries else "failed",
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
                "status": "passed" if has_evidence else "review_required",
                "details": {
                    "evidenceOutputCount": sum(
                        1 for item in self.request.report.output_files if item.role == "evidence"
                    ),
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


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) else 0


def render_report_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
