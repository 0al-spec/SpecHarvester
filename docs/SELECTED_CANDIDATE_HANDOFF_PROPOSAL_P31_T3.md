# SpecPM Selected Candidate Handoff Proposal

## Summary

- Selected candidates: 3
- Deferred candidates: 6
- Required evidence roles: 11
- Registry acceptance decision: `external_required`
- Authority: `producer_preview_evidence_only`

## Selected Candidates

| Candidate | Repository | Producer preflight | Viewer | Registry acceptance |
| --- | --- | --- | --- | --- |
| `flask.core` | `flask` | `passed` | `ok` | `external_required` |
| `gin.core` | `gin` | `passed` | `ok` | `external_required` |
| `docc2context.core` | `docc2context` | `passed` | `ok` | `external_required` |

## Deferred Candidates

| Candidate | Reason | Required action |
| --- | --- | --- |
| `xyflow.workspace` | `needs_regeneration` | Regenerate package-set AI draft evidence with package-set identity. |
| `xyflow.react` | `needs_regeneration` | Regenerate package-set AI draft evidence with package-set identity. |
| `xyflow.svelte` | `needs_regeneration` | Regenerate package-set AI draft evidence with package-set identity. |
| `xyflow.system` | `needs_regeneration` | Regenerate package-set AI draft evidence with package-set identity. |
| `cupertino.core` | `needs_regeneration` | Regenerate AI enrichment or provide an author-curated summary. |
| `navigation_split_view.core` | `needs_regeneration` | Resolve package id normalization before handoff. |

## Required Evidence Roles

- `candidate_bundle` (selected_candidate): candidate bundle root
- `manifest` (selected_candidate): specpm.yaml
- `boundary_spec` (selected_candidate): specs/*.spec.yaml
- `producer_receipt` (selected_candidate): producer-receipt.json
- `validation_report` (selected_candidate): validation-report.json
- `diagnostics` (selected_candidate): diagnostics.json
- `quality_report` (selected_candidate): author-ready-draft-quality-report.json
- `producer_preflight` (selected_candidate): preflight/<package_id>.json
- `static_viewer` (selected_candidate): viewer/<package_id>/index.html
- `static_viewer_payload` (selected_candidate): viewer/<package_id>/spec-package.json
- `selected_handoff_dry_run` (proposal): tests/fixtures/limited_popular_library_selected_handoff_dry_run/p30-t5-limited-popular-libraries.example.json

## Maintainer Checklist

- Verify selected candidate identity, namespace, and package version before intake.
- Verify every required evidence role and digest before trusting the handoff.
- Run SpecPM-side validation and preflight before any accepted-source change.
- Reject or request regeneration for weak evidence, package identity drift, or warning-bearing generated claims.
- Record the external registry acceptance decision outside producer evidence.

## Non-Authority Boundary

- This proposal is review evidence only.
- It is not SpecPM registry acceptance.
- It does not accept packages.
- It does not accept relations.
- It does not seed baselines.
- It does not remove preview_only.
- It does not publish registry metadata.
- It does not create a SpecPM pull request.
- It does not run prepare-accepted-entry.
- It does not run accepted-package-update-proposal.

This proposal does not accept packages, accept relations, seed baselines, remove `preview_only`, publish registry metadata, create a SpecPM pull request, or replace SpecPM maintainer review.
