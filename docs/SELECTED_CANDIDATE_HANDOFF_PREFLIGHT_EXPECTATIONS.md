# Selected Candidate Handoff Preflight Expectations

Status: P31-T4 downstream consumer contract target.

This page defines what a future SpecPM-side preflight should verify when it
receives `SpecHarvesterSelectedCandidateHandoffProposal` evidence.

SpecHarvester produces preview evidence. SpecPM owns validation, registry
policy, maintainer decisions, accepted-source mutation, and public index
publication.

The intended boundary is:

```text
SpecHarvesterSelectedCandidateHandoffProposal
  -> SpecPM selected handoff preflight
  -> maintainer review
  -> optional registry acceptance decision outside producer evidence
```

It is not:

```text
SpecHarvester handoff passed -> SpecPM accepts package automatically
```

## Input Identity

SpecPM should accept only a JSON object with:

```json
{
  "apiVersion": "spec-harvester.selected-candidate-handoff-proposal/v0",
  "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

Unsupported identity should fail with `unsupported_handoff_identity`.
Unsupported schema versions should fail with
`unsupported_handoff_schema_version`.
Any authority other than `producer_preview_evidence_only` should fail with
`unsupported_producer_authority`.

The P31-T3 fixture is the current concrete input target:

```text
tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json
```

## Required Checks

A future SpecPM preflight should verify the following groups.

### Summary and Candidate Sets

- `summary.selectedCandidateCount` equals `len(selectedCandidates)`.
- `summary.deferredCandidateCount` equals `len(deferredCandidates)`.
- `summary.requiredEvidenceRoleCount` equals `len(requiredEvidenceRoles)`.
- `summary.specpmPullRequestCreated` is `false`.
- `summary.registryMutationCount` is `0`.
- Selected candidate ids are unique.
- Deferred candidate ids are unique.
- No deferred candidate id appears in `selectedCandidates`.
- Every deferred candidate has `handoffStatus:
  excluded_from_selected_handoff`.

Suggested diagnostics:

- `selected_candidate_count_mismatch`;
- `deferred_candidate_count_mismatch`;
- `required_evidence_role_count_mismatch`;
- `duplicate_selected_candidate_id`;
- `duplicate_deferred_candidate_id`;
- `deferred_candidate_selected`;
- `unexpected_specpm_pull_request`;
- `unexpected_registry_mutation`.

### Selected Candidate Requirements

For every selected candidate:

- `previewOnly` is `true`;
- `producerPreflight.status` is `passed`;
- `producerPreflight.warningCount` is `0`;
- `producerPreflight.errorCount` is `0`;
- `staticViewer.status` is `ok`;
- `registryAcceptanceDecision.status` is `external_required`;
- `registryAcceptanceDecision.producerAuthority` is `evidence_only`;
- `registryAcceptanceDecision.requiredFor` includes or equals
  `public_index_acceptance`;
- `maintainerAction` is review-oriented, such as
  `review_for_possible_specpm_intake`.

Suggested diagnostics:

- `selected_candidate_not_preview_only`;
- `producer_preflight_not_passed`;
- `producer_preflight_warning_count_nonzero`;
- `producer_preflight_error_count_nonzero`;
- `static_viewer_not_ok`;
- `registry_acceptance_not_external_required`;
- `registry_acceptance_producer_authority_invalid`;
- `registry_acceptance_required_for_missing`;
- `selected_candidate_maintainer_action_invalid`.

### Evidence Roles and Digests

SpecPM should treat `requiredEvidenceRoles[]` as the expected role vocabulary.
For every selected candidate, `evidenceLinks[]` should include each required
role exactly once:

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

Digest-bearing roles should carry a `sha256:<hex>` digest. `candidate_bundle`
may be a directory marker without digest. `selected_handoff_dry_run` should
carry a digest for the proposal source fixture.

`pathScope` should be explicit. Current producer output uses `local_path` for
recorded dry-run evidence. SpecPM can preserve these paths as provenance, but
must not require historical `/tmp` paths to exist during consumer preflight.

Suggested diagnostics:

- `missing_required_evidence_role`;
- `duplicate_evidence_role`;
- `invalid_evidence_digest`;
- `missing_selected_handoff_dry_run_digest`;
- `unsupported_evidence_path_scope`;
- `historical_local_path_missing_nonfatal`.

### Source Fixture and Provenance

The `source.selectedDryRunFixture` record should name:

- the selected handoff dry-run `apiVersion`;
- the selected handoff dry-run `kind`;
- a stable source path;
- a `sha256:<hex>` digest;
- status `selected_handoff_dry_run_ready`.

For P31-T3, the expected path is:

```text
tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json
```

SpecPM may compare the source fixture digest against the
`selected_handoff_dry_run` evidence link digest when both are present.

Suggested diagnostics:

- `selected_handoff_source_missing`;
- `selected_handoff_source_digest_missing`;
- `selected_handoff_source_digest_mismatch`;
- `selected_handoff_source_status_invalid`.

### Non-Authority Boundary

The proposal must continue to say it is review evidence only and not registry
acceptance. A future SpecPM preflight should verify non-authority statements or
equivalent machine-readable flags covering:

- not SpecPM registry acceptance;
- does not accept packages;
- does not accept relations;
- does not seed baselines;
- does not remove `preview_only`;
- does not publish registry metadata;
- does not create or merge a SpecPM pull request;
- does not replace maintainer review.

Suggested diagnostics:

- `missing_non_authority_statement`;
- `producer_claims_registry_authority`;
- `producer_claims_acceptance`.

## Suggested Report Shape

A future SpecPM implementation may emit:

```json
{
  "apiVersion": "specpm.selected-candidate-handoff-preflight/v0",
  "kind": "SpecPMSelectedCandidateHandoffPreflightReport",
  "schemaVersion": 1,
  "status": "passed",
  "authority": "specpm_consumer_preflight",
  "input": {
    "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
    "digest": "sha256:<proposal-json-digest>"
  },
  "summary": {
    "selectedCandidateCount": 3,
    "deferredCandidateCount": 6,
    "requiredEvidenceRoleCount": 11,
    "errorCount": 0,
    "warningCount": 0
  },
  "diagnostics": [],
  "nonAuthority": {
    "preflightOnly": true,
    "acceptsPackages": false,
    "acceptsRelations": false,
    "seedsBaselines": false,
    "removesPreviewOnly": false,
    "publishesRegistryMetadata": false,
    "createsSpecPMPullRequest": false
  }
}
```

Suggested statuses:

- `passed`: the proposal is internally consistent review evidence;
- `failed`: required identity, candidate, evidence, digest, or boundary checks
  failed;
- `warnings`: only non-blocking provenance warnings remain, such as historical
  local paths that are not expected to exist in the SpecPM checkout.

## Meaning of a Pass

Passing selected handoff preflight means:

- the proposal shape is supported;
- required evidence roles are present;
- selected candidates meet producer-side zero-warning gates;
- deferred candidates remain out of selected handoff;
- the artifact preserves external registry acceptance authority.

Passing preflight does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create or merge a SpecPM pull request;
- replace SpecPM maintainer review;
- prove that generated claims are semantically perfect.

## Follow-Up

P31-T5 should record targeted regeneration requirements for deferred P30
candidates before any package-set, warning-bearing, or identity-drift candidate
can enter selected handoff.

See also:

- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
