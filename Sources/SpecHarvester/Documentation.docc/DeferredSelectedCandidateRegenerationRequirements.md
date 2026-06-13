# Deferred Selected Candidate Regeneration Requirements

This page mirrors
`docs/DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`.

It records the P31-T5 producer-side regeneration requirement contract for the
P30 deferred candidates before they can enter selected candidate handoff.

The machine-readable fixture is:

```text
tests/fixtures/deferred_selected_candidate_regeneration_requirements/p31-t5-deferred-selected-candidate-regeneration-requirements.example.json
```

Its identity is `SpecHarvesterDeferredSelectedCandidateRegenerationRequirements`
with
`apiVersion: spec-harvester.deferred-selected-candidate-regeneration-requirements/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Deferred Candidates

The fixture keeps `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`,
`xyflow.system`, `cupertino.core`, and `navigation_split_view.core` out of
selected handoff until targeted regeneration requirements are met.

The blocker classes are `package_set_identity_regeneration`,
`warning_bearing_enrichment_regeneration`, and `identity_drift_resolution`.
The finding codes include `package_set_id_missing`, `refined_summary_missing`,
and `package_id_hint_mismatch`.

P32-T2 turns these requirements into the safe operator procedure in
<doc:DeferredCandidateRegenerationRunbook>.

## Requirements

`xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system` require
package-set AI draft and enrichment regeneration with package-set identity,
`bundle_set_preflight`, `package_set_viewer`, member quality reports, and the
`contains` topology from `xyflow.workspace` to `xyflow.react`,
`xyflow.svelte`, and `xyflow.system`.

`cupertino.core` requires warning-bearing enrichment regeneration or
author-curated summary evidence before selected handoff.

`navigation_split_view.core` requires identity-drift resolution for
`navigation-split-view.core` versus `navigation_split_view.core`, followed by
regenerated deterministic, AI draft, and enrichment evidence under the
canonical package id.

For any deferred candidate to enter selected handoff, producer preflight must
be `passed` with warning and error counts `0`, static viewer status must be
`ok`, `preview_only` must remain intact, and
`registryAcceptanceDecision.status` must stay `external_required`.

## Non-Authority Boundary

This contract records regeneration requirements only. It does not regenerate
candidates, accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, create or merge a SpecPM pull
request, or replace author or SpecPM maintainer review.

See also <doc:LimitedPopularLibraryCandidateLayerTriage>,
<doc:LimitedPopularLibrarySelectedHandoffDryRun>,
<doc:DeferredCandidateRegenerationRunbook>,
<doc:SelectedCandidateHandoffProposal>,
<doc:SelectedCandidateHandoffPreflightExpectations>, and <doc:SpecPMHandoff>.
