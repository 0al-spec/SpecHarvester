from __future__ import annotations

import json
from pathlib import Path

from spec_harvester import cli
from spec_harvester.autonomous_candidate_batch import AutonomousCandidateBatchOptions
from spec_harvester.final_corpus_codex_spark_gate import (
    FinalCorpusCodexSparkGate,
    FinalCorpusCodexSparkGateOptions,
    coding_control_value,
    static_report_record,
)
from spec_harvester.producer_receipt import sha256_file


def test_p52_t7_gate_unblocks_p52_t8_with_passed_metrics(tmp_path: Path) -> None:
    inputs, readiness, digest = write_inputs_and_readiness(tmp_path)
    gate = FinalCorpusCodexSparkGate(
        FinalCorpusCodexSparkGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=digest,
            out=tmp_path / "out",
            run_codex=True,
        ),
        batch_runner=lambda options: write_batch(options, passed_count=50),
        codex_runner=lambda static_repositories, _passed, _schema: write_codex_result(
            static_repositories, completed=50, schema_valid=50, repository_specific=50
        ),
    )

    report = gate.run()

    assert report["status"] == "passed"
    assert report["decision"] == {
        "p52T8Unlocked": True,
        "selectedDecision": "unlock_p52_t8",
    }
    assert report["qualityMetrics"]["codexCompletionRate"]["passed"] is True


def test_p52_t7_gate_blocks_on_low_codex_threshold(tmp_path: Path) -> None:
    inputs, readiness, digest = write_inputs_and_readiness(tmp_path)
    gate = FinalCorpusCodexSparkGate(
        FinalCorpusCodexSparkGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=digest,
            out=tmp_path / "out",
            run_codex=True,
        ),
        batch_runner=lambda options: write_batch(options, passed_count=50),
        codex_runner=lambda static_repositories, _passed, _schema: write_codex_result(
            static_repositories,
            completed=40,
            schema_valid=40,
            repository_specific=40,
        ),
    )

    report = gate.run()

    assert report["status"] == "failed"
    assert report["qualityMetrics"]["codexCompletionRate"]["passed"] is False
    assert report["decision"] == {
        "p52T8Unlocked": False,
        "selectedDecision": "block_p52_t8",
    }


def test_readiness_mismatch_stops_before_static_run(tmp_path: Path) -> None:
    inputs, readiness, _digest = write_inputs_and_readiness(tmp_path)
    payload = json.loads(readiness.read_text(encoding="utf-8"))
    payload["repositories"][0]["id"] = "unexpected"
    readiness.write_text(json.dumps(payload), encoding="utf-8")
    digest = sha256_file(readiness)

    called = False

    def batch_runner(_options: AutonomousCandidateBatchOptions) -> dict:
        nonlocal called
        called = True
        return {}

    gate = FinalCorpusCodexSparkGate(
        FinalCorpusCodexSparkGateOptions(
            inputs=inputs,
            readiness=readiness,
            readiness_sha256=digest,
            out=tmp_path / "out",
        ),
        batch_runner=batch_runner,
    )

    with __import__("pytest").raises(ValueError, match="readiness source ids"):
        gate.run()
    assert called is False


def test_cli_maps_codex_spark_gate_args_to_options(monkeypatch, capsys) -> None:
    captured: list[FinalCorpusCodexSparkGateOptions] = []

    def run(options: FinalCorpusCodexSparkGateOptions) -> dict:
        captured.append(options)
        return {"status": "failed", "decision": {"p52T8Unlocked": False}}

    monkeypatch.setattr(cli, "run_final_corpus_codex_spark_gate", run)
    args = cli.build_parser().parse_args(
        [
            "final-corpus-codex-spark-gate",
            "inputs",
            "--readiness",
            "readiness.json",
            "--readiness-sha256",
            "a" * 64,
            "--out",
            "out",
            "--skip-codex",
        ]
    )

    assert args.func(args) in {0, 1}
    assert captured == [
        FinalCorpusCodexSparkGateOptions(
            inputs=Path("inputs"),
            readiness=Path("readiness.json"),
            readiness_sha256="a" * 64,
            out=Path("out"),
            codex_command="codex",
            codex_model="gpt-5.3-codex-spark",
            codex_schema=Path(
                "tests/fixtures/codex_spark_external_model_adapter_contract/"
                "package-set-ai-draft-final-message.schema.json"
            ),
            codex_timeout_seconds=300.0,
            run_codex=False,
        )
    ]
    assert json.loads(capsys.readouterr().out)["decision"]["p52T8Unlocked"] is False


def test_static_report_record_returns_path_and_digest(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir(parents=True)
    report = out / "report.json"
    report.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert static_report_record(out, report)["path"] == "report.json"


def test_coding_control_value_extracts_projection() -> None:
    control = coding_control_value(
        {"kind": "codex", "model": "x", "sandbox": "r", "execution": "y"}
    )
    assert control == {"kind": "codex", "model": "x", "sandbox": "r", "execution": "y"}


def write_inputs_and_readiness(tmp_path: Path) -> tuple[Path, Path, str]:
    inputs, _manifest_path, _metadata = write_inputs(tmp_path)
    readiness = tmp_path / "p52-t6-final-corpus-static-only-gate.json"
    readiness.write_text(
        json.dumps(
            {
                "task": "P52-T6",
                "status": "passed",
                "repositories": [
                    {
                        "id": repo["id"],
                        "repository": repo["repository"],
                        "revision": repo["revision"],
                        "status": "ready",
                    }
                    for repo in manifest_records(inputs)
                ],
                "decision": {"p52T7Unlocked": True},
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return inputs, readiness, sha256_file(readiness)


def write_batch(options: AutonomousCandidateBatchOptions, passed_count: int) -> dict:
    return {
        "status": "passed" if passed_count >= 48 else "failed",
        "repositories": [
            {
                "id": f"repo-{index:02d}",
                "status": "passed" if index < passed_count else "failed",
                "checkout": f"out/checkout/repo-{index:02d}",
                "preflight": {"status": "passed"},
                "packageSetDraft": {
                    "candidateCount": 0,
                    "relationCount": 0,
                },
            }
            for index in range(50)
        ],
        "reports": [],
        "ai": {"mode": "disabled", "provider": None, "model": None},
        "repositoryPluginAdapterEvidence": {"adapterExecution": "not_run"},
        "trustedLocalAdapterRunEvidence": {"adapterExecution": "not_run"},
    }


def write_codex_result(
    static_repositories: list[dict],
    *,
    completed: int,
    schema_valid: int,
    repository_specific: int,
) -> dict:
    repositories = []
    for index, item in enumerate(static_repositories):
        repositories.append(
            {
                "id": item.get("id") or f"repo-{index:02d}",
                "status": "completed" if index < completed else "failed",
                "schemaValid": index < schema_valid,
                "repositorySpecific": index < repository_specific,
                "unsupportedClaimCount": 0,
                "failure": None,
                "proposal": {
                    "provider": {
                        "kind": "codex_exec_external_model_output",
                        "name": "codex",
                        "model": "gpt-5.3-codex-spark",
                        "execution": "external_schema_validated",
                    },
                    "diagnostics": [],
                },
                "receipt": {
                    "model": "gpt-5.3-codex-spark",
                },
            }
        )
    return {
        "status": "completed" if completed == len(static_repositories) else "failed",
        "provider": {
            "kind": "codex_exec_external_model_output",
            "model": "gpt-5.3-codex-spark",
        },
        "repositories": repositories,
        "privacy": {},
        "authority": "proposal_only_not_registry_acceptance",
    }


def write_inputs(path: Path) -> tuple[Path, Path, list[dict[str, str]]]:
    inputs = path / "inputs"
    checkouts = inputs / "checkouts"
    manifest = ["repositories:"]
    for index in range(50):
        repository_id = f"repo-{index:02d}"
        revision = f"{index:040x}"
        manifest.extend(
            [
                f"  - id: {repository_id}",
                f"    repository: https://github.com/example/{repository_id}",
                f"    revision: {revision}",
                f"    checkout: checkouts/{repository_id}",
            ]
        )
        (checkouts / repository_id).mkdir(parents=True)
    inputs.mkdir(parents=True, exist_ok=True)
    manifest_path = inputs / "repositories.yml"
    manifest_path.write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return inputs, manifest_path, manifest_records(inputs)


def manifest_records(inputs: Path) -> list[dict[str, str]]:
    return [
        {
            "id": f"repo-{index:02d}",
            "repository": f"https://github.com/example/repo-{index:02d}",
            "revision": f"{index:040x}",
        }
        for index in range(50)
    ]
