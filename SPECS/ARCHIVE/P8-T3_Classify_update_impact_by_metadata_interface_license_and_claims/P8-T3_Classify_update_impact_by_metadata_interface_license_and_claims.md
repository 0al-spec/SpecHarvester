# P8-T3 - Classify Update Impact by Metadata, Interface, License, Provenance, Capability, and Intent

Branch: `feature/P8-T3-update-impact-classification`
Review subject: `p8_t3_update_impact_classification`

## Problem

The accepted-vs-candidate diff report (`accepted-candidate-diff-report`) shows what
changed but does not separate risks into impact buckets that reviewers can use for
prioritization.

Before proposal workflows and human triage, maintainers need a deterministic
classification layer that clearly distinguishes metadata, interface, license,
provenance, capability, and intent impact.

## Goals

- Introduce a new local-only report that classifies accepted-vs-candidate diff output
  into fixed buckets:
  - metadata impact
  - interface impact
  - license impact
  - provenance impact
  - capability impact
  - intent impact
- Keep report generation deterministic and read-only.
- Reuse the same local inputs and trust constraints as existing diff/report commands.
- Add CLI wiring and tests for stable output structure.
- Document the new command in GitHub docs and DocC.

## Non-Goals

- No proposal automation.
- No write operations on candidate or accepted package content.
- No SpecPM validation in this task.
- No external analyzers or network access.

## Acceptance Criteria

- Given accepted and candidate roots, the command produces a deterministic JSON
  classification report.
- Each bucket is separated and consistently populated.
- New/unchanged/changed package status is preserved from input comparisons.
- Upstream artifact and license-related metadata changes are classified distinctly
  from scope/interface/capability/intent changes.
- The command remains advisory and produces no mutation.

## Phases

1. Classification model
   - Define output schema and deterministic bucketing rules.
2. Implementation
   - Build classification module from existing accepted-vs-candidate comparison data.
   - Add CLI entrypoint and writer helper.
3. Validation
   - Add focused unit tests for changed/new/unchanged cases and bucket boundaries.
4. Documentation
   - Add GitHub docs page and DocC topic.
   - Update workflow and operation docs to reference the new report.

## Test Plan

- `PYTHONPATH=src python -m pytest tests/test_accepted_candidate_impact.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

---

**Archived:** 2026-05-18
**Verdict:** PASS

## Notes

This report is an advisory pre-priority signal. It intentionally does not execute
SpecPM, run analyzers, execute package scripts, or mutate generated content.
