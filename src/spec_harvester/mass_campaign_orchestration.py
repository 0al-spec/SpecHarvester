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
                "tokenUsed": 0,
                "wallTimeSeconds": 0,
            }
            for source in ordered
        ],
        "stop": None,
    }


def reserve_dispatch(checkpoint: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    _validate_checkpoint(checkpoint)
    if checkpoint["stop"] is not None:
        return checkpoint, []
    policy = checkpoint["budgetPolicy"]
    if (
        _total(checkpoint, "tokenUsed") >= policy["campaignMaxTokens"]
        or _total(checkpoint, "wallTimeSeconds") >= policy["campaignMaxWallTimeSeconds"]
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
        if record["state"] == "pending" or (
            record["state"] == "retryable_failed" and record["attemptCount"] < 2
        ):
            record["state"] = "running"
            record["attemptCount"] += 1
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
    if (
        token_used > updated["budgetPolicy"]["perRepositoryMaxTokens"]
        or wall_time_seconds > updated["budgetPolicy"]["perRepositoryMaxWallTimeSeconds"]
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
    if stop_trigger is not None:
        return _stop(updated, stop_trigger)
    if _total(updated, "tokenUsed") >= updated["budgetPolicy"]["campaignMaxTokens"]:
        return _stop(updated, "campaign_budget_limit")
    return updated


def write_campaign_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    _validate_checkpoint(checkpoint)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


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
