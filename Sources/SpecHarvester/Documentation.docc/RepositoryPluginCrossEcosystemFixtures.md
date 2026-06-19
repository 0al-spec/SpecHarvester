# Repository Plugin Cross-Ecosystem Fixtures

P38-T5 adds static `SpecHarvesterRepositoryPluginApplicabilityReport` examples
for varied repository shapes. The matrix proves that repository plugin
applicability is language- and framework-agnostic.

Fixture directory:

```text
tests/fixtures/repository_plugins/cross_ecosystem/
```

## Matrix

| Fixture | Shape | Purpose |
| --- | --- | --- |
| `single-package-applicability.example.json` | `manifest_backed_single_package` | Selected parser, repository profile, and manifest summary evidence for one root package. |
| `workspace-package-set-applicability.example.json` | `workspace_or_multi_package` | Package-set topology and review-surface evidence when required static inputs already exist. |
| `documentation-heavy-applicability.example.json` | `documentation_heavy_repository` | Conservative fallback and blocked evidence producers when workspace inventory is unavailable. |
| `nested-package-roots-applicability.example.json` | `nested_package_roots` | Nested root and member manifest evidence without naming a language or package manager. |
| `ambiguous-mixed-layout-applicability.example.json` | `ambiguous_mixed_layout` | Rejection and blocked decisions when mixed manifests make root selection unsafe. |

## Contract Rules

Every fixture declares `apiVersion:
spec-harvester.repository-plugin-applicability/v0`, `kind:
SpecHarvesterRepositoryPluginApplicabilityReport`, `schemaVersion: 1`, and
`authority: producer_plugin_applicability_only`.

Selected plugins must have all declared `inputEvidenceKinds[]` available in
`staticEvidence.evidenceKinds[]`. Missing, ambiguous, or unsafe inputs must
produce `fallback`, `rejected`, or `blocked` decisions instead of silent
selection.

## Coverage

Across the matrix, fixtures cover `selectedPlugins[]`, `rejectedPlugins[]`,
`fallbackPlugins[]`, `blockedPlugins[]`, `plugin_selected`,
`plugin_fallback`, `plugin_rejected_low_confidence`, and
`plugin_blocked_required_evidence_missing`.

## Non-Authority Boundary

These fixtures are static producer-side review evidence. They do not load
third-party plugin code, execute plugins, run plugin code, clone or fetch
repositories, install dependencies, execute harvested code, invoke package
managers, run AI, accept packages, accept relations, publish registry metadata,
remove `preview_only`, or treat plugin decisions as registry truth.

## Relationship to Real Runs

P38-T6 records <doc:RepositoryPluginRealRunFastMCP> as a real repository run
through the repository plugin evidence path, compared with current Phase 37
repository profile behavior. Later runtime work may use the same fixture
matrix as conformance input, but it must keep plugin execution and registry
authority separate from these static examples.
