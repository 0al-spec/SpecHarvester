# P48-T1 Plan AI Draft Blocker Follow-Up Pass

Status: Planned
Phase: Phase 48. AI Draft Blocker Follow-Up Before Larger Corpus
Task: P48-T1
Branch: `feature/P48-T1-plan-ai-draft-blocker-follow-up-pass`
Depends on: P47-T4 Record Targeted Quality Follow-Up Exit Decision

## Problem

P47-T4 selected another targeted quality pass before larger curated corpus
planning. The P47-T3 static-only gate passed, but the AI-enabled gate failed on
`gin.aiDraft` and `navigation-split-view.aiDraft` with
`ai_json_repair_exhausted` and `package_set_subject_metadata_missing`.

Phase 48 needs a concrete plan before any execution task. The plan must define
the P48-T2 target sidecars, success criteria, evidence boundaries, and the
P48-T3 bounded rerun gate requirements.

## Goal

Record a machine-readable and documented AI draft blocker follow-up plan that
keeps larger curated corpus planning blocked and defines the next execution
task without running AI or mutating registry truth.

## Deliverables

- Machine-readable P48-T1 blocker follow-up plan fixture under
  `tests/fixtures/ai_draft_blocker_follow_up_plan/`.
- GitHub Markdown and DocC documentation for the P48-T1 plan.
- Docs-contract coverage for fixture identity, P47-T4 source artifact linkage,
  target sidecars, workstreams, P48-T2 success criteria, P48-T3 rerun gate
  boundaries, non-authority statements, and current next-task pointer.
- Validation report and archive artifacts for P48-T1.

## Acceptance Criteria

- The plan references the P47-T4 exit decision fixture by digest.
- The plan targets `gin.aiDraft` and `navigation-split-view.aiDraft` as
  blocking AI draft sidecars.
- The plan keeps `docc2context.aiDraft` and `xyflow.aiEnrichment` warnings
  visible without treating them as registry truth.
- The plan keeps xyflow `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and `ai_json_repair_needed`
  caveats visible for P48-T2 and P48-T3.
- The plan defines P48-T2 success criteria for clearing or explicitly
  disposing `ai_json_repair_exhausted` and
  `package_set_subject_metadata_missing`.
- The plan defines P48-T3 as the same six-repository bounded rerun gate with
  static-only-before-AI ordering.
- P48-T1 does not approve a larger curated corpus, run AI, rerun the pilot,
  clone or fetch repositories, execute harvested code, run adapters, accept
  packages or relations, publish registry metadata, seed baselines, remove
  `preview_only`, or treat plan output as registry truth.
- P48-T1 updates `SPECS/INPROGRESS/next.md` after archival to show P48-T2.

## Boundaries

- Do not approve a larger curated corpus.
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
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat plan output, exit-decision output, static output, AI output, or
  adapter output as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P48-T1 plan and current next task.
- Run lint, format, coverage, Swift manifest, Swift docs build, and whitespace
  checks as required by Flow.

---

**Archived:** 2026-06-21
**Verdict:** PASS
