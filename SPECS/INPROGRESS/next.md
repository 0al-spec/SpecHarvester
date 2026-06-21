# Next Task: P48-T1 Plan AI Draft Blocker Follow-Up Pass

**Status:** Selected
**Branch:** `feature/P48-T1-plan-ai-draft-blocker-follow-up-pass`
**Phase:** Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
**Task:** `P48-T1`
**Last Archived:** `P47-T4` Record Targeted Quality Follow-Up Exit Decision
**Depends On:** `P47-T4` Record Targeted Quality Follow-Up Exit Decision

## Goal

Plan the next targeted AI draft blocker follow-up pass selected by P47-T4,
without expanding beyond the same six-repository bounded pilot scope.

## Context

P47-T4 selected
`run_another_targeted_quality_pass_before_larger_curated_corpus`. The P47-T3
static-only gate passed, but the AI-enabled gate failed because `gin.aiDraft`
and `navigation-split-view.aiDraft` exhausted JSON repair with
`package_set_subject_metadata_missing`.

`docc2context.aiDraft` improved to a repaired warning. `xyflow` did not repeat
`model_evidence_path_unsupported`, but still carries partial interface,
operator checkout origin, and `ai_json_repair_needed` caveats. The larger
curated corpus remains blocked until Phase 48 plans, executes, reruns, and
reviews the blocker follow-up.

## Scope

- Read the P47-T4 exit decision fixture and documentation.
- Define the P48 targeted blocker follow-up plan for:
  - `gin.aiDraft`
  - `navigation-split-view.aiDraft`
  - `docc2context.aiDraft`
  - `xyflow`
- Keep the same six-repository bounded pilot scope for any future rerun gate.
- Preserve proposal-only AI output and registry authority boundaries.

## Expected Deliverables

- P48-T1 blocker follow-up plan fixture or documentation.
- Explicit target list and success criteria for P48-T2.
- Boundaries for P48-T2 and P48-T3, including static-only-before-AI ordering
  and no registry mutation.
- Validation report and archive artifacts for P48-T1.

## Boundaries

- Do not approve a larger curated corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not expand beyond the same six-repository bounded pilot scope.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat plan output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P48-T1 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
