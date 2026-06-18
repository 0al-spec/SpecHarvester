# Next Task: Phase 37 Complete

**Status:** Complete
**Branch:** `main`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T8 Harvest Manifest Evidence for Repository Profile Detection

## Recently Archived

- `P37-T8` made repository profile detection consume harvested package manifest
  evidence when workspace inventory has no manifest records.
- Autonomous batch still prefers `workspace-inventory.json` workspace/member
  manifest evidence when available.
- When workspace inventory is empty, repository profile detection now falls
  back to already-collected `harvest.json` files with `kind:
  package_manifest` or `kind: workspace_manifest`.
- A root-manifest single-package checkout now selects
  `generic.single_package.v0` with high confidence using harvested manifest
  evidence such as `go.mod`.
- Disabled profile selection still records `decision: disabled`; ambiguous and
  conflicting evidence still falls back instead of silently selecting a profile.
- Docs and DocC now describe the harvested-manifest fallback path.
- Harvested manifest paths remain producer-side evidence only. They do not
  accept packages, do not accept relations, do not publish registry metadata,
  do not remove `preview_only`, do not treat manifests as registry truth, and
  do not replace maintainer review.

## Phase Summary

Phase 37 introduced a language- and framework-agnostic repository profile
selection layer:

- P37-T1 documented the selection contract.
- P37-T2 added the machine-readable detection fixture.
- P37-T3 added the opt-in CLI/report surface.
- P37-T4 connected selection to autonomous candidate batch sidecar evidence.
- P37-T5 added the generic discovery hint vocabulary.
- P37-T6 added cross-ecosystem fixtures.
- P37-T7 recorded a real FastMCP auto-selection comparison.
- P37-T8 closed the harvested-manifest evidence gap found by P37-T7.

## Suggested Next Planning Area

Start a new phase before implementation. The likely next planning area is
turning repository profile decisions and parser profiles into a broader,
language- and framework-agnostic plugin subsystem with explicit plugin
registration, evidence producers, applicability checks, and deterministic
selection boundaries.

## Boundary

Repository profile selection remains producer-side evidence. It can improve
operator targeting for candidate generation, but it does not accept generated
package claims or registry state.
