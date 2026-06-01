# REVIEW REPORT — p21_t2_producer_receipt_emission

**Task:** P21-T2 — Producer Receipt Emission
**Date:** 2026-06-02
**Reviewer:** Codex
**Verdict:** PASS

## Scope Reviewed

- `src/spec_harvester/producer_receipt.py`
- `src/spec_harvester/drafter.py`
- `tests/test_collector.py`
- P21-T2 Flow archive and validation report

## Findings

No blocking findings.

## Checks

- `draft_spec_package()` now writes `producer-receipt.json` after generated
  candidate files are written, so output digests are calculated from final file
  bytes.
- Receipt `outputs[]` includes `specpm.yaml`, generated BoundarySpec files, and
  optional `public-interface-index.json`.
- Receipt `outputs[]` excludes `producer-receipt.json`, preserving the
  self-hash boundary.
- Receipt defaults preserve the human-review boundary:
  `humanReview.status: required` and
  `humanReview.requiredFor: public_index_acceptance`.
- Validation and diagnostics are represented as placeholders only:
  `validation.status: not_run` and `diagnostics.status: clean`.

## Residual Risks

- `issuedAt` is intentionally time-based. `receiptId` does not include it, but
  the receipt file bytes are not identical across repeated draft runs. This is
  acceptable for P21-T2 because the receipt is excluded from `outputs[]`; P21-T4
  can decide whether preflight should tolerate timestamp-only drift.
- P21-T2 does not write `validation-report.json` or `diagnostics.json`; P21-T3
  must update receipt `outputs[]`, `validation.reportDigest`, and
  `diagnostics.digest` once those files exist.
- Producer source revision is not recorded yet because the current package does
  not expose a stable build-time revision. If SpecPM requires exact generator
  revision for public handoff, add it as a future packaging/release task.

## Follow-Up

No new follow-up tasks required. The remaining items are already covered by
P21-T3 and P21-T4.
