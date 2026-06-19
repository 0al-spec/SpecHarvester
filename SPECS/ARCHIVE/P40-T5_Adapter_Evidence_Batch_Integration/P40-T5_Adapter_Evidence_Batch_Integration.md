# P40-T5 Adapter Evidence Batch Integration

## Status

Planned for execution on `feature/P40-T5-adapter-evidence-batch-integration`.

## Context

P40-T1 defined the repository plugin adapter contract. P40-T2 added a
machine-readable adapter manifest fixture. P40-T3 added adapter preflight
report evidence, and P40-T4 documented the disabled-by-default execution policy.

P40-T5 connects that manifest and preflight evidence to
`autonomous-candidate-batch` as operator-supplied sidecar evidence. The batch
path remains review-only and must not execute adapters or treat adapter output
as accepted SpecPM truth.

## Motivation

Operators need a practical place to attach adapter manifest and preflight
evidence when running repository batches. Without this integration, adapter
contract work exists only as standalone fixtures and cannot travel with batch
review artifacts.

The integration must preserve the existing static repository plugin
applicability evaluator. Adapter evidence is an explicit opt-in sidecar, not a
new default inference path.

## Deliverables

- Add opt-in `autonomous-candidate-batch` inputs for adapter manifest and
  adapter preflight evidence.
- Require manifest and preflight inputs to be supplied together.
- Copy supplied adapter evidence into batch report artifacts.
- Record adapter manifest and preflight paths and SHA-256 digests in batch
  output.
- Record selected, rejected, fallback, blocked, diagnostic, and execution
  counts from preflight evidence.
- Record `appliedToDrafting: false`.
- Record `registryAuthority: false`.
- Preserve existing static repository plugin applicability behavior when
  adapter evidence is not supplied.
- Update CLI help, GitHub docs, DocC, roadmap, workplan, and regression tests.

## Acceptance Criteria

- Existing batch behavior remains unchanged when no adapter evidence inputs are
  supplied.
- Supplying only one of manifest or preflight fails before batch execution.
- Supplying both sidecars records copied artifact paths, source paths, digests,
  adapter counts, decision counts, diagnostics counts, and non-authority
  boundaries in the batch report.
- Batch output states that adapter evidence is review-only producer evidence.
- Batch output states `appliedToDrafting: false` and
  `registryAuthority: false`.
- Adapter evidence integration does not run adapters, load adapter code, run AI,
  install dependencies, invoke package managers, clone repositories, or publish
  registry metadata.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not auto-run adapters.
- Do not change static plugin applicability defaults.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
