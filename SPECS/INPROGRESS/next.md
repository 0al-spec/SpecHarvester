# Next Task: P47-T3 Run Bounded Pilot Rerun Gate

**Status:** Selected
**Branch:** `feature/P47-T3-run-bounded-pilot-rerun-gate`
**Phase:** Phase 47. Targeted Pilot Quality Follow-Up
**Task:** `P47-T3`
**Last Archived:** `P47-T2` Execute Targeted Pilot Quality Pass
**Depends On:** `P47-T2` Execute Targeted Pilot Quality Pass

## Goal

Run the bounded pilot rerun gate after the P47-T2 explicit dispositions while
preserving static-only-before-AI ordering, proposal-only AI output, and the
same six-repository bounded pilot scope.

## Context

P47-T2 explicitly excluded the current `gin.aiDraft`,
`docc2context.aiDraft`, and `xyflow.aiEnrichment` sidecars from bounded-rerun
promotion, accepted the current xyflow caveats only for the bounded rerun gate,
and kept larger curated corpus approval blocked.

P47-T3 is the gate that proves the targeted dispositions are sufficient for
another bounded pilot pass before P47-T4 records an exit decision.

## Scope

- Use the same six-repository bounded pilot scope from P46.
- Use `inputs/p46-bounded-popular-library-pilot/repositories.yml`.
- Verify pinned local checkouts without expanding the corpus.
- Run static-only evidence before AI-enabled evidence.
- Keep AI-enabled output proposal-only.
- Keep excluded current sidecars out of promotion:
  - `gin.aiDraft`
  - `docc2context.aiDraft`
  - `xyflow.aiEnrichment`
- Record new or remaining caveats from the rerun.

## Expected Deliverables

- Bounded rerun gate evidence for the same six repositories.
- Static-only-before-AI result ordering evidence.
- Proposal-only AI output evidence.
- Durable fixture and documentation showing new pass/fail state, remaining
  sidecar warnings, and remaining caveats.
- Validation report and archive artifacts for P47-T3.

## Boundaries

- Do not approve a larger curated corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not expand the pilot scope beyond the same six-repository bounded pilot.
- Do not clone or fetch repositories unless the P47-T3 plan explicitly
  verifies already-pinned local checkout inputs.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat plan output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P47-T3 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
