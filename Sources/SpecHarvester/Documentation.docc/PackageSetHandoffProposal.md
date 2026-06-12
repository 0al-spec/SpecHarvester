# Package-Set Handoff Proposal

`package-set-handoff-proposal` turns a generated package-set output directory
into reviewable SpecPM proposal evidence.

It summarizes the aggregate package, scoped member packages, relation
proposals, bundle-set preflight status, package-set viewer artifacts, and the
external registry acceptance decision boundary.

The required source artifacts are `package-set-draft.json` and
`package-relation-proposals.json`. `bundle-set-preflight.json` is optional
review evidence and is included when present.

## Author-Ready Stop Summary

The proposal includes `authorReadyDraftSummary`, aggregated from member
`member_quality_report` evidence. It records aggregate `status`, deterministic
`decision`, `memberCounts`, blocked member `blockingReasons`, and
`topAuthorActionItems`. The clean-path decision is `stop_for_author_review`;
warning and blocked paths use `continue_generation` and
`blocked_until_inputs_change`.

This is a producer-loop stop signal. It does not accept packages, accept
relations, or replace SpecPM maintainer review.

## Command

```bash
python3 -m spec_harvester package-set-handoff-proposal \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --viewer .smoke/xyflow-package-set/viewer \
  --output .smoke/xyflow-package-set/handoff/proposal.json \
  --proposal-body .smoke/xyflow-package-set/handoff/proposal.md
```

## Payload Identity

```json
{
  "apiVersion": "spec-harvester.package-set-handoff-proposal/v0",
  "kind": "SpecHarvesterPackageSetHandoffProposal",
  "schemaVersion": 1
}
```

## Evidence Roles

The proposal records `package_set_draft`, `package_relation_proposals`,
`bundle_set_preflight`, `package_set_viewer`, `member_candidate_bundle`,
`member_manifest`, `member_boundary_spec`, `member_producer_receipt`,
`member_validation_report`, `member_diagnostics`, `member_quality_report`, and
`package_relation_summary` evidence links.

## Boundary

Every proposal includes `registryAcceptanceDecision.status: external_required`
for `public_index_acceptance` and `package_relation_acceptance`.

The command does not accept packages, accept relations, publish public registry
metadata, mutate SpecPM sources, execute package code, run package managers, or
replace SpecPM maintainer review.
