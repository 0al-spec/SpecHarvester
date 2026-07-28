from __future__ import annotations

import json
from pathlib import Path

import pytest

import spec_harvester.cli as cli
import spec_harvester.p53_codex_spark_wave as wave_module
from spec_harvester.p53_codex_spark_wave import (
    P53CodexSparkWave,
    P53CodexSparkWaveOptions,
    outcome_kind,
    wave_one_sources,
    wave_sources,
)

ROOT = Path(__file__).resolve().parents[1]


def test_wave_one_source_selection_is_exactly_first_twenty_five_p53_positions() -> None:
    sources = wave_one_sources(
        ROOT / "inputs/p53-mass-corpus",
        ROOT / "inputs/p53-mass-corpus/selection-metadata.json",
    )

    assert len(sources) == 25
    assert sources[0]["id"] == "public-apis-public-apis"
    assert sources[-1]["id"] == "vinta-awesome-python"


def test_wave_two_source_selection_is_exactly_positions_twenty_six_through_fifty() -> None:
    sources = wave_sources(
        ROOT / "inputs/p53-mass-corpus",
        ROOT / "inputs/p53-mass-corpus/selection-metadata.json",
        "wave-2",
    )

    assert len(sources) == 25
    assert sources[0]["id"] == "n8n-io-n8n"
    assert sources[-1]["id"] == "react-create-react-app"


def test_wave_three_source_selection_is_exactly_positions_fifty_one_through_seventy_five() -> None:
    sources = wave_sources(
        ROOT / "inputs/p53-mass-corpus",
        ROOT / "inputs/p53-mass-corpus/selection-metadata.json",
        "wave-3",
    )

    assert len(sources) == 25
    assert sources[0]["id"] == "infiniflow-ragflow"
    assert sources[-1]["id"] == "ladybirdbrowser-ladybird"


def test_outcome_classification_only_retries_transport_or_schema_failures() -> None:
    assert outcome_kind({"status": "completed"}) == "completed"
    assert outcome_kind({"status": "failed", "failure": "codex_timeout"}) == "timeout"
    assert outcome_kind({"status": "failed", "failure": "codex_final_message_invalid_json"}) == (
        "schema_repairable_failure"
    )
    assert outcome_kind({"status": "failed", "failure": "unsupported_claim"}) == "terminal_failure"


def test_runner_dispatches_only_wave_one_and_persists_completed_checkpoint(
    tmp_path: Path, monkeypatch
) -> None:
    sources = [{"id": f"repo-{index:02d}", "revision": f"{index:040x}"} for index in range(25)]
    plan = wave_module.read_json(
        ROOT
        / "tests/fixtures/mass_repository_campaign_plan"
        / "p53-t1-mass-repository-campaign-plan.example.json"
    )
    static = {
        "status": "passed",
        "repositories": [
            {
                "id": source["id"],
                "status": "passed",
                "checkout": str(tmp_path / source["id"]),
            }
            for source in sources
        ],
    }
    monkeypatch.setattr(wave_module, "wave_sources", lambda *_args: sources)
    monkeypatch.setattr(wave_module, "read_json", lambda *_args: plan)
    monkeypatch.setattr(wave_module, "run_autonomous_candidate_batch", lambda *_args: static)
    runner = P53CodexSparkWave(
        P53CodexSparkWaveOptions(
            inputs=tmp_path,
            metadata=tmp_path / "metadata.json",
            campaign_plan=tmp_path / "plan.json",
            out=tmp_path / "out",
        )
    )
    monkeypatch.setattr(runner.calibration, "schema", lambda: {})
    monkeypatch.setattr(runner.calibration.codex_executor, "version", lambda: "test")
    calls: list[str] = []

    def completed_record(
        record: dict[str, object], _schema: object, _version: object
    ) -> dict[str, object]:
        calls.append(str(record["id"]))
        return {
            "id": record["id"],
            "status": "completed",
            "schemaValid": True,
            "repositorySpecific": True,
            "unsupportedClaimCount": 0,
            "receipt": {"durationMs": 1},
        }

    monkeypatch.setattr(runner.calibration, "codex_repository_record", completed_record)

    report = runner.run()

    assert report["status"] == "passed"
    assert report["checkpointSummary"] == {
        "completed": 25,
        "terminalFailed": 0,
        "stop": {
            "trigger": "wave_budget_limit",
            "outcome": "stop_current_wave_and_block_later_waves",
        },
    }
    assert len(report["codexSpark"]["repositories"]) == 25
    assert report["quality"]["passed"] is True

    resumed = runner.run()

    assert len(calls) == 25
    assert len(resumed["codexSpark"]["repositories"]) == 25
    assert resumed["status"] == "passed"


def test_runner_stops_when_aggregate_quality_threshold_fails(tmp_path: Path, monkeypatch) -> None:
    sources = [{"id": f"repo-{index:02d}", "revision": f"{index:040x}"} for index in range(25)]
    plan = wave_module.read_json(
        ROOT
        / "tests/fixtures/mass_repository_campaign_plan"
        / "p53-t1-mass-repository-campaign-plan.example.json"
    )
    static = {
        "status": "passed",
        "repositories": [{"id": source["id"], "status": "passed"} for source in sources],
    }
    monkeypatch.setattr(wave_module, "wave_sources", lambda *_args: sources)
    monkeypatch.setattr(wave_module, "read_json", lambda *_args: plan)
    monkeypatch.setattr(wave_module, "run_autonomous_candidate_batch", lambda *_args: static)
    runner = P53CodexSparkWave(
        P53CodexSparkWaveOptions(
            inputs=tmp_path,
            metadata=tmp_path / "metadata.json",
            campaign_plan=tmp_path / "plan.json",
            out=tmp_path / "out",
        )
    )
    monkeypatch.setattr(runner.calibration, "schema", lambda: {})
    monkeypatch.setattr(runner.calibration.codex_executor, "version", lambda: "test")
    monkeypatch.setattr(
        runner.calibration,
        "codex_repository_record",
        lambda record, _schema, _version: {
            "id": record["id"],
            "status": "completed",
            "schemaValid": True,
            "repositorySpecific": record["id"] != "repo-00",
            "unsupportedClaimCount": 1 if record["id"] == "repo-00" else 0,
            "receipt": {"durationMs": 1},
        },
    )

    report = runner.run()

    assert report["status"] == "failed"
    assert report["quality"]["passed"] is False
    assert report["checkpointSummary"]["stop"]["trigger"] == "quality_threshold_failure"


def test_wave_two_runner_requires_t7_authorization_before_dispatch(
    tmp_path: Path, monkeypatch
) -> None:
    sources = [{"id": f"repo-{index:02d}", "revision": f"{index:040x}"} for index in range(25)]
    plan = wave_module.read_json(
        ROOT
        / "tests/fixtures/mass_repository_campaign_plan"
        / "p53-t1-mass-repository-campaign-plan.example.json"
    )
    static = {
        "status": "passed",
        "repositories": [
            {"id": source["id"], "status": "passed", "checkout": str(tmp_path / source["id"])}
            for source in sources
        ],
    }
    monkeypatch.setattr(wave_module, "wave_sources", lambda *_args: sources)
    monkeypatch.setattr(wave_module, "read_json", lambda *_args: plan)
    monkeypatch.setattr(wave_module, "run_autonomous_candidate_batch", lambda *_args: static)
    source_report_path = tmp_path / "p53-t6-report.json"
    reviewed_ids = [f"review-{index}" for index in range(5)]
    source_report_path.write_text(
        json.dumps(
            {
                "task": "P53-T6",
                "status": "passed",
                "codexSpark": {
                    "repositories": [
                        {"id": repository_id, "status": "completed"}
                        for repository_id in reviewed_ids
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    decision_path = tmp_path / "p53-t7-decision.json"
    decision_path.write_text(
        json.dumps(
            {
                "apiVersion": "spec-harvester.p53-scale-out-decision/v0",
                "kind": "SpecHarvesterP53ScaleOutDecision",
                "phase": "P53",
                "task": "P53-T7",
                "status": "passed",
                "fromWave": "wave-1",
                "toWave": "wave-2",
                "decision": "unlock_wave-2_only",
                "sourceWaveReport": {
                    "task": "P53-T6",
                    "path": str(source_report_path),
                    "sha256": wave_module.calibration.sha256(
                        source_report_path.read_bytes()
                    ).hexdigest(),
                },
                "qualityMetrics": {
                    "codexCompletionRate": 1.0,
                    "schemaValidRate": 1.0,
                    "repositorySpecificRate": 1.0,
                    "unsupportedClaimRate": 0.0,
                    "terminalFailureCount": 0,
                },
                "humanReview": {
                    "minimumRequired": 5,
                    "reviewedRepositoryIds": reviewed_ids,
                },
            }
        ),
        encoding="utf-8",
    )
    runner = P53CodexSparkWave(
        P53CodexSparkWaveOptions(
            inputs=tmp_path,
            metadata=tmp_path / "metadata.json",
            campaign_plan=tmp_path / "plan.json",
            out=tmp_path / "out",
            wave="wave-2",
            scale_out_decision=decision_path,
        )
    )
    monkeypatch.setattr(runner.calibration, "schema", lambda: {})
    monkeypatch.setattr(runner.calibration.codex_executor, "version", lambda: "test")
    monkeypatch.setattr(
        runner.calibration,
        "codex_repository_record",
        lambda record, _schema, _version: {
            "id": record["id"],
            "status": "completed",
            "schemaValid": True,
            "repositorySpecific": True,
            "unsupportedClaimCount": 0,
            "receipt": {"durationMs": 1},
        },
    )

    report = runner.run()

    assert report["task"] == "P53-T8"
    assert report["wave"] == "wave-2"
    assert report["checkpointSummary"]["completed"] == 25
    assert report["scaleOutDecision"]["task"] == "P53-T7"

    source_payload = json.loads(source_report_path.read_text(encoding="utf-8"))
    source_payload["status"] = "failed"
    source_report_path.write_text(json.dumps(source_payload), encoding="utf-8")
    decision_payload = json.loads(decision_path.read_text(encoding="utf-8"))
    decision_payload["sourceWaveReport"]["sha256"] = wave_module.calibration.sha256(
        source_report_path.read_bytes()
    ).hexdigest()
    decision_path.write_text(json.dumps(decision_payload), encoding="utf-8")

    with pytest.raises(ValueError, match="source evidence is not a passed prior wave"):
        runner.validate_scale_out_decision(plan)

    source_payload["status"] = "passed"
    source_payload["codexSpark"]["repositories"].pop()
    source_report_path.write_text(json.dumps(source_payload), encoding="utf-8")
    decision_payload["sourceWaveReport"]["sha256"] = wave_module.calibration.sha256(
        source_report_path.read_bytes()
    ).hexdigest()
    decision_path.write_text(json.dumps(decision_payload), encoding="utf-8")

    with pytest.raises(ValueError, match="reviews are not backed by completed outcomes"):
        runner.validate_scale_out_decision(plan)


def test_wave_two_rejects_missing_t7_authorization(tmp_path: Path, monkeypatch) -> None:
    plan = wave_module.read_json(
        ROOT
        / "tests/fixtures/mass_repository_campaign_plan"
        / "p53-t1-mass-repository-campaign-plan.example.json"
    )
    monkeypatch.setattr(wave_module, "wave_sources", lambda *_args: [])
    monkeypatch.setattr(wave_module, "read_json", lambda *_args: plan)
    runner = P53CodexSparkWave(
        P53CodexSparkWaveOptions(
            inputs=tmp_path,
            metadata=tmp_path / "metadata.json",
            campaign_plan=tmp_path / "plan.json",
            out=tmp_path / "out",
            wave="wave-2",
        )
    )

    try:
        runner.run()
    except ValueError as exc:
        assert str(exc) == "P53 wave-2 requires a validated P53-T7 scale-out decision artifact"
    else:
        raise AssertionError("wave-2 must not run without a P53-T7 decision artifact")


def test_cli_passes_requested_wave_to_runner(tmp_path: Path, monkeypatch) -> None:
    args = cli.build_parser().parse_args(
        [
            "p53-codex-spark-wave-1",
            str(tmp_path / "inputs"),
            "--metadata",
            str(tmp_path / "metadata.json"),
            "--campaign-plan",
            str(tmp_path / "plan.json"),
            "--out",
            str(tmp_path / "out"),
            "--wave",
            "wave-2",
            "--scale-out-decision",
            str(tmp_path / "decision.json"),
        ]
    )
    captured: dict[str, object] = {}

    def fake_run(options: P53CodexSparkWaveOptions) -> dict[str, str]:
        captured["wave"] = options.wave
        captured["scale_out_decision"] = options.scale_out_decision
        return {"status": "passed"}

    monkeypatch.setattr(cli, "run_p53_codex_spark_wave", fake_run)

    assert cli.run_p53_codex_spark_wave_cli(args) == 0
    assert captured["wave"] == "wave-2"
    assert captured["scale_out_decision"] == tmp_path / "decision.json"
