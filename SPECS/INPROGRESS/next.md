# Next Task: P40-T6 Repository Plugin Adapter Cross-Ecosystem Fixture Matrix

**Status:** In Progress
**Branch:** `feature/P40-T6-repository-plugin-adapter-cross-ecosystem-fixture-matrix`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T5 Adapter Evidence Batch Integration

## Recently Archived

- `P40-T5` connected adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence.
- The GitHub-facing batch documentation is
  `docs/AUTONOMOUS_CANDIDATE_BATCH.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/AutonomousCandidateBatch.md`.
- The batch now accepts explicit `--repository-plugin-adapter-manifest` and
  `--repository-plugin-adapter-preflight` inputs.
- Batch output records `repositoryPluginAdapterEvidence` with source paths,
  copied paths, SHA-256 digests, adapter counts,
  allowed/rejected/fallback/blocked counts, diagnostic codes,
  `appliedToDrafting: false`, `registryAuthority: false`, and
  `adapterExecution: not_run`.
- The existing static evaluator path remains unchanged unless an operator
  explicitly supplies adapter evidence.
- Adapter evidence remains producer-side review-only evidence and does not
  execute adapters or become registry truth.

## Task

Record a cross-ecosystem adapter contract fixture matrix for manifest-backed
single packages, workspaces, documentation-heavy repositories, nested package
roots, and ambiguous mixed layouts without loading third-party adapter code.

## Why This Is Next

P40-T5 gives batch runs a safe sidecar surface for adapter manifest and
preflight evidence. The next gap is fixture breadth: before any real adapter
runtime exists, the contract should demonstrate how the same manifest/preflight
shape handles multiple repository layouts without becoming language- or
framework-specific.

## Scope

- Add a fixture matrix for adapter contract scenarios across repository shapes.
- Cover manifest-backed single packages.
- Cover workspace/package-set repositories.
- Cover documentation-heavy repositories.
- Cover nested package roots.
- Cover ambiguous mixed layouts.
- Record expected adapter manifest/preflight evidence for each case.
- Record expected allowed, rejected, fallback, and blocked adapter decisions.
- Keep all fixtures language- and framework-agnostic.
- Keep all fixture decisions producer-side review evidence only.
- Prove that no third-party adapter code is loaded or executed.

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
- [ ] `P40-T6` Record a cross-ecosystem adapter contract fixture matrix for
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts without
  loading third-party adapter code.
- [ ] `P40-T7` Run a real local adapter-contract validation over existing
  pinned checkouts, comparing FastMCP, FastAPI, xyflow, and at least one
  additional ecosystem shape when available, while proving that adapters remain
  producer-side evidence only.

Motivation:

- Adapter manifest, preflight, execution policy, and batch sidecar plumbing now
  exist, but fixture coverage is still single-scenario.
- Operators need to see how the adapter contract behaves across common
  repository shapes before trusting it as a generic subsystem.
- A matrix catches schema and policy assumptions without introducing runtime
  adapter loading.

Goal:

- Provide a reviewable, machine-readable fixture matrix proving the adapter
  contract can describe several repository shapes while remaining static,
  language-neutral, and producer-side only.

Acceptance:

- Fixture matrix covers single-package, workspace, documentation-heavy, nested
  root, and ambiguous mixed layouts.
- Each case records expected adapter manifest/preflight evidence.
- Each case records allowed, rejected, fallback, and blocked decisions.
- Each case records no adapter loading, no adapter execution, no package
  manager invocation, no dependency installation, no AI, no registry authority,
  and no accepted package/relation authority.
- Documentation and DocC explain how the matrix fits after P40-T5 and before
  P40-T7.
