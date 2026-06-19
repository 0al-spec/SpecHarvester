# Next Task: P40-T4 Adapter Execution Policy

**Status:** In Progress
**Branch:** `feature/P40-T4-adapter-execution-policy`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T3 Repository Plugin Adapter Preflight Report Fixture

## Recently Archived

- `P40-T3` added the first machine-readable
  `SpecHarvesterRepositoryPluginAdapterPreflightReport` fixture.
- The fixture is
  `tests/fixtures/repository_plugins/adapter-preflight-report.example.json`.
- The GitHub-facing documentation is
  `docs/REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterPreflightReportFixture.md`.
- The report validates the P40-T2 adapter manifest against static evidence
  availability by safe relative paths and SHA-256 digests.
- The report records allowed, rejected, fallback, and blocked adapter
  decisions.
- The report keeps `adapterCodeLoaded: false`, `adapterExecution: not_run`,
  and `executedAdapterCount: 0`.
- The report records `producer_plugin_adapter_preflight_only` authority,
  `registryAuthority: false`, and producer-side review-only boundaries.

## Task

Define adapter execution policy for future local adapters.

## Why This Is Next

P40-T3 now records adapter preflight decisions before runtime. The next step is
to define the future execution policy vocabulary and safety rules before any
adapter loading path exists.

## Scope

- Define default disabled execution for all repository plugin adapters.
- Define static-only mode as the only currently safe mode.
- Define future bounded local trusted mode as explicit policy, not
  implementation.
- Require path allowlists for every future non-static mode.
- Require no dependency installation.
- Require no package manager invocation.
- Require no network discovery.
- Require no harvested code execution.
- Require explicit operator opt-in for every non-static mode.
- Keep adapter output producer-side review evidence only.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not connect adapters to autonomous batch.
- Do not change static plugin applicability evaluation.
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
- [ ] `P40-T4` Define adapter execution policy for future local adapters:
  default disabled execution, static-only mode, bounded local trusted mode,
  path allowlists, no dependency installation, no package manager invocation,
  no network discovery, no harvested code execution, and explicit operator
  opt-in for every non-static mode.
- [ ] `P40-T5` Connect adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence while keeping
  the existing static evaluator path unchanged unless an operator explicitly
  supplies adapter evidence.
- [ ] `P40-T6` Record a cross-ecosystem adapter contract fixture matrix for
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts without
  loading third-party adapter code.
- [ ] `P40-T7` Run a real local adapter-contract validation over existing
  pinned checkouts, comparing FastMCP, FastAPI, xyflow, and at least one
  additional ecosystem shape when available, while proving that adapters remain
  producer-side evidence only.

Motivation:

- P40-T1 defined the adapter boundary, P40-T2 declared adapter manifests, and
  P40-T3 added preflight decisions.
- Before adapter evidence can participate in broader producer flows, the
  execution policy must make disabled-by-default behavior explicit.
- Future ecosystem-specific precision should improve review evidence without
  granting adapters crawler, build, package-manager, AI, or registry authority.

Goal:

- Define the future adapter execution safety policy in a language- and
  framework-agnostic way before any adapter runtime is implemented.

Acceptance:

- The policy keeps adapter execution disabled by default.
- Static-only mode remains the current safe path.
- Every future non-static mode requires explicit operator opt-in.
- Dependency installation, package manager invocation, network discovery, and
  harvested code execution remain blocked by default.
- Adapter output remains producer-side review evidence only.
