# Next Task: P26-T2 Trusted Package-Set Proposal Workflow Inputs

**Status:** Selected
**Last Archived:** P26-T1 Package-Set Handoff Proposal Artifact
**Archived:** 2026-06-07

## Recently Archived

- `P26-T1` added `package-set-handoff-proposal`, a deterministic JSON/Markdown
  handoff artifact for generated package-set bundles. It records aggregate and
  member candidates, `contains` relation proposals, preflight status, viewer
  links, evidence roles, and `registryAcceptanceDecision.status:
  external_required`.
- `P25-T7` added `xyflow-package-set-smoke`, a deterministic local synthetic
  scenario that writes workspace inventory, package-set draft, relation
  proposals, bundle-set preflight, viewer output, and smoke summary.
  Key handoff inputs now available for P26 are `package-set-draft.json`,
  `package-relation-proposals.json`, `bundle-set-preflight.json`, and the
  package-set static viewer output. The smoke summary is
  `xyflow-package-set-smoke.json`.
- `P25-T6` added `render-package-set-site`, a static viewer path for generated
  package-set outputs.
- `P25-T5` added `preflight-bundle-set`, a producer-side verifier for generated
  package-set output directories.

## Motivation

- `P26-T1` creates local review evidence, but trusted automation still needs a
  workflow path that can generate and attach those artifacts safely.
- Cross-repository write credentials must remain unavailable to untrusted pull
  request events.
- Operators need a dry-run path before letting package-set proposal evidence
  participate in any SpecPM handoff workflow.

## Goal

- Extend trusted SpecPM proposal automation or dry-run workflow inputs so
  package-set handoff proposal artifacts can be generated, uploaded, and
  attached as review evidence without granting cross-repository write
  credentials to untrusted events.

## Next Step

Start `P26-T2` by wiring `package-set-handoff-proposal` into the trusted
proposal/dry-run workflow path and documenting the credential boundary.
