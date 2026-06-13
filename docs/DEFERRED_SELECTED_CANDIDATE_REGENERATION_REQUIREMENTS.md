# Deferred Selected Candidate Regeneration Requirements

Status: P31-T5 producer-side regeneration requirement contract.

This page records what must happen before a P30 deferred candidate can enter a
future selected candidate handoff proposal.

The machine-readable companion fixture is:

```text
tests/fixtures/deferred_selected_candidate_regeneration_requirements/p31-t5-deferred-selected-candidate-regeneration-requirements.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.deferred-selected-candidate-regeneration-requirements/v0",
  "kind": "SpecHarvesterDeferredSelectedCandidateRegenerationRequirements",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P31-T5 consumes recorded evidence only:

- P30-T4 candidate-layer triage:
  `tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json`;
- P30-T5 selected handoff dry run:
  `tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json`;
- P31-T3 selected candidate handoff proposal:
  `tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`.

It does not run another scrape, call LM Studio, call SpecNode, clone
repositories, install dependencies, regenerate candidates, generate accepted
source, publish registry metadata, or create a SpecPM pull request.

P32-T2 turns these requirements into the safe operator procedure in
[`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md).

## Deferred Candidates

The six deferred P30 candidates remain excluded from selected handoff:

| Candidate | Blocker class | Finding codes | Required before selected handoff |
| --- | --- | --- | --- |
| `xyflow.workspace` | `package_set_identity_regeneration` | `package_set_id_missing` | regenerate package-set AI draft/enrichment evidence with package-set identity |
| `xyflow.react` | `package_set_identity_regeneration` | `package_set_id_missing` | regenerate member evidence from the package-set identity run |
| `xyflow.svelte` | `package_set_identity_regeneration` | `package_set_id_missing` | regenerate member evidence from the package-set identity run |
| `xyflow.system` | `package_set_identity_regeneration` | `package_set_id_missing` | regenerate member evidence from the package-set identity run |
| `cupertino.core` | `warning_bearing_enrichment_regeneration` | `refined_summary_missing` | regenerate AI enrichment or attach author-curated summary evidence |
| `navigation_split_view.core` | `identity_drift_resolution` | `package_set_id_missing`, `package_id_hint_mismatch` | resolve `navigation-split-view.core` versus `navigation_split_view.core` before handoff |

## Regeneration Classes

### Package-Set Identity Regeneration

`xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system`
cannot enter selected handoff until package-set AI draft evidence is
regenerated with package-set identity.

Before handoff, the regenerated evidence should include:

- `package_set_draft`;
- `package_relation_proposals`;
- `bundle_set_preflight`;
- `package_set_viewer`;
- `package_set_ai_draft_proposal`;
- `package_set_ai_enrichment_proposal`;
- member candidate bundles and `member_quality_report` evidence.

The package-set run should prove the workspace/member topology again:

```text
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
xyflow.workspace contains xyflow.system
```

### Warning-Bearing Enrichment Regeneration

`cupertino.core` cannot enter selected handoff while
`refined_summary_missing` remains unresolved.

Before handoff, the operator must either:

- regenerate AI enrichment until refined summary evidence is present and
  diagnostics are clean; or
- attach author-curated summary evidence and mark the model gap as resolved by
  review.

### Identity-Drift Resolution

`navigation_split_view.core` cannot enter selected handoff while the generated
candidate id and manifest hint disagree.

Before handoff, the operator must:

- choose and document the canonical package id;
- resolve `navigation-split-view.core` versus `navigation_split_view.core`;
- regenerate deterministic, AI draft, and enrichment evidence under the
  canonical id;
- explicitly reject or alias the non-canonical id;
- produce clean producer preflight and static viewer evidence.

## Minimum Proof Before Selection

For any deferred candidate to enter a future selected handoff proposal:

- `currentClassification` must no longer be `needs_regeneration`;
- `handoffStatus` must become `selected_candidate_ready`;
- required evidence roles for the blocker class must be present;
- producer preflight must be `passed`;
- producer preflight warning count must be `0`;
- producer preflight error count must be `0`;
- producer preflight warning and error counts `0` must be reviewable;
- static viewer status must be `ok`;
- `preview_only` must remain intact;
- `registryAcceptanceDecision.status` must remain `external_required`;
- regenerated evidence digests must be reviewable.

The candidate must remain deferred when package-set identity is still missing,
warning-bearing enrichment evidence is unresolved, package-id normalization is
unresolved, producer preflight has warnings/errors, static viewer output is
missing, or regenerated evidence digests are not available.

## Non-Authority Boundary

This contract records regeneration requirements only.
It does not regenerate candidates.

It does not:

- regenerate candidates;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create or merge a SpecPM pull request;
- replace author or SpecPM maintainer review.

See also:

- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
- [`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md)
- [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`](SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
