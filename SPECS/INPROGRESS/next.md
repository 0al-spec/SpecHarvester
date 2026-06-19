# Next Task: P40-T2 Repository Plugin Adapter Manifest Fixture

**Status:** In Progress
**Branch:** `feature/P40-T2-repository-plugin-adapter-manifest-fixture`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T1 Repository Plugin Adapter Contract

## Recently Archived

- `P40-T1` documented the language- and framework-agnostic repository plugin
  adapter contract.
- The GitHub-facing contract is
  `docs/REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterContract.md`.
- The contract defines adapter identity, manifest versioning, declared input
  evidence, output artifact categories, execution modes, sandbox expectations,
  diagnostics, adapter preflight, and review-only output evidence.
- Static applicability remains the default safe path.
- Adapter execution remains disabled until future explicit operator-controlled
  execution policy exists.
- Adapter output remains producer-side evidence and not registry truth.

## Task

Add a machine-readable `SpecHarvesterRepositoryPluginAdapterManifest` fixture.

## Why This Is Next

P40-T1 documented the adapter boundary. The next step is a concrete fixture
that downstream tests and future preflight policy can validate without loading
adapter code.

## Scope

- Add a JSON fixture for `SpecHarvesterRepositoryPluginAdapterManifest`.
- Include adapter ids, contract versions, supported roles, required and
  optional evidence kinds, declared outputs, execution mode, sandbox
  requirements, capability requests, and non-authority statements.
- Keep the fixture language- and framework-agnostic.
- Keep adapter execution disabled and review-only.

## Non-Goals

- Do not implement adapter preflight.
- Do not implement adapter loading or execution.
- Do not change static plugin applicability evaluation.
- Do not change `autonomous-candidate-batch`.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.
