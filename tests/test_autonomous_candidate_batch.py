from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.autonomous_candidate_batch import (
    AUTONOMOUS_CANDIDATE_BATCH_API_VERSION,
    AUTONOMOUS_CANDIDATE_BATCH_KIND,
    AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME,
    AutonomousCandidateBatch,
    AutonomousCandidateBatchOptions,
    run_autonomous_candidate_batch,
)
from spec_harvester.cli import main


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
    assert report["summary"]["processedCount"] == 1
    assert report["summary"]["passedPreflightCount"] == 1
    repository = report["repositories"][0]
    assert repository["status"] == "passed"
    assert repository["packageSetDraft"]["candidateCount"] == 3
    assert repository["packageSetDraft"]["relationCount"] == 2
    assert repository["preflight"]["status"] == "passed"
    assert repository["aiDraft"]["status"] == "skipped"
    assert repository["aiEnrichment"]["status"] == "skipped"
    assert repository["authorReadyDraftSummary"]["decision"] == "stop_for_author_review"

    saved = json.loads(
        (output / AUTONOMOUS_CANDIDATE_BATCH_REPORT_FILENAME).read_text(encoding="utf-8")
    )
    assert saved["status"] == "passed"
    assert (output / "collected" / "demo" / "workspace-inventory.json").is_file()
    assert (output / "package-sets" / "demo" / "package-set-draft.json").is_file()
    assert (output / "package-sets" / "demo" / "bundle-set-preflight.json").is_file()


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
        ]
    )

    assert exit_code == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["status"] == "passed"
    assert printed["collection"]["validationReport"].endswith("batch-validation-report.json")
    assert printed["repositories"][0]["preflight"]["status"] == "passed"


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
