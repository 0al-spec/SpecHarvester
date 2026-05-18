# P8-T2 - Add Accepted-vs-Candidate Package Diff Report

Branch: `feature/P8-T2-accepted-candidate-diff-report`
Review subject: `p8_t2_accepted_candidate_diff_report`

## Problem

SpecHarvester can generate candidates and governance reports, but reviewers do
not yet have a compact report that compares a candidate package against the
currently accepted package metadata for the same `metadata.id`.

Without this report, update review must inspect accepted and candidate YAML
manually before later automation can classify impact or prepare update PRs.

## Goals

- Add a deterministic local JSON report for accepted-vs-candidate comparisons.
- Match candidates to accepted package records by `metadata.id`.
- Compare candidate metadata with the latest accepted version for that package.
- Report changed package metadata, intent claims, capability claims, and upstream
  artifact references.
- Keep the report read-only and local-only.

## Non-Goals

- No impact classification; P8-T3 owns update impact categories.
- No SpecPM validation invocation.
- No mutation of accepted or candidate package content.
- No proposal PR creation.
- No network access, dependency installation, analyzer execution, or repository
  code execution.

## Deliverables

- Add an `accepted-candidate-diff-report` CLI command.
- Add a report module with deterministic JSON output.
- Add focused tests for changed, unchanged, and new-package candidates.
- Add GitHub docs and DocC mirror documentation.
- Archive Flow PRD, validation, and review artifacts.

## Acceptance Criteria

- The report scans accepted and candidate roots for `specpm.yaml` files.
- The report skips symlinked or malformed manifests and records issues.
- Candidates without an accepted package record are reported as `new_package`.
- Candidates with accepted records are compared against the latest accepted
  version by SemVer ordering.
- Changed metadata, added/removed intents, added/removed capabilities, and
  upstream artifact changes are visible in deterministic JSON.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_diff.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
