# P31-T1 Selected Candidate Handoff Proposal Contract

## Objective

Define a selected candidate handoff proposal contract that turns P30-style
selected candidate dry-run evidence into portable SpecPM review evidence.

The contract must preserve the boundary:

```text
SpecHarvester -> producer evidence envelope
SpecPM -> validation, acceptance, registry metadata, maintainer decision
```

## Background

P30-T5 recorded selected handoff dry-run evidence for:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

That fixture proves the selected candidates have producer preflight and static
viewer evidence. It is not yet a portable handoff proposal contract that can be
attached to SpecPM review or consumed by future SpecPM-side preflight.

P31-T1 should define that envelope without implementing runtime generation.

## Deliverables

- Add a GitHub-facing contract document for
  `SpecHarvesterSelectedCandidateHandoffProposal`.
- Add a DocC mirror for the same contract.
- Add a machine-readable example fixture that records:
  - contract identity;
  - selected candidates;
  - deferred candidates;
  - evidence roles;
  - producer preflight and static viewer status requirements;
  - external registry acceptance decision boundary;
  - maintainer checklist;
  - non-authority statements.
- Link the contract from:
  - docs README;
  - DocC root;
  - Roadmap;
  - SpecPM handoff guide;
  - P30 selected handoff dry-run docs.
- Add regression tests covering docs links, fixture shape, evidence roles,
  selected/deferred candidates, and non-authority boundaries.
- Archive Flow artifacts and leave the next task set to P31-T2.

## Contract Boundary

P31-T1 can:

- define JSON shape and review vocabulary;
- define required evidence roles;
- define selected/deferred candidate handling;
- define maintainer checklist expectations;
- define downstream SpecPM preflight expectations as future consumer work.

P31-T1 cannot:

- implement the CLI generator;
- mutate candidate bundles;
- create a SpecPM pull request;
- run `prepare-accepted-entry`;
- run `accepted-package-update-proposal`;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata.

## Acceptance Criteria

- The contract identity is:
  - `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`;
  - `kind: SpecHarvesterSelectedCandidateHandoffProposal`;
  - `schemaVersion: 1`;
  - `authority: producer_preview_evidence_only`.
- The example fixture includes exactly three selected candidates:
  `flask.core`, `gin.core`, and `docc2context.core`.
- The example fixture includes all six P30 deferred candidates:
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
  `cupertino.core`, and `navigation_split_view.core`.
- Evidence roles include:
  - `candidate_bundle`;
  - `manifest`;
  - `boundary_spec`;
  - `producer_receipt`;
  - `validation_report`;
  - `diagnostics`;
  - `quality_report`;
  - `producer_preflight`;
  - `static_viewer`;
  - `static_viewer_payload`;
  - `selected_handoff_dry_run`.
- Every selected candidate requires `previewOnly: true`,
  `producerPreflight.status: passed`, `staticViewer.status: ok`, and
  `registryAcceptanceDecision.status: external_required`.
- The docs explicitly state that passing producer preflight is review evidence
  only, not acceptance.
- The docs and fixture explicitly state that the proposal cannot accept
  packages, accept relations, seed baselines, remove `preview_only`, publish
  registry metadata, or create a SpecPM pull request.

## Non-Goals

- No CLI implementation.
- No real P30 proposal generation.
- No SpecPM repository mutation.
- No selected candidate curation.
- No regeneration of deferred candidates.
- No registry publication.
