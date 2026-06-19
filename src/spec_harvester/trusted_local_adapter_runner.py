from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.producer_receipt import canonical_sha256, sha256_file

TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_API_VERSION = (
    "spec-harvester.trusted-local-adapter-run-request/v0"
)
TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_KIND = "SpecHarvesterTrustedLocalAdapterRunRequest"
TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_AUTHORITY = "producer_trusted_local_adapter_run_request_only"

TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_API_VERSION = (
    "spec-harvester.trusted-local-adapter-run-preflight/v0"
)
TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_KIND = "SpecHarvesterTrustedLocalAdapterRunPreflightReport"
TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_AUTHORITY = "producer_trusted_local_adapter_run_preflight_only"

TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION = "spec-harvester.trusted-local-adapter-run/v0"
TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND = "SpecHarvesterTrustedLocalAdapterRunReport"
TRUSTED_LOCAL_ADAPTER_RUN_REPORT_SCHEMA_VERSION = 1
TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY = "producer_trusted_local_adapter_run_report_only"


@dataclass(frozen=True)
class TrustedLocalAdapterRunOptions:
    request: Path
    preflight: Path


def build_trusted_local_adapter_run_report(
    options: TrustedLocalAdapterRunOptions,
) -> dict[str, Any]:
    return TrustedLocalAdapterRunnerSkeleton(options).report()


def write_trusted_local_adapter_run_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(payload), encoding="utf-8")


class TrustedLocalAdapterRunnerSkeleton:
    def __init__(self, options: TrustedLocalAdapterRunOptions):
        self.options = options

    def report(self) -> dict[str, Any]:
        request = read_json_object(self.options.request, "trusted local adapter run request")
        preflight = read_json_object(
            self.options.preflight,
            "trusted local adapter run preflight report",
        )
        request_digest = digest_string(self.options.request)
        preflight_digest = digest_string(self.options.preflight)
        artifact_root = path_reference_root(self.options.request, self.options.preflight)

        check_request_identity(request)
        check_preflight_identity(preflight)
        check_preflight_result(preflight)
        check_preflight_request_reference(
            preflight,
            request_path=self.options.request,
            request_digest=request_digest,
            reference_root=artifact_root,
        )

        request_ref = artifact_reference(
            path=self.options.request,
            reference_root=artifact_root,
            digest=request_digest,
            api_version=TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_API_VERSION,
            kind=TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_KIND,
            schema_version=TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_SCHEMA_VERSION,
            authority=TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_AUTHORITY,
        )
        preflight_ref = artifact_reference(
            path=self.options.preflight,
            reference_root=artifact_root,
            digest=preflight_digest,
            api_version=TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_API_VERSION,
            kind=TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_KIND,
            schema_version=TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_SCHEMA_VERSION,
            authority=TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_AUTHORITY,
        )
        checks = accepted_checks()
        return {
            "apiVersion": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION,
            "kind": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND,
            "schemaVersion": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_SCHEMA_VERSION,
            "status": "no_execution_report_emitted",
            "runId": run_id(request_ref, preflight_ref),
            "authority": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
            "contract": {
                "purpose": (
                    "Validate trusted local adapter request and preflight artifacts through "
                    "a disabled no-execution runner skeleton."
                ),
                "contractVersion": "0.1.0",
                "defaultExecution": "disabled",
                "runnerAuthority": TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
                "requestAuthority": TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_AUTHORITY,
                "preflightAuthority": TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_AUTHORITY,
                "runnerReportIsExecutionPermission": False,
            },
            "request": request_ref,
            "preflight": {
                **preflight_ref,
                "status": "passed",
                "requestDigestVerified": True,
                "preflightPassIsExecutionPermission": False,
            },
            "runner": {
                "mode": "disabled_no_execution_skeleton",
                "enabled": False,
                "runtimeImplemented": False,
                "adapterExecution": "not_run",
                "adapterCodeLoaded": False,
                "adapterCodeImportAttempted": False,
                "adapterProcessSpawned": False,
                "executedAdapterCount": 0,
                "dependencyInstallation": "not_allowed",
                "packageManagers": "not_invoked",
                "harvestedCodeExecution": "not_allowed",
                "aiExecution": "not_run",
                "networkAccess": "none",
            },
            "validation": {
                "status": "passed",
                "acceptedChecks": checks,
                "errorCount": 0,
                "warningCount": 1,
            },
            "executionBoundary": {
                "adapterExecution": "not_run",
                "adapterCodeLoaded": False,
                "executedAdapterCount": 0,
                "runtimeImplemented": False,
                "requestIsExecutionPermission": False,
                "preflightPassIsExecutionPermission": False,
                "runnerReportIsExecutionPermission": False,
                "appliedToDrafting": False,
                "registryAuthority": False,
                "adapterOutputAccepted": False,
            },
            "summary": {
                "acceptedCount": len(checks),
                "errorCount": 0,
                "warningCount": 1,
                "executedAdapterCount": 0,
                "runtimeImplementedAdapterCount": 0,
            },
            "diagnostics": [
                {
                    "severity": "info",
                    "code": "trusted_local_adapter_runner_skeleton",
                    "message": (
                        "Disabled runner skeleton validated request and preflight artifacts "
                        "without loading adapter code or running adapter processes."
                    ),
                },
                {
                    "severity": "warning",
                    "code": "runner_skeleton_is_not_execution_permission",
                    "message": (
                        "This report is producer-side review evidence only and does not "
                        "grant execution authority or registry authority."
                    ),
                },
            ],
            "nonAuthorityStatements": non_authority_statements(),
            "followUp": {
                "batchEvidenceHandoffTask": "P41-T5",
                "realLocalReadinessValidationTask": "P41-T6",
            },
        }


def accepted_checks() -> list[dict[str, str]]:
    return [
        {
            "code": "request_identity_valid",
            "status": "passed",
            "target": "request",
            "message": "Request identity matches the trusted local adapter run request contract.",
        },
        {
            "code": "request_boundary_no_execution",
            "status": "passed",
            "target": "request.executionBoundary",
            "message": "Request records no execution permission and adapterExecution not_run.",
        },
        {
            "code": "preflight_identity_valid",
            "status": "passed",
            "target": "preflight",
            "message": "Preflight identity matches the trusted local adapter preflight contract.",
        },
        {
            "code": "preflight_status_passed_review_only",
            "status": "passed",
            "target": "preflight.result",
            "message": "Preflight passed but explicitly remains review evidence only.",
        },
        {
            "code": "preflight_request_digest_matches",
            "status": "passed",
            "target": "preflight.request",
            "message": "Preflight request digest matches the supplied request artifact bytes.",
        },
        {
            "code": "runner_disabled_no_execution",
            "status": "passed",
            "target": "runner",
            "message": "Runner skeleton did not load adapter code or spawn adapter processes.",
        },
        {
            "code": "non_authority_boundary_preserved",
            "status": "passed",
            "target": "executionBoundary",
            "message": "Runner report is not execution permission and has no registry authority.",
        },
    ]


def check_request_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_API_VERSION:
        raise ValueError(f"Unsupported request apiVersion: {payload.get('apiVersion')!r}")
    if payload.get("kind") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_KIND:
        raise ValueError(f"Unsupported request kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_SCHEMA_VERSION:
        raise ValueError(f"Unsupported request schemaVersion: {payload.get('schemaVersion')!r}")
    if payload.get("authority") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_AUTHORITY:
        raise ValueError(f"Unsupported request authority: {payload.get('authority')!r}")
    contract = object_value(payload.get("contract"), "request contract")
    if contract.get("requestIsExecutionPermission") is not False:
        raise ValueError("Request contract must record requestIsExecutionPermission false")
    boundary = object_value(payload.get("executionBoundary"), "request executionBoundary")
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError("Request executionBoundary adapterExecution must be not_run")
    if boundary.get("adapterCodeLoaded") is not False:
        raise ValueError("Request executionBoundary adapterCodeLoaded must be false")
    if boundary.get("registryAuthority") is not False:
        raise ValueError("Request executionBoundary registryAuthority must be false")


def check_preflight_identity(payload: dict[str, Any]) -> None:
    if payload.get("apiVersion") != TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_API_VERSION:
        raise ValueError(f"Unsupported preflight apiVersion: {payload.get('apiVersion')!r}")
    if payload.get("kind") != TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_KIND:
        raise ValueError(f"Unsupported preflight kind: {payload.get('kind')!r}")
    if payload.get("schemaVersion") != TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_SCHEMA_VERSION:
        raise ValueError(f"Unsupported preflight schemaVersion: {payload.get('schemaVersion')!r}")
    if payload.get("authority") != TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_AUTHORITY:
        raise ValueError(f"Unsupported preflight authority: {payload.get('authority')!r}")


def check_preflight_result(payload: dict[str, Any]) -> None:
    result = object_value(payload.get("result"), "preflight result")
    if result.get("status") != "passed":
        raise ValueError("Preflight result status must be passed")
    if result.get("preflightPassIsExecutionPermission") is not False:
        raise ValueError("Preflight result must record preflightPassIsExecutionPermission false")
    boundary = object_value(payload.get("executionBoundary"), "preflight executionBoundary")
    if boundary.get("adapterExecution") != "not_run":
        raise ValueError("Preflight executionBoundary adapterExecution must be not_run")
    if boundary.get("adapterCodeLoaded") is not False:
        raise ValueError("Preflight executionBoundary adapterCodeLoaded must be false")
    if boundary.get("registryAuthority") is not False:
        raise ValueError("Preflight executionBoundary registryAuthority must be false")


def check_preflight_request_reference(
    payload: dict[str, Any],
    *,
    request_path: Path,
    request_digest: str,
    reference_root: Path,
) -> None:
    reference = object_value(payload.get("request"), "preflight request reference")
    if reference.get("kind") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_KIND:
        raise ValueError(f"Preflight request kind mismatch: {reference.get('kind')!r}")
    if reference.get("authority") != TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_AUTHORITY:
        raise ValueError(f"Preflight request authority mismatch: {reference.get('authority')!r}")
    if reference.get("digest") != request_digest:
        raise ValueError("Preflight request digest does not match request artifact bytes")
    if not request_path_matches(
        str(reference.get("path") or ""),
        request_path,
        reference_root=reference_root,
    ):
        raise ValueError("Preflight request path does not reference the supplied request artifact")


def artifact_reference(
    *,
    path: Path,
    reference_root: Path,
    digest: str,
    api_version: str,
    kind: str,
    schema_version: int,
    authority: str,
) -> dict[str, Any]:
    return {
        "path": path_reference(path, reference_root=reference_root),
        "digest": digest,
        "apiVersion": api_version,
        "kind": kind,
        "schemaVersion": schema_version,
        "authority": authority,
    }


def request_path_matches(expected: str, path: Path, *, reference_root: Path) -> bool:
    return expected in path_reference_candidates(path, reference_root=reference_root)


def path_reference(path: Path, *, reference_root: Path) -> str:
    try:
        return (
            path.resolve(strict=False).relative_to(reference_root.resolve(strict=False)).as_posix()
        )
    except ValueError:
        return path.as_posix()


def path_reference_candidates(path: Path, *, reference_root: Path) -> set[str]:
    candidates = {path.as_posix(), str(path)}
    candidates.add(path_reference(path, reference_root=reference_root))
    try:
        candidates.add(path.resolve(strict=False).as_posix())
    except OSError:
        pass
    return {candidate for candidate in candidates if candidate}


def path_reference_root(*paths: Path) -> Path:
    resolved_paths = [path.resolve(strict=False) for path in paths]
    for path in resolved_paths:
        for parent in (path.parent, *path.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
    return Path(os.path.commonpath([str(path.parent) for path in resolved_paths]))


def run_id(request_ref: dict[str, Any], preflight_ref: dict[str, Any]) -> str:
    digest = canonical_sha256({"request": request_ref, "preflight": preflight_ref})
    return f"trusted-local-adapter-run-{digest[:16]}"


def digest_string(path: Path) -> str:
    return f"sha256:{sha256_file(path)}"


def non_authority_statements() -> list[str]:
    return [
        "runner_report_is_not_execution_permission",
        "preflight_pass_is_not_execution_permission",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_adapters",
        "does_not_run_adapter_processes",
        "does_not_clone_or_fetch_repositories",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_execute_harvested_code",
        "does_not_run_ai",
        "does_not_change_static_plugin_applicability_evaluation",
        "does_not_change_autonomous_batch_behavior",
        "does_not_accept_packages",
        "does_not_accept_relations",
        "does_not_seed_baselines",
        "does_not_publish_registry_metadata",
        "does_not_remove_preview_only",
        "does_not_treat_adapter_output_as_registry_truth",
        "does_not_treat_adapter_preflight_as_registry_truth",
        "does_not_treat_ai_output_as_registry_truth",
    ]


def object_value(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


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
