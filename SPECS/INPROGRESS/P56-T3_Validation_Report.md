# P56-T3 Validation Report

Date: 2026-09-06
Verdict: IN PROGRESS; I/O implementation checkpoint only

## Completed Scope

- Pinned read allowlist, descriptor-relative source reads, full-file digest
  checks, explicit UTF-8 ranges, shared source/generated evidence budgets.
- Portable source-read ledger without content or denied host paths.
- New candidate directory sink with aggregate output limit and path checks.
- Active task lifecycle documentation and docs-contract status correction.

## Validation

- Test-first collection failed because the new module did not yet exist.
- `.venv/bin/python -m pytest tests/test_investigative_authoring_io.py -q`:
  30 passed.
- `.venv/bin/python -m pytest tests/test_investigative_authoring_io.py
  --cov=spec_harvester.investigative_authoring_io --cov-report=term-missing
  --cov-fail-under=90 -q`: 30 passed; 95.68% focused coverage.
- `.venv/bin/python -m pytest tests/test_docs_contracts.py -q`:
  203 passed after correcting the active task status assertion.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: passed, 206 files.
- `.venv/bin/python -m spec_harvester architecture-lint --path
  src/spec_harvester/investigative_authoring_io.py --output
  /tmp/p56-t3-architecture-lint.json`: zero issues.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed, with an unhandled
  Documentation.docc resource warning.
- `git diff --check`: passed.
- First full coverage run: 124 failed, 1351 passed, six skipped. All failures
  were the shared docs-contract assertion that permitted only Ready rather
  than the selected In Progress status. The assertion now accepts the same
  lifecycle states as neighboring Phase 56 tasks.
- `.venv/bin/python -m pytest -q --tb=short --cov=spec_harvester
  --cov-report=term --cov-fail-under=90`: 1475 passed, six skipped;
  90.07% coverage. The corrected full run passed.

## Remaining Acceptance

This module cannot itself enforce worker filesystem/network isolation, total
generation time or model deadlines. It has no model transport, trusted
validation invocation, attempt scheduler or completed execution lock. No
denial-probe receipt, live-provider result, token measurement, empirical quality
claim or permission for P56-T4 is asserted.

Full task acceptance remains pending the isolated runtime and its actual
admission tests, bounded arm-A integration (or an explicit protocol revision),
and normalized provider/validation receipts. Workplan remains unchecked and
next.md remains on P56-T3. ARCHIVE through ARCHIVE-REVIEW are not complete.

## Repository State

PR #371 was merged with explicit user approval after green CI and zero
unresolved threads. Its merge commit is
9ccbc48a4c469450571420b655b3a8c6a421838c. T3 was rebased onto updated main.
User-owned untracked uv.lock remains untouched.
