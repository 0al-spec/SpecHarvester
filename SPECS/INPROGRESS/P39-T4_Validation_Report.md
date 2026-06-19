# P39-T4 Validation Report

## Summary

Status: PASS.

P39-T4 exposes the deterministic static plugin applicability helper through
`repository-plugin-applicability-detect`. The command reads explicit registry
and static evidence envelope JSON files, writes a full
`SpecHarvesterRepositoryPluginApplicabilityReport` JSON artifact to `--out`,
and prints compact summary counts.

## Validation

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_cli.py -q`
  - `4 passed`
- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
  - `4 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_repository_plugin_applicability_evaluator_plan or static_plugin_evidence_envelope or current_next_task'`
  - `2 passed, 112 deselected`
- `PYTHONPATH=src pytest -q`
  - `776 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `776 passed, 1 skipped`
  - coverage `91.11%`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `PYTHONPATH=src python -m spec_harvester repository-plugin-applicability-detect --registry tests/fixtures/repository_plugins/generic-registry.example.json --static-evidence-envelope tests/fixtures/repository_plugins/static-evidence-envelope.example.json --out /tmp/specharvester-p39-t4-validation-report.json`
  - `status: ok`
  - summary: `selectedCount: 3`, `rejectedCount: 0`, `fallbackCount: 0`,
    `blockedCount: 2`, `diagnosticCount: 5`

## Acceptance Notes

- The CLI accepts `--registry`, `--static-evidence-envelope`, and `--out`.
- The CLI writes a full `SpecHarvesterRepositoryPluginApplicabilityReport` to
  `--out`.
- The CLI prints a compact JSON summary with selected, rejected, fallback,
  blocked, and diagnostic counts.
- Invalid registry identities and unsafe static evidence paths return exit code
  `2` with JSON error payloads.
- Missing evidence fallback/blocking behavior is covered by regression tests.
- Autonomous batch integration remains deferred to P39-T5.
