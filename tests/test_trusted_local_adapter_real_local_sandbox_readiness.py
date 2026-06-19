from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.trusted_local_adapter_real_local_sandbox_readiness import (
    REAL_LOCAL_SANDBOX_READINESS_API_VERSION,
    REAL_LOCAL_SANDBOX_READINESS_AUTHORITY,
    REAL_LOCAL_SANDBOX_READINESS_KIND,
    RealLocalTrustedAdapterSandboxRunReadinessOptions,
    build_real_local_trusted_adapter_sandbox_run_readiness_report,
)
from spec_harvester.trusted_local_adapter_synthetic_sandbox_run_verifier import (
    SyntheticTrustedLocalAdapterSandboxRunVerifierOptions,
    build_synthetic_trusted_local_adapter_sandbox_run_verifier_report,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
SYNTHETIC_RUN = FIXTURES / "synthetic-trusted-local-adapter-sandbox-run.example.json"


def test_real_local_trusted_adapter_sandbox_readiness_passes_verifier_report(
    tmp_path: Path,
) -> None:
    verifier = write_verifier_report(tmp_path)

    report = build_real_local_trusted_adapter_sandbox_run_readiness_report(
        RealLocalTrustedAdapterSandboxRunReadinessOptions(verifier_report=verifier)
    )

    assert report["apiVersion"] == REAL_LOCAL_SANDBOX_READINESS_API_VERSION
    assert report["kind"] == REAL_LOCAL_SANDBOX_READINESS_KIND
    assert report["schemaVersion"] == 1
    assert report["status"] == "ready_for_explicit_real_run_review"
    assert report["authority"] == REAL_LOCAL_SANDBOX_READINESS_AUTHORITY
    assert report["verifierReport"]["status"] == "passed"
    assert report["verifierReport"]["digestVerified"] is True
    assert report["verifierReport"]["verifierIsExecutionPermission"] is False
    assert report["readinessDecision"] == {
        "status": "ready_for_explicit_real_run_review",
        "decision": "ready_for_review_not_execution",
        "readyForExplicitReview": True,
        "readyForExecution": False,
        "readinessIsExecutionPermission": False,
        "readinessIsRegistryAuthority": False,
    }
    assert report["realRunPrerequisites"]["operatorApproval"]["status"] == (
        "explicit_real_run_approval_required"
    )
    assert (
        report["realRunPrerequisites"]["operatorApproval"]["approvalProvidedByReadinessGate"]
        is False
    )
    assert report["realRunPrerequisites"]["sandboxRuntime"]["status"] == (
        "requirements_declared_not_invoked"
    )
    runtime_policy = report["realRunPrerequisites"]["sandboxRuntime"]
    assert runtime_policy["runtimeInvocationAllowedByReadinessGate"] is False
    assert (
        report["realRunPrerequisites"]["filesystemAndOutputPolicy"][
            "outputDigestVerificationRequired"
        ]
        is True
    )
    assert report["realRunPrerequisites"]["auditPolicy"]["replayableAuditRecordRequired"] is True
    assert report["readinessGate"] == {
        "mode": "review_only_no_execution_readiness_gate",
        "runtimeInvoked": False,
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
        "adapterProcessSpawned": False,
        "executedAdapterCount": 0,
        "runtimeInvoked": False,
        "realRunImplementationPresent": False,
        "readinessGateIsExecutionPermission": False,
        "syntheticRunVerificationIsExecutionPermission": False,
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterOutputAccepted": False,
    }
    assert report["summary"]["readyForExplicitReview"] is True
    assert report["summary"]["readyForExecution"] is False
    assert report["summary"]["executedAdapterCount"] == 0
    assert report["summary"]["runtimeInvoked"] is False
    assert {
        "real_local_sandbox_readiness_is_not_execution_permission",
        "does_not_load_third_party_adapter_code",
        "does_not_execute_real_adapters",
        "does_not_run_real_adapter_processes",
        "does_not_install_dependencies",
        "does_not_invoke_package_managers",
        "does_not_use_network",
        "does_not_treat_readiness_as_execution_permission",
        "does_not_publish_registry_metadata",
    }.issubset(set(report["nonAuthorityStatements"]))


def test_real_local_trusted_adapter_sandbox_readiness_is_deterministic(
    tmp_path: Path,
) -> None:
    verifier = write_verifier_report(tmp_path)
    options = RealLocalTrustedAdapterSandboxRunReadinessOptions(verifier_report=verifier)

    assert build_real_local_trusted_adapter_sandbox_run_readiness_report(options) == (
        build_real_local_trusted_adapter_sandbox_run_readiness_report(options)
    )


def test_real_local_trusted_adapter_sandbox_readiness_cli_writes_report(
    tmp_path: Path,
    capsys,
) -> None:
    verifier = write_verifier_report(tmp_path)
    output = tmp_path / "readiness.json"

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(verifier),
            "--output",
            str(output),
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(output.read_text(encoding="utf-8"))
    assert file_payload == stdout_payload
    assert file_payload["kind"] == REAL_LOCAL_SANDBOX_READINESS_KIND
    assert file_payload["readinessDecision"]["readyForExecution"] is False


def test_real_local_trusted_adapter_sandbox_readiness_rejects_bad_verifier_identity(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["apiVersion"] = "example.invalid/v0"
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_bad_verifier_status(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["status"] = "failed"
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_execution_drift(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["executionBoundary"]["realAdapterProcessSpawned"] = True
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_approval_permission_drift(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["operatorApproval"]["approvalIsExecutionPermission"] = True
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_bad_approval_binding(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    del verifier["operatorApproval"]["approvalBinding"]["adapterDigest"]
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_output_truth_drift(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["syntheticOutputCandidates"][0]["outputIsRegistryTruth"] = True
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def test_real_local_trusted_adapter_sandbox_readiness_rejects_missing_non_authority(
    tmp_path: Path,
) -> None:
    verifier = verifier_payload()
    verifier["nonAuthorityStatements"].remove("does_not_execute_real_adapters")
    bad_verifier = write_json(tmp_path / "verifier.json", verifier)

    result = main(
        [
            "real-local-trusted-adapter-sandbox-run-readiness",
            "--verifier-report",
            str(bad_verifier),
        ]
    )

    assert result == 2


def verifier_payload() -> dict:
    return build_synthetic_trusted_local_adapter_sandbox_run_verifier_report(
        SyntheticTrustedLocalAdapterSandboxRunVerifierOptions(fixture=SYNTHETIC_RUN)
    )


def write_verifier_report(tmp_path: Path) -> Path:
    return write_json(tmp_path / "verifier.json", verifier_payload())


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
