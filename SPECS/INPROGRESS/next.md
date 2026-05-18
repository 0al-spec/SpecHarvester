# Recommended Task: P7-T3 - Distinguish absent license evidence from ambiguous unknown license evidence

**Priority:** P7
**Phase:** Smoke-Test Signal Quality
**Effort:** Medium
**Dependencies:** P6-T2, P7-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P7-T3-license-evidence-classification`
**Review Subject:** `p7_t3_license_evidence_classification`

**Current Phase:** SELECT

## Description

The local smoke license/provenance report now has one remaining medium-risk
`unknown_license` issue for `puzzle.core`. The current report does not explain
whether `UNKNOWN` means no license evidence was found or license-like evidence
was present but could not be classified.

Distinguish absent license evidence from ambiguous unknown license evidence so
reviewers can prioritize missing upstream metadata differently from
unclassifiable license text.

## Acceptance Criteria

- License provenance records include enough evidence classification to separate
  absent license metadata from ambiguous license evidence.
- `UNKNOWN` generated from no manifest license and no license file hint is
  reported differently from unrecognized license-like evidence.
- Existing SPDX-like known license handling remains unchanged.
- Report output remains deterministic and sorted.
- Coverage remains above the project threshold.

## Recently Archived

- `P7-T1` Treat package namespace matches against upstream repository names as
  valid namespace evidence: PASS,
  `SPECS/ARCHIVE/P7-T1_Treat_Package_Namespace_Matches_Against_Upstream_Repository_Names_as_Valid_Namespace_Evidence/`.
- `P7-T2` Derive less generic Swift package intents from package products and
  manifests: PASS,
  `SPECS/ARCHIVE/P7-T2_Derive_Less_Generic_Swift_Package_Intents_from_Package_Products_and_Manifests/`.

## Next Step

Plan task `P7-T3` when ready.

## Backlog Note

`P8` is planned for accepted specification update lifecycle work after the
smoke-test signal quality tasks. It covers immutable accepted versions,
accepted-vs-candidate diffing, update impact classification, PR-ready SpecPM
update proposals, and correction/errata handling for accepted metadata fixes.
