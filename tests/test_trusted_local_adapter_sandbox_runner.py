from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.trusted_local_adapter_sandbox_runner import (
    TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_API_VERSION,
    TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_AUTHORITY,
    TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_KIND,
    TrustedLocalAdapterSandboxRunnerValidationOptions,
    build_trusted_local_adapter_sandbox_runner_validation_report,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
CONTRACT = FIXTURES / "trusted-local-adapter-sandbox-contract.example.json"
PREFLIGHT = FIXTURES / "trusted-local-adapter-sandbox-preflight-report.example.json"


def test_disabled_trusted_local_adapter_sandbox_runner_emits_validation_report() -> None:
    report = build_trusted_local_adapter_sandbox_runner_validation_report(
        TrustedLocalAdapterSandboxRunnerValidationOptions(
            contract=CONTRACT,
            preflight=PREFLIGHT,
        )
    )

    assert report["apiVersion"] == TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_API_VERSION
    assert report["kind"] == TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_KIND
    assert report["schemaVersion"] == 1
    assert report["status"] == "no_execution_validation_report_emitted"
    assert report["authority"] == TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_AUTHORITY
    assert report["sandboxContract"]["path"] == (
        "tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json"
    )
    assert report["sandboxPreflight"]["path"] == (
        "tests/fixtures/repository_plugins/"
        "trusted-local-adapter-sandbox-preflight-report.example.json"
    )
    assert report["sandboxPreflight"]["contractDigestVerified"] is True
    assert report["runner"] == {
        "mode": "disabled_no_execution_sandbox_runner_validation",
        "enabled": False,
        "runtimeImplemented": False,
        "sandboxRunnerImplemented": False,
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
        "registryAuthority": False,
    }
    assert report["executionBoundary"] == {
        "adapterExecution": "not_run",
        "adapterCodeLoaded": False,
        "adapterProcessSpawned": False,
        "executedAdapterCount": 0,
        "runtimeImplemented": False,
        "sandboxRunnerImplemented": False,
        "sandboxContractIsExecutionPermission": False,
        "sandboxPreflightIsExecutionPermission": False,
        "runnerValidationIsExecutionPermission": False,
        "operatorApprovalProvided": False,
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
        "sandbox_runner_validation_is_not_execution_permission",
        "sandbox_contract_is_not_execution_permission",
        "sandbox_preflight_is_not_execution_permission",
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
        "does_not_remove_preview_only",
    }.issubset(set(report["nonAuthorityStatements"]))


def test_disabled_trusted_local_adapter_sandbox_runner_is_deterministic() -> None:
    options = TrustedLocalAdapterSandboxRunnerValidationOptions(
        contract=CONTRACT,
        preflight=PREFLIGHT,
    )

    assert build_trusted_local_adapter_sandbox_runner_validation_report(options) == (
        build_trusted_local_adapter_sandbox_runner_validation_report(options)
    )


def test_trusted_local_adapter_sandbox_runner_cli_writes_report(tmp_path: Path, capsys) -> None:
    output = tmp_path / "trusted-local-adapter-sandbox-runner-validation-report.json"

    result = main(
        [
            "trusted-local-adapter-sandbox-runner-validation",
            "--contract",
            str(CONTRACT),
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
    assert file_payload["kind"] == TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION_KIND
    assert file_payload["runner"]["adapterProcessSpawned"] is False


def test_trusted_local_adapter_sandbox_runner_rejects_bad_contract_identity(
    tmp_path: Path,
) -> None:
    contract = read_json(CONTRACT)
    contract["apiVersion"] = "example.invalid/v0"
    bad_contract = tmp_path / "contract.json"
    write_json(bad_contract, contract)

    result = main(
        [
            "trusted-local-adapter-sandbox-runner-validation",
            "--contract",
            str(bad_contract),
            "--preflight",
            str(PREFLIGHT),
        ]
    )

    assert result == 2


def test_trusted_local_adapter_sandbox_runner_rejects_bad_preflight_identity(
    tmp_path: Path,
) -> None:
    preflight = read_json(PREFLIGHT)
    preflight["kind"] = "ExampleInvalidPreflight"
    bad_preflight = tmp_path / "preflight.json"
    write_json(bad_preflight, preflight)

    result = main(
        [
            "trusted-local-adapter-sandbox-runner-validation",
            "--contract",
            str(CONTRACT),
            "--preflight",
            str(bad_preflight),
        ]
    )

    assert result == 2


def test_trusted_local_adapter_sandbox_runner_rejects_contract_digest_mismatch(
    tmp_path: Path,
) -> None:
    preflight = read_json(PREFLIGHT)
    preflight["sandboxContract"]["digest"] = "sha256:" + ("0" * 64)
    bad_preflight = tmp_path / "preflight.json"
    write_json(bad_preflight, preflight)

    result = main(
        [
            "trusted-local-adapter-sandbox-runner-validation",
            "--contract",
            str(CONTRACT),
            "--preflight",
            str(bad_preflight),
        ]
    )

    assert result == 2


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
