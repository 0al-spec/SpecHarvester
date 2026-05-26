# P16-T16 — Upstream Issue Evaluation Object

Branch: `feature/P16-T16-upstream-issue-evaluation`
Review subject: `p16_t16_upstream_issue_evaluation_object`

## Context

After P16-T15, the builtin duplicate-code backend reports two upstream issue
generation clusters shared by:

- `src/spec_harvester/namespace_reports.py`
- `src/spec_harvester/license_provenance_reports.py`

The repeated behavior is the same policy shape over `upstream_repository`
foreign artifacts: missing entry, duplicate entry, missing URI, invalid URI, and
namespace/upstream mismatch. The reports differ in issue severity and in whether
non-GitHub upstream URIs are reported.

## Scope

- Add a shared upstream issue evaluation object for report-layer
  `upstream_repository` checks.
- Move upstream repository reference parsing and namespace matching into shared
  upstream evidence code while preserving the existing namespace report imports.
- Refactor namespace/upstream and license provenance reports to use the shared
  evaluator with report-specific policies.
- Preserve issue codes, messages, severities, sorting, report schemas, and
  summary counts.
- Re-run duplicate-code, architecture-lint, and report behavior tests.

## Non-Goals

- Do not change license risk classification.
- Do not change namespace normalization rules.
- Do not add network checks for upstream repositories.
- Do not execute harvested repository code.
- Do not change report JSON schemas.

## Acceptance Criteria

- Namespace/upstream report tests and license provenance report tests pass.
- Builtin duplicate-code report no longer contains the upstream issue-generation
  clusters, or any remaining upstream cluster is justified as below practical
  minimum.
- `pylint` duplicate-code remains at zero duplicate blocks.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_namespace_upstream_reports.py tests/test_license_provenance_risk_reports.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t16-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t16-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t16-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
