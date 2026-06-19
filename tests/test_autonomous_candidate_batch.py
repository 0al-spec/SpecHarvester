from __future__ import annotations

import hashlib
import json
from pathlib import Path

from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_API_VERSION,
    AUTONOMOUS_CANDIDATE_BATCH_KIND,
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    REPOSITORY_PLUGIN_ADAPTER_EVIDENCE_DIRNAME,
    REPOSITORY_PLUGIN_ADAPTER_MANIFEST_API_VERSION,
    REPOSITORY_PLUGIN_ADAPTER_MANIFEST_AUTHORITY,
    REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FILENAME,
    REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND,
    REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_API_VERSION,
    REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY,
    REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_FILENAME,
    REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_KIND,
    REPOSITORY_PLUGIN_APPLICABILITY_API_VERSION,
    REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
    REPOSITORY_PLUGIN_APPLICABILITY_FILENAME,
    REPOSITORY_PLUGIN_APPLICABILITY_KIND,
    REPOSITORY_PROFILE_DETECTION_FILENAME,
    TRUSTED_LOCAL_ADAPTER_RUN_EVIDENCE_DIRNAME,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_FILENAME,
    AutonomousCandidateBatch,
    AutonomousCandidateBatchOptions,
    ai_proposal_record,
    run_autonomous_candidate_batch,
)
from spec_harvester.cli import main
from spec_harvester.trusted_local_adapter_runner import (
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY,
    TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND,
    TrustedLocalAdapterRunOptions,
    build_trusted_local_adapter_run_report,
)

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_PLUGIN_FIXTURES = ROOT / "tests" / "fixtures" / "repository_plugins"
GENERIC_REPOSITORY_PLUGIN_REGISTRY = REPOSITORY_PLUGIN_FIXTURES / "generic-registry.example.json"
STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE = (
    REPOSITORY_PLUGIN_FIXTURES / "static-evidence-envelope.example.json"
)
REPOSITORY_PLUGIN_ADAPTER_MANIFEST = REPOSITORY_PLUGIN_FIXTURES / "adapter-manifest.example.json"
REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT = (
    REPOSITORY_PLUGIN_FIXTURES / "adapter-preflight-report.example.json"
)
TRUSTED_LOCAL_ADAPTER_RUN_REQUEST = (
    REPOSITORY_PLUGIN_FIXTURES / "trusted-local-adapter-run-request.example.json"
)
TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT = (
    REPOSITORY_PLUGIN_FIXTURES / "trusted-local-adapter-run-preflight-report.example.json"
)


def test_autonomous_candidate_batch_runs_offline_preview_pipeline(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
        )
    )

    assert report["apiVersion"] == AUTONOMOUS_CANDIDATE_BATCH_API_VERSION
    assert report["kind"] == AUTONOMOUS_CANDIDATE_BATCH_KIND
    assert report["status"] == "passed"
    assert report["ai"]["mode"] == "disabled"
    assert report["repositoryProfileSelection"]["mode"] == "none"
    assert report["repositoryProfileSelection"]["authority"] == "producer_profile_selection_only"
    assert report["repositoryProfileSelection"]["advisoryHintsAppliedToDrafting"] is False
    assert report["repositoryPluginApplicability"] == {
        "status": "not_provided",
        "reason": "operator_not_provided",
        "appliedToDrafting": False,
        "registryAuthority": False,
    }
    assert report["repositoryPluginAdapterEvidence"] == {
        "status": "not_provided",
        "reason": "operator_not_provided",
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterExecution": "not_run",
    }
    assert report["trustedLocalAdapterRunEvidence"] == {
        "status": "not_provided",
        "reason": "operator_not_provided",
        "appliedToDrafting": False,
        "registryAuthority": False,
        "adapterExecution": "not_run",
    }
    assert report["summary"]["processedCount"] == 1
    assert report["summary"]["passedPreflightCount"] == 1
    assert report["summary"]["repositoryPluginApplicabilitySidecarCount"] == 0
    assert report["summary"]["repositoryPluginAdapterEvidenceSidecarCount"] == 0
    assert report["summary"]["trustedLocalAdapterRunEvidenceSidecarCount"] == 0
    assert report["summary"]["repositoryProfileDetectionCount"] == 1
    assert report["summary"]["repositoryProfileDisabledCount"] == 1
    assert report["summary"]["repositoryProfileSelectedCount"] == 0
    repository = report["repositories"][0]
    assert repository["status"] == "passed"
    assert repository["repositoryProfileDetection"]["status"] == "completed"
    assert repository["repositoryProfileDetection"]["decision"] == "disabled"
    assert repository["repositoryProfileDetection"]["selectedProfileId"] is None
    assert repository["repositoryProfileDetection"]["path"].endswith(
        REPOSITORY_PROFILE_DETECTION_FILENAME
    )
    assert repository["packageSetDraft"]["candidateCount"] == 3
    assert repository["packageSetDraft"]["relationCount"] == 2
    assert repository["preflight"]["status"] == "passed"
    assert repository["aiDraft"]["status"] == "skipped"
    assert repository["aiEnrichment"]["status"] == "skipped"
    assert repository["aiEnrichedPreview"]["status"] == "skipped"
    assert repository["authorReadyDraftSummary"]["decision"] == "stop_for_author_review"
    assert report["summary"]["aiEnrichedPreviewAppliedCount"] == 0
    assert report["summary"]["aiEnrichedPreviewSkippedCount"] == 0
    assert report["summary"]["aiEnrichedPreviewFailedCount"] == 0

    saved = json.loads(
        (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).read_text(encoding="utf-8")
    )
    assert saved["status"] == "passed"
    assert (output / "collected" / "demo" / "workspace-inventory.json").is_file()
    assert (output / "package-sets" / "demo" / "package-set-draft.json").is_file()
    assert (output / "package-sets" / "demo" / "bundle-set-preflight.json").is_file()
    detection = json.loads(
        Path(repository["repositoryProfileDetection"]["path"]).read_text(encoding="utf-8")
    )
    assert detection["selection"]["decision"] == "disabled"
    assert detection["selection"]["mode"] == "none"
    assert detection["authority"] == "producer_profile_selection_only"


def test_autonomous_candidate_batch_records_auto_repository_profile_selection(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="auto",
        )
    )

    repository = report["repositories"][0]
    detection = repository["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert report["repositoryProfileSelection"]["mode"] == "auto"
    assert report["summary"]["repositoryProfileDetectionCount"] == 1
    assert report["summary"]["repositoryProfileSelectedCount"] == 1
    assert report["summary"]["repositoryProfileDisabledCount"] == 0
    assert detection["decision"] == "selected"
    assert detection["selectedProfileId"] == "generic.package_set.v0"
    assert detection["confidence"] == "high"
    assert detection["advisoryHintCount"] >= 3
    assert repository["packageSetDraft"]["candidateCount"] == 3
    assert repository["packageSetDraft"]["relationCount"] == 2

    payload = json.loads(Path(detection["path"]).read_text(encoding="utf-8"))
    assert payload["kind"] == "SpecHarvesterRepositoryProfileDetection"
    assert payload["selection"]["selectedProfileId"] == "generic.package_set.v0"
    assert "does_not_treat_plugin_decisions_as_registry_truth" in payload["nonAuthorityStatements"]
    assert {"hint": "package_set_root", "path": "."} in [
        {"hint": item["hint"], "path": item["path"]} for item in payload["advisoryDownstreamHints"]
    ]


def test_autonomous_candidate_batch_records_repository_plugin_applicability_sidecar(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    applicability = write_repository_plugin_applicability_report(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_plugin_applicability=applicability,
        )
    )

    sidecar = report["repositoryPluginApplicability"]
    sidecar_path = Path(sidecar["path"])

    assert report["status"] == "passed"
    assert report["summary"]["repositoryPluginApplicabilitySidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["source"] == str(applicability)
    assert sidecar["sourceMode"] == "explicit_sidecar"
    assert sidecar_path == (
        output
        / "reports"
        / "repository-plugin-applicability"
        / REPOSITORY_PLUGIN_APPLICABILITY_FILENAME
    )
    assert sidecar_path.is_file()
    assert sidecar["digest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(sidecar_path.read_bytes()).hexdigest(),
    }
    assert sidecar["apiVersion"] == REPOSITORY_PLUGIN_APPLICABILITY_API_VERSION
    assert sidecar["kind"] == REPOSITORY_PLUGIN_APPLICABILITY_KIND
    assert sidecar["schemaVersion"] == 1
    assert sidecar["authority"] == REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY
    assert sidecar["summary"] == {
        "selectedCount": 1,
        "rejectedCount": 1,
        "fallbackCount": 1,
        "blockedCount": 2,
        "diagnosticCount": 5,
    }
    assert sidecar["diagnosticCodes"] == [
        "plugin_blocked_required_evidence_missing",
        "plugin_fallback",
        "plugin_rejected_low_confidence",
        "plugin_selected",
    ]
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False
    assert "plugin_execution" in sidecar["nonGoals"]
    assert "registry_publication" in sidecar["nonGoals"]
    assert report["repositories"][0]["packageSetDraft"]["candidateCount"] == 3
    assert report["repositories"][0]["repositoryProfileDetection"]["decision"] == "disabled"

    copied = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert copied["kind"] == REPOSITORY_PLUGIN_APPLICABILITY_KIND
    assert copied["summary"]["selectedCount"] == 1


def test_autonomous_candidate_batch_records_repository_plugin_adapter_evidence_sidecar(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_plugin_adapter_manifest=REPOSITORY_PLUGIN_ADAPTER_MANIFEST,
            repository_plugin_adapter_preflight=REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT,
        )
    )

    sidecar = report["repositoryPluginAdapterEvidence"]
    manifest_path = Path(sidecar["manifest"]["path"])
    preflight_path = Path(sidecar["preflight"]["path"])

    assert report["status"] == "passed"
    assert report["summary"]["repositoryPluginAdapterEvidenceSidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["sourceMode"] == "explicit_sidecar"
    assert sidecar["authority"] == REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY
    assert manifest_path == (
        output
        / "reports"
        / REPOSITORY_PLUGIN_ADAPTER_EVIDENCE_DIRNAME
        / REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FILENAME
    )
    assert preflight_path == (
        output
        / "reports"
        / REPOSITORY_PLUGIN_ADAPTER_EVIDENCE_DIRNAME
        / REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_FILENAME
    )
    assert manifest_path.is_file()
    assert preflight_path.is_file()
    assert sidecar["manifest"]["source"] == str(REPOSITORY_PLUGIN_ADAPTER_MANIFEST)
    assert sidecar["manifest"]["sourceDigest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(REPOSITORY_PLUGIN_ADAPTER_MANIFEST.read_bytes()).hexdigest(),
    }
    assert sidecar["manifest"]["digest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    }
    assert sidecar["manifest"]["apiVersion"] == REPOSITORY_PLUGIN_ADAPTER_MANIFEST_API_VERSION
    assert sidecar["manifest"]["kind"] == REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND
    assert sidecar["manifest"]["schemaVersion"] == 1
    assert sidecar["manifest"]["authority"] == REPOSITORY_PLUGIN_ADAPTER_MANIFEST_AUTHORITY
    assert sidecar["manifest"]["adapterCount"] == 3
    assert sidecar["preflight"]["source"] == str(REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT)
    assert sidecar["preflight"]["sourceDigest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT.read_bytes()).hexdigest(),
    }
    assert sidecar["preflight"]["digest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(preflight_path.read_bytes()).hexdigest(),
    }
    assert sidecar["preflight"]["apiVersion"] == REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_API_VERSION
    assert sidecar["preflight"]["kind"] == REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_KIND
    assert sidecar["preflight"]["schemaVersion"] == 1
    assert sidecar["preflight"]["authority"] == REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_AUTHORITY
    assert sidecar["preflight"]["allowedCount"] == 3
    assert sidecar["preflight"]["rejectedCount"] == 1
    assert sidecar["preflight"]["fallbackCount"] == 1
    assert sidecar["preflight"]["blockedCount"] == 1
    assert sidecar["preflight"]["diagnosticCount"] == 2
    assert sidecar["preflight"]["executedAdapterCount"] == 0
    assert sidecar["summary"] == {
        "adapterCount": 3,
        "allowedCount": 3,
        "rejectedCount": 1,
        "fallbackCount": 1,
        "blockedCount": 1,
        "diagnosticCount": 2,
        "executedAdapterCount": 0,
    }
    assert sidecar["diagnosticCodes"] == [
        "adapter_manifest_preflight_fixture",
        "decision_categories_recorded",
    ]
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False
    assert sidecar["adapterExecution"] == "not_run"
    assert sidecar["adapterOutputAccepted"] is False
    assert "adapter_execution" in sidecar["nonGoals"]
    assert "registry_publication" in sidecar["nonGoals"]

    copied_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    copied_preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
    assert copied_manifest["kind"] == REPOSITORY_PLUGIN_ADAPTER_MANIFEST_KIND
    assert copied_preflight["kind"] == REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_KIND
    assert copied_preflight["summary"]["executedAdapterCount"] == 0
    assert report["repositories"][0]["packageSetDraft"]["candidateCount"] == 3


def test_autonomous_candidate_batch_records_trusted_local_adapter_run_evidence_sidecar(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    run_report = write_trusted_local_adapter_run_report_fixture(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            trusted_local_adapter_run_report=run_report,
        )
    )

    sidecar = report["trustedLocalAdapterRunEvidence"]
    sidecar_path = Path(sidecar["path"])

    assert report["status"] == "passed"
    assert report["summary"]["trustedLocalAdapterRunEvidenceSidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["source"] == str(run_report)
    assert sidecar["sourceMode"] == "explicit_sidecar"
    assert sidecar["sourceDigest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(run_report.read_bytes()).hexdigest(),
    }
    assert sidecar_path == (
        output
        / "reports"
        / TRUSTED_LOCAL_ADAPTER_RUN_EVIDENCE_DIRNAME
        / TRUSTED_LOCAL_ADAPTER_RUN_REPORT_FILENAME
    )
    assert sidecar_path.is_file()
    assert sidecar["digest"] == {
        "algorithm": "sha256",
        "value": hashlib.sha256(sidecar_path.read_bytes()).hexdigest(),
    }
    assert sidecar["apiVersion"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_API_VERSION
    assert sidecar["kind"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND
    assert sidecar["schemaVersion"] == 1
    assert sidecar["authority"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_AUTHORITY
    assert sidecar["runStatus"] == "no_execution_report_emitted"
    assert sidecar["runner"]["mode"] == "disabled_no_execution_skeleton"
    assert sidecar["runner"]["enabled"] is False
    assert sidecar["runner"]["runtimeImplemented"] is False
    assert sidecar["runner"]["adapterExecution"] == "not_run"
    assert sidecar["runner"]["adapterCodeLoaded"] is False
    assert sidecar["runner"]["adapterProcessSpawned"] is False
    assert sidecar["runner"]["executedAdapterCount"] == 0
    assert sidecar["runner"]["dependencyInstallation"] == "not_allowed"
    assert sidecar["runner"]["packageManagers"] == "not_invoked"
    assert sidecar["runner"]["harvestedCodeExecution"] == "not_allowed"
    assert sidecar["runner"]["aiExecution"] == "not_run"
    assert sidecar["runner"]["networkAccess"] == "none"
    assert sidecar["executionBoundary"]["appliedToDrafting"] is False
    assert sidecar["executionBoundary"]["registryAuthority"] is False
    assert sidecar["executionBoundary"]["runnerReportIsExecutionPermission"] is False
    assert sidecar["executionBoundary"]["adapterOutputAccepted"] is False
    assert sidecar["summary"]["executedAdapterCount"] == 0
    assert sidecar["summary"]["runtimeImplementedAdapterCount"] == 0
    assert sidecar["validation"]["status"] == "passed"
    assert sidecar["validation"]["errorCount"] == 0
    assert sidecar["diagnosticCodes"] == [
        "runner_skeleton_is_not_execution_permission",
        "trusted_local_adapter_runner_skeleton",
    ]
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False
    assert sidecar["adapterExecution"] == "not_run"
    assert sidecar["adapterCodeLoaded"] is False
    assert sidecar["adapterProcessSpawned"] is False
    assert sidecar["executedAdapterCount"] == 0
    assert sidecar["adapterOutputAccepted"] is False
    assert "runner_report_is_not_execution_permission" in sidecar["nonAuthorityStatements"]
    assert "does_not_change_autonomous_batch_behavior" in sidecar["nonAuthorityStatements"]
    assert "adapter_execution" in sidecar["nonGoals"]
    assert "registry_publication" in sidecar["nonGoals"]

    copied = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert copied["kind"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND
    assert copied["executionBoundary"]["registryAuthority"] is False
    assert report["repositoryPluginApplicability"]["status"] == "not_provided"
    assert report["repositoryPluginAdapterEvidence"]["status"] == "not_provided"
    assert report["repositories"][0]["packageSetDraft"]["candidateCount"] == 3


def test_autonomous_candidate_batch_auto_generates_repository_plugin_applicability(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_plugin_registry=GENERIC_REPOSITORY_PLUGIN_REGISTRY,
            repository_plugin_static_evidence_envelope=(STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE),
        )
    )

    sidecar = report["repositoryPluginApplicability"]
    sidecar_path = Path(sidecar["path"])

    assert report["status"] == "passed"
    assert report["summary"]["repositoryPluginApplicabilitySidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["source"] == "auto_static_evaluator"
    assert sidecar["sourceMode"] == "auto_static_evaluator"
    assert sidecar["inputs"] == {
        "registry": str(GENERIC_REPOSITORY_PLUGIN_REGISTRY),
        "staticEvidenceEnvelope": str(STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE),
    }
    assert sidecar["summary"] == {
        "selectedCount": 3,
        "rejectedCount": 0,
        "fallbackCount": 0,
        "blockedCount": 2,
        "diagnosticCount": 5,
    }
    assert sidecar["diagnosticCodes"] == [
        "plugin_blocked_required_evidence_missing",
        "plugin_selected",
    ]
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False
    assert sidecar_path.is_file()

    generated = json.loads(sidecar_path.read_text(encoding="utf-8"))
    assert generated["kind"] == REPOSITORY_PLUGIN_APPLICABILITY_KIND
    assert generated["summary"]["selectedCount"] == 3
    assert generated["sidecarBoundary"] == {
        "appliedToDrafting": False,
        "registryAuthority": False,
        "evaluatorExecution": "deterministic_static_metadata_only",
    }


def test_autonomous_candidate_batch_prefers_explicit_repository_plugin_applicability(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    applicability = write_repository_plugin_applicability_report(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_plugin_applicability=applicability,
            repository_plugin_registry=GENERIC_REPOSITORY_PLUGIN_REGISTRY,
            repository_plugin_static_evidence_envelope=(STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE),
        )
    )

    sidecar = report["repositoryPluginApplicability"]

    assert report["status"] == "passed"
    assert sidecar["source"] == str(applicability)
    assert sidecar["sourceMode"] == "explicit_sidecar"
    assert "inputs" not in sidecar
    assert sidecar["summary"] == {
        "selectedCount": 1,
        "rejectedCount": 1,
        "fallbackCount": 1,
        "blockedCount": 2,
        "diagnosticCount": 5,
    }


def test_autonomous_candidate_batch_rejects_partial_auto_repository_plugin_inputs(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_registry=GENERIC_REPOSITORY_PLUGIN_REGISTRY,
            )
        )
    except ValueError as exc:
        assert "--repository-plugin-registry" in str(exc)
        assert "--repository-plugin-static-evidence-envelope" in str(exc)
    else:
        raise AssertionError("expected partial repository plugin auto inputs to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_partial_repository_plugin_adapter_inputs(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_adapter_manifest=REPOSITORY_PLUGIN_ADAPTER_MANIFEST,
            )
        )
    except ValueError as exc:
        assert "--repository-plugin-adapter-manifest" in str(exc)
        assert "--repository-plugin-adapter-preflight" in str(exc)
    else:
        raise AssertionError("expected partial repository plugin adapter inputs to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_invalid_auto_repository_plugin_inputs(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    invalid_evidence = tmp_path / "static-evidence-envelope.json"
    payload = json.loads(STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE.read_text(encoding="utf-8"))
    payload["evidence"][0]["path"] = "../unsafe.json"
    invalid_evidence.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_registry=GENERIC_REPOSITORY_PLUGIN_REGISTRY,
                repository_plugin_static_evidence_envelope=invalid_evidence,
            )
        )
    except ValueError as exc:
        assert "unsafe static evidence path" in str(exc)
    else:
        raise AssertionError("expected invalid static evidence envelope to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_invalid_repository_plugin_applicability(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    applicability = write_repository_plugin_applicability_report(tmp_path)
    payload = json.loads(applicability.read_text(encoding="utf-8"))
    payload["kind"] = "WrongKind"
    applicability.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_applicability=applicability,
            )
        )
    except ValueError as exc:
        assert "unsupported kind" in str(exc)
    else:
        raise AssertionError("expected invalid repository plugin applicability report to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_mismatched_repository_plugin_adapter_preflight(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    invalid_preflight = tmp_path / "adapter-preflight-report.json"
    payload = json.loads(REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT.read_text(encoding="utf-8"))
    payload["manifest"]["digest"] = "sha256:0" * 32
    invalid_preflight.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_adapter_manifest=REPOSITORY_PLUGIN_ADAPTER_MANIFEST,
                repository_plugin_adapter_preflight=invalid_preflight,
            )
        )
    except ValueError as exc:
        assert "manifest.digest does not match manifest" in str(exc)
    else:
        raise AssertionError("expected mismatched repository plugin adapter preflight to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_authority_bearing_trusted_run_report(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    run_report = write_trusted_local_adapter_run_report_fixture(tmp_path)
    payload = json.loads(run_report.read_text(encoding="utf-8"))
    payload["authority"] = "registry_authority"
    run_report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                trusted_local_adapter_run_report=run_report,
            )
        )
    except ValueError as exc:
        assert "trusted local adapter run report" in str(exc)
        assert "unsupported authority" in str(exc)
    else:
        raise AssertionError("expected authority-bearing trusted run report to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_executing_trusted_run_report_boundary(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    run_report = write_trusted_local_adapter_run_report_fixture(tmp_path)
    payload = json.loads(run_report.read_text(encoding="utf-8"))
    payload["executionBoundary"]["adapterExecution"] = "run"
    run_report.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                trusted_local_adapter_run_report=run_report,
            )
        )
    except ValueError as exc:
        assert "executionBoundary.adapterExecution" in str(exc)
    else:
        raise AssertionError("expected executing trusted run report boundary to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_rejects_boolean_repository_plugin_applicability_counts(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    applicability = write_repository_plugin_applicability_report(tmp_path)
    payload = json.loads(applicability.read_text(encoding="utf-8"))
    payload["summary"]["selectedCount"] = True
    applicability.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                skip_ai=True,
                repository_plugin_applicability=applicability,
            )
        )
    except ValueError as exc:
        assert "integer summary.selectedCount" in str(exc)
    else:
        raise AssertionError("expected boolean repository plugin applicability count to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_uses_harvested_manifest_evidence_when_inventory_empty(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="auto",
        )
    )

    repository = report["repositories"][0]
    detection = repository["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert report["summary"]["repositoryProfileSelectedCount"] == 1
    assert detection["decision"] == "selected"
    assert detection["selectedProfileId"] == "generic.single_package.v0"
    assert detection["confidence"] == "high"
    assert detection["reasonCodes"] == ["root_manifest_present"]

    inventory = json.loads(
        (output / "collected" / "gin" / "workspace-inventory.json").read_text(encoding="utf-8")
    )
    assert inventory["summary"]["packageManifestCount"] == 0

    harvest = json.loads(
        (output / "collected" / "gin" / "harvest.json").read_text(encoding="utf-8")
    )
    assert harvest["summary"]["packageManifestCount"] == 1
    assert [
        item["path"] for item in harvest["files"] if item.get("kind") == "package_manifest"
    ] == ["go.mod"]

    payload = json.loads(Path(detection["path"]).read_text(encoding="utf-8"))
    candidates = {candidate["profileId"]: candidate for candidate in payload["candidateProfiles"]}
    assert candidates["generic.single_package.v0"]["evidencePaths"] == ["go.mod"]
    assert payload["diagnostics"][0]["evidencePaths"] == ["go.mod"]
    assert "does_not_treat_plugin_decisions_as_registry_truth" in payload["nonAuthorityStatements"]


def test_autonomous_candidate_batch_normalizes_harvested_manifest_evidence_for_source_target(
    tmp_path: Path,
) -> None:
    inputs = write_scoped_go_target_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="auto",
        )
    )

    repository = report["repositories"][0]
    detection = repository["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert detection["decision"] == "selected"
    assert detection["selectedProfileId"] == "generic.single_package.v0"
    assert detection["confidence"] == "high"
    assert detection["reasonCodes"] == ["root_manifest_present"]

    inventory = json.loads(
        (output / "collected" / "gin-scoped" / "workspace-inventory.json").read_text(
            encoding="utf-8"
        )
    )
    assert inventory["summary"]["packageManifestCount"] == 0

    harvest = json.loads(
        (output / "collected" / "gin-scoped" / "harvest.json").read_text(encoding="utf-8")
    )
    assert [
        item["path"] for item in harvest["files"] if item.get("kind") == "package_manifest"
    ] == ["packages/gin/go.mod"]

    payload = json.loads(Path(detection["path"]).read_text(encoding="utf-8"))
    candidates = {candidate["profileId"]: candidate for candidate in payload["candidateProfiles"]}
    assert candidates["generic.single_package.v0"]["evidencePaths"] == ["go.mod"]
    assert payload["diagnostics"][0]["evidencePaths"] == ["go.mod"]


def test_autonomous_candidate_batch_normalizes_repository_profile_selection(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection=" auto ",
        )
    )

    detection = report["repositories"][0]["repositoryProfileDetection"]

    assert report["repositoryProfileSelection"]["mode"] == "auto"
    assert detection["mode"] == "auto"


def test_autonomous_candidate_batch_records_explicit_repository_profile_override(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
            repository_profile_selection="custom.repository_profile.v0",
        )
    )

    detection = report["repositories"][0]["repositoryProfileDetection"]

    assert report["status"] == "passed"
    assert detection["decision"] == "selected"
    assert detection["overrideSource"] == "cli"
    assert detection["selectedProfileId"] == "custom.repository_profile.v0"
    assert detection["reasonCodes"] == ["explicit_cli_profile_override"]
    assert report["repositories"][0]["packageSetDraft"]["candidateCount"] == 1


def test_autonomous_candidate_batch_uses_single_package_fallback(
    tmp_path: Path,
) -> None:
    inputs = write_single_package_source_manifest(tmp_path)
    output = tmp_path / "output"

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            skip_ai=True,
        )
    )

    assert report["status"] == "passed"
    assert report["summary"]["processedCount"] == 1
    assert report["summary"]["passedPreflightCount"] == 1
    repository = report["repositories"][0]
    assert repository["id"] == "gin"
    assert repository["packageId"] == "gin.core"
    assert repository["status"] == "passed"
    assert repository["packageSetDraft"]["candidateCount"] == 1
    assert repository["packageSetDraft"]["relationCount"] == 0
    assert repository["preflight"]["status"] == "passed"
    assert repository["preflight"]["candidateCount"] == 1
    assert repository["preflight"]["relationCount"] == 0
    assert repository["aiDraft"]["status"] == "skipped"
    assert repository["aiEnrichment"]["status"] == "skipped"
    assert repository["aiEnrichedPreview"]["status"] == "skipped"
    assert repository["authorReadyDraftSummary"]["memberCounts"]["total"] == 1

    bundle_set = output / "package-sets" / "gin"
    summary = json.loads((bundle_set / "package-set-draft.json").read_text(encoding="utf-8"))
    assert summary["candidates"][0]["packageId"] == "gin.core"
    assert summary["candidates"][0]["selectionReason"] == (
        "single_package_source_manifest_fallback"
    )
    assert summary["relationProposals"]["relationCount"] == 0
    relation_payload = json.loads(
        (bundle_set / "package-relation-proposals.json").read_text(encoding="utf-8")
    )
    assert relation_payload["relations"] == []
    assert "id: gin.core" in (bundle_set / "gin.core" / "specpm.yaml").read_text(encoding="utf-8")
    assert "preview_only: true" in (bundle_set / "gin.core" / "specpm.yaml").read_text(
        encoding="utf-8"
    )
    assert (bundle_set / "gin.core" / "producer-receipt.json").is_file()
    assert (bundle_set / "gin.core" / "validation-report.json").is_file()
    assert (bundle_set / "gin.core" / "diagnostics.json").is_file()
    assert (bundle_set / "gin.core" / "author-ready-draft-quality-report.json").is_file()


def test_autonomous_candidate_batch_requires_model_without_skip_ai(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=tmp_path / "output",
            )
        )
    except ValueError as exc:
        assert "--lm-studio-model" in str(exc)
    else:
        raise AssertionError("expected missing LM Studio model to fail")


def test_autonomous_candidate_batch_rejects_lm_studio_credentials_before_report(
    tmp_path: Path,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    try:
        run_autonomous_candidate_batch(
            AutonomousCandidateBatchOptions(
                inputs=inputs,
                out=output,
                lm_studio_base_url="http://token@127.0.0.1:1234",
                lm_studio_model="openai/gpt-oss-20b",
            )
        )
    except ValueError as exc:
        assert "must not include credentials" in str(exc)
    else:
        raise AssertionError("expected LM Studio URL with credentials to fail")

    assert not (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).exists()


def test_autonomous_candidate_batch_records_normalized_lm_studio_base_url(
    tmp_path: Path,
) -> None:
    batch = AutonomousCandidateBatch(
        AutonomousCandidateBatchOptions(
            inputs=tmp_path / "inputs.yml",
            out=tmp_path / "output",
            lm_studio_base_url="http://localhost:1234/v1",
            lm_studio_model="openai/gpt-oss-20b",
        )
    )

    assert batch.ai_mode_record()["baseUrl"] == "http://localhost:1234"
    assert batch.ai_mode_record()["jsonRepairMaxAttempts"] == 1


def test_autonomous_candidate_batch_ai_record_surfaces_json_repair_diagnostics(
    tmp_path: Path,
) -> None:
    proposal = {
        "status": "failed",
        "authority": "proposal_only_not_registry_acceptance",
        "summary": {},
        "diagnostics": [
            {"severity": "warning", "code": "ai_json_repair_needed"},
            {"severity": "error", "code": "ai_json_repair_exhausted"},
        ],
        "providerReceipt": {
            "jsonRepairNeeded": True,
            "jsonRepairAttemptCount": 1,
            "jsonRepairStatus": "exhausted",
        },
        "privacy": {"rawModelResponsesPersisted": False},
    }

    record = ai_proposal_record(
        tmp_path / "request.json",
        tmp_path / "proposal.json",
        proposal,
    )

    assert record["status"] == "failed"
    assert record["diagnosticCodes"] == [
        "ai_json_repair_exhausted",
        "ai_json_repair_needed",
    ]
    assert record["jsonRepair"] == {
        "attemptCount": 1,
        "needed": True,
        "status": "exhausted",
    }


def test_autonomous_candidate_batch_applies_clean_ai_enrichment_when_opted_in(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace"),
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    assert report["status"] == "passed"
    assert report["summary"]["aiEnrichedPreviewAppliedCount"] == 1
    assert report["summary"]["aiEnrichedPreviewSkippedCount"] == 2
    assert report["summary"]["aiEnrichedPreviewFailedCount"] == 0
    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert enriched["status"] == "prepared"
    assert enriched["summary"] == {
        "appliedCount": 1,
        "failedCount": 0,
        "skippedCount": 2,
    }
    assert enriched["applied"][0]["packageId"] == "demo.workspace"
    assert enriched["applied"][0]["previewOnly"] is True
    assert enriched["applied"][0]["sourceMutated"] is False
    enriched_root = output / "package-sets" / "demo" / "enriched" / "demo.workspace"
    assert (enriched_root / "specpm.yaml").is_file()
    assert (enriched_root / "ai-enrichment-candidate-patch.json").is_file()
    assert "AI-enriched Demo Workspace" in (enriched_root / "specpm.yaml").read_text(
        encoding="utf-8"
    )


def test_autonomous_candidate_batch_skips_warning_ai_enrichment_application(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace", status="warning"),
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert enriched["status"] == "skipped"
    assert enriched["reason"] == "ai_enrichment_not_clean"
    assert enriched["summary"]["appliedCount"] == 0
    assert enriched["summary"]["skippedCount"] == 3
    assert not (output / "package-sets" / "demo" / "enriched").exists()


def test_autonomous_candidate_batch_failed_ai_enrichment_application_fails_repository(
    tmp_path: Path,
    monkeypatch,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_draft_proposal",
        lambda _options: completed_ai_draft_proposal(),
    )
    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_package_set_ai_enrichment_proposal",
        lambda _options: completed_ai_enrichment_proposal("demo.workspace"),
    )

    def fail_patch(_options: object) -> dict[str, object]:
        raise RuntimeError("unexpected patch failure")

    monkeypatch.setattr(
        "spec_harvester.autonomous_candidate_batch.build_ai_enrichment_candidate_patch",
        fail_patch,
    )

    report = run_autonomous_candidate_batch(
        AutonomousCandidateBatchOptions(
            inputs=inputs,
            out=output,
            lm_studio_model="openai/gpt-oss-20b",
            apply_ai_enrichment=True,
        )
    )

    enriched = report["repositories"][0]["aiEnrichedPreview"]
    assert report["status"] == "failed"
    assert report["repositories"][0]["status"] == "failed"
    assert enriched["status"] == "failed"
    assert enriched["summary"]["failedCount"] == 3
    assert enriched["failed"][0]["reason"] == "ai_enrichment_patch_failed"


def test_autonomous_candidate_batch_cli_writes_report(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    exit_code = main(
        [
            "autonomous-candidate-batch",
            str(inputs),
            "--out",
            str(output),
            "--skip-ai",
            "--repository-profile-selection",
            "auto",
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "passed"
    assert printed["collection"]["validationReport"].endswith("batch-validation-report.json")
    assert printed["repositories"][0]["preflight"]["status"] == "passed"
    assert printed["repositories"][0]["repositoryProfileDetection"]["selectedProfileId"] == (
        "generic.package_set.v0"
    )


def test_autonomous_candidate_batch_cli_auto_generates_repository_plugin_applicability(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    exit_code = main(
        [
            "autonomous-candidate-batch",
            str(inputs),
            "--out",
            str(output),
            "--skip-ai",
            "--repository-plugin-registry",
            str(GENERIC_REPOSITORY_PLUGIN_REGISTRY),
            "--repository-plugin-static-evidence-envelope",
            str(STATIC_REPOSITORY_PLUGIN_EVIDENCE_ENVELOPE),
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    sidecar = printed["repositoryPluginApplicability"]
    assert printed["status"] == "passed"
    assert sidecar["status"] == "recorded"
    assert sidecar["sourceMode"] == "auto_static_evaluator"
    assert sidecar["summary"]["selectedCount"] == 3
    assert sidecar["summary"]["blockedCount"] == 2


def test_autonomous_candidate_batch_cli_records_repository_plugin_adapter_evidence(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = write_source_manifest(tmp_path)
    output = tmp_path / "output"

    exit_code = main(
        [
            "autonomous-candidate-batch",
            str(inputs),
            "--out",
            str(output),
            "--skip-ai",
            "--repository-plugin-adapter-manifest",
            str(REPOSITORY_PLUGIN_ADAPTER_MANIFEST),
            "--repository-plugin-adapter-preflight",
            str(REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT),
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    sidecar = printed["repositoryPluginAdapterEvidence"]
    assert printed["status"] == "passed"
    assert printed["summary"]["repositoryPluginAdapterEvidenceSidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["summary"]["allowedCount"] == 3
    assert sidecar["summary"]["blockedCount"] == 1
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False
    assert sidecar["adapterExecution"] == "not_run"


def test_autonomous_candidate_batch_cli_records_trusted_local_adapter_run_evidence(
    tmp_path: Path,
    capsys,
) -> None:
    inputs = write_source_manifest(tmp_path)
    run_report = write_trusted_local_adapter_run_report_fixture(tmp_path)
    output = tmp_path / "output"

    exit_code = main(
        [
            "autonomous-candidate-batch",
            str(inputs),
            "--out",
            str(output),
            "--skip-ai",
            "--trusted-local-adapter-run-report",
            str(run_report),
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    sidecar = printed["trustedLocalAdapterRunEvidence"]
    assert printed["status"] == "passed"
    assert printed["summary"]["trustedLocalAdapterRunEvidenceSidecarCount"] == 1
    assert sidecar["status"] == "recorded"
    assert sidecar["kind"] == TRUSTED_LOCAL_ADAPTER_RUN_REPORT_KIND
    assert sidecar["runStatus"] == "no_execution_report_emitted"
    assert sidecar["adapterExecution"] == "not_run"
    assert sidecar["adapterCodeLoaded"] is False
    assert sidecar["adapterProcessSpawned"] is False
    assert sidecar["executedAdapterCount"] == 0
    assert sidecar["appliedToDrafting"] is False
    assert sidecar["registryAuthority"] is False


def write_trusted_local_adapter_run_report_fixture(tmp_path: Path) -> Path:
    payload = build_trusted_local_adapter_run_report(
        TrustedLocalAdapterRunOptions(
            request=TRUSTED_LOCAL_ADAPTER_RUN_REQUEST,
            preflight=TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT,
        )
    )
    path = tmp_path / "trusted-local-adapter-run-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_source_manifest(tmp_path: Path) -> Path:
    inputs = tmp_path / "inputs"
    checkout = write_workspace_checkout(tmp_path / "demo")
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        f"""
repositories:
  - id: demo
    repository: https://github.com/example/demo
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {checkout}
    packageId: demo.workspace
""",
        encoding="utf-8",
    )
    return inputs


def write_single_package_source_manifest(tmp_path: Path) -> Path:
    inputs = tmp_path / "single-inputs"
    checkout = write_go_single_package_checkout(tmp_path / "gin")
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        f"""
repositories:
  - id: gin
    repository: https://github.com/gin-gonic/gin
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {checkout}
    packageId: gin.core
""",
        encoding="utf-8",
    )
    return inputs


def write_scoped_go_target_source_manifest(tmp_path: Path) -> Path:
    inputs = tmp_path / "scoped-inputs"
    checkout = tmp_path / "scoped-go"
    (checkout / "packages").mkdir(parents=True)
    write_go_single_package_checkout(checkout / "packages" / "gin")
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        f"""
repositories:
  - id: gin-scoped
    repository: https://github.com/gin-gonic/gin
    revision: 0123456789abcdef0123456789abcdef01234567
    checkout: {checkout}
    target: packages/gin
    packageId: gin.core
""",
        encoding="utf-8",
    )
    return inputs


def write_repository_plugin_applicability_report(tmp_path: Path) -> Path:
    report = tmp_path / "repository-plugin-applicability-report.json"
    report.write_text(
        json.dumps(
            {
                "apiVersion": REPOSITORY_PLUGIN_APPLICABILITY_API_VERSION,
                "kind": REPOSITORY_PLUGIN_APPLICABILITY_KIND,
                "schemaVersion": 1,
                "authority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                "mode": "auto",
                "registry": {
                    "path": "tests/fixtures/repository_plugins/generic-registry.example.json",
                    "kind": "SpecHarvesterRepositoryPluginRegistry",
                    "authority": "producer_plugin_registry_only",
                },
                "repository": {
                    "id": "demo",
                    "sourceManifestPath": "inputs/repositories.yml",
                    "sourceManifestEntryId": "demo",
                    "revision": "0123456789abcdef0123456789abcdef01234567",
                },
                "staticEvidence": {
                    "inputAuthority": "static_local_evidence_only",
                    "paths": [
                        "package.json",
                        "packages/data/package.json",
                        "packages/ui/package.json",
                    ],
                    "evidenceKinds": [
                        "source_manifest",
                        "harvest_snapshot",
                        "workspace_inventory",
                        "repository_profile_detection",
                        "operator_label",
                    ],
                    "signals": ["workspace_manifest", "member_manifest"],
                },
                "summary": {
                    "selectedCount": 1,
                    "rejectedCount": 1,
                    "fallbackCount": 1,
                    "blockedCount": 2,
                    "diagnosticCount": 5,
                },
                "selectedPlugins": [
                    {
                        "pluginId": "spec_harvester.generic.repository_profile.v0",
                        "role": "repository_profile",
                        "decision": "selected",
                        "decisionAuthority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                        "pluginOutputAuthority": "producer_side_evidence_only",
                        "confidence": "high",
                        "reasonCodes": ["workspace_manifest_present"],
                        "evidencePaths": ["package.json"],
                        "outputArtifactKinds": ["repository_profile_detection"],
                    },
                ],
                "rejectedPlugins": [
                    {
                        "pluginId": "spec_harvester.generic.review_surface.v0",
                        "role": "review_surface",
                        "decision": "rejected",
                        "decisionAuthority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                        "pluginOutputAuthority": "producer_side_evidence_only",
                        "confidence": "low",
                        "reasonCodes": ["missing_review_panel_evidence"],
                        "evidencePaths": [],
                        "outputArtifactKinds": ["review_panel_data"],
                    }
                ],
                "fallbackPlugins": [
                    {
                        "pluginId": "spec_harvester.generic.parser_profile.v0",
                        "role": "parser_profile",
                        "decision": "fallback",
                        "decisionAuthority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                        "pluginOutputAuthority": "producer_side_evidence_only",
                        "confidence": "medium",
                        "reasonCodes": ["conservative_default_path_classification"],
                        "evidencePaths": ["package.json"],
                        "outputArtifactKinds": ["repository_parsing_profile_decision"],
                    }
                ],
                "blockedPlugins": [
                    {
                        "pluginId": "spec_harvester.generic.manifest_summary.v0",
                        "role": "evidence_producer",
                        "decision": "blocked",
                        "decisionAuthority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                        "pluginOutputAuthority": "producer_side_evidence_only",
                        "confidence": "blocked",
                        "reasonCodes": ["required_manifest_digest_missing"],
                        "evidencePaths": ["package.json"],
                        "outputArtifactKinds": ["manifest_summary"],
                    },
                    {
                        "pluginId": "spec_harvester.generic.package_topology.v0",
                        "role": "topology_helper",
                        "decision": "blocked",
                        "decisionAuthority": REPOSITORY_PLUGIN_APPLICABILITY_AUTHORITY,
                        "pluginOutputAuthority": "producer_side_evidence_only",
                        "confidence": "blocked",
                        "reasonCodes": ["requires_manifest_summary_evidence"],
                        "evidencePaths": [
                            "packages/data/package.json",
                            "packages/ui/package.json",
                        ],
                        "outputArtifactKinds": ["package_topology_hint"],
                    },
                ],
                "diagnostics": [
                    {
                        "severity": "info",
                        "code": "plugin_selected",
                        "pluginId": "spec_harvester.generic.repository_profile.v0",
                        "message": "Repository profile selected.",
                        "evidencePaths": ["package.json"],
                    },
                    {
                        "severity": "error",
                        "code": "plugin_blocked_required_evidence_missing",
                        "pluginId": "spec_harvester.generic.package_topology.v0",
                        "message": "Topology helper blocked.",
                        "evidencePaths": ["packages/data/package.json"],
                    },
                    {
                        "severity": "info",
                        "code": "plugin_fallback",
                        "pluginId": "spec_harvester.generic.parser_profile.v0",
                        "message": "Parser profile fell back.",
                        "evidencePaths": ["package.json"],
                    },
                    {
                        "severity": "warning",
                        "code": "plugin_rejected_low_confidence",
                        "pluginId": "spec_harvester.generic.review_surface.v0",
                        "message": "Review surface rejected.",
                        "evidencePaths": [],
                    },
                    {
                        "severity": "error",
                        "code": "plugin_blocked_required_evidence_missing",
                        "pluginId": "spec_harvester.generic.manifest_summary.v0",
                        "message": "Manifest summary blocked.",
                        "evidencePaths": ["package.json"],
                    },
                ],
                "nonAuthorityStatements": [
                    "does_not_load_third_party_plugin_code",
                    "does_not_execute_plugins",
                    "does_not_change_parser_profile_behavior",
                    "does_not_change_repository_profile_scoring",
                    "does_not_accept_packages",
                    "does_not_accept_relations",
                    "does_not_publish_registry_metadata",
                    "does_not_remove_preview_only",
                    "does_not_treat_plugin_decisions_as_registry_truth",
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return report


def write_workspace_checkout(path: Path) -> Path:
    path.mkdir()
    (path / "README.md").write_text(
        "# Demo\n\nDemo workspace for autonomous candidate batch tests.\n",
        encoding="utf-8",
    )
    (path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (path / "package.json").write_text(
        json.dumps(
            {
                "name": "@demo/workspace",
                "private": True,
                "workspaces": ["packages/*"],
                "description": "Demo workspace.",
                "license": "MIT",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    write_package_manifest(
        path / "packages" / "data",
        "@demo/data",
        "Data package.",
    )
    write_package_manifest(
        path / "packages" / "ui",
        "@demo/ui",
        "UI binding package.",
    )
    return path


def write_go_single_package_checkout(path: Path) -> Path:
    path.mkdir()
    (path / "README.md").write_text(
        "# Gin\n\nGin is a web framework written in Go.\n",
        encoding="utf-8",
    )
    (path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (path / "go.mod").write_text(
        "module github.com/gin-gonic/gin\n\ngo 1.22\n",
        encoding="utf-8",
    )
    (path / "gin.go").write_text(
        "package gin\n\nfunc New() *Engine { return &Engine{} }\n\ntype Engine struct{}\n",
        encoding="utf-8",
    )
    return path


def write_package_manifest(package_root: Path, name: str, description: str) -> None:
    package_root.mkdir(parents=True)
    (package_root / "package.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "0.1.0",
                "description": description,
                "license": "MIT",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (package_root / "README.md").write_text(f"# {name}\n\n{description}\n", encoding="utf-8")


def completed_ai_draft_proposal() -> dict[str, object]:
    return {
        "apiVersion": "spec-harvester.package-set-ai-draft/v0",
        "kind": "SpecHarvesterPackageSetAIDraftProposal",
        "schemaVersion": 1,
        "status": "completed",
        "authority": "proposal_only_not_registry_acceptance",
        "summary": {"proposalCount": 1},
        "diagnostics": [],
        "providerReceipt": {
            "jsonRepairNeeded": False,
            "jsonRepairAttemptCount": 0,
            "jsonRepairStatus": "not_needed",
        },
        "privacy": {"rawModelResponsesPersisted": False},
    }


def completed_ai_enrichment_proposal(
    package_id: str, *, status: str = "completed"
) -> dict[str, object]:
    return {
        "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
        "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
        "schemaVersion": 1,
        "status": status,
        "authority": "proposal_only_not_registry_acceptance",
        "provider": {
            "name": "lm_studio",
            "model": "openai/gpt-oss-20b",
            "execution": "operator_opt_in_local",
        },
        "summary": {"proposalCount": 1},
        "diagnostics": [],
        "proposals": [
            {
                "packageId": package_id,
                "status": "proposed",
                "refinedSummary": (
                    "AI-enriched Demo Workspace captures the public workspace "
                    "contract for reviewable starter specs."
                ),
                "overallConfidence": "high",
                "capabilities": [
                    {
                        "id": "demo.workspace.ai_enriched_review",
                        "summary": "Provides AI-enriched review evidence for the demo workspace.",
                        "intentIds": ["intent.spec_authoring.review_ready_starter"],
                        "evidencePaths": [f"{package_id}/specpm.yaml"],
                        "confidence": "high",
                    }
                ],
                "interfaces": [
                    {
                        "id": f"package.{package_id}",
                        "kind": "library",
                        "summary": "Reviewable package interface for the demo workspace.",
                        "evidencePaths": [f"{package_id}/specpm.yaml"],
                        "confidence": "high",
                    }
                ],
                "evidenceGaps": [],
                "providerReceipt": {
                    "responseDigest": "sha256:test",
                    "jsonRepairNeeded": False,
                    "jsonRepairAttemptCount": 0,
                    "jsonRepairStatus": "not_needed",
                },
            }
        ],
        "privacy": {"rawModelResponsesPersisted": False},
    }
