# P33-T7 Durable Next-Corpus Selected Handoff Artifact

Status: Planned
Phase: Phase 33. Bounded Corpus Expansion Planning
Owner: SpecHarvester producer evidence, SpecPM consumer preflight

## Motivation

P33-T6 proved an important boundary: the P33-T5 candidate-layer triage fixture
selects `serena.core`, `transmission.core`, and `specpm.core`, but it is not a
supported SpecPM selected handoff payload. SpecPM correctly returned
`selected_handoff_payload_missing`.

The next step is to produce durable selected handoff evidence that SpecPM can
preflight without rerunning the corpus or fabricating per-file evidence digests
that are not present in committed fixtures.

## Goal

Create a committed, digest-backed selected handoff artifact for the P33 next
corpus selected scope and prove that the current SpecPM selected handoff
consumer gate can preflight it.

## Deliverables

- Add a durable `SpecHarvesterSelectedCandidateHandoffProposal` fixture for the
  P33 selected scope:
  - `serena.core`;
  - `transmission.core`;
  - `specpm.core`.
- Keep deferred candidates outside selected handoff:
  - `mcpm.system`;
  - `specgraph.system`.
- Reference only committed, digest-backed evidence:
  - P33-T5 candidate-layer triage fixture;
  - P33-T4 live local-model fixture;
  - P33-T3 deterministic fixture;
  - P33-T2 source manifest.
- Run `specpm producer-bundle preflight-selected-candidate-handoff` against
  the durable handoff artifact and record a passing result.
- Add GitHub docs, DocC docs, validation report, and docs-contract tests.
- Archive the task and advance `next.md` to the next bounded follow-up.

## Acceptance Criteria

- The durable handoff fixture has supported identity:
  `SpecHarvesterSelectedCandidateHandoffProposal` with
  `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`.
- SpecPM selected handoff preflight passes with:
  - `selectedCandidateCount: 3`;
  - `deferredCandidateCount: 2`;
  - `errorCount: 0`;
  - `warningCount: 0`;
  - at least one verified source digest.
- The fixture does not include synthetic per-file digests for generated
  `specpm.yaml`, `specs/*.spec.yaml`, receipts, validation reports,
  diagnostics, quality reports, preflight reports, or viewer payloads unless
  those files are committed and digest-backed.
- The fixture states that package acceptance, relation acceptance, baseline
  seeding, `preview_only` removal, public registry publication, and SpecPM pull
  request creation remain outside producer authority.
- Deferred candidates remain excluded from selected handoff.

## Non-Goals

- Do not run a new scrape.
- Do not rerun LM Studio or any model provider.
- Do not clone repositories, fetch remote state, install dependencies, or
  execute harvested repository code.
- Do not mutate generated candidate bundles.
- Do not accept packages or relations in SpecPM.
- Do not seed baselines, remove `preview_only`, publish registry metadata, or
  create a SpecPM pull request.

