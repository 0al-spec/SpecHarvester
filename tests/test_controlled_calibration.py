from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from spec_harvester.autonomous_candidate_batch import AutonomousCandidateBatchOptions
from spec_harvester.controlled_calibration import (
    CONTROLLED_CALIBRATION_REPOSITORY_IDS,
    CodexExecutionResult,
    ControlledCalibration,
    ControlledCalibrationOptions,
    privacy_record,
    quality_metrics,
    schema_validation_errors,
)


class FakeCodexExecutor:
    def __init__(self, final_payload: dict[str, object]):
        self.final_payload = final_payload
        self.commands: list[list[str]] = []
        self.stage_paths: list[Path] = []

    def version(self) -> str:
        return "codex-cli test"

    def execute(self, command: list[str]) -> CodexExecutionResult:
        self.commands.append(command)
        self.stage_paths.append(Path(command[command.index("--cd") + 1]))
        output = Path(command[command.index("--output-last-message") + 1])
        output.write_text(json.dumps(self.final_payload), encoding="utf-8")
        return CodexExecutionResult(exit_code=0, duration_ms=7)


def test_offline_diagnostic_run_writes_report_without_unlocking_p52_t4(tmp_path: Path) -> None:
    inputs, revisions = write_p52_inputs(tmp_path)
    calls: list[AutonomousCandidateBatchOptions] = []

    def batch_runner(options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
        calls.append(options)
        options.out.mkdir(parents=True)
        return {
            "status": "passed",
            "repositories": [
                {
                    "id": repository_id,
                    "checkout": str(inputs / "checkouts" / repository_id),
                    "status": "passed",
                    "preflight": {"status": "passed"},
                }
                for repository_id in revisions
            ],
        }

    options = ControlledCalibrationOptions(
        inputs=inputs,
        out=tmp_path / "out",
        codex_schema=schema_path(),
        run_lm_studio=False,
        run_codex=False,
    )
    calibration = ControlledCalibration(
        options,
        batch_runner=batch_runner,
        checkout_head_reader=lambda checkout: revisions[checkout.name],
    )

    report = calibration.run()

    assert len(calls) == 1
    batch_options = calls[0]
    assert batch_options.inputs == inputs
    assert batch_options.out == options.out / "static-only"
    assert batch_options.skip_ai is True
    assert batch_options.repository_profile_selection == "auto"
    assert report["status"] == "failed"
    assert report["lmStudio"]["reason"] == "disabled_by_operator"
    assert report["codexSpark"]["reason"] == "disabled_by_operator"
    assert report["decision"] == {
        "thresholdsMet": False,
        "controlsCompleted": False,
        "p52T4Unlocked": False,
        "selectedDecision": "block_p52_t4",
    }
    persisted = json.loads(
        (options.out / "controlled-calibration-report.json").read_text(encoding="utf-8")
    )
    assert persisted == report


def test_codex_repository_handoff_uses_ephemeral_read_only_stage(tmp_path: Path) -> None:
    inventory, checkout = write_inventory_and_checkout(tmp_path)
    schema = read_schema()
    executor = FakeCodexExecutor(valid_final_message())
    options = ControlledCalibrationOptions(
        inputs=tmp_path / "inputs",
        out=tmp_path / "out",
        codex_schema=schema_path(),
        run_lm_studio=False,
    )
    calibration = ControlledCalibration(options, codex_executor=executor)
    target = calibration.static_root / "collected" / "demo"
    target.mkdir(parents=True)
    target_inventory = target / "workspace-inventory.json"
    target_inventory.write_bytes(inventory.read_bytes())

    record = calibration.codex_repository_record(
        {"id": "demo", "checkout": str(checkout)},
        schema,
        executor.version(),
    )

    command = executor.commands[0]
    assert record["status"] == "completed"
    assert record["schemaValid"] is True
    assert record["repositorySpecific"] is True
    assert "--sandbox" in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    assert {"--ephemeral", "--ignore-user-config", "--skip-git-repo-check"} <= set(command)
    assert "--add-dir" not in command
    assert "--dangerously-bypass-approvals-and-sandbox" not in command
    assert "--full-auto" not in command
    assert "--json" not in command
    assert "never cite package-set-ai-draft-request.json" in command[-1]
    assert "selectedMembers must include at least one package" in command[-1]
    assert not executor.stage_paths[0].exists()
    durable = options.out / record["proposal"]["path"]
    payload = json.loads(durable.read_text(encoding="utf-8"))
    assert payload["provider"]["kind"] == "codex_exec_external_model_output"
    assert payload["providerReceipt"]["rawPromptPersisted"] is False
    assert payload["providerReceipt"]["rawResponsePersisted"] is False
    assert privacy_record()["scope"] == "spec_harvester_durable_artifacts"


def test_codex_schema_failure_does_not_persist_raw_final_message(tmp_path: Path) -> None:
    inventory, checkout = write_inventory_and_checkout(tmp_path)
    schema = read_schema()
    raw_marker = "do-not-persist-this-model-content"
    executor = FakeCodexExecutor({"proposal": {"unexpected": raw_marker}})
    options = ControlledCalibrationOptions(
        inputs=tmp_path / "inputs",
        out=tmp_path / "out",
        codex_schema=schema_path(),
        run_lm_studio=False,
    )
    calibration = ControlledCalibration(options, codex_executor=executor)
    target = calibration.static_root / "collected" / "demo"
    target.mkdir(parents=True)
    (target / "workspace-inventory.json").write_bytes(inventory.read_bytes())

    record = calibration.codex_repository_record(
        {"id": "demo", "checkout": str(checkout)},
        schema,
        executor.version(),
    )

    serialized = json.dumps(record)
    assert record["status"] == "failed"
    assert record["failure"] == "codex_final_message_schema_invalid"
    assert record["schemaValid"] is False
    assert raw_marker not in serialized
    assert not executor.stage_paths[0].exists()
    assert not (options.out / "codex-spark" / "demo").exists()


def test_schema_validation_errors_are_value_free() -> None:
    errors = schema_validation_errors(read_schema(), {"proposal": {"secret": "not retained"}})

    assert errors
    assert all(set(item) == {"keyword", "path"} for item in errors)
    assert "not retained" not in json.dumps(errors)


def test_quality_metrics_enforce_phase_52_thresholds() -> None:
    static = {"repositories": [{"status": "passed"} for _ in range(5)]}
    clean_codex = {
        "repositories": [
            {
                "status": "completed",
                "schemaValid": True,
                "repositorySpecific": True,
                "unsupportedClaimCount": 0,
            }
            for _ in range(5)
        ]
    }

    metrics = quality_metrics(static, clean_codex)

    assert all(item["passed"] for item in metrics.values())
    clean_codex["repositories"][0]["unsupportedClaimCount"] = 1
    assert quality_metrics(static, clean_codex)["unsupportedClaimRate"]["passed"] is False


def test_sources_reject_any_non_p52_five_repository_set(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    (inputs / "repositories.yml").write_text(
        """
repositories:
  - id: not-p52
    repository: https://github.com/example/not-p52
    revision: abc123
    checkout: ../checkout
""",
        encoding="utf-8",
    )
    calibration = ControlledCalibration(
        ControlledCalibrationOptions(
            inputs=inputs,
            out=tmp_path / "out",
            run_lm_studio=False,
            run_codex=False,
        )
    )

    with pytest.raises(ValueError, match="requires exactly the five controlled repositories"):
        calibration.sources()

    assert len(CONTROLLED_CALIBRATION_REPOSITORY_IDS) == 5


def write_inventory_and_checkout(tmp_path: Path) -> tuple[Path, Path]:
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    (checkout / "README.md").write_text("# Demo\n", encoding="utf-8")
    (checkout / "package.json").write_text('{"name":"demo"}\n', encoding="utf-8")
    inventory = {
        "apiVersion": "spec-harvester.workspace-inventory/v0",
        "kind": "SpecHarvesterWorkspaceInventory",
        "schemaVersion": 1,
        "source": {
            "repository": "https://github.com/example/demo",
            "exactRevision": "abc123",
            "revisionAuthority": "source_manifest_revision",
            "declaredRef": None,
        },
        "workspaceManifests": [],
        "packages": [
            {
                "ecosystem": "npm",
                "evidenceReferences": [{"kind": "package_manifest", "path": "package.json"}],
                "manifestPath": "package.json",
                "name": "demo",
                "packageManager": "npm",
                "proposedSpecpmPackageId": "demo.core",
                "role": "member_package",
                "sourceTargetPath": ".",
                "version": "1.0.0",
            }
        ],
        "summary": {
            "workspaceManifestCount": 0,
            "packageManifestCount": 1,
            "packageCount": 1,
            "diagnosticCount": 0,
        },
        "diagnostics": [],
        "authority": "producer_observed_review_evidence",
    }
    inventory_path = tmp_path / "workspace-inventory.json"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    return inventory_path, checkout


def write_p52_inputs(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    inputs = tmp_path / "inputs"
    checkouts = inputs / "checkouts"
    revisions = {
        "flask": "revision-flask",
        "gin": "revision-gin",
        "xyflow": "revision-xyflow",
        "fastapi": "revision-fastapi",
        "fastmcp": "revision-fastmcp",
    }
    for repository_id in revisions:
        (checkouts / repository_id).mkdir(parents=True)
    entries = "\n".join(
        "\n".join(
            (
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {revision}",
                f"    checkout: checkouts/{repository_id}",
            )
        )
        for repository_id, revision in revisions.items()
    )
    inputs.mkdir(exist_ok=True)
    (inputs / "repositories.yml").write_text(
        f"repositories:\n{entries}\n",
        encoding="utf-8",
    )
    return inputs, revisions


def valid_final_message() -> dict[str, object]:
    return {
        "proposal": {
            "packageSet": {
                "packageId": "demo.workspace",
                "summary": "Demo package set.",
                "evidencePaths": ["workspace-inventory.json"],
                "confidence": "high",
            },
            "selectedMembers": [
                {
                    "packageId": "demo.core",
                    "role": "primary_package",
                    "sourceTargetPath": ".",
                    "reason": "The deterministic inventory has one package.",
                    "evidencePaths": ["workspace-inventory.json", "package.json"],
                    "confidence": "high",
                }
            ],
            "excludedPackages": [],
            "relations": [
                {
                    "id": "demo.workspace.contains.demo.core",
                    "type": "contains",
                    "sourcePackageId": "demo.workspace",
                    "targetPackageId": "demo.core",
                    "evidencePaths": ["workspace-inventory.json"],
                    "confidence": "high",
                }
            ],
            "evidenceGaps": [],
            "overallConfidence": "high",
        }
    }


def schema_path() -> Path:
    return (
        Path(__file__).parent
        / "fixtures"
        / "codex_spark_external_model_adapter_contract"
        / "package-set-ai-draft-final-message.schema.json"
    )


def read_schema() -> dict[str, object]:
    return json.loads(schema_path().read_text(encoding="utf-8"))
