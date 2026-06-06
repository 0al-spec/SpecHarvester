from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.package_set_drafter import (
    PACKAGE_RELATION_PROPOSALS_API_VERSION,
    PACKAGE_RELATION_PROPOSALS_FILENAME,
    PACKAGE_RELATION_PROPOSALS_KIND,
    PACKAGE_SET_DRAFT_API_VERSION,
    PACKAGE_SET_DRAFT_FILENAME,
    PACKAGE_SET_DRAFT_KIND,
)
from spec_harvester.producer_receipt import digest_record, sha256_file

BUNDLE_SET_PREFLIGHT_API_VERSION = "spec-harvester.bundle-set-preflight/v0"
BUNDLE_SET_PREFLIGHT_KIND = "SpecHarvesterBundleSetPreflightReport"
BUNDLE_SET_PREFLIGHT_SCHEMA_VERSION = 1
RELATION_REVIEW_STATUSES = {"producer_observed", "pending", "approved", "rejected"}


@dataclass(frozen=True)
class BundleSetPreflightOptions:
    bundle_set: Path


class BundleSetPreflight:
    def __init__(self, options: BundleSetPreflightOptions):
        self.root = options.bundle_set
        self.resolved_root = options.bundle_set.resolve()
        self.diagnostics: list[dict[str, str]] = []
        self.candidate_reports: list[dict[str, Any]] = []

    def report(self) -> dict[str, Any]:
        draft = self.read_json_object(PACKAGE_SET_DRAFT_FILENAME)
        relations = self.read_json_object(PACKAGE_RELATION_PROPOSALS_FILENAME)
        candidates = candidate_records(draft)
        relation_records_value = relation_records(relations)

        self.check_draft_identity(draft)
        self.check_relation_identity(relations)
        self.check_candidate_ids(candidates)
        self.check_candidate_bundles(candidates)
        self.check_relation_inputs(draft, relations)
        self.check_relation_records(candidates, relation_records_value)
        self.check_summary_counts(draft, candidates, relation_records_value)
        self.check_review_boundaries(draft, relations, relation_records_value)

        return {
            "apiVersion": BUNDLE_SET_PREFLIGHT_API_VERSION,
            "kind": BUNDLE_SET_PREFLIGHT_KIND,
            "schemaVersion": BUNDLE_SET_PREFLIGHT_SCHEMA_VERSION,
            "status": "passed" if not self.errors() else "failed",
            "bundleSet": str(self.root),
            "artifacts": {
                "packageSetDraft": PACKAGE_SET_DRAFT_FILENAME,
                "packageRelationProposals": PACKAGE_RELATION_PROPOSALS_FILENAME,
            },
            "summary": {
                "candidateCount": len(candidates),
                "candidatePreflightPassedCount": sum(
                    1 for item in self.candidate_reports if item.get("status") == "passed"
                ),
                "relationCount": len(relation_records_value),
                "errorCount": len(self.errors()),
                "warningCount": len(self.warnings()),
                "diagnosticCount": len(self.diagnostics),
            },
            "candidateReports": sorted(
                self.candidate_reports,
                key=lambda item: str(item.get("packageId") or item.get("candidatePath") or ""),
            ),
            "diagnostics": sorted(
                self.diagnostics,
                key=lambda item: (item["severity"], item["code"], item.get("path", "")),
            ),
            "authority": "producer_side_preflight",
            "nonGoals": [
                "specpm_acceptance",
                "relation_acceptance",
                "package_execution",
                "dependency_installation",
            ],
        }

    def read_json_object(self, relative: str) -> dict[str, Any] | None:
        path = self.bundle_file(relative, "required_file_missing")
        if path is None:
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

    def check_draft_identity(self, draft: dict[str, Any] | None) -> None:
        if draft is None:
            return
        expected = {
            "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
            "kind": PACKAGE_SET_DRAFT_KIND,
            "schemaVersion": 1,
        }
        for key, value in expected.items():
            if draft.get(key) != value:
                self.error("package_set_draft_identity_invalid", f"{key} must be {value!r}.")

    def check_relation_identity(self, relations: dict[str, Any] | None) -> None:
        if relations is None:
            return
        expected = {
            "apiVersion": PACKAGE_RELATION_PROPOSALS_API_VERSION,
            "kind": PACKAGE_RELATION_PROPOSALS_KIND,
            "schemaVersion": 1,
        }
        for key, value in expected.items():
            if relations.get(key) != value:
                self.error("relation_proposals_identity_invalid", f"{key} must be {value!r}.")

    def check_candidate_ids(self, candidates: list[dict[str, Any]]) -> None:
        seen: set[str] = set()
        for candidate in candidates:
            package_id = candidate.get("packageId")
            if not isinstance(package_id, str) or not package_id:
                self.error("candidate_package_id_missing", "Candidate packageId is required.")
                continue
            if package_id in seen:
                self.error(
                    "candidate_package_id_duplicate",
                    f"Duplicate candidate packageId: {package_id}.",
                    package_id,
                )
            seen.add(package_id)

    def check_candidate_bundles(self, candidates: list[dict[str, Any]]) -> None:
        for candidate in candidates:
            package_id = str(candidate.get("packageId") or "")
            candidate_path = candidate.get("candidatePath")
            candidate_root = self.bundle_dir(candidate_path, "candidate_bundle_missing")
            if candidate_root is None:
                self.candidate_reports.append(
                    {
                        "packageId": package_id,
                        "candidatePath": candidate_path,
                        "status": "failed",
                    }
                )
                continue
            report = run_candidate_bundle_preflight(
                CandidateBundlePreflightOptions(candidate=candidate_root)
            )
            diagnostics_status = self.candidate_diagnostics_status(candidate_root, candidate)
            self.candidate_reports.append(
                {
                    "packageId": package_id,
                    "candidatePath": candidate_path,
                    "status": report["status"],
                    "diagnosticsStatus": diagnostics_status,
                    "errorCount": report["summary"]["errorCount"],
                    "warningCount": report["summary"]["warningCount"],
                }
            )
            if report["status"] != "passed":
                self.error(
                    "candidate_preflight_failed",
                    f"Candidate bundle preflight failed for {package_id}.",
                    str(candidate_path),
                )
            if diagnostics_status not in {"clean", "warnings"}:
                self.error(
                    "candidate_diagnostics_status_failed",
                    f"Candidate diagnostics status is not handoff-safe: {diagnostics_status}.",
                    str(candidate_path),
                )

    def candidate_diagnostics_status(
        self,
        candidate_root: Path,
        candidate: dict[str, Any],
    ) -> str:
        path = candidate.get("diagnosticsReport")
        if isinstance(path, str) and path:
            relative = Path(path)
            if not relative.is_absolute() and ".." not in relative.parts:
                diagnostics_path = self.root / relative
            else:
                diagnostics_path = candidate_root / "diagnostics.json"
        else:
            diagnostics_path = candidate_root / "diagnostics.json"
        try:
            payload = json.loads(diagnostics_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return "unreadable"
        if not isinstance(payload, dict):
            return "invalid"
        status = payload.get("status")
        if not isinstance(status, str) or not status:
            return "missing"
        return status

    def check_relation_inputs(
        self,
        draft: dict[str, Any] | None,
        relations: dict[str, Any] | None,
    ) -> None:
        if draft is None or relations is None:
            return
        inputs = relations.get("inputs")
        if not isinstance(inputs, dict):
            self.error("relation_inputs_invalid", "Relation inputs must be an object.")
            return
        self.check_package_set_draft_input(inputs.get("packageSetDraft"))
        self.check_workspace_inventory_input(draft, inputs.get("workspaceInventory"))

    def check_package_set_draft_input(self, input_record: Any) -> None:
        if not isinstance(input_record, dict):
            self.error(
                "relation_package_set_draft_input_invalid",
                "Relation packageSetDraft input must be an object.",
            )
            return
        if input_record.get("path") != PACKAGE_SET_DRAFT_FILENAME:
            self.error(
                "relation_package_set_draft_path_invalid",
                "Relation packageSetDraft input must point at package-set-draft.json.",
            )
        if input_record.get("apiVersion") != PACKAGE_SET_DRAFT_API_VERSION:
            self.error(
                "relation_package_set_draft_api_version_invalid",
                "Relation packageSetDraft input apiVersion is invalid.",
            )
        if input_record.get("kind") != PACKAGE_SET_DRAFT_KIND:
            self.error(
                "relation_package_set_draft_kind_invalid",
                "Relation packageSetDraft input kind is invalid.",
            )
        expected = digest_record(sha256_file(self.root / PACKAGE_SET_DRAFT_FILENAME))
        if input_record.get("digest") != expected:
            self.error(
                "relation_package_set_draft_digest_mismatch",
                "Relation packageSetDraft digest must match package-set-draft.json.",
                PACKAGE_SET_DRAFT_FILENAME,
            )

    def check_workspace_inventory_input(
        self,
        draft: dict[str, Any],
        input_record: Any,
    ) -> None:
        draft_record = draft.get("workspaceInventory")
        if not isinstance(draft_record, dict):
            self.error(
                "package_set_workspace_inventory_invalid",
                "Package-set draft workspaceInventory must be an object.",
            )
            return
        if not isinstance(input_record, dict):
            self.error(
                "relation_workspace_inventory_input_invalid",
                "Relation workspaceInventory input must be an object.",
            )
            return
        for key in ("path", "digest", "apiVersion", "kind"):
            if input_record.get(key) != draft_record.get(key):
                self.error(
                    "workspace_inventory_input_mismatch",
                    f"Relation workspaceInventory.{key} must match package-set draft.",
                    f"workspaceInventory.{key}",
                )
        path = draft_record.get("path")
        if isinstance(path, str) and (self.root / path).is_file():
            expected = digest_record(sha256_file(self.root / path))
            if draft_record.get("digest") != expected:
                self.error(
                    "workspace_inventory_digest_mismatch",
                    "Workspace inventory digest must match file when present.",
                    path,
                )

    def check_relation_records(
        self,
        candidates: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> None:
        candidate_ids = {
            candidate["packageId"]
            for candidate in candidates
            if isinstance(candidate.get("packageId"), str)
        }
        for relation in relations:
            source_id = relation_endpoint_id(relation.get("source"))
            target_id = relation_endpoint_id(relation.get("target"))
            relation_id = relation.get("id")
            relation_path = str(relation_id or "relation")
            if relation.get("type") != "contains":
                self.error("relation_type_unsupported", "Only contains relations are supported.")
            if source_id not in candidate_ids:
                self.error(
                    "relation_source_missing",
                    f"Relation source package is missing: {source_id}.",
                    relation_path,
                )
            if target_id not in candidate_ids:
                self.error(
                    "relation_target_missing",
                    f"Relation target package is missing: {target_id}.",
                    relation_path,
                )
            if source_id == target_id and source_id is not None:
                self.error(
                    "relation_self_reference",
                    "Relation source and target must be different packages.",
                    relation_path,
                )

    def check_summary_counts(
        self,
        draft: dict[str, Any] | None,
        candidates: list[dict[str, Any]],
        relations: list[dict[str, Any]],
    ) -> None:
        if draft is None:
            return
        summary = draft.get("summary")
        if not isinstance(summary, dict):
            self.error("package_set_summary_invalid", "Package-set summary must be an object.")
            return
        expected = {
            "candidateCount": len(candidates),
            "relationProposalCount": len(relations),
        }
        for key, value in expected.items():
            if summary.get(key) != value:
                self.error(
                    "package_set_summary_count_mismatch",
                    f"Package-set summary.{key} must be {value}.",
                    f"summary.{key}",
                )
        relation_proposals = draft.get("relationProposals")
        if isinstance(relation_proposals, dict):
            if relation_proposals.get("path") != PACKAGE_RELATION_PROPOSALS_FILENAME:
                self.error(
                    "package_set_relation_path_invalid",
                    "Package-set relationProposals.path is invalid.",
                )
            if relation_proposals.get("relationCount") != len(relations):
                self.error(
                    "package_set_relation_count_mismatch",
                    "Package-set relationProposals.relationCount must match relations.",
                )
        else:
            self.error(
                "package_set_relation_proposals_invalid",
                "Package-set relationProposals must be an object.",
            )

    def check_review_boundaries(
        self,
        draft: dict[str, Any] | None,
        relations: dict[str, Any] | None,
        relation_records_value: list[dict[str, Any]],
    ) -> None:
        if draft is not None and draft.get("authority") != "producer_observed_review_evidence":
            self.error(
                "package_set_authority_invalid",
                "Package-set draft authority must stay producer observed.",
            )
        if relations is None:
            return
        if relations.get("authority") != "producer_observed_review_evidence":
            self.error(
                "relation_authority_invalid",
                "Relation proposal authority must stay producer observed.",
            )
        if relations.get("reviewStatus") not in RELATION_REVIEW_STATUSES:
            self.error(
                "relation_review_status_invalid",
                "Relation proposal reviewStatus is invalid.",
            )
        for relation in relation_records_value:
            if relation.get("reviewStatus") not in RELATION_REVIEW_STATUSES:
                self.error(
                    "relation_record_review_status_invalid",
                    "Relation record reviewStatus is invalid.",
                    str(relation.get("id") or ""),
                )

    def bundle_file(self, path: Any, missing_code: str) -> Path | None:
        target = self.bundle_path(path, missing_code)
        if target is None:
            return None
        if not target.is_file():
            self.error(missing_code, f"Bundle-set file is missing: {path}", str(path))
            return None
        return target

    def bundle_dir(self, path: Any, missing_code: str) -> Path | None:
        target = self.bundle_path(path, missing_code)
        if target is None:
            return None
        if not target.is_dir():
            self.error(missing_code, f"Bundle-set directory is missing: {path}", str(path))
            return None
        return target

    def bundle_path(self, path: Any, code: str) -> Path | None:
        if not isinstance(path, str) or not path:
            self.error(code, "Bundle-set path must be a non-empty relative path.")
            return None
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            self.error("bundle_set_path_escape", f"Path escapes bundle-set root: {path}", path)
            return None
        target = (self.root / relative).resolve()
        try:
            target.relative_to(self.resolved_root)
        except ValueError:
            self.error("bundle_set_path_escape", f"Path escapes bundle-set root: {path}", path)
            return None
        return target

    def error(self, code: str, message: str, path: str | None = None) -> None:
        self.diagnostics.append(diagnostic("error", code, message, path))

    def errors(self) -> list[dict[str, str]]:
        return [item for item in self.diagnostics if item["severity"] == "error"]

    def warnings(self) -> list[dict[str, str]]:
        return [item for item in self.diagnostics if item["severity"] == "warning"]


def run_bundle_set_preflight(options: BundleSetPreflightOptions) -> dict[str, Any]:
    return BundleSetPreflight(options).report()


def candidate_records(draft: dict[str, Any] | None) -> list[dict[str, Any]]:
    if draft is None:
        return []
    candidates = draft.get("candidates")
    if not isinstance(candidates, list):
        return []
    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def relation_records(relations: dict[str, Any] | None) -> list[dict[str, Any]]:
    if relations is None:
        return []
    records = relations.get("relations")
    if not isinstance(records, list):
        return []
    return [relation for relation in records if isinstance(relation, dict)]


def relation_endpoint_id(endpoint: Any) -> str | None:
    if not isinstance(endpoint, dict):
        return None
    value = endpoint.get("packageId")
    if not isinstance(value, str) or not value:
        return None
    return value


def diagnostic(severity: str, code: str, message: str, path: str | None = None) -> dict[str, str]:
    item = {"severity": severity, "code": code, "message": message}
    if path is not None:
        item["path"] = path
    return item
