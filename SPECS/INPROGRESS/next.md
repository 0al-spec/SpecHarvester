# Next Task: P38-T5 Repository Plugin Cross-Ecosystem Fixtures

**Status:** In Progress
**Branch:** `feature/P38-T5-repository-plugin-cross-ecosystem-fixtures`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T4 Repository Plugin Batch Integration

## Recently Archived

- `P38-T4` connected `SpecHarvesterRepositoryPluginApplicabilityReport`
  sidecar evidence to `autonomous-candidate-batch`.
- The batch now accepts `--repository-plugin-applicability` and copies the
  provided report to
  `reports/repository-plugin-applicability/repository-plugin-applicability-report.json`.
- The autonomous batch report records `repositoryPluginApplicability` with
  path, SHA-256 digest, `apiVersion`, `kind`, `schemaVersion`, `authority`,
  mode, repository metadata, registry metadata, selected/rejected/fallback/
  blocked counts, diagnostic codes, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- Default batch behavior remains explicit and unchanged: when no applicability
  sidecar is provided, the report records `status: not_provided` and
  `repositoryPluginApplicabilitySidecarCount: 0`.
- The integration validates sidecar identity before copying it.
- P38-T4 preserved the producer-only boundary: it does not execute plugins,
  load third-party plugin code, change parser profile behavior, change
  repository profile scoring, run package managers, install dependencies,
  invoke AI, accept packages, accept relations, publish registry metadata, seed
  baselines, remove `preview_only`, or treat plugin decisions as registry
  truth.

## Current Task

`P38-T5` should add cross-ecosystem repository plugin subsystem fixtures that
exercise the registry/applicability/report shapes beyond the generic workspace
example.

The fixtures should stay language- and framework-agnostic in contract terms
while covering varied repository shapes:

- manifest-backed single-package repositories;
- workspace or multi-package repositories;
- documentation-heavy repositories;
- nested package roots;
- ambiguous mixed layouts.

## Motivation

P38-T2 through P38-T4 define the plugin registry, applicability report, and
batch sidecar integration. The next risk is overfitting those contracts to the
single generic workspace fixture. P38-T5 should prove the subsystem can describe
different repository shapes without making JavaScript, Python, FastAPI,
FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle, or any other ecosystem
normative.

## Non-Goals

P38-T5 must not implement plugin execution, load third-party code, run
package managers, install dependencies, clone or fetch repositories, execute
harvested code, invoke AI, accept packages, accept relations, publish registry
metadata, remove `preview_only`, or treat plugin decisions as registry truth.

## Planned Deliverables

- Add cross-ecosystem plugin applicability fixture examples.
- Cover selected, rejected, fallback, and blocked decisions across varied
  repository shapes.
- Document the fixture matrix in GitHub docs and DocC.
- Add regression coverage that keeps fixture identity, authority, and
  non-authority boundaries stable.
- Archive the task through Flow.

## Boundary

Cross-ecosystem fixtures are static producer-side review evidence. They are
not plugin execution, runtime plugin loading, package acceptance, relation
acceptance, registry publication, accepted package truth, or permission to
remove `preview_only`.
