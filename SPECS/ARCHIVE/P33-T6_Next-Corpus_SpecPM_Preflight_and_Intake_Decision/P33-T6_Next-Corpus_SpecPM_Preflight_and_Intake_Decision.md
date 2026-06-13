# P33-T6 Next-Corpus SpecPM Preflight and Intake Decision

Status: Planned
Phase: Phase 33. Bounded Corpus Expansion Planning
Owner: SpecHarvester coordination, SpecPM consumer gate

## Motivation

P33-T5 selected `serena.core`, `transmission.core`, and `specpm.core` for the
next SpecPM-facing handoff, while keeping `mcpm.system` and `specgraph.system`
deferred. That triage is useful producer review evidence, but it is not itself
a supported SpecPM selected handoff payload.

Before Phase 33 can claim the next corpus is ready for maintainer intake
review, SpecPM must either preflight a supported selected handoff artifact or
the task must record why the current evidence is not yet preflightable.

## Goal

Run or coordinate the SpecPM-side selected candidate handoff preflight for the
P33 next corpus and record the resulting intake readiness decision without
mutating registry state.

## Deliverables

- Run the current SpecPM selected candidate handoff preflight against the
  committed P33-T5 candidate-layer triage fixture.
- Record the command result and explain whether the selected candidates are
  ready for SpecPM maintainer intake review.
- Add a machine-readable P33-T6 decision fixture that preserves:
  - selected candidates: `serena.core`, `transmission.core`, `specpm.core`;
  - deferred candidates: `mcpm.system`, `specgraph.system`;
  - the SpecPM preflight result;
  - the non-authority boundary.
- Add or update documentation, DocC references, and regression coverage for
  the P33-T6 decision.
- Archive the task and advance the workplan to the next bounded follow-up if
  the current evidence is not preflight-ready.

## Acceptance Criteria

- The validation report links the exact SpecPM command, SpecPM revision, and
  observed preflight output.
- The decision fixture records that no package, relation, baseline, preview
  flag, public registry metadata, or SpecPM pull request was created.
- If the current committed P33-T5 fixture is not a supported SpecPM handoff
  input, the task records a follow-up that creates a durable selected handoff
  artifact or extends the consumer gate before intake review.
- Deferred candidates remain outside selected handoff scope.
- The task runs the repository documentation/test gates required by Flow.

## Non-Goals

- Do not rerun the P33 corpus scrape.
- Do not rerun LM Studio or any model provider.
- Do not clone repositories, fetch remote state, install dependencies, or
  execute harvested repository code.
- Do not fabricate per-file evidence digests that are not present in committed
  artifacts.
- Do not accept packages or relations in SpecPM.
- Do not seed baselines, remove `preview_only`, publish registry metadata, or
  create a SpecPM pull request.

## Archive

Archived: 2026-06-14
Verdict: PASS

P33-T6 ran the current SpecPM selected candidate handoff preflight against the
committed P33-T5 candidate-layer triage fixture. The gate returned
`selected_handoff_payload_missing`, which confirms that P33-T5 triage is not a
supported selected handoff payload.

The intake decision is
`not_ready_requires_durable_selected_handoff_artifact`. The next selected task
is P33-T7: create durable selected handoff evidence for `serena.core`,
`transmission.core`, and `specpm.core`, or explicitly extend the SpecPM
consumer gate before maintainer intake review.
