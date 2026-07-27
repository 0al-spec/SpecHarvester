from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MASS_CAMPAIGN_CHECKPOINT_API_VERSION = "spec-harvester.mass-campaign-checkpoint/v0"
MASS_CAMPAIGN_CHECKPOINT_KIND = "SpecHarvesterMassCampaignCheckpoint"
ALLOWED_STATES = frozenset(
    {"pending", "running", "completed", "retryable_failed", "terminal_failed"}
)
RETRYABLE_OUTCOMES = frozenset({"transport_failure", "timeout", "schema_repairable_failure"})


@dataclass(frozen=True)
class CampaignRepositoryInput:
    repository_id: str
    input_digest: str
    wave_id: str


def build_campaign_checkpoint(
    campaign_plan: dict[str, Any], sources: tuple[CampaignRepositoryInput, ...]
) -> dict[str, Any]:
    _validate_plan(campaign_plan)
    ordered = sorted(sources, key=lambda source: source.repository_id)
    if not ordered or len({source.repository_id for source in ordered}) != len(ordered):
        raise ValueError("P53-T2 requires unique non-empty repository inputs")
    if any(not source.repository_id or len(source.input_digest) != 64 for source in ordered):
        raise ValueError("P53-T2 requires 64-char immutable input digests")
    run_id = _digest({"plan": campaign_plan, "sources": [source.__dict__ for source in ordered]})
    return {
        "apiVersion": MASS_CAMPAIGN_CHECKPOINT_API_VERSION,
        "kind": MASS_CAMPAIGN_CHECKPOINT_KIND,
        "runId": f"sha256:{run_id}",
        "planDigest": f"sha256:{_digest(campaign_plan)}",
        "worker": campaign_plan["worker"],
        "budgetPolicy": campaign_plan["budgetPolicy"],
        "stopPolicy": campaign_plan["stopPolicy"],
        "repositories": [
            {
                "id": source.repository_id,
                "inputDigest": source.input_digest,
                "wave": source.wave_id,
                "state": "pending",
                "attemptCount": 0,
                "reservedTokens": 0,
                "reservedWallTimeSeconds": 0,
                "tokenUsed": 0,
                "wallTimeSeconds": 0,
            }
            for source in ordered
        ],
        "failureStreak": 0,
        "stop": None,
        "unlockedWave": "wave-1",
    }


def reserve_dispatch(checkpoint: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    _validate_checkpoint(checkpoint)
    if checkpoint["stop"] is not None:
        return checkpoint, []
    policy = checkpoint["budgetPolicy"]
    if (
        _reserved_total(checkpoint, "tokenUsed", "reservedTokens") >= policy["campaignMaxTokens"]
        or _reserved_total(checkpoint, "wallTimeSeconds", "reservedWallTimeSeconds")
        >= policy["campaignMaxWallTimeSeconds"]
    ):
        return _stop(checkpoint, "campaign_budget_limit"), []
    available = 2 - sum(record["state"] == "running" for record in checkpoint["repositories"])
    if available <= 0:
        return checkpoint, []
    updated = _copy(checkpoint)
    dispatched: list[str] = []
    for record in updated["repositories"]:
        if len(dispatched) == available:
            break
        if record["wave"] != updated["unlockedWave"]:
            continue
        if record["state"] == "pending" or (
            record["state"] == "retryable_failed" and record["attemptCount"] < 2
        ):
            if not _can_reserve(updated, record):
                return _stop(updated, "campaign_budget_limit"), dispatched
            record["state"] = "running"
            record["attemptCount"] += 1
            record["reservedTokens"] = policy["perRepositoryMaxTokens"]
            record["reservedWallTimeSeconds"] = policy["perRepositoryMaxWallTimeSeconds"]
            dispatched.append(record["id"])
    return updated, dispatched


def apply_repository_result(
    checkpoint: dict[str, Any],
    repository_id: str,
    *,
    outcome: str,
    token_used: int,
    wall_time_seconds: int,
    stop_trigger: str | None = None,
) -> dict[str, Any]:
    _validate_checkpoint(checkpoint)
    updated = _copy(checkpoint)
    record = next((item for item in updated["repositories"] if item["id"] == repository_id), None)
    if record is None or record["state"] != "running":
        raise ValueError("P53-T2 result must match one running repository")
    if token_used < 0 or wall_time_seconds < 0:
        raise ValueError("P53-T2 receipt values must be non-negative")
    record["tokenUsed"] += token_used
    record["wallTimeSeconds"] += wall_time_seconds
    record["reservedTokens"] = 0
    record["reservedWallTimeSeconds"] = 0
    if (
        record["tokenUsed"] > updated["budgetPolicy"]["perRepositoryMaxTokens"]
        or record["wallTimeSeconds"] > updated["budgetPolicy"]["perRepositoryMaxWallTimeSeconds"]
    ):
        stop_trigger = "campaign_budget_limit"
    record["state"] = (
        "completed"
        if outcome == "completed"
        else (
            "retryable_failed"
            if outcome in RETRYABLE_OUTCOMES and record["attemptCount"] < 2
            else "terminal_failed"
        )
    )
    updated["failureStreak"] = 0 if outcome == "completed" else updated["failureStreak"] + 1
    if updated["failureStreak"] >= 3:
        return _stop(updated, "consecutive_codex_schema_or_transport_failures")
    if stop_trigger is not None:
        return _stop(updated, stop_trigger)
    if _total(updated, "tokenUsed") >= updated["budgetPolicy"]["campaignMaxTokens"]:
        return _stop(updated, "campaign_budget_limit")
    if (
        _total_wave(updated, record["wave"], "tokenUsed")
        >= updated["budgetPolicy"]["perWaveMaxTokens"]
    ):
        return _stop(updated, "wave_budget_limit")
    return updated


def write_campaign_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    _validate_checkpoint(checkpoint)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_campaign_checkpoint(path: Path) -> dict[str, Any]:
    try:
        checkpoint = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"P53-T2 cannot read campaign checkpoint: {path}") from exc
    if not isinstance(checkpoint, dict):
        raise ValueError("P53-T2 checkpoint must be a JSON object")
    _validate_checkpoint(checkpoint)
    return checkpoint


def stop_campaign(checkpoint: dict[str, Any], trigger: str) -> dict[str, Any]:
    """Persist a non-retryable campaign gate after aggregate evaluation."""
    _validate_checkpoint(checkpoint)
    return _stop(checkpoint, trigger)


def recover_interrupted_reservations(checkpoint: dict[str, Any]) -> dict[str, Any]:
    """Release persisted reservations after the caller confirms interruption."""
    _validate_checkpoint(checkpoint)
    updated = _copy(checkpoint)
    for record in updated["repositories"]:
        if record["state"] == "running":
            record["state"] = "pending" if record["attemptCount"] == 1 else "retryable_failed"
            record["reservedTokens"] = 0
            record["reservedWallTimeSeconds"] = 0
    return updated


def record_scale_out_decision(checkpoint: dict[str, Any], decision_task: str) -> dict[str, Any]:
    _validate_checkpoint(checkpoint)
    waves = {"P53-T7": "wave-2", "P53-T9": "wave-3", "P53-T11": "wave-4"}
    if decision_task not in waves:
        raise ValueError("P53-T2 received an unknown scale-out decision")
    updated = _copy(checkpoint)
    current = updated["unlockedWave"]
    if any(
        record["wave"] == current and record["state"] not in {"completed", "terminal_failed"}
        for record in updated["repositories"]
    ):
        raise ValueError("P53-T2 cannot unlock a later wave before the current wave finishes")
    updated["unlockedWave"] = waves[decision_task]
    return updated


def _validate_plan(plan: dict[str, Any]) -> None:
    if plan.get("task") != "P53-T1" or plan.get("worker", {}).get("model") != "gpt-5.3-codex-spark":
        raise ValueError("P53-T2 requires the P53-T1 Codex 5.3 Spark campaign plan")
    if (
        plan["worker"].get("lmStudioAllowed") is not False
        or plan["worker"].get("alternateAIWorkersAllowed") is not False
    ):
        raise ValueError("P53-T2 permits only the sole Codex 5.3 Spark worker")


def _validate_checkpoint(checkpoint: dict[str, Any]) -> None:
    if checkpoint.get("apiVersion") != MASS_CAMPAIGN_CHECKPOINT_API_VERSION:
        raise ValueError("P53-T2 checkpoint apiVersion mismatch")
    if any(
        record.get("state") not in ALLOWED_STATES for record in checkpoint.get("repositories", [])
    ):
        raise ValueError("P53-T2 checkpoint contains an invalid repository state")


def _can_reserve(checkpoint: dict[str, Any], record: dict[str, Any]) -> bool:
    policy = checkpoint["budgetPolicy"]
    return (
        _reserved_total(checkpoint, "tokenUsed", "reservedTokens")
        + policy["perRepositoryMaxTokens"]
        <= policy["campaignMaxTokens"]
        and _reserved_total(checkpoint, "wallTimeSeconds", "reservedWallTimeSeconds")
        + policy["perRepositoryMaxWallTimeSeconds"]
        <= policy["campaignMaxWallTimeSeconds"]
        and _reserved_total(checkpoint, "tokenUsed", "reservedTokens", record["wave"])
        + policy["perRepositoryMaxTokens"]
        <= policy["perWaveMaxTokens"]
    )


def _stop(checkpoint: dict[str, Any], trigger: str) -> dict[str, Any]:
    updated = _copy(checkpoint)
    updated["stop"] = {
        "trigger": trigger,
        "outcome": "stop_current_wave_and_block_later_waves",
    }
    return updated


def _copy(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value))


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _total(checkpoint: dict[str, Any], key: str) -> int:
    return sum(record[key] for record in checkpoint["repositories"])


def _reserved_total(
    checkpoint: dict[str, Any], used_key: str, reserved_key: str, wave: str | None = None
) -> int:
    return sum(
        record[used_key] + record[reserved_key]
        for record in checkpoint["repositories"]
        if wave is None or record["wave"] == wave
    )


def _total_wave(checkpoint: dict[str, Any], wave: str, key: str) -> int:
    return sum(record[key] for record in checkpoint["repositories"] if record["wave"] == wave)
