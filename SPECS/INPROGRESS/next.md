# Recommended Task: P6-T2 - Infer candidate license metadata from allowlisted LICENSE files

**Priority:** P6
**Phase:** Smoke-Test Feedback
**Effort:** Medium
**Dependencies:** P5-T3, P6-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P6-T2-infer-candidate-license-metadata-from-license-files`
**Review Subject:** `p6_t2_license_file_metadata_inference`

**Current Phase:** SELECT

## Description

The local smoke test against `cupertino`, `xyflow`, `docc2context`, and `Puzzle`
showed that Swift-oriented candidates often get `metadata.license: UNKNOWN`
even when allowlisted `LICENSE` files are present in the harvested evidence.

Add deterministic license inference from collected static license files so the
candidate drafter can avoid avoidable `unknown_license` advisory findings
without executing repository code or trusting unreviewed content as authority.

## Acceptance Criteria

- The collector continues to collect allowlisted `LICENSE`, `LICENSE.md`, and
  `COPYING` files as static evidence.
- The drafter can infer common license identifiers from bounded license-file
  text when package manifest metadata has no license.
- License inference records only conservative identifiers and leaves ambiguous
  files as `UNKNOWN`.
- Existing package-manifest license metadata remains preferred.
- Focused tests cover MIT-style license-file inference and ambiguous fallback.
- Coverage remains above the project threshold.

## Recently Archived

- `P5-T2` Add namespace and upstream relationship review report: PASS,
  `SPECS/ARCHIVE/P5-T2_Add_Namespace_and_Upstream_Relationship_Review_Report/`.
- `P5-T3` Add license and provenance risk report: PASS,
  `SPECS/ARCHIVE/P5-T3_Add_License_and_Provenance_Risk_Report/`.
- `P6-T1` Discover nested Swift package manifests during static harvest: PASS,
  `SPECS/ARCHIVE/P6-T1_Discover_Nested_Swift_Package_Manifests_during_Static_Harvest/`.

## Next Step

Plan task `P6-T2` when ready.
