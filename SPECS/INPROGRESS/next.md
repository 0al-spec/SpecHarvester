# Recommended Task: P7-T2 - Derive less generic Swift package intents from package products and manifests

**Priority:** P7
**Phase:** Smoke-Test Signal Quality
**Effort:** Medium
**Dependencies:** P6-T1, P7-T1
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P7-T2-swift-package-product-intents`
**Review Subject:** `p7_t2_swift_package_product_intents`

**Current Phase:** PLAN

## Description

The local smoke governance report still shows duplicate generic
`intent.package.public_repository_metadata` claims across Swift candidates.
Swift package manifests already expose product and package metadata that can
support more specific deterministic intent claims for candidates such as
Cupertino, docc2context, and Puzzle.

Use static Swift package manifest evidence to derive less generic package
intents when product names or manifest metadata provide reviewable signals.

## Acceptance Criteria

- Swift package candidates avoid duplicate generic metadata intents when package
  product evidence supports a more specific deterministic intent.
- Intent derivation remains static and does not execute SwiftPM or package code.
- Existing JavaScript/TypeScript intent behavior remains unchanged.
- Generated intent IDs stay deterministic and sorted.
- Coverage remains above the project threshold.

## Recently Archived

- `P6-T4` Add reproducible local smoke-test fixture documentation: PASS,
  `SPECS/ARCHIVE/P6-T4_Add_Reproducible_Local_Smoke-Test_Fixture_Documentation/`.
- `P7-T1` Treat package namespace matches against upstream repository names as
  valid namespace evidence: PASS,
  `SPECS/ARCHIVE/P7-T1_Treat_Package_Namespace_Matches_Against_Upstream_Repository_Names_as_Valid_Namespace_Evidence/`.

## Next Step

Create `SPECS/INPROGRESS/P7-T2_Derive_Less_Generic_Swift_Package_Intents_from_Package_Products_and_Manifests.md`
with implementation scope and validation gates.

## Backlog Note

`P8` is planned for accepted specification update lifecycle work after the
smoke-test signal quality tasks. It covers immutable accepted versions,
accepted-vs-candidate diffing, update impact classification, PR-ready SpecPM
update proposals, and correction/errata handling for accepted metadata fixes.
