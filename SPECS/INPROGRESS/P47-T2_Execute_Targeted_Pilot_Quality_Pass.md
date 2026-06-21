# P47-T2 Execute Targeted Pilot Quality Pass

Status: Planned
Phase: Phase 47. Targeted Pilot Quality Follow-Up
Task: P47-T2
Branch: `feature/P47-T2-execute-targeted-pilot-quality-pass`
Depends on: P47-T1 Targeted Pilot Quality Follow-Up Plan

## Problem

P47-T1 planned the targeted quality follow-up, but the P46 blockers still need
explicit disposition before the bounded rerun gate can run. Without a durable
P47-T2 pass, `gin.aiDraft`, `docc2context.aiDraft`, `xyflow.aiEnrichment`, and
the xyflow caveats could either be forgotten or incorrectly treated as cleared
for larger corpus expansion.

## Goal

Record a targeted quality pass that explicitly disposes the current P46
blockers for the bounded rerun gate while keeping larger curated corpus
approval blocked until P47-T3 and P47-T4 complete.

## Deliverables

- Machine-readable P47-T2 targeted quality pass fixture under
  `tests/fixtures/targeted_pilot_quality_pass/`.
- GitHub Markdown and DocC documentation describing blocker dispositions,
  bounded rerun readiness, larger corpus gate state, and authority boundaries.
- Docs-contract coverage for source artifact linkage, blocker dispositions,
  current sidecar exclusions, xyflow caveat treatment, no-authority boundaries,
  and current next-task pointer.
- Validation report and archive artifacts for P47-T2.

## Acceptance Criteria

- The pass references the P47-T1 plan by digest.
- `gin.aiDraft` and `docc2context.aiDraft` current sidecars are explicitly
  excluded from promotion and treated as non-blocking for the bounded rerun
  gate, not as registry truth.
- `xyflow.aiEnrichment` is explicitly carried and excluded as the unsupported
  AI enrichment sidecar.
- xyflow `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and
  `model_evidence_path_unsupported` receive explicit bounded-rerun
  dispositions.
- The pass selects readiness for P47-T3 bounded rerun gate, not larger curated
  corpus approval.
- P47-T2 does not rerun the pilot, run AI, run adapters, clone or fetch
  repositories, execute harvested code, accept packages or relations, publish
  registry metadata, seed baselines, or remove `preview_only`.
- P47-T2 updates `SPECS/INPROGRESS/next.md` after archival to show P47-T3.

## Boundaries

- Do not approve a larger curated corpus.
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
- Do not treat quality-pass output, plan output, static output, AI output, or
  adapter output as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P47-T2 targeted quality pass and
  current next task.
- Run lint, format, coverage, Swift manifest, Swift docs build, and whitespace
  checks as required by Flow.
