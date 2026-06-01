# REVIEW REPORT — p21_t3_validation_diagnostics_report_emission

**Task:** P21-T3 — Validation and Diagnostics Report Emission
**Date:** 2026-06-02
**Reviewer:** Codex
**Verdict:** PASS

## Scope Reviewed

- `src/spec_harvester/producer_reports.py`
- `src/spec_harvester/producer_receipt.py`
- `src/spec_harvester/drafter.py`
- `tests/test_collector.py`
- P21-T3 Flow archive and validation report

## Findings

No blocking findings.

## Checks

- `draft_spec_package()` now writes `validation-report.json` and
  `diagnostics.json` before `producer-receipt.json`.
- Receipt `outputs[]` includes both report files with digest roles
  `validation_report` and `diagnostics`.
- Receipt `validation.reportDigest` matches `validation-report.json` bytes.
- Receipt `diagnostics.digest` matches `diagnostics.json` bytes.
- Clean report output uses `validation.status: valid` and
  `diagnostics.status: clean`.
- Diagnostics entries include privacy and human-review boundary notes without
  implying SpecPM acceptance.
- `producer-receipt.json` remains excluded from `outputs[]`.

## Residual Risks

- P21-T3 emits producer-side report artifacts but does not verify a complete
  bundle after receipt emission. P21-T4 must perform that preflight check.
- The validation report is intentionally producer-side shape evidence, not
  SpecPM validation authority.
- Diagnostics entries are compact policy notes. P21-T4 should decide which
  diagnostics become blocking preflight errors.

## Follow-Up

No new follow-up tasks required. The remaining verifier work is already covered
by P21-T4.
