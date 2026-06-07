# Next Task: Phase 25 Complete

**Status:** Phase Complete
**Last Archived:** P25-T7 Xyflow Package-Set Smoke Scenario
**Archived:** 2026-06-07

## Recently Archived

- `P25-T7` added `xyflow-package-set-smoke`, a deterministic local synthetic
  scenario that writes a fixture checkout, source manifest, workspace inventory,
  `package-set-draft.json`, `package-relation-proposals.json`,
  `bundle-set-preflight.json`, static viewer output, and
  `xyflow-package-set-smoke.json` summary.
- `P25-T6` added `render-package-set-site`, a static viewer path for generated
  package-set outputs.
- `P25-T5` added `preflight-bundle-set`, a producer-side verifier for generated
  package-set output directories.

## Completed Phase

Phase 25 now covers the package-set monorepo discovery path:

- workspace inventory;
- package-set and scoped member candidate drafting;
- producer-observed relation proposals;
- bundle-set preflight;
- static package-set viewer;
- local `xyflow` end-to-end smoke scenario.

## Suggested Next Planning Step

Define a new phase for package-set handoff/proposal automation between
SpecHarvester and SpecPM. Candidate themes:

- package-set proposal body generation;
- package-set relation evidence links;
- SpecPM-side package-set preflight handoff;
- package-set viewer artifact upload or PR attachment strategy;
- maintainer acceptance workflow for package-set relations.
