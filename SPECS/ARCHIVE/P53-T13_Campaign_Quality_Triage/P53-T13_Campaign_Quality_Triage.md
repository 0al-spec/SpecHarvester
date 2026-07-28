# P53-T13 Campaign Quality Triage

**Task:** `P53-T13`
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Status:** In progress
**Worker boundary:** `gpt-5.3-codex-spark` through `codex exec`

## Objective

Produce one deterministic, machine-readable campaign triage that accounts for
all 100 frozen Phase 53 repositories exactly once and reconciles static,
proposal, retry, failure, budget, privacy, and stop-policy evidence from the
four bounded Codex Spark waves.

## Dependencies

- P53-T1 campaign plan and quality thresholds.
- P53-T3 frozen source metadata and wave assignments.
- P53-T5 static-only gate.
- P53-T6, P53-T8, P53-T10, and P53-T12 wave reports.
- A bounded `bitcoin-bitcoin` corrective record with proposal, static evidence,
  and receipt bound by SHA-256.

## Deliverables

1. A `p53-campaign-quality-triage` command and reusable Python builder.
2. Strict source/report validation for exactly four expected tasks, waves, and
   immutable source ranges.
3. Deterministic per-repository disposition into:
   `selected_for_author_review`, `deferred`, or `do_not_promote`.
4. Aggregate static and Codex completion, schema-valid, repository-specific,
   unsupported-claim, retry, terminal-failure, token reservation, duration,
   privacy, authority, and stop-policy summaries.
5. Durable sanitized wave-1 and wave-4 evidence restoration because their
   original `/tmp` roots are no longer present.
6. A committed example triage artifact and validation report suitable as the
   sole P53-T14 input.

## Classification Rules

- Select only completed, schema-valid, repository-specific proposals with zero
  unsupported claims and a completed or warning-only proposal artifact.
- Defer retryable transport, timeout, or schema-repairable outcomes and
  completed records whose proposal evidence is incomplete but not unsupported.
- Mark terminal failures, schema-invalid records, unsupported claims, source
  drift, authority violations, or privacy violations as do-not-promote.
- Apply a corrective replacement only when its repository identity and
  supporting artifact digests are explicit; preserve the original outcome in
  the audit record.

## Acceptance Criteria

- Exactly 100 unique frozen source IDs are present, in positions 1-100 and in
  their assigned waves.
- Each wave report is `passed`, names the expected P53 task, contains exactly
  25 expected sources, and preserves proposal-only/privacy boundaries.
- Every source has exactly one effective disposition and one source-wave
  outcome.
- Aggregate metrics and thresholds are computed from effective outcomes rather
  than copied from Markdown summaries.
- Every input artifact has a SHA-256 digest in the triage.
- Missing, duplicate, mismatched, malformed, or policy-violating evidence
  causes a hard failure.
- No package or relation is accepted, no registry truth is changed, and raw
  prompts, responses, secrets, or chain-of-thought are not persisted.
- Project tests, Ruff, format check, Swift manifest/docs gates, and coverage at
  or above 90% pass.

## Non-Goals

- SpecPM intake or registry promotion.
- Automatic maintainer disposition.
- Expanding beyond the frozen 100-repository corpus.
- Increasing concurrency or changing the model/provider.
- Reclassifying unsupported evidence by editorial judgment.

---
**Archived:** 2026-07-28
**Verdict:** PASS
