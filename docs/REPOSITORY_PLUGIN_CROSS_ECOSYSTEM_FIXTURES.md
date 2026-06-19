# Repository Plugin Cross-Ecosystem Fixtures

Status: Phase 38 fixture matrix.

P38-T5 adds static `SpecHarvesterRepositoryPluginApplicabilityReport` examples
for varied repository shapes. The goal is to prove that repository plugin
applicability is a language- and framework-agnostic contract, not a rule set
for one ecosystem.

Fixture directory:

```text
tests/fixtures/repository_plugins/cross_ecosystem/
```

## Matrix

| Fixture | Shape | Purpose |
| --- | --- | --- |
| `single-package-applicability.example.json` | `manifest_backed_single_package` | Shows selected parser, repository profile, and manifest summary evidence for one root package. |
| `workspace-package-set-applicability.example.json` | `workspace_or_multi_package` | Shows package-set topology and review-surface evidence when required static inputs already exist. |
| `documentation-heavy-applicability.example.json` | `documentation_heavy_repository` | Shows conservative fallback and blocked evidence producers when workspace inventory is unavailable. |
| `nested-package-roots-applicability.example.json` | `nested_package_roots` | Shows nested root and member manifest evidence without naming a language or package manager. |
| `ambiguous-mixed-layout-applicability.example.json` | `ambiguous_mixed_layout` | Shows rejection and blocked decisions when mixed manifests make root selection unsafe. |

## Contract Rules

Every fixture declares:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-applicability/v0",
  "kind": "SpecHarvesterRepositoryPluginApplicabilityReport",
  "schemaVersion": 1,
  "authority": "producer_plugin_applicability_only"
}
```

Each fixture references the P38-T2 registry fixture:

```text
tests/fixtures/repository_plugins/generic-registry.example.json
```

Selected plugins must have all of their declared `inputEvidenceKinds[]`
available in `staticEvidence.evidenceKinds[]`. Missing, ambiguous, or unsafe
inputs must produce `fallback`, `rejected`, or `blocked` decisions instead of
silent selection.

## Coverage

Across the matrix, fixtures cover:

- `selectedPlugins[]`;
- `rejectedPlugins[]`;
- `fallbackPlugins[]`;
- `blockedPlugins[]`;
- `plugin_selected`;
- `plugin_fallback`;
- `plugin_rejected_low_confidence`;
- `plugin_blocked_required_evidence_missing`.

The shapes are intentionally generic:

- manifest-backed single package;
- workspace or multi-package repository;
- documentation-heavy repository;
- nested package roots;
- ambiguous mixed layout.

## Non-Authority Boundary

These fixtures are static producer-side review evidence. They do not load
third-party plugin code, execute plugins, run plugin code, clone or fetch
repositories, install dependencies, execute harvested code, invoke package
managers, run AI, accept packages, accept relations, publish registry metadata,
remove `preview_only`, or treat plugin decisions as registry truth.

## Relationship to Later Tasks

- `P38-T6` should run one real repository through the repository plugin
  evidence path and compare the result with the Phase 37 repository profile
  behavior.
- Later runtime work may use the same fixture matrix as conformance input, but
  it must keep plugin execution and registry authority separate from these
  static examples.
