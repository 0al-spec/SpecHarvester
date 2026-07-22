from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from spec_harvester.autonomous_candidate_batch import AutonomousCandidateBatchOptions
from spec_harvester.twenty_repository_controlled_pilot import (
    PILOT_REPOSITORY_COUNT,
    TWENTY_REPOSITORY_CONTROLLED_PILOT_REPORT_FILENAME,
    TwentyRepositoryControlledPilot,
    TwentyRepositoryControlledPilotOptions,
)


def test_static_baseline_runs_before_models_when_provider_logging_is_unconfirmed(
    tmp_path: Path,
) -> None:
    inputs, revisions = write_pilot_inputs(tmp_path)
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

    options = TwentyRepositoryControlledPilotOptions(
        inputs=inputs,
        out=tmp_path / "out",
        lm_studio_model="test-model",
    )
    pilot = TwentyRepositoryControlledPilot(
        options,
        batch_runner=batch_runner,
        checkout_head_reader=lambda checkout: revisions[checkout.name],
        checkout_dirty_reader=lambda _checkout: "",
    )

    report = pilot.run()

    assert len(calls) == 1
    assert calls[0].skip_ai is True
    assert calls[0].out == options.out / "static-only"
    assert report["status"] == "blocked"
    assert report["lmStudio"]["reason"] == "provider_logging_not_confirmed_disabled"
    assert report["codexSpark"]["reason"] == "provider_logging_not_confirmed_disabled"
    assert report["concurrency"]["configured"] == 1
    assert report["decision"] == {
        "status": "blocked",
        "selectedDecision": "blocked_provider_logging_precondition",
        "p52T5Unlocked": False,
    }
    persisted = json.loads(
        (options.out / TWENTY_REPOSITORY_CONTROLLED_PILOT_REPORT_FILENAME).read_text(
            encoding="utf-8"
        )
    )
    assert persisted == report


def test_sources_require_twenty_clean_public_checkouts(tmp_path: Path) -> None:
    inputs, revisions = write_pilot_inputs(tmp_path)
    pilot = TwentyRepositoryControlledPilot(
        TwentyRepositoryControlledPilotOptions(
            inputs=inputs,
            out=tmp_path / "out",
            run_lm_studio=False,
            run_codex=False,
        ),
        checkout_head_reader=lambda checkout: revisions[checkout.name],
        checkout_dirty_reader=lambda _checkout: "?? untracked.txt\n",
    )

    with pytest.raises(ValueError, match="checkout must be clean"):
        pilot.sources()

    assert PILOT_REPOSITORY_COUNT == 20


def test_sources_reject_non_public_repository_url(tmp_path: Path) -> None:
    inputs, revisions = write_pilot_inputs(tmp_path, repository="https://example.test/private/repo")
    pilot = TwentyRepositoryControlledPilot(
        TwentyRepositoryControlledPilotOptions(
            inputs=inputs,
            out=tmp_path / "out",
            run_lm_studio=False,
            run_codex=False,
        ),
        checkout_head_reader=lambda checkout: revisions[checkout.name],
        checkout_dirty_reader=lambda _checkout: "",
    )

    with pytest.raises(ValueError, match="public GitHub URL"):
        pilot.sources()


def test_pilot_rejects_parallelism_until_a_bounded_parallel_runner_exists(tmp_path: Path) -> None:
    pilot = TwentyRepositoryControlledPilot(
        TwentyRepositoryControlledPilotOptions(
            inputs=tmp_path / "inputs",
            out=tmp_path / "out",
            max_concurrency=2,
            run_lm_studio=False,
            run_codex=False,
        )
    )

    with pytest.raises(ValueError, match="--max-concurrency 1"):
        pilot.validate_pilot_options()


def write_pilot_inputs(
    tmp_path: Path,
    *,
    repository: str = "https://github.com/example/repository",
) -> tuple[Path, dict[str, str]]:
    inputs = tmp_path / "inputs"
    checkouts = inputs / "checkouts"
    revisions = {f"repository-{index:02d}": f"revision-{index:02d}" for index in range(20)}
    entries = []
    for repository_id, revision in revisions.items():
        (checkouts / repository_id).mkdir(parents=True)
        entries.extend(
            (
                f"  - id: {repository_id}",
                f"    repository: {repository}",
                f"    revision: {revision}",
                f"    checkout: checkouts/{repository_id}",
            )
        )
    inputs.mkdir(exist_ok=True)
    (inputs / "repositories.yml").write_text(
        "repositories:\n" + "\n".join(entries) + "\n",
        encoding="utf-8",
    )
    return inputs, revisions
