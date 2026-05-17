# Recommended Task: P6-T1 - Discover nested Swift package manifests during static harvest

**Priority:** P6
**Phase:** Smoke-Test Feedback
**Effort:** Medium
**Dependencies:** P3-T2, P3-T3
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P6-T1-discover-nested-swift-package-manifests`
**Review Subject:** `p6_t1_nested_swift_package_manifest_discovery`

**Current Phase:** SELECT

## Description

The local smoke test against `cupertino`, `xyflow`, `docc2context`, and `Puzzle`
showed that `cupertino` was downgraded to medium confidence because the current
collector did not recognize its nested `Packages/Package.swift` file as package
manifest evidence.

Add deterministic static discovery for nested Swift package manifests while
preserving the current trust boundary: no SwiftPM invocation, no package-script
execution, no network access, and no dependency installation.

## Acceptance Criteria

- `collect-local` and `collect-batch` can collect allowlisted nested
  `Package.swift` files.
- Batch validation confidence recognizes nested Swift package manifests as
  package-manifest evidence.
- Existing JavaScript/TypeScript package manifest behavior is unchanged.
- Focused tests cover nested Swift package discovery and confidence reporting.
- Coverage remains above the project threshold.

## Smoke-Test Evidence

- `cupertino`: collected 3 files but `packageManifestCount` was `0`; warning
  `no_package_manifests`.
- `xyflow`: high confidence with 4 package manifests.
- `docc2context`: high confidence with 1 package manifest.
- `Puzzle`: high confidence with 1 package manifest.

## Recently Archived

- `P5-T1` Add duplicate intent and capability claim report: PASS,
  `SPECS/ARCHIVE/P5-T1_Add_Duplicate_Intent_and_Capability_Claim_Report/`.
- `P5-T2` Add namespace and upstream relationship review report: PASS,
  `SPECS/ARCHIVE/P5-T2_Add_Namespace_and_Upstream_Relationship_Review_Report/`.
- `P5-T3` Add license and provenance risk report: PASS,
  `SPECS/ARCHIVE/P5-T3_Add_License_and_Provenance_Risk_Report/`.

## Next Step

Plan task `P6-T1` when ready.
