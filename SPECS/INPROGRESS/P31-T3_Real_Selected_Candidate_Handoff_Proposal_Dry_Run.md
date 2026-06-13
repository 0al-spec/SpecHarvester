# P31-T3 Real Selected Candidate Handoff Proposal Dry Run

## Objective

Run the P31-T2 `selected-candidate-handoff-proposal` helper against the real
P30 selected candidate evidence and record the resulting dry-run handoff
proposal artifacts.

The output should prove that the documented contract and helper can produce a
portable SpecPM review envelope for the selected candidates without requiring
SpecHarvester to become a registry authority.

## Background

P30-T5 recorded selected handoff dry-run evidence for:

- `flask.core`;
- `gin.core`;
- `docc2context.core`.

P31-T1 documented the `SpecHarvesterSelectedCandidateHandoffProposal`
contract. P31-T2 implemented a helper that can emit JSON and Markdown proposal
artifacts from the selected dry-run source.

The durable input for this task is the recorded P30-T5 dry-run fixture,
including its selected candidate list, deferred candidate list, paths,
SHA-256 digests, producer preflight summaries, static viewer summaries, and
non-authority boundary.

When the original P30-T5 local `/tmp` candidate, preflight, and viewer roots
are still present, the helper should compute `local_file` SHA-256 digests from
those files. If those local roots are unavailable in a future rerun, the helper
must still preserve the recorded P30-T5 digest evidence instead of treating the
candidate as accepted registry truth.

## Deliverables

- Run:

  ```bash
  python -m spec_harvester selected-candidate-handoff-proposal \
    --selected-handoff-dry-run tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json \
    --output tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json \
    --proposal-body docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md
  ```

- Add the generated JSON fixture:
  `tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`.
- Add a Markdown companion:
  `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`.
- Add a DocC mirror for the P31-T3 dry-run artifact.
- Update selected handoff docs, SpecPM handoff docs, roadmap, and docs index to
  reference the real selected candidate handoff dry run.
- Add regression tests that verify:
  - the fixture identity matches `SpecHarvesterSelectedCandidateHandoffProposal`;
  - the fixture was produced from the P30-T5 selected handoff dry-run input;
  - the selected candidates are exactly `flask.core`, `gin.core`, and
    `docc2context.core`;
  - the deferred candidates remain exactly the six P30 deferred candidates;
  - each selected candidate records required evidence roles;
  - missing local `/tmp` candidate/preflight/viewer files are preserved as
    expected recorded evidence rather than treated as accepted registry truth;
  - non-authority statements remain present.

## Acceptance Criteria

- The generated JSON fixture is valid JSON and has:
  - `apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`;
  - `kind: SpecHarvesterSelectedCandidateHandoffProposal`;
  - `schemaVersion: 1`;
  - `authority: producer_preview_evidence_only`.
- The fixture records exactly 3 selected candidates and 6 deferred candidates.
- Every selected candidate has:
  - `previewOnly: true`;
  - producer preflight `passed`;
  - `warningCount: 0`;
  - `errorCount: 0`;
  - static viewer status `ok`;
  - `registryAcceptanceDecision.status: external_required`;
  - `registryAcceptanceDecision.producerAuthority: evidence_only`.
- Evidence links include every required P31-T1/P31-T2 role.
- The fixture records `local_file` digests when the P30 candidate, preflight,
  and viewer artifacts are present.
- The helper still has a fallback path that keeps P30-T5 recorded digests when
  local candidate/preflight/viewer files are not present.
- The Markdown companion includes selected candidate, deferred candidate,
  evidence role, maintainer checklist, and non-authority sections.
- No SpecPM PR is created.
- No package is accepted.
- No relation is accepted.
- No baseline is seeded.
- No `preview_only` marker is removed.
- No registry metadata is published.

## Non-Goals

- No SpecPM-side preflight implementation; that is P31-T4.
- No regeneration of deferred candidates; that is P31-T5.
- No candidate curation.
- No accepted-source mutation.
- No live LM Studio call.
- No rerun of the full P30 corpus.
