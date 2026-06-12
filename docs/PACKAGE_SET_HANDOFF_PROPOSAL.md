# Package-Set Handoff Proposal

Status: Producer-side SpecPM handoff artifact

`package-set-handoff-proposal` turns a generated package-set output directory
into reviewable SpecPM proposal evidence. It is the package-set counterpart to
single-package proposal artifacts: it summarizes the aggregate package, scoped
member packages, relation proposals, bundle-set preflight status, viewer
artifacts, and the external registry acceptance decision boundary.

The command does not open a SpecPM pull request. It prepares deterministic JSON
and Markdown that a future trusted workflow or maintainer can attach to a
SpecPM review.

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

## Inputs

Required package-set artifacts:

- `package-set-draft.json`
- `package-relation-proposals.json`

Optional review artifacts:

- `bundle-set-preflight.json`
- package-set viewer output containing `index.html` and `package-set.json`

## Author-Ready Stop Summary

The proposal includes `authorReadyDraftSummary`, aggregated from member
`member_quality_report` evidence. It records:

- `status`: aggregate `author_ready_draft`, `needs_regeneration`, or `blocked`;
- `decision`: `stop_for_author_review`, `continue_generation`, or
  `blocked_until_inputs_change`;
- `memberCounts`: total and per-status member counts;
- `blockingReasons`: blocked member reports and stop reasons;
- `topAuthorActionItems`: the first deterministic author review actions.

This is a producer-loop stop signal. It does not accept packages, accept
relations, or replace SpecPM maintainer review.

## Author Review Checklist

The proposal also includes `authorReview`, derived from the same
`authorReadyDraftSummary` and member quality reports. JSON consumers get the
same review surface as the package-set viewer, while the generated Markdown
body includes human-facing sections:

- `Author Review Checklist`
- `Weak Claims and Evidence Gaps`
- `Recommended Edits`

The checklist explains whether generation should stop for author review,
continue because warning-level gaps need regeneration, or block until failed
inputs are repaired. Weak claims summarize reviewable dimensions such as
`repositorySpecificity`, `packageTopology`, and `claimConservatism`. Evidence
gaps call out missing or weak support from member action items and quality
dimensions. Recommended edits tell the author what to inspect first: package
identity, summaries, capabilities, intents, constraints, evidence references,
and downstream validation.

These sections are author handoff guidance only. They are not SpecPM registry
acceptance, not maintainer approval, and not upstream project endorsement.

## Evidence Roles

The proposal records stable evidence links for:

- `package_set_draft`
- `package_relation_proposals`
- `bundle_set_preflight`
- `package_set_viewer`
- `member_candidate_bundle`
- `member_manifest`
- `member_boundary_spec`
- `member_producer_receipt`
- `member_validation_report`
- `member_diagnostics`
- `member_quality_report`
- `package_relation_summary`

These links are evidence only. Missing optional links can be marked `expected`;
required package-set artifacts must exist and have the expected identity.

## Acceptance Boundary

Every proposal includes:

`registryAcceptanceDecision.status: external_required` is the stable summary
phrase used by docs and review checks.

```json
{
  "registryAcceptanceDecision": {
    "status": "external_required",
    "requiredFor": ["public_index_acceptance", "package_relation_acceptance"],
    "recordKind": "SpecPMRegistryAcceptanceDecision",
    "producerAuthority": "evidence_only"
  }
}
```

SpecHarvester can propose evidence. SpecPM validates package shape and registry
policy. Maintainers accept or reject packages and relations.

The command does not accept packages, accept relations, publish public registry
metadata, mutate SpecPM sources, execute package code, run package managers, or
replace SpecPM maintainer review.

## Relation To P25

Phase 25 proves the package-set producer pipeline:

```text
workspace inventory -> draft-package-set -> preflight-bundle-set -> render-package-set-site
```

P26-T1 adds the handoff layer that turns those artifacts into proposal evidence
for SpecPM review.

## Relation To Fresh Refresh Decisions

Use `fresh-candidate-refresh-run` when the same package-set output needs to be
compared against current SpecPM generated artifacts:

```bash
python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set .smoke/xyflow-package-set/package-set \
  --fresh-generated-root .smoke/xyflow-package-set/fresh-generated \
  --output .smoke/xyflow-package-set/fresh-candidate-refresh-run.json
```

The handoff proposal explains review context. The fresh refresh run prepares
the `<package_id>/<version>/specpm.yaml` and `specs/*.spec.yaml` layout plus
digests that SpecPM's `prepare-refresh-decision` helper can compare.
