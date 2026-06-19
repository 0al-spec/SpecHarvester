# REVIEW P39-T3 Deterministic Static Applicability Evaluator Helper

## Verdict

PASS.

## Findings

No blocking findings.

## Scope Review

- The implementation adds
  `spec_harvester.repository_plugin_applicability.evaluate_repository_plugin_applicability`.
- The helper accepts already-loaded registry and static evidence envelope JSON
  objects. It does not add a CLI or change autonomous batch behavior.
- The helper emits a
  `SpecHarvesterRepositoryPluginApplicabilityReport` with
  selected/rejected/fallback/blocked decision arrays, summary counts,
  diagnostics, sidecar boundary, non-authority statements, and follow-up task
  markers.
- The helper rejects unsafe evidence paths and invalid `sha256:<64 hex>`
  digests before constructing a report.

## Boundary Review

The task preserves the intended authority boundary:

- no third-party plugin loading;
- no plugin execution;
- no repository source file reads;
- no clone/fetch behavior;
- no dependency installation;
- no package manager invocation;
- no harvested code execution;
- no AI invocation;
- no package or relation acceptance;
- no registry publication;
- no `preview_only` removal;
- no treatment of plugin decisions as registry truth.

## Tests Reviewed

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_plugin_evidence_envelope or static_repository_plugin_applicability_evaluator_plan or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

## Follow-Up

Proceed to P39-T4:

```text
repository-plugin-applicability-detect
```

P39-T4 should expose the helper through an explicit CLI/report surface while
keeping autonomous batch integration deferred to P39-T5.
