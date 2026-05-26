# P16-T16 Validation Report

Task: `P16-T16 — Upstream Issue Evaluation Object`
Branch: `feature/P16-T16-upstream-issue-evaluation`
Date: 2026-05-26
Verdict: PASS

## Summary

- Added `UpstreamIssuePolicy` and related upstream issue evidence objects for
  shared `upstream_repository` report evaluation.
- Moved upstream repository parsing, namespace matching, normalized identifier
  comparison, and issue subject mapping into shared upstream issue code.
- Refactored namespace/upstream and license provenance reports to use
  report-specific policies while preserving issue codes, messages, severities,
  sorting, summaries, and report schemas.
- Added direct tests for upstream issue subject mapping, non-GitHub policy,
  repository parsing, namespace matching, and mismatch reporting.

## Duplicate-Code Metrics

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t16-dup-builtin.json`
  - ATTENTION: `duplicateBlockCount=7`, `duplicateOccurrenceCount=14`
  - Upstream issue-generation clusters are removed.
  - Remaining advisory clusters are all in `real_repo_quality_report.py` rating
    guards and are tracked by P16-T17.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t16-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`

## Architecture-Lint Metrics

- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t16-architecture-lint.json`
  - ATTENTION: `issueCount=1`
  - Existing advisory: `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`.
  - This issue is unrelated to the upstream issue evaluator refactor.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_upstream_issue_evaluation.py tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q`
  - PASS: `26 passed`
- `PYTHONPATH=src python -m pytest`
  - PASS: `411 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `411 passed, 1 skipped`
  - Coverage: `91.76%`
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: `67 files already formatted`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Follow-Up Candidates

- P16-T17 should address the remaining real repository quality rating guard
  duplicate clusters.
- P16-T18 should run the final practical-minimum duplicate-code audit after
  P16-T17.
