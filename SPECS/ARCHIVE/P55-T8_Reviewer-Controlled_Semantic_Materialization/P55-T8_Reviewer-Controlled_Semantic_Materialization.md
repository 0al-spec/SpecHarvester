# P55-T8 Reviewer-Controlled Semantic Materialization

## Objective

Create a new preview-only candidate revision from an existing candidate and an
explicit accepted or edited P55-T7 semantic decision, while preserving the
original candidate and all review provenance.

## Dependencies

- P55-T6 complete portable semantic proposal records.
- P55-T7 digest-bound semantic reviewer edits.
- Existing SpecHarvester manifest checks and read-only SpecPM validation runner.

## Deliverables

- A deterministic materializer accepting one candidate package root, one
  complete portable semantic record, and one current candidate decision.
- Fail-closed revalidation of candidate identity, reviewer identity, semantic
  decision, packet, portable record, proposal, source, and reviewer-edit
  digests.
- Claim-to-field application rules:
  - selected purpose updates package and BoundarySpec intent summaries;
  - selected capability text updates existing capability summaries;
  - selected interface claims extend included scope;
  - selected non-goals and nearby-intent differences extend excluded scope;
  - selected observed or experimental intent decisions update manifest and
    capability intent lists while experimental IDs remain non-canonical.
- A new output revision that preserves `preview_only: true`, copies only
  allowlisted YAML, leaves the source directory unchanged, and records exact
  before/after file digests and applied claim/intent IDs.
- SpecHarvester structural validation plus bounded read-only SpecPM validation
  of the new revision.
- A portable materialization report binding the output, decision, validation
  results, and zero registry mutations.
- CLI, schemas/docs, DocC, and focused valid, edited, rejected, stale, unsafe,
  validation-failure, and immutability tests.

## Acceptance Criteria

- Only claim IDs listed in `acceptedOrEditedClaimIds` are applied; edited text
  replaces only its matching selected claim.
- Rejected, deferred, missing-reviewer, stale, unknown-claim, or incoherent
  decisions cannot create output.
- Input candidate files remain byte-identical after success and failure.
- Output is deterministic for equal inputs apart from no timestamps or
  machine-local paths.
- The output manifest remains preview-only and experimental intents remain
  proposal metadata rather than accepted taxonomy truth.
- SpecHarvester validation and read-only SpecPM validation both run before a
  passing report is written.
- No accepted package source, registry, public index, or SpecPM checkout is
  modified.
- Full tests pass with at least 90% coverage; Ruff, formatting, diff, Swift
  manifest, and DocC checks pass.

## Non-Goals

- Provider execution or semantic quality calibration.
- Automatic reviewer decisions or broad corpus materialization.
- Canonical intent governance, registry mutation, publication, or SpecPM pull
  request creation.
