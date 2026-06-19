# Next Task: P40-T7 Real Local Adapter-Contract Validation

**Status:** Planned
**Branch:** `feature/P40-T7-real-local-adapter-contract-validation`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T6 Repository Plugin Adapter Cross-Ecosystem Fixture Matrix

## Recently Archived

- `P40-T6` recorded a static cross-ecosystem adapter fixture matrix.
- The GitHub-facing documentation is
  `docs/REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterCrossEcosystemFixtureMatrix.md`.
- The machine-readable fixture is
  `tests/fixtures/repository_plugins/adapter_cross_ecosystem/adapter-fixture-matrix.example.json`.
- The matrix covers:
  - `manifest_backed_single_package`;
  - `workspace_or_multi_package`;
  - `documentation_heavy_repository`;
  - `nested_package_roots`;
  - `ambiguous_mixed_layout`.
- Every case records `adapterExecution: not_run`,
  `adapterCodeLoaded: false`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- The matrix remains producer-side review evidence only and does not load or
  execute third-party adapter code.

## Task

Run a real local adapter-contract validation over existing pinned checkouts,
comparing FastMCP, FastAPI, xyflow, and at least one additional ecosystem shape
when available, while proving that adapters remain producer-side evidence only.

## Why This Is Next

P40-T6 proves the adapter contract against static matrix fixtures. The next
step is to compare those expectations with real local repository evidence that
already exists in the operator workspace, without turning adapters into a
runtime execution path.

## Scope

- Use existing pinned local checkouts only.
- Compare FastMCP, FastAPI, xyflow, and at least one additional ecosystem shape
  when available.
- Record adapter manifest/preflight evidence for each real checkout.
- Compare real evidence shape against the P40-T6 fixture matrix categories.
- Record allowed, rejected, fallback, and blocked adapter decisions.
- Prove `adapterExecution: not_run`.
- Prove `adapterCodeLoaded: false`.
- Prove adapter output remains producer-side evidence only.
- Document the validation result in GitHub docs and DocC.

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

## Phase 40. Repository Plugin Adapter Contract

- [x] `P40-T1` Document a language- and framework-agnostic repository plugin
  adapter contract. The contract must define adapter identity, versioned
  manifests, declared input evidence, output artifacts, execution modes,
  sandbox expectations, diagnostics, and authority boundaries without making
  Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven,
  Gradle, or any other ecosystem normative.
- [x] `P40-T2` Add a machine-readable
  `SpecHarvesterRepositoryPluginAdapterManifest` fixture that records adapter
  ids, contract versions, supported roles, required and optional evidence
  kinds, declared outputs, execution mode, sandbox requirements, capability
  requests, and non-authority statements.
- [x] `P40-T3` Add a repository plugin adapter preflight report fixture that
  validates one or more adapter manifests against a static evidence envelope,
  records allowed, rejected, fallback, and blocked adapter decisions, and
  refuses unsafe execution or missing required evidence before any adapter code
  can run.
- [x] `P40-T4` Define adapter execution policy for future local adapters:
  default disabled execution, static-only mode, bounded local trusted mode,
  path allowlists, no dependency installation, no package manager invocation,
  no network discovery, no harvested code execution, and explicit operator
  opt-in for every non-static mode.
- [x] `P40-T5` Connect adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence while keeping
  the existing static evaluator path unchanged unless an operator explicitly
  supplies adapter evidence.
- [x] `P40-T6` Record a cross-ecosystem adapter contract fixture matrix for
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts without
  loading third-party adapter code.
- [ ] `P40-T7` Run a real local adapter-contract validation over existing
  pinned checkouts, comparing FastMCP, FastAPI, xyflow, and at least one
  additional ecosystem shape when available, while proving that adapters remain
  producer-side evidence only.

Motivation:

- Fixture coverage is useful, but real local evidence can expose assumptions
  that fixture-only validation misses.
- The validation should compare real repository shapes to the static matrix
  without adding an adapter runtime.
- The next task should prove the adapter contract can guide future work while
  keeping all output producer-side and review-only.

Goal:

- Produce a documented real-checkout validation run that maps FastMCP,
  FastAPI, xyflow, and one additional available ecosystem shape to adapter
  contract categories while preserving the no-runtime boundary.

Acceptance:

- Validation uses existing pinned local checkouts only.
- Validation records FastMCP, FastAPI, xyflow, and one additional available
  ecosystem shape.
- Validation records adapter decisions and diagnostics for each case.
- Validation records no adapter loading, no adapter execution, no package
  manager invocation, no dependency installation, no AI, no registry authority,
  and no accepted package/relation authority.
- Documentation and DocC explain how the real run follows P40-T6 and keeps
  adapter evidence producer-side only.
