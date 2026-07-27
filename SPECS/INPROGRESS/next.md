# Next Task: P53-T2 Resumable Mass-Run Orchestration

**Status:** Selected
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Depends On:** `P53-T1` Mass Corpus Operating Plan
**Started:** 2026-07-27
**Active Task:** `P53-T2` Implement and validate the resumable mass-run
orchestration contract.
**Branch:** feature/p53-t2-resumable-mass-run-orchestration

## Objective

Implement the campaign runner contract for deterministic run identity,
per-repository state, two-worker bounded concurrency, atomic checkpoints,
idempotent resume, classified retries, token/time receipts, and aggregate
budget enforcement. It must enforce the P53-T1 `gpt-5.3-codex-spark` worker
policy but must not select sources or invoke a live model.

## Preconditions

- P53-T1 is archived with its 100-source, four-wave campaign contract.
- The sole future campaign worker is `gpt-5.3-codex-spark` through the
  schema-validated `codex exec` external-model-output boundary.
- P53-T2 does not acquire repositories, run static parsing, invoke Codex or LM
  Studio, execute adapters/package managers/harvested code, or mutate registry
  truth.

## Recently Archived

- `P53-T1` Mass Corpus Operating Plan: PASS. No review follow-up was needed.
