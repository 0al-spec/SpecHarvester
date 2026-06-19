# Next Task: P40-T3 Repository Plugin Adapter Preflight Report Fixture

**Status:** Planned
**Branch:** `feature/P40-T3-repository-plugin-adapter-preflight-report-fixture`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T2 Repository Plugin Adapter Manifest Fixture

## Recently Archived

- `P40-T2` added the first machine-readable
  `SpecHarvesterRepositoryPluginAdapterManifest` fixture.
- The fixture is
  `tests/fixtures/repository_plugins/adapter-manifest.example.json`.
- The GitHub-facing documentation is
  `docs/REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterManifestFixture.md`.
- The fixture declares adapter ids, contract versions, supported roles,
  required and optional evidence kinds, declared outputs, execution mode,
  sandbox requirements, capability requests, diagnostics, and non-authority
  statements.
- Fixture adapters use `mode: static_only`, `defaultEnabled: false`,
  `requiresOperatorOptIn: true`, `adapterCodeLoaded: false`, and
  `runtimeImplemented: false`.
- The fixture records `appliedToDrafting: false`, `registryAuthority: false`,
  `adapterPreflight: not_run`, and `adapterExecution: not_run`.

## Task

Add a repository plugin adapter preflight report fixture.

## Why This Is Next

P40-T2 declared adapter manifests. The next step is a machine-readable
preflight report shape that can validate adapter manifests against static
evidence and record allowed, rejected, fallback, and blocked adapter decisions
without executing adapter code.

## Scope

- Add a JSON fixture for `SpecHarvesterRepositoryPluginAdapterPreflightReport`.
- Validate the P40-T2 manifest fixture against static evidence envelope
  availability.
- Record allowed, rejected, fallback, and blocked adapter decisions.
- Refuse unsafe execution or missing required evidence before any adapter code
  can run.
- Keep the report language- and framework-agnostic and review-only.

## Non-Goals

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
