# P46-T6 Bounded Popular-Library Pilot Exit Decision

Status: Planned
Phase: Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
Task: P46-T6
Branch: `feature/P46-T6-bounded-popular-library-pilot-exit-decision`
Depends on: P46-T5 Bounded Popular-Library Pilot Author Handoff Summaries

## Problem

P46-T5 produced author-facing summaries for the bounded pilot, but Phase 46
still needs a durable exit decision. The decision must say whether the pilot is
ready to proceed to a larger curated corpus, needs a targeted quality pass, or
must stop on a documented blocker.

## Goal

Record a machine-readable and documented Phase 46 exit decision without
changing registry truth.

## Deliverables

- Machine-readable P46-T6 exit decision fixture under
  `tests/fixtures/bounded_popular_library_pilot_exit_decision/`.
- GitHub Markdown and DocC documentation explaining the selected decision,
  rejected alternatives, evidence inputs, and follow-up direction.
- Docs-contract coverage for decision identity, P46-T5 source artifact linkage,
  selected and rejected decision options, readiness signals, no-authority
  boundaries, and current next-task pointer.
- Validation report and archive artifacts for P46-T6.

## Acceptance Criteria

- The decision references the P46-T5 author handoff by digest.
- The selected path is explicit and one of:
  `proceed_to_larger_curated_corpus`,
  `run_targeted_quality_pass_before_larger_curated_corpus`, or
  `stop_on_documented_blocker`.
- The decision accounts for reviewable static evidence across all six pilot
  repositories.
- The decision keeps `gin.aiDraft` and `docc2context.aiDraft` as
  do-not-promote AI sidecars.
- The decision keeps xyflow caveats visible:
  `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and
  `model_evidence_path_unsupported`.
- P46-T6 does not accept packages or relations, publish registry metadata,
  seed baselines, or remove `preview_only`.
- P46-T6 updates `SPECS/INPROGRESS/next.md` after archival to show Phase 46
  completion and the recommended follow-up planning direction.

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
- Do not treat exit-decision output, handoff output, static output, AI output,
  or adapter output as registry truth.

## Validation Plan

- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for the P46-T6 exit decision and current next
  task.
- Run lint, format, and whitespace checks for touched files.
