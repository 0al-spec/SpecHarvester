# Selected Candidate Handoff Proposal

Status: P31-T1 producer-side contract.

This page defines `SpecHarvesterSelectedCandidateHandoffProposal`, the portable
handoff envelope for selected preview candidates. It turns P30-style selected
candidate dry-run evidence into SpecPM review evidence without treating the
producer as a registry authority.

The machine-readable companion fixture is:

```text
tests/fixtures/selected_candidate_handoff_proposal/p31-t1-selected-candidate-handoff.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.selected-candidate-handoff-proposal/v0",
  "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

The proposal consumes already-reviewed producer evidence:

- P30-T4 candidate-layer triage:
  `tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json`;
- P30-T5 selected handoff dry run:
  `tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json`.

It does not run another scrape, call LM Studio, clone repositories, install
dependencies, generate accepted-source content, or create a SpecPM pull
request.

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

`--selected-handoff-dry-run` is required. The candidate, preflight, and viewer
roots are optional, but when they are provided the helper reads those local
files and computes SHA-256 digests for present artifacts. Missing files remain
expected evidence with the digest recorded by the selected handoff dry-run
source.

The helper rejects a selected candidate unless it remains `previewOnly: true`,
has producer preflight `passed` with `0` warnings and `0` errors, has static
viewer status `ok`, and keeps
`registryAcceptanceDecision.status: external_required` with
`producerAuthority: evidence_only`.

## P31-T3 Real Dry Run

P31-T3 runs the helper on the recorded P30-T5 selected candidate evidence and
commits both generated artifacts:

```text
tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json
docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md
```

The fixture records the real P30 selected candidates `flask.core`, `gin.core`,
and `docc2context.core`. It preserves `producer_preview_evidence_only`
authority, `previewOnly: true`, zero-warning producer preflight, static viewer
status `ok`, and `registryAcceptanceDecision.status: external_required`.

The P31-T3 artifact is still not SpecPM acceptance. It does not create a
SpecPM pull request, does not accept packages, does not accept relations, seed
baselines, remove `preview_only`, or publish registry metadata.

## Selected Candidates

The example proposal includes exactly three selected candidates:

| Candidate | Repository | Producer preflight | Viewer | Registry acceptance |
| --- | --- | --- | --- | --- |
| `flask.core` | Flask | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `gin.core` | Gin | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |
| `docc2context.core` | docc2context | `passed`, `0` warnings, `0` errors | `ok` | `external_required` |

Every selected candidate remains `previewOnly: true`. Passing
producer-side preflight is review evidence only. It is not SpecPM acceptance,
does not remove `preview_only`, and does not publish registry metadata.

## Required Evidence Roles

Each selected candidate must provide stable evidence roles:

| Role | Scope | Required evidence |
| --- | --- | --- |
| `candidate_bundle` | candidate | Candidate bundle root |
| `manifest` | candidate | `specpm.yaml` |
| `boundary_spec` | candidate | `specs/*.spec.yaml` |
| `producer_receipt` | candidate | `producer-receipt.json` |
| `validation_report` | candidate | `validation-report.json` |
| `diagnostics` | candidate | `diagnostics.json` |
| `quality_report` | candidate | `author-ready-draft-quality-report.json` |
| `producer_preflight` | candidate | Candidate bundle preflight report |
| `static_viewer` | candidate | Static viewer `index.html` |
| `static_viewer_payload` | candidate | Static viewer `spec-package.json` |
| `selected_handoff_dry_run` | proposal | P30-T5 selected dry-run fixture |

The fixture records SHA-256 digests for the contract-bearing files, producer
preflight reports, and static viewer artifacts that came from P30-T5.

## Deferred Candidates

The proposal explicitly keeps the six P30 deferred candidates out of selected
handoff:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `cupertino.core`;
- `navigation_split_view.core`.

All six remain `needs_regeneration`. They require targeted regeneration,
package identity fixes, author-supplied summary evidence, warning resolution,
or package-set-specific review before they can enter a selected handoff
proposal.

## Maintainer Checklist

Before SpecPM intake, a maintainer should:

- verify selected candidate identity, namespace, and package version;
- verify every required evidence role and digest;
- run SpecPM-side validation and preflight;
- reject or request regeneration for weak evidence, package identity drift, or
  warning-bearing generated claims;
- record the external registry acceptance decision outside producer evidence.

## Future SpecPM Boundary

SpecPM may later add consumer-side preflight for
`SpecHarvesterSelectedCandidateHandoffProposal`. That preflight can verify the
proposal identity, selected candidate list, deferred candidate list, evidence
roles, preflight status, viewer status, and non-authority statements.
This is the future SpecPM-side preflight contract target.

It still cannot make producer evidence authoritative. Acceptance remains an
external maintainer decision in SpecPM.

## Non-Authority Boundary

The proposal cannot:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- run `prepare-accepted-entry`;
- run `accepted-package-update-proposal`;
- replace author or SpecPM maintainer review;
- treat producer output as accepted SpecPM truth.

See also:

- [`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md)
- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
