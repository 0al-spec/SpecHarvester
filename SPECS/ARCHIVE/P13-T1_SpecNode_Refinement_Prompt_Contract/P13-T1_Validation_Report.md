# P13-T1 Validation Report

Task: `P13-T1` SpecNode Refinement Prompt Contract
Date: 2026-05-22
Verdict: PASS

## Summary

P13-T1 adds a versioned `SpecNodeRefinementPromptContract` for first-pass
SpecNode refinement prompts. The contract defines deterministic prompt
sections, allowed `compactModelInput` sources, schema-bound output,
evidence-reference rules, negative-claim policy, confidence calibration, and
authority boundaries.

The change is documentation and contract-test only. It does not execute models,
call LM Studio, implement semantic review, implement retries, or apply patches.

## Validation

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: 14 passed
- `PYTHONPATH=src python -m pytest`
  - PASS: 247 passed
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: 46 files already formatted
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 247 passed, total coverage 91.22%
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Notes

- The prompt contract is repository-owned policy, not ad-hoc runtime wording.
- Prompt output remains untrusted proposal metadata until schema validation,
  SpecPM validation, and human review pass.
- `P13-T2` remains responsible for clean-context semantic review.
- `P13-T3` remains responsible for feedback-driven retry orchestration.
