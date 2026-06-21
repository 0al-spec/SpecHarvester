# P47-T4 Record Targeted Quality Follow-Up Exit Decision

Status: Planned
Phase: Phase 47. Targeted Pilot Quality Follow-Up
Task: P47-T4
Branch: `feature/P47-T4-record-targeted-quality-follow-up-exit-decision`
Depends on: P47-T3 Run Bounded Pilot Rerun Gate

## Problem

P47-T3 executed the bounded rerun gate over the same six-repository pilot. The
static-only gate passed, but the AI-enabled gate failed because `gin.aiDraft`
and `navigation-split-view.aiDraft` failed after one JSON repair attempt.

Phase 47 still needs a durable exit decision. The decision must explicitly say
whether larger curated corpus planning can proceed, whether another targeted
quality pass is required, or whether expansion stops on a documented blocker.

## Goal

Record a machine-readable and documented targeted quality follow-up exit
decision that preserves proposal-only authority and keeps larger curated corpus
planning blocked unless the P47-T3 evidence supports readiness.

## Deliverables

- Machine-readable P47-T4 exit decision fixture under
  `tests/fixtures/targeted_pilot_quality_follow_up_exit_decision/`.
- GitHub Markdown and DocC documentation explaining the selected decision,
  rejected alternatives, evidence inputs, and next workplan direction.
- Docs-contract coverage for decision identity, P47-T3 source artifact linkage,
  selected and rejected decision options, blocker treatment, no-authority
  boundaries, Workplan extension, and current next-task pointer.
- Workplan and `SPECS/INPROGRESS/next.md` updates reflecting the selected next
  path.
- Validation report and archive artifacts for P47-T4.

## Acceptance Criteria

- The decision references the P47-T3 bounded rerun gate fixture by digest.
- The selected path is explicit and one of:
  `proceed_to_larger_curated_corpus_planning`,
  `run_another_targeted_quality_pass_before_larger_curated_corpus`, or
  `stop_on_documented_blocker`.
- The decision records that the P47-T3 static-only gate passed and the
  AI-enabled gate failed.
- The decision keeps `gin.aiDraft` and `navigation-split-view.aiDraft` as
  blocking AI draft sidecars.
- The decision records `docc2context.aiDraft` as a repaired non-blocking
  warning.
- The decision keeps xyflow `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and `ai_json_repair_needed`
  caveats visible.
- P47-T4 does not accept packages or relations, publish registry metadata,
  seed baselines, remove `preview_only`, rerun the pilot, run AI, run adapters,
  install dependencies, invoke harvested package managers, execute harvested
  code, or treat any output as registry truth.
- P47-T4 updates `SPECS/INPROGRESS/next.md` after archival to show the selected
  follow-up task.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers inside harvested repositories.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not approve a larger curated corpus while the P47-T3 failed AI-enabled
  gate remains the controlling result.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat exit-decision output, bounded rerun gate output, static output,
  AI output, or adapter output as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P47-T4 exit decision and current next
  task.
- Run lint, format, coverage, Swift manifest, Swift docs build, and whitespace
  checks as required by Flow.

---

**Archived:** 2026-06-21
**Verdict:** PASS
