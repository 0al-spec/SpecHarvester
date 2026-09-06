# P56-T3A Validation Report

Date: 2026-09-06
Verdict: PASS for protocol preparation only

## Delivered

- Versioned exploratory protocol with the unchanged five target pins/scopes,
  explicit Luna medium settings, one original candidate per target and a
  single validation-error repair allowance.
- Practical human side-by-side review, honest timing/usage limits, baseline
  mismatch disclosure and no inferred scale-out/publication authority.
- P56-T3 deferred; #372 still OPEN/DRAFT and unmerged. No I/O checkpoint code
  is included in this branch. T4-T8 now follow v2 rather than paired/blinded v1.
- P56-T1 protocol, benchmark and skill assets unchanged; regression tests bind
  the historical benchmark digest and all five revisions/scopes.

## Commands Run

- `.venv/bin/python -m pytest tests/test_p56_exploratory_pilot_protocol.py
  tests/test_p56_practical_utility_benchmark.py tests/test_docs_contracts.py
  -q --tb=short`: 207 passed.
- `.venv/bin/python -m pytest -q --tb=short --cov=spec_harvester
  --cov-report=term --cov-fail-under=90`: 1448 passed, six skipped;
  coverage 90.03%.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed after formatting the new
  test file; 205 files checked.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed; existing unhandled
  Documentation.docc warning remains.
- `git diff --check`: passed.
- `git diff --exit-code origin/main -- docs/P56_T1_Practical_Utility_Benchmark.md
  SPECS/EVIDENCE/P56-T1/benchmark.json skills/specpm-author-candidate`: passed,
  no changes to those historical/input artifacts.

## Limits

No provider was invoked, no candidate generated or accepted, and no source
repository, registry or publication state changed. Human review and empirical
usefulness remain future work. Type checking is not configured in params.
Architecture lint is not needed for this documentation/test-only change.

Six full-suite tests were skipped under the local environment; no claim is made
that a live SpecPM integration or external-provider gate ran for this task.

## PR Review Corrections

Before merging #373, addressed source-pin and baseline-review feedback:
require commit-object exports plus verification of every frozen source hash
before authoring, and retain per-question answers/lookups for each displayed
baseline without transferring facts between artifacts. Added regression checks;
the 207 focused benchmark/docs tests passed again. No target or model changed.
