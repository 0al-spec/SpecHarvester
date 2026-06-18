# Repository Profile Cross-Ecosystem Fixtures

Repository profile cross-ecosystem fixtures prove that profile selection is
driven by static repository shape rather than a language or framework rule.

The fixtures live under:

```text
tests/fixtures/repository_profile_detection/
```

The fixture set covers workspace-shaped, single-package, nested-package, and
ambiguous multi-signal repositories.

| Fixture | Shape | Expected selection |
| --- | --- | --- |
| `cross-ecosystem-workspace.example.json` | workspace manifest plus multiple member manifests | `generic.package_set.v0` |
| `cross-ecosystem-single-package.example.json` | root package manifest plus docs | `generic.single_package.v0` |
| `cross-ecosystem-nested-package.example.json` | nested package manifests without workspace root evidence | fallback to `generic.repository.v0` |
| `cross-ecosystem-ambiguous-multi-signal.example.json` | workspace and documentation signals without enough member evidence | fallback to `generic.repository.v0` |

Each fixture uses `apiVersion:
spec-harvester.repository-profile-detection/v0`,
`kind: SpecHarvesterRepositoryProfileDetection`, `schemaVersion: 1`, and
`authority: producer_profile_selection_only`.

The workspace fixture emits generic discovery hints for `package_set_root`,
`member_package`, and `documentation_source`. The single-package fixture selects
`generic.single_package.v0`. The nested-package and ambiguous multi-signal
fixtures fall back to `generic.repository.v0` because no single
high-confidence profile is selected.

## Boundary

These fixtures do not implement ecosystem-specific plugins, change profile
scoring, collect source files, install dependencies, execute harvested code,
invoke package managers, run AI, accept packages, accept relations, publish
registry metadata, remove `preview_only`, treat profile decisions as registry
truth, or treat profile hints as registry truth.
