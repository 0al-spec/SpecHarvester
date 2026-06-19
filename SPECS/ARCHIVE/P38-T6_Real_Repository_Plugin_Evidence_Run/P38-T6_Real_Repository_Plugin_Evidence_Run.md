# P38-T6 Real Repository Plugin Evidence Run

## Motivation

P38-T2 through P38-T5 define the repository plugin registry, applicability
report, autonomous batch sidecar integration, and static cross-ecosystem
fixtures. The remaining gap is practical evidence from a real local checkout:
the plugin evidence path should be compared with the existing Phase 37
repository profile selection behavior without adding runtime plugin execution.

## Goal

Run one already-available local repository through a static repository plugin
evidence path and record a durable comparison with Phase 37 repository profile
selection behavior.

## Deliverables

- Use an operator-managed local checkout, preferably the existing FastMCP
  checkout used by P37-T7 when available.
- Run or reuse SpecHarvester local batch/profile evidence commands against the
  checkout with AI disabled.
- Record a durable fixture that compares:
  - source repository identity and revision;
  - repository profile detection behavior from Phase 37;
  - repository plugin applicability sidecar evidence from Phase 38;
  - autonomous batch sidecar discovery;
  - trust boundary and non-authority statements.
- Add GitHub docs and DocC docs for the real repository plugin evidence run.
- Add regression coverage for artifact identity, boundary, selected-input
  consistency, docs links, and current `next.md`.
- Archive the task through Flow.

## Acceptance Criteria

- The durable fixture declares a versioned identity for the P38 real-run
  comparison.
- The fixture references one real local checkout revision and run root.
- The fixture records repository profile detection summary from Phase 37.
- The fixture records repository plugin applicability summary from Phase 38.
- The fixture records autonomous batch sidecar discovery when the applicability
  report is provided to `autonomous-candidate-batch`.
- The fixture clearly states the run is producer-side review evidence only.
- The fixture does not claim plugin execution, plugin loading, package
  acceptance, relation acceptance, registry publication, or upstream
  endorsement.
- Docs and tests verify the comparison.

## Non-Goals

- Do not implement plugin execution.
- Do not load third-party plugin code.
- Do not implement runtime plugin discovery or selection.
- Do not clone or fetch repositories.
- Do not run package managers.
- Do not install dependencies.
- Do not execute harvested code.
- Do not invoke AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat plugin decisions as registry truth.

## Dependencies

- P37 repository profile selection behavior and real-run documentation.
- P38-T2 repository plugin registry fixture.
- P38-T3 repository plugin applicability report fixture shape.
- P38-T4 autonomous candidate batch sidecar integration.
- P38-T5 cross-ecosystem fixture matrix.

## Validation Plan

- `python3 -m json.tool tests/fixtures/repository_plugins/real_runs/p38-t6-*.json`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_real_run or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
