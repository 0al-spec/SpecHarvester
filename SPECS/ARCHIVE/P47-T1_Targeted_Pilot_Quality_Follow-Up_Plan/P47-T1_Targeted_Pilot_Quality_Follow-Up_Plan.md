# P47-T1 Targeted Pilot Quality Follow-Up Plan

Status: Planned
Phase: Phase 47. Targeted Pilot Quality Follow-Up
Task: P47-T1
Branch: `feature/P47-T1-targeted-pilot-quality-follow-up-plan`
Depends on: P46-T6 Bounded Popular-Library Pilot Exit Decision

## Problem

P46-T6 selected `run_targeted_quality_pass_before_larger_curated_corpus`.
The bounded pilot produced reviewable static evidence, but larger curated
corpus expansion remains blocked by do-not-promote AI sidecars and unresolved
xyflow caveats. Phase 47 needs a concrete plan before any rerun or expansion.

## Goal

Record a targeted quality follow-up plan that preserves the P46 blockers,
defines repair and disposition paths, and gates any larger curated corpus on a
bounded rerun review.

## Deliverables

- Machine-readable P47-T1 quality follow-up plan fixture under
  `tests/fixtures/targeted_pilot_quality_follow_up_plan/`.
- GitHub Markdown and DocC documentation describing blockers, workstreams,
  bounded rerun gate, promotion boundaries, and exit criteria.
- Docs-contract coverage for plan identity, P46-T6 source artifact linkage,
  do-not-promote sidecar handling, xyflow caveat disposition, no-authority
  boundaries, and current next-task pointer.
- Validation report and archive artifacts for P47-T1.

## Acceptance Criteria

- The plan references the P46-T6 exit decision by digest.
- `gin.aiDraft` and `docc2context.aiDraft` remain visible as
  do-not-promote AI sidecars until regenerated or explicitly accepted as
  non-blocking.
- xyflow `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and
  `model_evidence_path_unsupported` remain visible until resolved or explicitly
  accepted.
- The bounded rerun gate must pass before any larger curated corpus approval.
- P47-T1 does not rerun the pilot, run AI, run adapters, clone or fetch
  repositories, execute harvested code, accept packages or relations, publish
  registry metadata, seed baselines, or remove `preview_only`.
- P47-T1 updates `SPECS/INPROGRESS/next.md` after archival to show the next
  Phase 47 execution task.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat plan output, exit-decision output, handoff output, static
  output, AI output, or adapter output as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P47-T1 quality follow-up plan and
  current next task.
- Run lint, format, coverage, Swift manifest, Swift docs build, and whitespace
  checks as required by Flow.

---
**Archived:** 2026-06-21
**Verdict:** PASS
