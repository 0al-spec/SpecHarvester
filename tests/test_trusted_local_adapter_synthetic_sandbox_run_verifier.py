from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.trusted_local_adapter_synthetic_sandbox_run_verifier import (
    SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION,
    SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY,
    SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND,
    SyntheticTrustedLocalAdapterSandboxRunVerifierOptions,
    build_synthetic_trusted_local_adapter_sandbox_run_verifier_report,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
SYNTHETIC_RUN = FIXTURES / "synthetic-trusted-local-adapter-sandbox-run.example.json"


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_passes_fixture() -> None:
    report = build_synthetic_trusted_local_adapter_sandbox_run_verifier_report(
        SyntheticTrustedLocalAdapterSandboxRunVerifierOptions(fixture=SYNTHETIC_RUN)
    )

    assert report["apiVersion"] == SYNTHETIC_SANDBOX_RUN_VERIFIER_API_VERSION
    assert report["kind"] == SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND
    assert report["schemaVersion"] == 1
    assert report["status"] == "passed"
    assert report["authority"] == SYNTHETIC_SANDBOX_RUN_VERIFIER_AUTHORITY
    assert report["fixture"]["path"] == (
        "tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json"
    )
    assert report["fixture"]["digestVerified"] is True
    assert {item["role"] for item in report["linkedArtifacts"]} == {
        "sandboxContract",
        "sandboxPreflight",
        "sandboxRunnerValidation",
    }
    assert all(item["digestVerified"] is True for item in report["linkedArtifacts"])
    assert report["operatorApproval"]["bindingVerified"] is True
    assert report["operatorApproval"]["approvedForRealAdapterExecution"] is False
    assert report["operatorApproval"]["approvalIsExecutionPermission"] is False
    assert report["operatorApproval"]["approvalIsRegistryAcceptance"] is False
    assert report["operatorApproval"]["approvalIsReusableAcrossRepositories"] is False
    assert {item["role"] for item in report["syntheticOutputCandidates"]} == {
        "trusted_local_adapter_output",
        "trusted_local_adapter_diagnostics",
        "trusted_local_adapter_audit_record",
    }
    assert all(item["byteSizeVerified"] is True for item in report["syntheticOutputCandidates"])
    assert all(item["digestVerified"] is True for item in report["syntheticOutputCandidates"])
    assert report["auditRecord"]["digestVerified"] is True
    assert report["executionBoundary"] == {
        "adapterExecution": "synthetic_fixture_only",
        "realAdapterProcessSpawned": False,
        "thirdPartyAdapterCodeLoaded": False,
        "adapterCodeImportAttempted": False,
        "executedAdapterCount": 0,
        "dependencyInstallation": "not_allowed",
        "packageManagers": "not_invoked",
        "harvestedCodeExecution": "not_allowed",
        "aiExecution": "not_run",
        "networkAccess": "none",
        "operatorApprovalIsReusable": False,
        "syntheticRunIsRealExecutionPermission": False,
        "syntheticRunVerificationIsExecutionPermission": False,
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterOutputAccepted": False,
    }
    assert report["summary"]["linkedArtifactCount"] == 3
    assert report["summary"]["syntheticOutputCandidateCount"] == 3
    assert report["summary"]["realAdapterProcessSpawned"] is False
    assert report["summary"]["thirdPartyAdapterCodeLoaded"] is False
    assert report["summary"]["executedAdapterCount"] == 0
    assert {
        "synthetic_sandbox_run_verifier_is_not_execution_permission",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_treat_synthetic_run_verification_as_execution_permission",
        "does_not_accept_packages",
        "does_not_publish_registry_metadata",
    }.issubset(set(report["nonAuthorityStatements"]))


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_is_deterministic() -> None:
    options = SyntheticTrustedLocalAdapterSandboxRunVerifierOptions(fixture=SYNTHETIC_RUN)

    assert build_synthetic_trusted_local_adapter_sandbox_run_verifier_report(options) == (
        build_synthetic_trusted_local_adapter_sandbox_run_verifier_report(options)
    )


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_cli_writes_report(
    tmp_path: Path,
    capsys,
) -> None:
    output = tmp_path / "synthetic-sandbox-run-verifier-report.json"

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(SYNTHETIC_RUN),
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert file_payload == stdout_payload
    assert file_payload["kind"] == SYNTHETIC_SANDBOX_RUN_VERIFIER_KIND
    assert file_payload["executionBoundary"]["realAdapterProcessSpawned"] is False


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_bad_identity(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["apiVersion"] = "example.invalid/v0"
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_linked_digest_mismatch(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["linkedArtifacts"]["sandboxRunnerValidation"]["digest"] = "sha256:" + ("0" * 64)
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_output_size_mismatch(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["syntheticOutputCandidates"][0]["byteSize"] = 1
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_audit_digest_mismatch(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["auditRecord"]["digest"] = "sha256:" + ("0" * 64)
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_real_execution_drift(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["executionBoundary"]["realAdapterProcessSpawned"] = True
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def test_synthetic_trusted_local_adapter_sandbox_run_verifier_rejects_unsafe_path(
    tmp_path: Path,
) -> None:
    fixture = read_json(SYNTHETIC_RUN)
    fixture["syntheticOutputCandidates"][0]["path"] = "../unsafe.json"
    bad_fixture = write_json(tmp_path / "fixture.json", fixture)

    result = main(
        [
            "synthetic-trusted-local-adapter-sandbox-run-verifier",
            "--fixture",
            str(bad_fixture),
        ]
    )

    assert result == 2


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
