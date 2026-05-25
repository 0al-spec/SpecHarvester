# P16-T6 — Duplicate-Code Quality Report

Branch: `feature/P16-T6-duplicate-code-quality-gate`
Review subject: `p16_t6_duplicate_code_quality_report`

## Context

P16-T2 review found duplicated license filename allowlists and predicate logic
between collection and license provenance reporting. The immediate fix moved
the predicate into a shared module, but the broader failure class remains:
policy constants, normalization predicates, schema fragments, and report
issue-code logic can drift when copied between modules.

## Goal

Add a deterministic, local-only duplicate-code report that can be run as an
advisory quality gate. The report should identify repeated implementation
blocks in source files without executing repository code, installing harvested
dependencies, or requiring network access.

## Deliverables

- Add a `SpecHarvesterCodeDuplicationReport` JSON format.
- Add a CLI command that scans selected local source roots and emits the report.
- Keep the command non-blocking by default, with an explicit
  `--fail-on-duplicates` option for future CI/baseline enforcement.
- Add regression tests covering duplicate detection, ignored comments/blank
  lines, output writing, and fail-on-duplicates behavior.
- Document validation results in a Flow validation report.

## Non-Goals

- Do not replace established external clone detectors such as `jscpd`, `pylint
  R0801`, or language-specific linters.
- Do not add a new package dependency in this task.
- Do not make CI fail on the current repository baseline by default.
- Do not scan harvested third-party repositories unless a caller explicitly
  passes those paths.

## Acceptance Criteria

- Running the CLI against duplicated Python fixtures reports stable duplicate
  block fingerprints and source locations.
- Running without `--fail-on-duplicates` exits successfully even when duplicates
  exist.
- Running with `--fail-on-duplicates` returns a non-zero exit code when
  duplicates exist.
- The report includes trust-boundary notes explaining that it reads local text
  files only and remains advisory.
- Configured Python tests, lint, format, coverage, and Swift documentation gates
  pass.
