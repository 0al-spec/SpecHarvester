# Selected Candidate Handoff Preflight Expectations

This page mirrors
`docs/SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`.

It defines the downstream SpecPM-side preflight expectations for
`SpecHarvesterSelectedCandidateHandoffProposal` evidence.

The input identity is:

```json
{
  "apiVersion": "spec-harvester.selected-candidate-handoff-proposal/v0",
  "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

The P31-T3 fixture is the concrete input target:

```text
tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json
```

## Expected Checks

SpecPM should verify identity, schema version, selected and deferred candidate
counts, duplicate candidate ids, required evidence roles, SHA-256 digests,
producer preflight `passed` status, zero warning and error counts, static
viewer `ok` status, `previewOnly: true`, and
`registryAcceptanceDecision.status: external_required` with
`producerAuthority: evidence_only`.

SpecPM should reject missing non-authority statements that cover package
acceptance, relation acceptance, baseline seeding, `preview_only` removal,
registry publication, SpecPM pull request creation, and maintainer review.

Suggested diagnostics include `selected_candidate_count_mismatch`,
`deferred_candidate_selected`, `selected_candidate_not_preview_only`,
`producer_preflight_not_passed`, `static_viewer_not_ok`,
`registry_acceptance_not_external_required`, `missing_required_evidence_role`,
`invalid_evidence_digest`, `selected_handoff_source_digest_mismatch`, and
`missing_non_authority_statement`.

## Suggested Report

A future SpecPM implementation may emit
`SpecPMSelectedCandidateHandoffPreflightReport` with
`apiVersion: specpm.selected-candidate-handoff-preflight/v0`,
`schemaVersion: 1`, status `passed | failed | warnings`, and authority
`specpm_consumer_preflight`.

## Meaning of a Pass

Passing selected handoff preflight means the proposal is internally consistent
review evidence. It does not accept packages, does not accept relations, does not
seed baselines, does not remove `preview_only`, does not publish registry metadata,
does not create or merge a SpecPM pull request, does not replace maintainer review,
or prove generated claims are semantically perfect.

P31-T5 remains the follow-up for deferred candidate regeneration requirements.

See also <doc:SelectedCandidateHandoffProposal>,
<doc:SelectedCandidateHandoffProposalP31T3>, and <doc:SpecPMHandoff>.
