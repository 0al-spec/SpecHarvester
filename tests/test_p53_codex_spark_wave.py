from __future__ import annotations

from pathlib import Path

import spec_harvester.p53_codex_spark_wave as wave_module
from spec_harvester.p53_codex_spark_wave import (
    P53CodexSparkWave,
    P53CodexSparkWaveOptions,
    outcome_kind,
    wave_one_sources,
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
            {"id": source["id"], "checkout": str(tmp_path / source["id"])} for source in sources
        ],
    }
    monkeypatch.setattr(wave_module, "wave_one_sources", lambda *_args: sources)
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
            "repositorySpecific": True,
            "unsupportedClaimCount": 0,
            "receipt": {"durationMs": 1},
        },
    )

    report = runner.run()

    assert report["status"] == "passed"
    assert report["checkpointSummary"] == {
        "completed": 25,
        "terminalFailed": 0,
        "stop": None,
    }
    assert len(report["codexSpark"]["repositories"]) == 25
