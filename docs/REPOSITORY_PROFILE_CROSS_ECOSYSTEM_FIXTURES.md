# Repository Profile Cross-Ecosystem Fixtures

Status: Phase 37 fixture coverage.

Repository profile selection must stay language- and framework-agnostic. These
fixtures exercise the same `SpecHarvesterRepositoryProfileDetection` contract
across different static repository shapes without implementing
ecosystem-specific plugins.

## Fixture Set

The fixture set covers workspace-shaped, single-package, nested-package, and
ambiguous multi-signal repositories.

The fixtures live under:

```text
tests/fixtures/repository_profile_detection/
```

| Fixture | Shape | Expected selection |
| --- | --- | --- |
| `cross-ecosystem-workspace.example.json` | workspace manifest plus multiple member manifests | `generic.package_set.v0` |
| `cross-ecosystem-single-package.example.json` | root package manifest plus docs | `generic.single_package.v0` |
| `cross-ecosystem-nested-package.example.json` | nested package manifests without workspace root evidence | fallback to `generic.repository.v0` |
| `cross-ecosystem-ambiguous-multi-signal.example.json` | workspace and documentation signals without enough member evidence | fallback to `generic.repository.v0` |

Each fixture uses:

```json
{
  "apiVersion": "spec-harvester.repository-profile-detection/v0",
  "kind": "SpecHarvesterRepositoryProfileDetection",
  "schemaVersion": 1,
  "authority": "producer_profile_selection_only"
}
```

## Expected Behavior

The workspace fixture selects `generic.package_set.v0` with high confidence and
emits generic hints:

- `package_set_root`;
- `member_package`;
- `documentation_source`.

The single-package fixture selects `generic.single_package.v0` with high
confidence from a root manifest.

The nested-package fixture records multiple nested manifest paths, but it does
not select a high-confidence profile because there is no workspace root signal.

The ambiguous multi-signal fixture records workspace and documentation signals,
but it falls back because the evidence does not identify one high-confidence
profile.

## Boundary

Cross-ecosystem fixtures are producer-side evidence only.

They do not implement ecosystem-specific plugins.

They do not:

- change profile scoring;
- collect source files;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run AI;
- accept packages;
- accept relations;
- publish registry metadata;
- remove `preview_only`;
- treat profile decisions as registry truth;
- treat profile hints as registry truth.

## Relationship to Parser Profiles

Parser profiles classify files inside a repository. Repository profile
selection classifies the repository shape before drafting. These fixtures only
exercise repository profile selection and generic discovery hints; they do not
add parser profile rules for any language or framework.
