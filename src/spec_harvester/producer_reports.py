from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester import __version__
from spec_harvester.producer_receipt import CandidateOutputFile, digest_record, sha256_file

VALIDATION_REPORT_FILENAME = "validation-report.json"
DIAGNOSTICS_REPORT_FILENAME = "diagnostics.json"


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


def diagnostics_status(entries: list[dict[str, str]]) -> str:
    severities = {entry.get("severity") for entry in entries}
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warnings"
    return "clean"


def check_path_suffix(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", path).strip("_").lower()


def render_report_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
