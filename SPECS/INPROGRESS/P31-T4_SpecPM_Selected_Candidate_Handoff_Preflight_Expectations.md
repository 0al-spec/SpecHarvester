# P31-T4 SpecPM Selected Candidate Handoff Preflight Expectations

## Objective

Define the downstream SpecPM-side preflight expectations for
`SpecHarvesterSelectedCandidateHandoffProposal` evidence.

The output should give SpecPM enough stable consumer-side policy to implement a
future preflight gate without treating SpecHarvester producer evidence as
registry authority.

## Background

P31-T1 defined `SpecHarvesterSelectedCandidateHandoffProposal`.
P31-T2 implemented the producer helper.
P31-T3 ran the helper on the real P30 selected candidates and recorded a
generated fixture.

The next gap is downstream. SpecPM can now receive a portable selected
candidate handoff proposal, but the expected consumer-side checks need to be
explicit before implementation:

```text
SpecHarvesterSelectedCandidateHandoffProposal
  -> SpecPM selected handoff preflight
  -> maintainer review
  -> optional acceptance decision outside producer evidence
```

It must not become:

```text
SpecHarvester handoff passed -> SpecPM accepts package automatically
```

## Deliverables

- Add a GitHub docs page, likely
  `docs/SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`, covering:
  - expected input identity;
  - supported proposal schema version;
  - required authority value;
  - selected/deferred candidate consistency checks;
  - required evidence role checks;
  - digest and path checks;
  - producer preflight and static viewer checks;
  - registry acceptance decision boundaries;
  - privacy/provenance boundaries;
  - expected report shape and diagnostic categories;
  - pass/fail meaning;
  - non-goals and non-authority statements.
- Add a DocC mirror.
- Link the document from:
  - selected candidate handoff proposal docs;
  - SpecPM handoff guide;
  - roadmap;
  - docs index and DocC root.
- Add regression tests that assert:
  - the new docs cover the P31-T4 policy terms;
  - P31-T3 remains the fixture target for future preflight;
  - next task state remains coherent;
  - the document says a passing preflight is not acceptance.
- Archive Flow artifacts and leave P31-T5 as the next selected task.

## Acceptance Criteria

- The document names `SpecHarvesterSelectedCandidateHandoffProposal`,
  `spec-harvester.selected-candidate-handoff-proposal/v0`, `schemaVersion: 1`,
  and `producer_preview_evidence_only`.
- The document states that SpecPM should reject or fail preflight when:
  - input identity is unsupported;
  - `authority` is not `producer_preview_evidence_only`;
  - selected/deferred counts do not match `summary`;
  - selected candidate ids are duplicated;
  - deferred candidates appear in selected candidates;
  - required evidence roles are missing;
  - digests are missing or malformed for digest-bearing evidence;
  - producer preflight is not `passed`;
  - producer preflight warning or error counts are nonzero;
  - static viewer status is not `ok`;
  - selected candidates are not `previewOnly: true`;
  - `registryAcceptanceDecision.status` is not `external_required`;
  - `registryAcceptanceDecision.producerAuthority` is not `evidence_only`;
  - non-authority statements are missing.
- The document defines a report identity for a future SpecPM preflight report,
  without implementing that report.
- The document explicitly states that a passing preflight:
  - does not accept packages;
  - does not accept relations;
  - does not seed baselines;
  - does not remove `preview_only`;
  - does not publish registry metadata;
  - does not create or merge a SpecPM pull request.
- The document names `P31-T5` as the deferred-candidate regeneration follow-up.

## Non-Goals

- No SpecPM repository changes.
- No SpecPM preflight implementation.
- No new CLI command.
- No generated candidate regeneration.
- No accepted-source mutation.
- No package or relation acceptance.
- No registry publication.
