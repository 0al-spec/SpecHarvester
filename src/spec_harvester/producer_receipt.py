from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from spec_harvester import __version__

PRODUCER_RECEIPT_FILENAME = "producer-receipt.json"
PRODUCER_RECEIPT_API_VERSION = "specpm.receipts/v0"
PRODUCER_RECEIPT_KIND = "SpecPMProducerReceipt"
PRODUCER_RECEIPT_PROFILE = "generated_spec_package_v0"
SPECHARVESTER_REPOSITORY = "https://github.com/0al-spec/SpecHarvester"


@dataclass(frozen=True)
class CandidateOutputFile:
    root: Path
    path: str
    role: str

    def record(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "role": self.role,
            "digest": digest_record(sha256_file(self.root / self.path)),
        }


@dataclass(frozen=True)
class ProducerReceiptInput:
    kind: str
    path: Path
    public_path: str
    location: str = "bundle"
    redaction: str = "none"

    def record(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "path": self.public_path,
            "location": self.location,
            "digest": digest_record(sha256_file(self.path)),
            "redaction": self.redaction,
        }


@dataclass(frozen=True)
class ProducerReceiptRequest:
    candidate_root: Path
    package_id: str
    package_version: str
    package_api_version: str
    spec_paths: tuple[str, ...]
    snapshot_path: Path
    configuration: dict[str, Any]
    output_files: tuple[CandidateOutputFile, ...]
    public_interface_index_path: Path | None = None
    validation_report_path: Path | None = None
    diagnostics_report_path: Path | None = None
    diagnostics_entries: tuple[dict[str, Any], ...] = ()


class ProducerReceipt:
    def __init__(self, request: ProducerReceiptRequest):
        self.request = request

    def payload(self) -> dict[str, Any]:
        subject = self.subject()
        inputs = self.inputs()
        configuration = self.configuration()
        outputs = self.outputs()
        return {
            "apiVersion": PRODUCER_RECEIPT_API_VERSION,
            "kind": PRODUCER_RECEIPT_KIND,
            "schemaVersion": 1,
            "receiptProfile": PRODUCER_RECEIPT_PROFILE,
            "receiptId": self.receipt_id(subject, inputs, configuration, outputs),
            "issuedAt": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "subject": subject,
            "producer": {
                "name": "SpecHarvester",
                "version": __version__,
                "repository": SPECHARVESTER_REPOSITORY,
                "workflow": "draft",
            },
            "inputs": inputs,
            "configuration": configuration,
            "outputs": outputs,
            "validation": self.validation(),
            "diagnostics": self.diagnostics(),
            "privacy": {
                "secretsIncluded": False,
                "redactions": [],
            },
            "audit": {
                "evidence": [
                    {
                        "kind": "producer_receipt_contract",
                        "path": "docs/PRODUCER_CANDIDATE_BUNDLE.md",
                        "retention": "repository",
                    }
                ]
            },
            "humanReview": {
                "handoff": "pull_request",
                "status": "required",
                "requiredFor": ["public_index_acceptance"],
            },
        }

    def subject(self) -> dict[str, Any]:
        return {
            "packageId": self.request.package_id,
            "packageVersion": self.request.package_version,
            "packageApiVersion": self.request.package_api_version,
            "packageRoot": ".",
            "boundarySpecs": list(self.request.spec_paths),
            "candidateStatus": "review-ready",
        }

    def inputs(self) -> list[dict[str, Any]]:
        records = [
            ProducerReceiptInput(
                kind="harvested_evidence",
                path=self.request.snapshot_path,
                **public_input_reference(
                    self.request.snapshot_path,
                    root=self.request.candidate_root,
                ),
            ).record()
        ]
        if self.request.public_interface_index_path is not None:
            records.append(
                ProducerReceiptInput(
                    kind="public_interface_index",
                    path=self.request.public_interface_index_path,
                    **public_input_reference(
                        self.request.public_interface_index_path,
                        root=self.request.candidate_root,
                    ),
                ).record()
            )
        records.append(
            {
                "kind": "config",
                "path": "spec_harvester.draft.configuration",
                "digest": configuration_digest_record(self.request.configuration),
                "redaction": "none",
            }
        )
        return sorted(records, key=lambda item: (item["kind"], item["path"]))

    def configuration(self) -> dict[str, Any]:
        return {
            "mode": "deterministic_draft",
            "deterministic": True,
            "templates": [{"name": "specpm-package-boundary", "version": __version__}],
            "digest": configuration_digest_record(self.request.configuration),
            "normalizedSummary": "SpecHarvester deterministic draft generation",
        }

    def outputs(self) -> list[dict[str, Any]]:
        records = [item.record() for item in self.request.output_files]
        return sorted(records, key=lambda item: item["path"])

    def validation(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "status": "not_run",
            "warningCount": 0,
            "errorCount": 0,
        }
        if self.request.validation_report_path is not None:
            report = read_json_object(self.request.validation_report_path)
            record["status"] = report.get("status", "unknown")
            record["warningCount"] = report.get("warningCount", 0)
            record["errorCount"] = report.get("errorCount", 0)
            record["reportPath"] = self.request.validation_report_path.name
            record["reportDigest"] = digest_record(sha256_file(self.request.validation_report_path))
        return record

    def diagnostics(self) -> dict[str, Any]:
        entries = [dict(entry) for entry in self.request.diagnostics_entries]
        record: dict[str, Any] = {
            "status": diagnostics_status(entries),
            "entries": entries,
        }
        if self.request.diagnostics_report_path is not None:
            report = read_json_object(self.request.diagnostics_report_path)
            report_entries = report.get("entries", [])
            if isinstance(report_entries, list):
                entries = [dict(entry) for entry in report_entries if isinstance(entry, dict)]
            record["status"] = report.get("status", diagnostics_status(entries))
            record["entries"] = entries
            record["path"] = self.request.diagnostics_report_path.name
            record["digest"] = digest_record(sha256_file(self.request.diagnostics_report_path))
        return record

    def receipt_id(
        self,
        subject: dict[str, Any],
        inputs: list[dict[str, Any]],
        configuration: dict[str, Any],
        outputs: list[dict[str, Any]],
    ) -> str:
        digest = canonical_sha256(
            {
                "subject": subject,
                "inputs": inputs,
                "configuration": configuration,
                "outputs": outputs,
            }
        )
        return (
            f"{self.request.package_id}@{self.request.package_version}:"
            f"producer:sha256:{digest[:12]}"
        )

    def write(self) -> Path:
        path = self.request.candidate_root / PRODUCER_RECEIPT_FILENAME
        path.write_text(render_receipt_json(self.payload()), encoding="utf-8")
        return path


def render_receipt_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return value


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def digest_record(value: str) -> dict[str, str]:
    return {"algorithm": "sha256", "value": value}


def configuration_digest_record(configuration: dict[str, Any]) -> dict[str, str]:
    return digest_record(canonical_sha256(configuration))


def public_input_reference(path: Path, *, root: Path) -> dict[str, str]:
    try:
        return {
            "public_path": path.resolve().relative_to(root.resolve()).as_posix(),
            "location": "bundle",
        }
    except ValueError:
        return {"public_path": f"external:{path.name}", "location": "external"}


def diagnostics_status(entries: list[dict[str, Any]]) -> str:
    severities = {entry.get("severity") for entry in entries}
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warnings"
    return "clean"
