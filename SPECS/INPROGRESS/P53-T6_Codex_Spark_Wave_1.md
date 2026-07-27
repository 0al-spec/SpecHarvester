# P53-T6 Codex Spark Wave 1

**Status:** Planned
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Task:** `P53-T6`
**Depends On:** `P53-T5` Mass Corpus Static-Only Gate

## Objective

Execute only positions 1-25 of the immutable P53 corpus through Codex 5.3
Spark. Produce schema-validated package-set draft proposals and sanitized
receipts under the P53 checkpoint, budget, retry, and stop-policy contract.

## Deliverables

- A P53 wave runner that selects exactly wave 1 from the committed manifest.
- Atomic checkpoint persistence and idempotent resume using P53-T2 state rules.
- At-most-two concurrent read-only `codex exec` invocations.
- Per-repository result receipts, aggregate quality metrics, and a sanitized
  wave report.
- A live wave-1 evidence run only after deterministic contract tests pass.

## Acceptance Criteria

- Only the first 25 immutable sources are eligible; later waves are never
  dispatched.
- Every selected checkout is clean and matches its pinned revision before static
  evidence or Codex input is prepared.
- Each final Codex message is validated against the external-model output schema.
- Resume does not redispatch completed entries; only classified retryable
  failures receive one additional attempt.
- Concurrency, token, wall-time, and campaign/wave limits are enforced through
  the P53-T2 checkpoint and stop policy.
- Output remains proposal-only. No source mutation, package/relation acceptance,
  registry publication, raw prompt/response, secret, session state, stdout,
  stderr, or chain-of-thought persistence is permitted.

## Implementation Plan

1. Add deterministic tests for wave selection, checkpoint dispatch/resume,
   receipt classification, and the read-only Codex invocation contract.
2. Implement the wave runner around existing static drafting, compact evidence
   staging, JSON Schema validation, and P53-T2 checkpoint functions.
3. Run a bounded live wave only after the static and contract gates pass; retain
   sanitized metrics and final proposals, never raw model material.
