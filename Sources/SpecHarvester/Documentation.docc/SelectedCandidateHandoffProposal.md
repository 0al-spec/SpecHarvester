# Selected Candidate Handoff Proposal

This page mirrors `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md` and defines
`SpecHarvesterSelectedCandidateHandoffProposal`, the portable producer evidence
envelope for selected preview candidates.

The machine-readable companion fixture is:

```text
tests/fixtures/selected_candidate_handoff_proposal/p31-t1-selected-candidate-handoff.example.json
```

Its identity is
`SpecHarvesterSelectedCandidateHandoffProposal` with
`apiVersion: spec-harvester.selected-candidate-handoff-proposal/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Inputs

The proposal consumes P30-T4 candidate-layer triage evidence and the P30-T5
selected handoff dry-run fixture. It does not run another scrape, call LM
Studio, clone repositories, install dependencies, generate accepted-source
content, or create a SpecPM pull request.

## Helper Command

P31-T2 adds a producer helper for writing JSON and Markdown handoff artifacts:

```bash
python -m spec_harvester selected-candidate-handoff-proposal \
  --selected-handoff-dry-run .smoke/selected-handoff/p30-t5-selected-handoff.json \
  --candidate-root .smoke/selected-handoff/selected \
  --preflight-root .smoke/selected-handoff/preflight \
  --viewer-root .smoke/selected-handoff/viewer \
  --output .smoke/selected-handoff/selected-candidate-handoff-proposal.json \
  --proposal-body .smoke/selected-handoff/selected-candidate-handoff-proposal.md
```

`--selected-handoff-dry-run` is required. The optional candidate, preflight,
and viewer roots let the helper read local files and compute SHA-256 digests
for present artifacts. Missing files remain expected evidence with the digest
recorded by the selected handoff dry-run source.

The helper rejects selected candidates unless they remain `previewOnly: true`,
have producer preflight `passed` with `0` warnings and `0` errors, have static
viewer status `ok`, and keep
`registryAcceptanceDecision.status: external_required` with
`producerAuthority: evidence_only`.

## Selected Candidates

The example proposal includes exactly `flask.core`, `gin.core`, and
`docc2context.core`. Each selected candidate remains `previewOnly: true`, has
producer-side preflight `passed` with `0` warnings and `0` errors, has static
viewer status `ok`, and keeps
`registryAcceptanceDecision.status: external_required`.

Passing producer-side preflight is review evidence only. It is not SpecPM
acceptance, does not remove `preview_only`, and does not publish registry
metadata.

## Required Evidence Roles

The stable required evidence roles are `candidate_bundle`, `manifest`,
`boundary_spec`, `producer_receipt`, `validation_report`, `diagnostics`,
`quality_report`, `producer_preflight`, `static_viewer`,
`static_viewer_payload`, and `selected_handoff_dry_run`.

The fixture records SHA-256 digests for the contract-bearing files, producer
preflight reports, and static viewer artifacts that came from P30-T5.

## Deferred Candidates

The proposal explicitly keeps `xyflow.workspace`, `xyflow.react`,
`xyflow.svelte`, `xyflow.system`, `cupertino.core`, and
`navigation_split_view.core` out of selected handoff. All six remain
`needs_regeneration` until targeted regeneration, package identity fixes,
author-supplied summary evidence, warning resolution, or package-set-specific
review makes them suitable for selected handoff.

## Maintainer Checklist

Before SpecPM intake, maintainers should verify selected candidate identity and
namespace, verify required evidence roles and digests, run SpecPM-side
validation and preflight, reject or request regeneration for weak evidence, and
record the external registry acceptance decision outside producer evidence.

## Future SpecPM Boundary

SpecPM may later add consumer-side preflight for
`SpecHarvesterSelectedCandidateHandoffProposal`. That preflight can verify
identity, selected candidates, deferred candidates, evidence roles, preflight
status, viewer status, and non-authority statements.
This is the future SpecPM-side preflight contract target.

It still cannot make producer evidence authoritative. Acceptance remains an
external maintainer decision in SpecPM.

## Non-Authority Boundary

The proposal cannot accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, create a SpecPM pull request, run
`prepare-accepted-entry`, run `accepted-package-update-proposal`, replace
author or SpecPM maintainer review, or treat producer output as accepted
SpecPM truth.

See also <doc:LimitedPopularLibrarySelectedHandoffDryRun>,
<doc:LimitedPopularLibraryCandidateLayerTriage>, and <doc:SpecPMHandoff>.
