from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from spec_harvester.producer_receipt import (
    PRODUCER_RECEIPT_API_VERSION,
    PRODUCER_RECEIPT_FILENAME,
    PRODUCER_RECEIPT_KIND,
    PRODUCER_RECEIPT_PROFILE,
    digest_record,
    sha256_file,
)
from spec_harvester.producer_reports import (
    DIAGNOSTICS_REPORT_FILENAME,
    VALIDATION_REPORT_FILENAME,
)

VALID_REVIEW_STATUSES = {"required", "pending", "approved", "rejected", "not_applicable"}
PUBLIC_ACCEPTANCE_REVIEW_STATUSES = {"required", "pending", "approved"}


@dataclass(frozen=True)
class CandidateBundlePreflightOptions:
    candidate: Path


class CandidateBundlePreflight:
    def __init__(self, options: CandidateBundlePreflightOptions):
        self.root = options.candidate
        self.resolved_root = options.candidate.resolve()
        self.diagnostics: list[dict[str, str]] = []

    def report(self) -> dict[str, Any]:
        manifest = self.read_yaml_object("specpm.yaml")
        receipt = self.read_json_object(PRODUCER_RECEIPT_FILENAME)
        validation = self.read_json_object(VALIDATION_REPORT_FILENAME)
        diagnostics = self.read_json_object(DIAGNOSTICS_REPORT_FILENAME)

        self.check_receipt_identity(receipt)
        self.check_manifest_subject(manifest, receipt)
        self.check_required_specs(manifest, receipt)
        self.check_evidence_paths(manifest)
        self.check_outputs(receipt)
        self.check_report_digest(receipt, validation, "validation")
        self.check_report_digest(receipt, diagnostics, "diagnostics")
        self.check_review_status(receipt)
        self.check_bundle_inputs(receipt)

        return {
            "kind": "SpecHarvesterCandidateBundlePreflightReport",
            "schemaVersion": 1,
            "status": "passed" if not self.errors() else "failed",
            "candidate": str(self.root),
            "summary": {
                "errorCount": len(self.errors()),
                "warningCount": len(self.warnings()),
                "diagnosticCount": len(self.diagnostics),
            },
            "diagnostics": sorted(
                self.diagnostics,
                key=lambda item: (item["severity"], item["code"], item.get("path", "")),
            ),
            "authority": "producer_side_preflight",
        }

    def read_json_object(self, relative: str) -> dict[str, Any] | None:
        path = self.root / relative
        if not path.is_file():
            self.error("required_file_missing", f"Required file is missing: {relative}", relative)
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self.error("json_invalid", f"Invalid JSON: {exc.msg}", relative)
            return None
        if not isinstance(value, dict):
            self.error("json_not_object", "JSON artifact must be an object.", relative)
            return None
        return value

    def read_yaml_object(self, relative: str) -> dict[str, Any] | None:
        path = self.root / relative
        if not path.is_file():
            self.error("required_file_missing", f"Required file is missing: {relative}", relative)
            return None
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            self.error("yaml_invalid", f"Invalid YAML: {exc}", relative)
            return None
        if not isinstance(value, dict):
            self.error("yaml_not_object", "YAML artifact must be an object.", relative)
            return None
        return value

    def check_receipt_identity(self, receipt: dict[str, Any] | None) -> None:
        if receipt is None:
            return
        expected = {
            "apiVersion": PRODUCER_RECEIPT_API_VERSION,
            "kind": PRODUCER_RECEIPT_KIND,
            "schemaVersion": 1,
            "receiptProfile": PRODUCER_RECEIPT_PROFILE,
        }
        for key, value in expected.items():
            if receipt.get(key) != value:
                self.error("receipt_identity_invalid", f"receipt.{key} must be {value!r}.")

    def check_manifest_subject(
        self,
        manifest: dict[str, Any] | None,
        receipt: dict[str, Any] | None,
    ) -> None:
        if manifest is None or receipt is None:
            return
        metadata = manifest.get("metadata")
        subject = receipt.get("subject")
        if not isinstance(metadata, dict) or not isinstance(subject, dict):
            self.error(
                "subject_metadata_missing", "Manifest metadata and receipt subject required."
            )
            return
        if metadata.get("id") != subject.get("packageId"):
            self.error("subject_package_id_mismatch", "Receipt packageId must match specpm.yaml.")
        if metadata.get("version") != subject.get("packageVersion"):
            self.error(
                "subject_package_version_mismatch", "Receipt packageVersion must match specpm.yaml."
            )

    def check_required_specs(
        self,
        manifest: dict[str, Any] | None,
        receipt: dict[str, Any] | None,
    ) -> None:
        if manifest is None or receipt is None:
            return
        manifest_specs = manifest_spec_paths(manifest)
        receipt_specs = receipt_spec_paths(receipt)
        for spec_path in sorted(manifest_specs | receipt_specs):
            self.bundle_file(spec_path, "required_spec_missing")
        if manifest_specs != receipt_specs:
            self.error(
                "subject_specs_mismatch", "Receipt boundarySpecs must match specpm.yaml specs."
            )

    def check_evidence_paths(self, manifest: dict[str, Any] | None) -> None:
        if manifest is None:
            return
        for spec_path in sorted(manifest_spec_paths(manifest)):
            spec = self.read_yaml_object(spec_path)
            if spec is None:
                continue
            evidence = spec.get("evidence")
            if not isinstance(evidence, list):
                continue
            for index, item in enumerate(evidence):
                if not isinstance(item, dict):
                    continue
                path = item.get("path")
                if path is not None:
                    self.bundle_file(path, "evidence_path_missing")
                paths = item.get("paths")
                if paths is None:
                    continue
                if not isinstance(paths, list):
                    self.error(
                        "evidence_paths_invalid",
                        "Evidence paths must be a list when present.",
                        f"{spec_path}:evidence.{index}.paths",
                    )
                    continue
                for evidence_path in paths:
                    self.bundle_file(evidence_path, "evidence_path_missing")

    def check_outputs(self, receipt: dict[str, Any] | None) -> None:
        if receipt is None:
            return
        outputs = receipt.get("outputs")
        if not isinstance(outputs, list):
            self.error("outputs_invalid", "Receipt outputs must be a list.")
            return
        for output in outputs:
            if not isinstance(output, dict):
                self.error("output_invalid", "Receipt output must be an object.")
                continue
            path = output.get("path")
            if path == PRODUCER_RECEIPT_FILENAME:
                self.error(
                    "receipt_self_hash", "producer-receipt.json must not appear in outputs[].", path
                )
                continue
            self.check_digest_record(output, path, "output_digest_mismatch")

    def check_report_digest(
        self,
        receipt: dict[str, Any] | None,
        report: dict[str, Any] | None,
        kind: str,
    ) -> None:
        if receipt is None or report is None:
            return
        section = receipt.get(kind)
        if not isinstance(section, dict):
            self.error(f"{kind}_section_invalid", f"Receipt {kind} section must be an object.")
            return
        path_key = "reportPath" if kind == "validation" else "path"
        digest_key = "reportDigest" if kind == "validation" else "digest"
        expected_path = (
            VALIDATION_REPORT_FILENAME if kind == "validation" else DIAGNOSTICS_REPORT_FILENAME
        )
        if section.get(path_key) != expected_path:
            self.error(
                f"{kind}_path_invalid", f"Receipt {kind}.{path_key} must be {expected_path}."
            )
        if section.get(digest_key) != digest_record(sha256_file(self.root / expected_path)):
            self.error(
                f"{kind}_digest_mismatch",
                f"Receipt {kind}.{digest_key} must match {expected_path}.",
            )

    def check_review_status(self, receipt: dict[str, Any] | None) -> None:
        if receipt is None:
            return
        review = receipt.get("humanReview")
        if not isinstance(review, dict):
            self.error("human_review_missing", "Receipt humanReview must be an object.")
            return
        status = review.get("status")
        if status not in VALID_REVIEW_STATUSES:
            self.error("human_review_status_invalid", "Receipt humanReview.status is invalid.")
        required_for = review.get("requiredFor")
        if (
            isinstance(required_for, list)
            and "public_index_acceptance" in required_for
            and status not in PUBLIC_ACCEPTANCE_REVIEW_STATUSES
        ):
            self.error(
                "public_acceptance_review_not_gated",
                "Public index acceptance must stay required, pending, or approved.",
            )

    def check_bundle_inputs(self, receipt: dict[str, Any] | None) -> None:
        if receipt is None:
            return
        inputs = receipt.get("inputs")
        if not isinstance(inputs, list):
            self.error("inputs_invalid", "Receipt inputs must be a list.")
            return
        for item in inputs:
            if not isinstance(item, dict):
                self.error("input_invalid", "Receipt input must be an object.")
                continue
            if item.get("location") != "bundle":
                continue
            self.check_digest_record(item, item.get("path"), "input_digest_mismatch")

    def check_digest_record(self, record: dict[str, Any], path: Any, code: str) -> None:
        target = self.bundle_file(path, code)
        if target is None:
            return
        if record.get("digest") != digest_record(sha256_file(target)):
            self.error(code, f"Digest mismatch for {path}.", path)

    def bundle_file(self, path: Any, missing_code: str) -> Path | None:
        if not isinstance(path, str) or not path:
            self.error(missing_code, "Bundle path must be a non-empty relative path.")
            return None
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            self.error("bundle_path_escape", f"Bundle path escapes candidate root: {path}", path)
            return None
        target = (self.root / relative).resolve()
        try:
            target.relative_to(self.resolved_root)
        except ValueError:
            self.error("bundle_path_escape", f"Bundle path escapes candidate root: {path}", path)
            return None
        if not target.is_file():
            self.error(missing_code, f"Bundle file is missing: {path}", path)
            return None
        return target

    def error(self, code: str, message: str, path: str | None = None) -> None:
        self.diagnostics.append(diagnostic("error", code, message, path))

    def errors(self) -> list[dict[str, str]]:
        return [item for item in self.diagnostics if item["severity"] == "error"]

    def warnings(self) -> list[dict[str, str]]:
        return [item for item in self.diagnostics if item["severity"] == "warning"]


def run_candidate_bundle_preflight(options: CandidateBundlePreflightOptions) -> dict[str, Any]:
    return CandidateBundlePreflight(options).report()


def diagnostic(severity: str, code: str, message: str, path: str | None = None) -> dict[str, str]:
    item = {"severity": severity, "code": code, "message": message}
    if path is not None:
        item["path"] = path
    return item


def manifest_spec_paths(manifest: dict[str, Any]) -> set[str]:
    specs = manifest.get("specs")
    if not isinstance(specs, list):
        return set()
    return {
        item["path"]
        for item in specs
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }


def receipt_spec_paths(receipt: dict[str, Any]) -> set[str]:
    subject = receipt.get("subject")
    if not isinstance(subject, dict):
        return set()
    specs = subject.get("boundarySpecs")
    if not isinstance(specs, list):
        return set()
    return {item for item in specs if isinstance(item, str)}
