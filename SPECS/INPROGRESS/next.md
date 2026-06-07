# Next Task: P26-T3 SpecPM Package-Set Proposal Intake Checklist

**Status:** Selected
**Last Archived:** P26-T2 Trusted Package-Set Proposal Workflow Inputs
**Archived:** 2026-06-07

## Recently Archived

- `P26-T2` wired `package-set-handoff-proposal` into the trusted
  `propose-to-specpm.yml` workflow as a dry-run evidence mode. Operators can
  select `proposal_kind: package_set`, provide package-set bundle/viewer paths,
  and upload `package-set-handoff-proposal.json` plus
  `package-set-handoff-proposal.md` without using `SPECPM_PROPOSAL_TOKEN` or
  creating a SpecPM PR.
- `P26-T1` added the package-set handoff proposal artifact itself, including
  aggregate/member candidates, `contains` relation proposals, bundle-set
  preflight status, viewer links, evidence roles, and
  `registryAcceptanceDecision.status: external_required`.
- `P25-T7` added `xyflow-package-set-smoke`, a deterministic local synthetic
  package-set scenario with package-set draft, relation proposals, bundle-set
  preflight, viewer output, and smoke summary. The key artifacts remain
  `package-set-draft.json`, `package-relation-proposals.json`,
  `bundle-set-preflight.json`, and `xyflow-package-set-smoke.json`.

## Motivation

- SpecHarvester can now produce and upload package-set handoff evidence, but
  SpecPM maintainers still need an explicit intake checklist before accepting
  member packages or relation proposals.
- Package-set evidence includes multiple candidate bundles and relation
  records. The existing single-package proposal checklist is not specific
  enough for aggregate/member review.
- The acceptance boundary must remain explicit: SpecHarvester proposes
  evidence, SpecPM validates and records registry acceptance decisions.

## Goal

- Define the SpecPM-side package-set proposal intake checklist and evidence
  roles required before maintainers accept package members or relations.

## Next Step

Start `P26-T3` by documenting the SpecPM intake checklist expected for
`package-set-handoff-proposal.json` and its linked candidate/member evidence.
