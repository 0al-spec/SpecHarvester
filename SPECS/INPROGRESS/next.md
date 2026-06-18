# Next Task: P38-T3 Repository Plugin Applicability Report Fixture

**Status:** In Progress
**Branch:** `feature/P38-T3-repository-plugin-applicability-report-fixture`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T2 Repository Plugin Registry Fixture

## Recently Archived

- `P38-T2` added the machine-readable repository plugin registry fixture at
  `tests/fixtures/repository_plugins/generic-registry.example.json`.
- The fixture defines `SpecHarvesterRepositoryPluginRegistry` with authority
  `producer_plugin_registry_only`.
- The registry records plugin roles for `parser_profile`,
  `repository_profile`, `evidence_producer`, `topology_helper`, and
  `review_surface`.
- The fixture records static evidence kinds, output artifact kinds, safety
  constraints, applicability signals, fallback behavior, diagnostics, and
  non-authority statements.
- Registry fixture output remains producer-side evidence only. It must not
  load third-party plugin code, must not execute plugins, must not accept
  packages, must not accept relations, must not publish registry metadata, must
  not remove `preview_only`, and must not treat plugin output as registry truth.

## Current Task

`P38-T3` should add a machine-readable
`SpecHarvesterRepositoryPluginApplicabilityReport` fixture.

The report should read the P38-T2 registry fixture conceptually and evaluate
several generic plugins against static repository evidence, recording:

P38-T3 reads the P38-T2 registry fixture as declared plugin contract input.

```text
selected, rejected, fallback, and blocked decisions
```

- selected plugin decisions;
- rejected plugin decisions;
- fallback decisions;
- blocked decisions;
- diagnostics and reason codes;
- evidence paths used for the decision;
- authority and non-authority boundaries.

## Motivation

P38-T2 declares available plugin contracts, but the next layer needs a
reviewable applicability decision shape before autonomous candidate batch can
consume plugin decisions as sidecar evidence.

## Non-Goals

P38-T3 must not implement plugin execution, must not run plugins, must not
load third-party code, must not change parser profile behavior, must not change
repository profile scoring, must not run package managers, must not install
dependencies, must not invoke AI, must not accept packages, must not accept
relations, must not publish registry metadata, and must not remove
`preview_only`.

## Planned Deliverables

- Add a fixture for `SpecHarvesterRepositoryPluginApplicabilityReport`.
- Add docs and DocC references for the fixture.
- Add docs-contract regression coverage.
- Keep decisions deterministic and based on static evidence.
- Archive the task through Flow.

## Boundary

Applicability reports are producer-side evidence. They can recommend which
declared plugin contracts apply to a repository shape, but they are not plugin
execution, package acceptance, relation acceptance, registry publication, or
accepted package truth.
