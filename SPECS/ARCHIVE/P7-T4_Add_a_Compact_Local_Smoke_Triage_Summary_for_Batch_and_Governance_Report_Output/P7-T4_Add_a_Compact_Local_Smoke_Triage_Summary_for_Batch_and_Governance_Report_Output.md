# P7-T4 - Add a Compact Local Smoke Triage Summary for Batch and Governance Report Output

Branch: `feature/P7-T4-local-smoke-triage-summary`
Review subject: `p7_t4_local_smoke_triage_summary`

## Problem

Local smoke validation produces multiple JSON files: batch validation,
duplicate governance, namespace/upstream, and license/provenance reports.
Reviewers must inspect each file separately to understand whether a smoke run is
clean and where to drill into remaining issues.

## Goals

- Add a compact deterministic smoke triage summary from existing report files.
- Preserve links to detailed report paths for reviewer follow-up.
- Distinguish batch warnings, duplicate claims, namespace/upstream signals, and
  license/provenance signals.
- Keep the workflow local-only and read-only over generated smoke outputs.
- Keep coverage above the project threshold.

## Non-Goals

- No automatic collection, drafting, or governance report generation.
- No promotion of generated candidates.
- No policy decision about whether remaining smoke signals are acceptable.
- No repository code execution, package installation, or network access.

## Deliverables

- Add a `smoke-triage-summary` CLI command that reads existing JSON reports.
- Emit deterministic JSON with status, detail paths, counts, and issue buckets.
- Add tests for clean and issue-bearing smoke summaries.
- Update local smoke fixture documentation and DocC.
- Add validation report and archive artifacts.

## Acceptance Criteria

- Smoke triage output summarizes batch status and governance issue counts in a
  compact reviewable format.
- The summary distinguishes duplicate, namespace/upstream, and
  license/provenance signals.
- The summary can point reviewers to the detailed report files.
- The command remains local-only and deterministic.
- Coverage remains above the project threshold.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_smoke_triage.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
