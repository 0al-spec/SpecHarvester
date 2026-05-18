# Recommended Task: P7-T1 - Treat package namespace matches against upstream repository names as valid namespace evidence

**Priority:** P7
**Phase:** Smoke-Test Signal Quality
**Effort:** Medium
**Dependencies:** P5-T2, P6-T3, P6-T4
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P7-T1-upstream-repository-name-namespace-evidence`
**Review Subject:** `p7_t1_upstream_repository_name_namespace_evidence`

**Current Phase:** PLAN

## Description

The reproducible local smoke run collected and drafted Cupertino, xyflow,
docc2context, and Puzzle successfully with high batch confidence, but namespace
governance reports still emitted four `upstream_namespace_mismatch` issues.

The current report compares the package namespace only against the GitHub owner
parsed from `upstream_repository`. For smoke candidates such as `xyflow.core`,
`docc2context.core`, and `puzzle.core`, the package namespace matches the
repository name rather than the repository owner. That is valid namespace
evidence and should not be reported as an owner mismatch.

## Smoke Triage Context

- `batch-validation.json`: `collectedCount=4`, `highConfidenceCount=4`,
  `warningCount=0`.
- `governance-claims.json`: one duplicate generic intent claim across Swift
  candidates.
- `namespace-upstream.json`: four namespace/upstream mismatch issues caused by
  owner-vs-repository-name comparison.
- `license-provenance.json`: one `unknown_license` issue for `puzzle.core` and
  four low-severity namespace mismatch echoes.

## Acceptance Criteria

- Namespace/upstream report parsing extracts both upstream owner and upstream
  repository name for GitHub HTTPS and SSH URLs.
- Namespace mismatch checks treat a package namespace as valid when it matches
  either upstream owner or upstream repository name case-insensitively.
- Existing behavior around missing upstream info, duplicate upstream artifacts,
  malformed URIs, and deterministic sorting is preserved.
- License provenance report no longer echoes namespace mismatch risk when the
  namespace matches the upstream repository name.
- Coverage remains above the project threshold.

## Recently Archived

- `P6-T1` Discover nested Swift package manifests during static harvest: PASS,
  `SPECS/ARCHIVE/P6-T1_Discover_Nested_Swift_Package_Manifests_during_Static_Harvest/`.
- `P6-T2` Infer candidate license metadata from allowlisted LICENSE files: PASS,
  `SPECS/ARCHIVE/P6-T2_Infer_Candidate_License_Metadata_from_License_Files/`.
- `P6-T3` Make namespace and upstream owner comparison case-insensitive: PASS,
  `SPECS/ARCHIVE/P6-T3_Make_Namespace_Upstream_Owner_Comparison_Case_Insensitive/`.
- `P6-T4` Add reproducible local smoke-test fixture documentation: PASS,
  `SPECS/ARCHIVE/P6-T4_Add_Reproducible_Local_Smoke-Test_Fixture_Documentation/`.

## Next Step

Create `SPECS/INPROGRESS/P7-T1_Treat_Package_Namespace_Matches_Against_Upstream_Repository_Names_as_Valid_Namespace_Evidence.md`
with implementation scope and validation gates.

## Backlog Note

`P8` is planned for accepted specification update lifecycle work after the
smoke-test signal quality tasks. It covers immutable accepted versions,
accepted-vs-candidate diffing, update impact classification, PR-ready SpecPM
update proposals, and correction/errata handling for accepted metadata fixes.
