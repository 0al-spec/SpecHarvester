# P31-T2 Selected Candidate Handoff Proposal Helper

## Objective

Implement a `selected-candidate-handoff-proposal` producer helper that emits
JSON and Markdown artifacts matching the P31-T1
`SpecHarvesterSelectedCandidateHandoffProposal` contract.

The helper must convert selected candidate dry-run evidence into portable
SpecPM review evidence without mutating candidate bundles or implying registry
acceptance.

## Background

P31-T1 documented the portable contract and example fixture. Operators still
cannot generate that artifact from real selected candidate evidence.

P31-T2 should provide the producer-side helper only:

```text
selected handoff dry-run fixture
+ selected candidate bundles
+ producer preflight reports
+ static viewer outputs
-> selected-candidate-handoff-proposal.json
-> selected-candidate-handoff-proposal.md
```

SpecPM-side preflight and acceptance remain downstream work.

## Deliverables

- Add a `spec_harvester.selected_candidate_handoff_proposal` module with:
  - constants for the P31-T1 API version, kind, and schema version;
  - an options dataclass;
  - JSON proposal builder;
  - Markdown proposal builder;
  - JSON and Markdown writer functions.
- Add CLI command:

  ```bash
  python -m spec_harvester selected-candidate-handoff-proposal \
    --selected-handoff-dry-run <p30-t5-json> \
    --candidate-root <selected-candidate-root> \
    --preflight-root <preflight-root> \
    --viewer-root <viewer-root> \
    --output <proposal.json> \
    --proposal-body <proposal.md>
  ```

- Support deterministic helper behavior:
  - `--selected-handoff-dry-run` is required;
  - candidate/preflight/viewer roots are optional, but when provided they must
    be used for digest checks and path resolution;
  - selected candidates come from the dry-run fixture;
  - deferred candidates come from the dry-run fixture;
  - required evidence roles match P31-T1.
- Preserve the non-authority boundary:
  - `authority: producer_preview_evidence_only`;
  - selected candidates remain `previewOnly: true`;
  - `registryAcceptanceDecision.status: external_required`;
  - no acceptance, relation acceptance, baseline seeding, `preview_only`
    removal, SpecPM PR creation, or registry publication.
- Update docs and DocC:
  - `SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`;
  - `SPECPM_HANDOFF.md`;
  - roadmap;
  - docs index/root if needed.
- Add tests:
  - builder success path from fixture-style selected artifacts;
  - CLI writes JSON and Markdown;
  - missing or invalid dry-run identity is rejected;
  - selected candidate with non-passing preflight is rejected;
  - output evidence roles and non-authority statements are stable;
  - docs mention the helper command and boundaries.
- Archive Flow artifacts and leave P31-T3 as the next selected task.

## Acceptance Criteria

- `selected-candidate-handoff-proposal` emits:
  - `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`;
  - `kind: SpecHarvesterSelectedCandidateHandoffProposal`;
  - `schemaVersion: 1`;
  - `authority: producer_preview_evidence_only`.
- The helper output includes exactly the selected candidates from the dry-run
  fixture.
- The helper output includes exactly the deferred candidates from the dry-run
  fixture.
- Each selected candidate records:
  - candidate bundle evidence;
  - `specpm.yaml`;
  - `specs/*.spec.yaml`;
  - `producer-receipt.json`;
  - `validation-report.json`;
  - `diagnostics.json`;
  - `author-ready-draft-quality-report.json`;
  - producer preflight report;
  - static viewer `index.html`;
  - static viewer `spec-package.json`;
  - selected handoff dry-run source fixture.
- The helper rejects selected candidates unless:
  - `previewOnly` is true;
  - producer preflight status is `passed`;
  - producer preflight warning and error counts are zero;
  - static viewer status is `ok`;
  - `registryAcceptanceDecision.status` is `external_required`;
  - `registryAcceptanceDecision.producerAuthority` is `evidence_only`.
- Markdown output includes:
  - selected candidate table;
  - deferred candidate table;
  - required evidence roles;
  - maintainer checklist;
  - non-authority boundary.
- Tests and docs prove the helper does not create a SpecPM pull request,
  mutate candidates, accept packages, accept relations, seed baselines, remove
  `preview_only`, or publish registry metadata.

## Non-Goals

- No SpecPM repository mutation.
- No SpecPM-side preflight implementation.
- No real P30 helper run fixture; that is P31-T3.
- No candidate curation.
- No regeneration of deferred candidates.
- No registry publication.

## Archive Status

Archived: 2026-06-13
Verdict: PASS
