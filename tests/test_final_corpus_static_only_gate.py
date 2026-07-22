from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from spec_harvester import cli
from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    AutonomousCandidateBatchOptions,
)
from spec_harvester.final_corpus_static_only_gate import (
    FINAL_CORPUS_STATIC_ONLY_GATE_REPORT_FILENAME,
    FinalCorpusStaticOnlyGate,
    FinalCorpusStaticOnlyGateOptions,
)
from spec_harvester.producer_receipt import sha256_file


def test_ninety_six_percent_static_completion_unlocks_p52_t7(tmp_path: Path) -> None:
    inputs, readiness, digest = write_inputs_and_readiness(tmp_path)
    calls: list[AutonomousCandidateBatchOptions] = []

    def batch_runner(options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
        calls.append(options)
        return write_batch(options, passed_count=48)

    options = FinalCorpusStaticOnlyGateOptions(
        inputs=inputs,
        readiness=readiness,
        readiness_sha256=digest,
        out=tmp_path / "out",
    )
    report = FinalCorpusStaticOnlyGate(options, batch_runner=batch_runner).run()

    assert len(calls) == 1
    assert calls[0].skip_ai is True
    assert calls[0].repository_profile_selection == "auto"
    assert report["status"] == "passed"
    assert report["staticBatch"]["status"] == "failed"
    assert report["staticCompletionRate"] == {
        "value": 0.96,
        "numerator": 48,
        "denominator": 50,
        "minimum": 0.95,
        "passed": True,
    }
    assert report["failedRepositoryIds"] == ["repo-48", "repo-49"]
    assert report["decision"]["p52T7Unlocked"] is True
    assert all(value is False for value in report["nonAuthority"].values())
    persisted = json.loads(
        (options.out / FINAL_CORPUS_STATIC_ONLY_GATE_REPORT_FILENAME).read_text()
    )
    assert persisted == report


def test_below_threshold_static_completion_blocks_p52_t7(tmp_path: Path) -> None:
    inputs, readiness, digest = write_inputs_and_readiness(tmp_path)
    gate = FinalCorpusStaticOnlyGate(
        FinalCorpusStaticOnlyGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=digest,
            out=tmp_path / "out",
        ),
        batch_runner=lambda options: write_batch(options, passed_count=47),
    )

    report = gate.run()

    assert report["status"] == "failed"
    assert report["staticCompletionRate"]["value"] == 0.94
    assert report["decision"] == {
        "p52T7Unlocked": False,
        "selectedDecision": "block_p52_t7",
    }


def test_readiness_digest_mismatch_stops_before_static_batch(tmp_path: Path) -> None:
    inputs, readiness, _digest = write_inputs_and_readiness(tmp_path)
    called = False

    def batch_runner(_options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
        nonlocal called
        called = True
        return {}

    gate = FinalCorpusStaticOnlyGate(
        FinalCorpusStaticOnlyGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256="0" * 64,
            out=tmp_path / "out",
        ),
        batch_runner=batch_runner,
    )

    with pytest.raises(ValueError, match="readiness digest mismatch"):
        gate.run()
    assert called is False


def test_readiness_source_mismatch_stops_before_static_batch(tmp_path: Path) -> None:
    inputs, readiness, _digest = write_inputs_and_readiness(tmp_path)
    payload = json.loads(readiness.read_text())
    payload["repositories"][0]["id"] = "unexpected"
    readiness.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    called = False

    def batch_runner(_options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
        nonlocal called
        called = True
        return {}

    gate = FinalCorpusStaticOnlyGate(
        FinalCorpusStaticOnlyGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=sha256_file(readiness),
            out=tmp_path / "out",
        ),
        batch_runner=batch_runner,
    )

    with pytest.raises(ValueError, match="source ids do not match"):
        gate.run()
    assert called is False


def test_ai_activity_blocks_static_execution_boundary(tmp_path: Path) -> None:
    inputs, readiness, digest = write_inputs_and_readiness(tmp_path)

    def batch_runner(options: AutonomousCandidateBatchOptions) -> dict[str, Any]:
        batch = write_batch(options, passed_count=50)
        batch["ai"] = {"mode": "local_lm_studio", "provider": "test", "model": "test"}
        batch["repositories"][0]["aiDraft"] = {"status": "completed"}
        return batch

    gate = FinalCorpusStaticOnlyGate(
        FinalCorpusStaticOnlyGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=digest,
            out=tmp_path / "out",
        ),
        batch_runner=batch_runner,
    )

    report = gate.run()

    assert report["staticCompletionRate"]["passed"] is True
    assert report["staticExecutionBoundary"]["passed"] is False
    assert report["decision"]["p52T7Unlocked"] is False


def test_static_only_gate_cli_maps_passing_report_to_zero(monkeypatch, capsys) -> None:
    captured: list[FinalCorpusStaticOnlyGateOptions] = []

    def run(options: FinalCorpusStaticOnlyGateOptions) -> dict[str, Any]:
        captured.append(options)
        return {"status": "passed", "decision": {"p52T7Unlocked": True}}

    monkeypatch.setattr(cli, "run_final_corpus_static_only_gate", run)
    args = cli.build_parser().parse_args(
        [
            "final-corpus-static-only-gate",
            "inputs",
            "--readiness",
            "readiness.json",
            "--readiness-sha256",
            "a" * 64,
            "--out",
            "out",
        ]
    )

    assert args.func(args) == 0
    assert captured == [
        FinalCorpusStaticOnlyGateOptions(
            inputs=Path("inputs"),
            readiness=Path("readiness.json"),
            readiness_sha256="a" * 64,
            out=Path("out"),
        )
    ]
    assert json.loads(capsys.readouterr().out)["status"] == "passed"


def test_durable_p52_t6_fixture_records_passing_static_gate() -> None:
    root = Path(__file__).resolve().parents[1]
    report = json.loads(
        (
            root / "tests/fixtures/final_corpus_static_only_gate/"
            "p52-t6-final-corpus-static-only-gate.example.json"
        ).read_text(encoding="utf-8")
    )

    assert report["status"] == "passed"
    assert report["sourceCoverage"]["resultCount"] == 50
    assert report["staticCompletionRate"]["value"] == 0.96
    assert report["failedRepositoryIds"] == ["actix-web", "uv"]
    assert report["staticExecutionBoundary"]["passed"] is True
    assert report["decision"] == {
        "p52T7Unlocked": True,
        "selectedDecision": "unlock_p52_t7",
    }


def write_inputs_and_readiness(tmp_path: Path) -> tuple[Path, Path, str]:
    inputs = tmp_path / "inputs"
    inputs.mkdir()
    manifest = ["repositories:"]
    repositories = []
    for index in range(50):
        repository_id = f"repo-{index:02d}"
        manifest.extend(
            [
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {index:040x}",
                f"    checkout: checkouts/{repository_id}",
            ]
        )
        repositories.append({"id": repository_id, "status": "ready"})
    (inputs / "repositories.yml").write_text("\n".join(manifest) + "\n")
    readiness = tmp_path / "readiness.json"
    readiness.write_text(
        json.dumps(
            {
                "task": "P52-T5",
                "status": "passed",
                "repositories": repositories,
                "decision": {"p52T6Unlocked": True},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return inputs, readiness, sha256_file(readiness)


def write_batch(
    options: AutonomousCandidateBatchOptions,
    *,
    passed_count: int,
) -> dict[str, Any]:
    options.out.mkdir(parents=True)
    repositories = []
    for index in range(50):
        status = "passed" if index < passed_count else "failed"
        record: dict[str, Any] = {
            "id": f"repo-{index:02d}",
            "status": status,
            "preflight": {"status": "passed" if status == "passed" else "failed"},
            "packageSetDraft": {"candidateCount": 1, "relationCount": 0},
            "aiDraft": {"status": "skipped"},
            "aiEnrichment": {"status": "skipped"},
            "aiEnrichedPreview": {"status": "skipped"},
        }
        if status == "failed":
            record["diagnostics"] = [{"code": "fixture_static_failure"}]
        repositories.append(record)
    batch = {
        "status": "passed" if passed_count == 50 else "failed",
        "authority": "producer_preview_evidence_only",
        "ai": {"mode": "disabled", "provider": None, "model": None},
        "repositoryPluginAdapterEvidence": {"adapterExecution": "not_run"},
        "trustedLocalAdapterRunEvidence": {"adapterExecution": "not_run"},
        "repositories": repositories,
    }
    (options.out / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).write_text(
        json.dumps(batch, indent=2, sort_keys=True) + "\n"
    )
    reports = options.out / "reports"
    reports.mkdir()
    (reports / "batch-validation-report.json").write_text(
        json.dumps(
            {
                "records": [
                    {
                        "id": f"repo-{index:02d}",
                        "errors": (
                            [] if index < passed_count else [{"code": "fixture_static_failure"}]
                        ),
                        "warnings": [],
                    }
                    for index in range(50)
                ]
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return batch
