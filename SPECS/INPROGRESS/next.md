# Next Task: P38-T2 Repository Plugin Registry Fixture

**Status:** In Progress
**Branch:** `feature/P38-T2-repository-plugin-registry-fixture`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T1 Repository Plugin Subsystem Contract

## Recently Archived

- `P38-T1` documented the repository plugin subsystem contract in
  `REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`.
- The contract defines plugin identity, plugin roles, registration metadata,
  static evidence, applicability checks, deterministic selection boundaries,
  output artifact categories, diagnostics, and authority limits.
- The planned machine-readable artifacts are named
  `SpecHarvesterRepositoryPluginRegistry` and
  `SpecHarvesterRepositoryPluginApplicabilityReport`.
- Parser profiles from Phase 36 map to the `parser_profile` role, and
  repository profile selection from Phase 37 maps to the
  `repository_profile` role.
- Plugin output remains producer-side evidence only. It must not accept
  packages, must not accept relations, must not publish registry metadata, must
  not seed baselines, must not remove `preview_only`, must not treat plugin
  output as registry truth, and must not treat AI output as registry truth.

## Current Task

`P38-T2` should add a machine-readable repository plugin registry fixture for
the contract introduced in P38-T1.

The fixture should define `SpecHarvesterRepositoryPluginRegistry` with:

- plugin ids;
- versioned contracts;
- plugin roles;
- input evidence kinds;
- output artifact kinds;
- safety constraints;
- applicability signals;
- fallback behavior;
- diagnostics vocabulary;
- non-authority statements.

## Motivation

P38-T1 documented the plugin subsystem boundary, but downstream tasks need a
small fixture before they can test applicability decisions, autonomous batch
sidecar evidence, or cross-ecosystem plugin behavior.

## Non-Goals

P38-T2 must not implement plugin execution, must not load third-party code,
must not change parser profile behavior, must not change repository profile
scoring, must not run package managers, must not install dependencies, must
not invoke AI, must not accept packages, must not accept relations, must not
publish registry metadata, must not remove `preview_only`, and must not treat
plugin registry records as accepted package truth.

## Planned Deliverables

- Add a registry fixture for `SpecHarvesterRepositoryPluginRegistry`.
- Add docs and DocC references for the fixture.
- Add docs-contract regression coverage.
- Keep the fixture language- and framework-agnostic.
- Archive the task through Flow.

## Boundary

The registry fixture is producer-side evidence about available plugin
contracts. It is not plugin execution, registry acceptance, package acceptance,
relation acceptance, or public metadata publication.
