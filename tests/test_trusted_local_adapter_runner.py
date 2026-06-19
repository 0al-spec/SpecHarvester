from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.trusted_local_adapter_runner import (
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND,
    TrustedLocalAdapterRunOptions,
    build_trusted_local_adapter_run_report,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
REQUEST = FIXTURES / "trusted-local-adapter-run-request.example.json"
PREFLIGHT = FIXTURES / "trusted-local-adapter-run-preflight-report.example.json"


def test_disabled_trusted_local_adapter_runner_emits_no_execution_report() -> None:
    report = build_trusted_local_adapter_run_report(
        TrustedLocalAdapterRunOptions(request=REQUEST, preflight=PREFLIGHT)
    )

    assert report["apiVersion"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION
    assert report["kind"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND
    assert report["schemaVersion"] == 1
    assert report["status"] == "no_execution_report_emitted"
    assert report["authority"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY
    assert report["request"]["path"] == (
        "tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json"
    )
    assert report["preflight"]["path"] == (
        "tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json"
    )
    assert report["preflight"]["requestDigestVerified"] is True
    assert report["runner"] == {
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
    }
    assert report["executionBoundary"] == {
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
    }
    assert report["summary"] == {
        "acceptedCount": len(report["validation"]["acceptedChecks"]),
        "errorCount": 0,
        "warningCount": 1,
        "executedAdapterCount": 0,
        "runtimeImplementedAdapterCount": 0,
    }
    assert {
        "runner_report_is_not_execution_permission",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_adapters",
        "does_not_run_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_execute_harvested_code",
        "does_not_run_ai",
        "does_not_accept_packages",
        "does_not_accept_relations",
        "does_not_publish_registry_metadata",
    }.issubset(set(report["nonAuthorityStatements"]))


def test_disabled_trusted_local_adapter_runner_is_deterministic() -> None:
    options = TrustedLocalAdapterRunOptions(request=REQUEST, preflight=PREFLIGHT)

    assert build_trusted_local_adapter_run_report(options) == (
        build_trusted_local_adapter_run_report(options)
    )


def test_disabled_trusted_local_adapter_runner_paths_do_not_depend_on_cwd(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    report = build_trusted_local_adapter_run_report(
        TrustedLocalAdapterRunOptions(request=REQUEST, preflight=PREFLIGHT)
    )

    assert report["request"]["path"] == (
        "tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json"
    )
    assert report["preflight"]["path"] == (
        "tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json"
    )
    assert report["preflight"]["requestDigestVerified"] is True


def test_trusted_local_adapter_runner_cli_writes_report(tmp_path: Path, capsys) -> None:
    output = tmp_path / "trusted-local-adapter-run-report.json"

    result = main(
        [
            "trusted-local-adapter-runner-skeleton",
            "--request",
            str(REQUEST),
            "--preflight",
            str(PREFLIGHT),
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert file_payload == stdout_payload
    assert file_payload["kind"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND
    assert file_payload["runner"]["adapterProcessSpawned"] is False


def test_trusted_local_adapter_runner_rejects_bad_request_identity(
    tmp_path: Path,
) -> None:
    request = read_json(REQUEST)
    request["apiVersion"] = "example.invalid/v0"
    bad_request = tmp_path / "request.json"
    write_json(bad_request, request)

    result = main(
        [
            "trusted-local-adapter-runner-skeleton",
            "--request",
            str(bad_request),
            "--preflight",
            str(PREFLIGHT),
        ]
    )

    assert result == 2


def test_trusted_local_adapter_runner_rejects_bad_preflight_identity(
    tmp_path: Path,
) -> None:
    preflight = read_json(PREFLIGHT)
    preflight["kind"] = "ExampleInvalidPreflight"
    bad_preflight = tmp_path / "preflight.json"
    write_json(bad_preflight, preflight)

    result = main(
        [
            "trusted-local-adapter-runner-skeleton",
            "--request",
            str(REQUEST),
            "--preflight",
            str(bad_preflight),
        ]
    )

    assert result == 2


def test_trusted_local_adapter_runner_rejects_request_digest_mismatch(
    tmp_path: Path,
) -> None:
    preflight = read_json(PREFLIGHT)
    preflight["request"]["digest"] = "sha256:" + ("0" * 64)
    bad_preflight = tmp_path / "preflight.json"
    write_json(bad_preflight, preflight)

    result = main(
        [
            "trusted-local-adapter-runner-skeleton",
            "--request",
            str(REQUEST),
            "--preflight",
            str(bad_preflight),
        ]
    )

    assert result == 2


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
