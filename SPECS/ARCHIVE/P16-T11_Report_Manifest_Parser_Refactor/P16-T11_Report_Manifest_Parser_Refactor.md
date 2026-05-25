# P16-T11 — Report Manifest Parser Refactor

Branch: `feature/P16-T11-report-manifest-refactor`
Review subject: `p16_t11_report_manifest_parser_refactor`

## Context

P16-T10 introduced `SpecPackageManifest` as the shared manifest-reading object
seam. The next stacked PR should start using that seam in existing report
modules, while preserving public report JSON behavior.

## Goal

Replace duplicated manifest parser bodies in accepted diff and namespace
upstream reports with `SpecPackageManifest` behavior.

## Deliverables

- Refactor `accepted_diff.parse_specpm_diff_record` to use
  `SpecPackageManifest`.
- Refactor `namespace_reports.parse_specpm_namespace_upstream` to use
  `SpecPackageManifest`.
- Preserve existing tests and report JSON behavior.
- Verify architecture lint baseline decreases from three
  `manifest_parser_pattern` issues to one remaining issue in license
  provenance reporting.

## Non-Goals

- Do not refactor license provenance parsing in this PR; it has extra
  `licenseEvidence` behavior and should be a separate stacked PR if needed.
- Do not change report schemas or issue codes.
- Do not make architecture lint blocking.

## Acceptance Criteria

- Accepted diff and namespace upstream tests pass unchanged.
- Architecture lint reports only the remaining license provenance manifest
  parser pattern.
- Full Flow quality gates pass.
