# P56-T4 Validation Report

Date: 2026-09-06
Verdict: PASS for complete outcome collection; practical utility NOT EVALUATED.

## Completed Evidence

Five originals generated with fresh gpt-5.6-luna/medium contexts under v2.
No validation-error repairs were needed: zero errors, seven warnings across
five independently checked packages. Source inventories remained unchanged.
The 58-member portable archive retains all 38 candidate files, including RTK's
provenance file omitted by SpecPM package collection. Original bytes unchanged.
Baselines were locked before generation; old pipeline and deferred T3 did not run.

See docs/P56_T4_Five_Exploratory_Candidates.md and
SPECS/EVIDENCE/P56-T4/generation-report.json for evidence defects, per-target
receipts, actual permissions, unavailable usage and static-audit limitations.
In particular RTK changed code while claiming unchanged excerpts. Schema success
does not establish faithful evidence, author quality, acceptance or publication.

## Commands Run

- `.venv/bin/python -m pytest -q --tb=short --cov=spec_harvester --cov-report=term --cov-fail-under=90`:
  1452 passed, 7 skipped, coverage 90.03% (final run after archive and review).
- `PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src:src .venv/bin/python -m pytest tests/test_p56_exploratory_candidates.py tests/test_authoring_skill_assets.py -q`:
  13 passed, including historical-baseline digests and exact validator diagnostics.
- `.venv/bin/python -m pytest tests/test_docs_contracts.py tests/test_p56_exploratory_candidates.py -q`:
  207 passed, 1 skipped (optional SpecPM import, covered by the explicit run above).
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed; existing unhandled DocC
  directory warning remains.
- Portable archive scan: no `/Users/` paths in member contents.

Independent validator revision: SpecPM
`8a5ce3dece3d18bf8f601a5a599520bd520c7839`, clean checkout. CI now repeats the
retained-candidate validation in its SpecPM integration job. Live generation
used desktop subagents; available CLI version is not falsely labeled transport.

## Limits and Handoff

No human review, runtime test, proven isolation, exact token accounting,
mass-corpus claim, registry mutation or publication. Warnings and source-fidelity
defects remain visible, not repaired outside budget. T5 must show these originals
and mismatched historical baselines honestly; T6 records human disposition.
