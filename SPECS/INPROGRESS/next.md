# Next Task: P47-T1 Targeted Pilot Quality Follow-Up Plan

**Status:** Selected
**Branch:** `feature/P47-T1-targeted-pilot-quality-follow-up-plan`
**Phase:** Phase 47. Targeted Pilot Quality Follow-Up
**Task:** `P47-T1`
**Last Archived:** `P46-T6` Bounded Popular-Library Pilot Exit Decision
**Depends On:** `P46-T6` Bounded Popular-Library Pilot Exit Decision

## Goal

Plan the targeted pilot quality follow-up selected by P46-T6 before any larger
curated corpus expansion.

## Context

Phase 46 is complete. P46-T6 selected
`run_targeted_quality_pass_before_larger_curated_corpus`: the bounded pilot
produced reviewable static evidence across all six pilot repositories, but a
larger curated corpus is not approved yet.

## Carry-Forward Signals

Keep do-not-promote AI sidecars visible:

- `gin.aiDraft`
- `docc2context.aiDraft`

Keep xyflow caveats visible:

- `partial_public_interface_index`
- `operator_checkout_origin_fork_mismatch`
- `model_evidence_path_unsupported`

These signals mean the next work is Phase 47 Targeted Pilot Quality Follow-Up
Planning, not immediate larger curated corpus execution.

## Expected Deliverables

- Phase 47 targeted quality follow-up plan.
- Explicit repair or disposition path for Gin and docc2context AI draft
  blockers.
- Explicit disposition path for xyflow evidence-gap and unsupported enrichment
  caveats.
- bounded rerun gate before any larger curated corpus approval.
- Validation report and archive artifacts for P47-T1.

## Completed Phase 46 Tasks

- `P46-T1` Bounded Popular-Library Pilot Manifest: PASS on 2026-06-20.
- `P46-T2` Bounded Popular-Library Pilot Static-Only Run: PASS on 2026-06-20.
- `P46-T3` Bounded Popular-Library Pilot AI-Enabled Run: PASS as evidence
  capture on 2026-06-20.
- `P46-T4` Bounded Popular-Library Pilot Output Triage: PASS on 2026-06-20.
- `P46-T5` Bounded Popular-Library Pilot Author Handoff Summaries: PASS on
  2026-06-20.
- `P46-T6` Bounded Popular-Library Pilot Exit Decision: PASS on 2026-06-20.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat handoff output as registry truth.
- Do not treat exit-decision output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P47-T1 plan and current next task.
- Run formatting/lint/whitespace checks scaled to touched files.
