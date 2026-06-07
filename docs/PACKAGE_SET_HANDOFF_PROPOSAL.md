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
