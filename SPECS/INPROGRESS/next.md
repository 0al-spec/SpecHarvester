# Recommended Task: P7-T4 - Add a compact local smoke triage summary for batch and governance report output

**Priority:** P7
**Phase:** Smoke-Test Signal Quality
**Effort:** Medium
**Dependencies:** P6-T4, P7-T1, P7-T2, P7-T3
**Status:** Open
**Updated:** 2026-05-18
**Suggested Branch:** `feature/P7-T4-local-smoke-triage-summary`
**Review Subject:** `p7_t4_local_smoke_triage_summary`

**Current Phase:** SELECT

## Description

Local smoke runs now generate batch validation, duplicate governance,
namespace/upstream, and license/provenance outputs. Reviewers still need to
open multiple JSON reports to understand whether a run is clean, which issues
remain, and whether those issues are expected review signals.

Add a compact deterministic smoke triage summary that can be generated from the
existing local smoke output without committing generated candidates.

## Acceptance Criteria

- Smoke triage output summarizes batch status and governance issue counts in a
  compact reviewable format.
- The summary distinguishes duplicate, namespace/upstream, and
  license/provenance signals.
- The summary can point reviewers to the detailed report files.
- The command or documented workflow remains local-only and deterministic.
- Coverage remains above the project threshold.

## Recently Archived

- `P7-T2` Derive less generic Swift package intents from package products and
  manifests: PASS,
  `SPECS/ARCHIVE/P7-T2_Derive_Less_Generic_Swift_Package_Intents_from_Package_Products_and_Manifests/`.
- `P7-T3` Distinguish absent license evidence from ambiguous unknown license
  evidence: PASS,
  `SPECS/ARCHIVE/P7-T3_Distinguish_Absent_License_Evidence_from_Ambiguous_Unknown_License_Evidence/`.

## Next Step

Plan task `P7-T4` when ready.

## Backlog Note

`P8` is planned for accepted specification update lifecycle work after the
smoke-test signal quality tasks. It covers immutable accepted versions,
accepted-vs-candidate diffing, update impact classification, PR-ready SpecPM
update proposals, and correction/errata handling for accepted metadata fixes.
