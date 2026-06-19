# P40-T7 Real Local Adapter-Contract Validation

Status: Planned
Phase: Phase 40. Repository Plugin Adapter Contract

## Motivation

P40-T6 records a static adapter fixture matrix. That proves the contract shape,
but fixture-only coverage can miss assumptions that appear in real repositories:
multiple manifests, documentation-heavy frameworks, workspace roots, and
language-specific package markers.

This task validates the adapter contract against existing pinned local
checkouts without adding an adapter runtime. The goal is to prove that real
repository evidence can be mapped to the Phase 40 adapter categories while the
adapter output remains producer-side review evidence only.

## Goal

Record a real local adapter-contract validation run for FastMCP, FastAPI,
xyflow, and one additional available ecosystem shape. The run must compare real
static evidence against the P40-T6 matrix categories and preserve the no-runtime
boundary.

## Scope

- Use existing pinned local checkouts only.
- Record FastMCP, FastAPI, xyflow, and one additional available ecosystem
  shape.
- Capture each checkout revision and origin URL as review context.
- Map each repository to the closest P40-T6 matrix category.
- Record static evidence paths, adapter decisions, diagnostics, and counts.
- Prove `adapterExecution: not_run`.
- Prove `adapterCodeLoaded: false`.
- Prove no package managers, dependency installers, harvested code execution,
  network discovery, or AI were invoked.
- Keep adapter output producer-side and non-authoritative for registry
  acceptance.
- Document the result in GitHub docs and DocC.

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

## Plan

1. Record the local checkout evidence for FastMCP, FastAPI, xyflow, and one
   additional available ecosystem repository.
2. Add a machine-readable `SpecHarvesterRepositoryPluginAdapterRealLocalValidation`
   fixture that references the P40-T6 matrix, adapter manifest, and adapter
   preflight fixture.
3. Add GitHub and DocC documentation explaining the real validation result,
   repository mapping, and non-authority boundary.
4. Add regression coverage for fixture shape, digests, decisions, docs, and
   Phase 40 completion state.
5. Archive the Flow task and create the pull request.

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

## Success Criteria

- The fixture records four real local checkouts and at least three distinct
  matrix categories.
- Every case records allowed, rejected, fallback, or blocked adapter decisions.
- Every case records `adapterExecution: not_run` and no loaded adapter code.
- The docs explain that this is producer-side evidence only, not adapter
  execution and not registry acceptance.
- Phase 40 is marked complete in Flow after archive.
