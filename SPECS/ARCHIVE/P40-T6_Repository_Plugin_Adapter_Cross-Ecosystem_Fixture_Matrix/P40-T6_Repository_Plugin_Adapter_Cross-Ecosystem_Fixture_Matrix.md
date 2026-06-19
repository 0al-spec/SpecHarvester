# P40-T6 Repository Plugin Adapter Cross-Ecosystem Fixture Matrix

## Status

Planned for execution on
`feature/P40-T6-repository-plugin-adapter-cross-ecosystem-fixture-matrix`.

## Context

P40-T1 defined the repository plugin adapter contract. P40-T2 added the adapter
manifest fixture. P40-T3 added adapter preflight report evidence. P40-T4
documented disabled-by-default execution policy. P40-T5 connected
operator-supplied adapter manifest/preflight sidecars to
`autonomous-candidate-batch` as `repositoryPluginAdapterEvidence`.

P40-T6 broadens the fixture coverage before any adapter runtime exists. The
matrix should demonstrate how the same static contract can represent several
repository shapes without loading third-party adapter code or making a language
or framework normative.

## Motivation

The current adapter evidence fixtures prove the contract in one generic
workspace scenario. That is not enough to evaluate whether the shape stays
useful across common repository layouts: single packages, workspaces,
documentation-heavy repositories, nested package roots, and ambiguous mixed
layouts.

A static matrix gives reviewers a stable way to inspect expected decisions
before future real validation work. It also prevents the future adapter runtime
from being designed around one repository shape.

## Deliverables

- Add a machine-readable fixture matrix for repository plugin adapter contract
  scenarios.
- Cover these repository shapes:
  - manifest-backed single package;
  - workspace/package-set;
  - documentation-heavy repository;
  - nested package root;
  - ambiguous mixed layout.
- For each case, record static evidence signals, expected adapter manifest and
  preflight evidence, allowed/rejected/fallback/blocked counts, and diagnostic
  codes.
- For each case, record no adapter loading, no adapter execution, no package
  manager invocation, no dependency installation, no AI, no registry authority,
  and no accepted package/relation authority.
- Update GitHub docs, DocC mirrors, capabilities, roadmap, workplan, and next
  task state.
- Add regression tests proving the matrix shape, coverage, and non-authority
  boundaries.

## Acceptance Criteria

- The fixture matrix is machine-readable JSON with versioned identity.
- The matrix includes exactly the five required repository shape classes.
- Every case has stable ids, repository shape metadata, expected evidence
  paths, expected adapter decisions, expected counts, diagnostics, and
  non-authority statements.
- Every case records `adapterExecution: not_run`.
- Every case records `adapterCodeLoaded: false`.
- Every case records `appliedToDrafting: false`.
- Every case records `registryAuthority: false`.
- Every case records no package manager invocation, no dependency
  installation, no harvested code execution, no AI, no package acceptance, no
  relation acceptance, no registry publication, and no `preview_only` removal.
- Documentation explains that the matrix is fixture evidence after P40-T5 and
  before P40-T7, not adapter runtime execution.

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

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
