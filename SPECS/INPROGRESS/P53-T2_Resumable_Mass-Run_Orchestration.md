# P53-T2 Resumable Mass-Run Orchestration

## Objective

Implement a deterministic, no-execution orchestration layer that consumes the
P53-T1 campaign contract and governs future `gpt-5.3-codex-spark` work. It
must construct atomic checkpoints, resume without duplicate dispatch, apply
classified retry rules, enforce concurrency and budget limits, and stop later
waves on every machine-readable trigger.

## Acceptance Criteria

- Checkpoint identity is a stable digest of the P53-T1 plan and immutable
  repository input identities.
- Checkpoint records use only the permitted states and completed or terminal
  records are never dispatched again.
- Retryable failure may dispatch exactly once more; other failures become
  terminal.
- Dispatch cannot exceed two concurrent records, per-repository/per-wave/
  campaign token and wall-time limits, or a stopped campaign.
- A stop trigger creates a bounded diagnostic result and blocks later waves.
- Tests cover interruption/resume, duplicate dispatch prevention, retry limit,
  each stop trigger, and atomic checkpoint write behavior.

## Plan

1. Add failing unit tests for deterministic identity and dispatch decisions.
2. Add a small orchestration module with JSON checkpoint persistence only.
3. Add a fixture/documentation contract and run Python, Ruff, and Swift gates.

## Constraints

No repository checkout, static collection, Codex/LM Studio invocation, adapter,
package manager, harvested code, package/relation acceptance, or registry
mutation is permitted by this task.
