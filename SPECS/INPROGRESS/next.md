# Next Task: P26-T1 Package-Set Handoff Proposal Artifact

**Status:** Selected
**Last Archived:** P25-T7 Xyflow Package-Set Smoke Scenario
**Archived:** 2026-06-07

## Recently Archived

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

- Phase 25 proves the package-set producer pipeline works as plumbing.
- Operators still need a SpecPM handoff artifact that explains what should be
  reviewed: aggregate package, scoped members, relation proposals, preflight
  status, viewer output, and acceptance boundary.
- The existing accepted package update proposal flow is single-package oriented
  and does not model package-set relations.

## Goal

- Add a deterministic package-set handoff proposal artifact that converts a
  generated bundle-set output into reviewable SpecPM proposal evidence without
  accepting packages or relations automatically.

## Next Step

Start `P26-T1` by adding the JSON/Markdown builder and CLI command for
`package-set-handoff-proposal`.
