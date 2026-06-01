# P21-T1 Validation Report

**Task:** P21-T1 — Producer Candidate Bundle Output Planning
**Date:** 2026-06-02
**Branch:** `feature/P21-T1-producer-candidate-bundle-output-planning`
**Verdict:** PASS

## Scope Validated

- Added SpecHarvester-facing GitHub documentation for the SpecPM Producer
  Candidate Bundle handoff.
- Added DocC mirror page for the same contract.
- Linked the new documentation from `docs/README.md` and DocC topics.
- Updated P21-T2 planning to match the merged SpecPM contract
  `apiVersion: specpm.receipts/v0` and `kind: SpecPMProducerReceipt`.
- Added documentation contract coverage for bundle layout, receipt profile,
  digest rules, self-hash boundary, review boundary, privacy notes, and
  rejection diagnostics.

## Quality Gates

| Gate | Command | Result |
|------|---------|--------|
| Targeted docs tests | `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` | PASS — 28 passed |
| Full tests | `PYTHONPATH=src python -m pytest` | PASS — 476 passed, 1 skipped |
| Lint | `ruff check src tests` | PASS — All checks passed |
| Format | `ruff format --check src tests` | PASS — 79 files already formatted |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS — 476 passed, 1 skipped; total coverage 91.76% |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| DocC build target | `swift build --target SpecHarvesterDocs` | PASS |

## Notes

- The actual merged SpecPM contract uses `apiVersion: specpm.receipts/v0`.
  Earlier draft wording that referenced `specpm.producer_receipt/v1` was
  removed from the P21 implementation plan.
- This task intentionally does not emit runtime bundle artifacts. Emission and
  verification remain assigned to P21-T2 through P21-T4.
