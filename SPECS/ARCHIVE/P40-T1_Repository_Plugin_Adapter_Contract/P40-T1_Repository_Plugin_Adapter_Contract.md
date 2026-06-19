# P40-T1 Repository Plugin Adapter Contract

## Motivation

Phase 38 defined repository plugins as producer-side evidence. Phase 39 added a
static applicability evaluator that can derive plugin decisions from declared
registry metadata and bounded static evidence without loading plugin code.

The remaining gap is the future adapter boundary. Before SpecHarvester can add
runtime adapter manifests, preflight, or execution policy, it needs a
language- and framework-agnostic contract that states what an adapter is, what
it may declare, what it may read, what it may emit, and what authority it never
has.

## Goal

Document the repository plugin adapter contract before implementation.

The contract must cover adapter identity, manifest versioning, roles, declared
input evidence, output artifact categories, execution modes, sandbox
expectations, diagnostics, and non-authority boundaries. Python, JavaScript,
FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle, and similar
ecosystems may appear as examples only.

## Deliverables

- Add a GitHub-facing adapter contract document.
- Add a DocC mirror for the adapter contract.
- Link the contract from docs index, DocC root, capabilities, roadmap, and the
  repository plugin subsystem contract.
- Update `SPECS/Workplan.md` and `SPECS/INPROGRESS/next.md` for P40-T1 state.
- Add docs regression coverage for the contract identity, adapter fields,
  planned follow-ups, static-first policy, sandbox expectations, and
  non-authority boundaries.
- Archive and review the task through Flow.

## Acceptance Criteria

- The contract is language- and framework-agnostic.
- The contract distinguishes plugin applicability, adapter manifest,
  preflight, execution policy, and output evidence.
- The contract keeps static applicability as the default safe path.
- The contract says adapter execution is disabled until a future explicit
  execution policy is implemented.
- The contract lists safe input requirements: declared evidence artifacts,
  safe relative paths, digests, and authority labels.
- The contract lists output categories without treating them as accepted
  package truth.
- The contract rejects unsafe defaults: dependency installation, package
  manager invocation, network discovery, harvested code execution, unbounded
  local tools, AI invocation, registry publication, package acceptance,
  relation acceptance, baseline seeding, and `preview_only` removal.

## Non-Goals

- Do not implement adapter manifests.
- Do not add adapter preflight.
- Do not add adapter loading or execution.
- Do not change static plugin applicability evaluation.
- Do not change `autonomous-candidate-batch` behavior.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Dependencies

- P38 repository plugin subsystem contract.
- P39 static repository plugin applicability evaluator.
- P39-T6 real FastMCP, FastAPI, and xyflow static evaluator validation.

## Test-First Plan

1. Add docs-contract assertions for the new adapter contract and current
   `P40-T1` next-task state.
2. Add GitHub and DocC contract docs with the required vocabulary.
3. Add references from docs index, DocC root, capabilities, roadmap, and
   repository plugin subsystem docs.
4. Run focused docs-contract tests, then full pytest, lint, format, diff-check,
   and Swift docs build.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_adapter_contract or current_next_task'`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
