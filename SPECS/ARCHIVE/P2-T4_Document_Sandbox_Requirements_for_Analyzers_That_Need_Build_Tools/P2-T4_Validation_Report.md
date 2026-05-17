# P2-T4 Validation Report

Task: Document Sandbox Requirements for Analyzers That Need Build Tools
Branch: `feature/P2-T4-document-sandbox-requirements-for-analyzers-that-need-build-tools`
Date: 2026-05-17
Verdict: PASS

## Implementation Summary

Documented future analyzer sandbox requirements:

- Added `docs/ANALYZER_SANDBOX_REQUIREMENTS.md`.
- Added DocC mirror `AnalyzerSandboxRequirements.md`.
- Linked sandbox requirements from trust-boundary and architecture docs.
- Linked the new page from the DocC root topics.
- Added documentation contract tests for required sandbox invariants and DocC
  navigation links.

## Sandbox Requirements Covered

The documentation covers:

- `execution: none`, `metadata_tool_only`, and `build_tool_sandboxed`;
- no network access;
- no package scripts;
- no harvested dependency installation;
- no secret access;
- pinned analyzer and toolchain identity;
- bounded filesystem access;
- deterministic output;
- source digest evidence;
- diagnostics on failures;
- audit log requirements;
- `collect-local` remaining static;
- sandboxed output remaining untrusted evidence.

## Coverage Baseline

P2-T3 finished at 90.62% total coverage. P2-T4 finished at 90.62% total
coverage, so coverage did not decline.

## Validation Commands

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` | PASS, 2 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 67 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 16 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 67 passed, total coverage 90.62% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Trust Boundary Validation

- `collect-local` still does not run analyzers.
- No sandbox runtime implementation was added.
- No build-tool analyzer execution was added.
- No package manager, dependency installation, network, or package script
  execution path was introduced.
- The new documentation treats sandboxed analyzer output as untrusted evidence.

## Residual Risks

- This task defines requirements only. A future implementation task must add
  concrete sandbox enforcement, analyzer orchestration, and runtime tests before
  enabling any `metadata_tool_only` or `build_tool_sandboxed` analyzer.
