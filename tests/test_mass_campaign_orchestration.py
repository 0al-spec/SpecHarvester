from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.mass_campaign_orchestration import (
    CampaignRepositoryInput,
    apply_repository_result,
    build_campaign_checkpoint,
    reserve_dispatch,
    write_campaign_checkpoint,
)


def plan() -> dict:
    return json.loads(
        Path(
            "tests/fixtures/mass_repository_campaign_plan/"
            "p53-t1-mass-repository-campaign-plan.example.json"
        ).read_text(encoding="utf-8")
    )


def sources() -> tuple[CampaignRepositoryInput, ...]:
    return (
        CampaignRepositoryInput("alpha", "a" * 64, "wave-1"),
        CampaignRepositoryInput("beta", "b" * 64, "wave-1"),
        CampaignRepositoryInput("gamma", "c" * 64, "wave-2"),
    )


def test_checkpoint_identity_is_stable_and_dispatch_is_idempotent() -> None:
    checkpoint = build_campaign_checkpoint(plan(), sources())
    same = build_campaign_checkpoint(plan(), tuple(reversed(sources())))

    assert checkpoint["runId"] == same["runId"]
    reserved, dispatched = reserve_dispatch(checkpoint)
    assert dispatched == ["alpha", "beta"]
    again, repeated = reserve_dispatch(reserved)
    assert repeated == []
    assert again == reserved


def test_resume_skips_completed_and_allows_one_classified_retry() -> None:
    checkpoint, dispatched = reserve_dispatch(build_campaign_checkpoint(plan(), sources()))
    checkpoint = apply_repository_result(
        checkpoint, dispatched[0], outcome="completed", token_used=10, wall_time_seconds=1
    )
    checkpoint = apply_repository_result(
        checkpoint, dispatched[1], outcome="transport_failure", token_used=10, wall_time_seconds=1
    )

    resumed, dispatched = reserve_dispatch(checkpoint)
    assert dispatched == ["beta", "gamma"]
    checkpoint = apply_repository_result(
        resumed, "beta", outcome="transport_failure", token_used=10, wall_time_seconds=1
    )
    _resumed, dispatched = reserve_dispatch(checkpoint)
    assert dispatched == []


@pytest.mark.parametrize(
    "trigger",
    [
        "quality_threshold_failure",
        "consecutive_codex_schema_or_transport_failures",
        "input_revision_or_digest_drift",
        "authority_boundary_breach",
    ],
)
def test_stop_trigger_blocks_later_wave_dispatch(trigger: str) -> None:
    checkpoint, dispatched = reserve_dispatch(build_campaign_checkpoint(plan(), sources()))
    stopped = apply_repository_result(
        checkpoint,
        dispatched[0],
        outcome="terminal_failure",
        token_used=1,
        wall_time_seconds=1,
        stop_trigger=trigger,
    )
    assert stopped["stop"]["trigger"] == trigger
    assert reserve_dispatch(stopped)[1] == []


def test_budget_limit_stops_campaign_and_checkpoint_write_is_atomic(tmp_path: Path) -> None:
    campaign_plan = plan()
    campaign_plan["budgetPolicy"]["campaignMaxTokens"] = 10
    checkpoint, dispatched = reserve_dispatch(build_campaign_checkpoint(campaign_plan, sources()))
    stopped = apply_repository_result(
        checkpoint, dispatched[0], outcome="completed", token_used=10, wall_time_seconds=1
    )
    assert stopped["stop"]["trigger"] == "campaign_budget_limit"
    output = tmp_path / "checkpoint.json"
    write_campaign_checkpoint(output, stopped)
    assert json.loads(output.read_text(encoding="utf-8")) == stopped


def test_cumulative_per_repository_budget_stops_campaign() -> None:
    campaign_plan = plan()
    campaign_plan["budgetPolicy"]["perRepositoryMaxTokens"] = 10
    checkpoint, dispatched = reserve_dispatch(build_campaign_checkpoint(campaign_plan, sources()))
    checkpoint = apply_repository_result(
        checkpoint, dispatched[0], outcome="transport_failure", token_used=6, wall_time_seconds=1
    )
    checkpoint, dispatched = reserve_dispatch(checkpoint)
    stopped = apply_repository_result(
        checkpoint, dispatched[0], outcome="completed", token_used=5, wall_time_seconds=1
    )
    assert stopped["stop"]["trigger"] == "campaign_budget_limit"
