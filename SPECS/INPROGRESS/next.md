# Next Task: Phase 38 Complete

**Status:** Phase Complete
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T6 Real Repository Plugin Evidence Run

## Recently Archived

- `P38-T1` documented the language- and framework-agnostic repository plugin
  subsystem contract.
- `P38-T2` added the machine-readable
  `SpecHarvesterRepositoryPluginRegistry` fixture.
- `P38-T3` added the machine-readable
  `SpecHarvesterRepositoryPluginApplicabilityReport` fixture for selected,
  rejected, fallback, and blocked decisions.
- `P38-T4` connected applicability reports to `autonomous-candidate-batch` as
  `repositoryPluginApplicability` sidecar evidence with
  `appliedToDrafting: false` and `registryAuthority: false`.
- `P38-T5` added cross-ecosystem static applicability fixtures for
  single-package, workspace, documentation-heavy, nested, and ambiguous
  repository shapes.
- `P38-T6` recorded a real FastMCP plugin evidence run in
  `tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.

## Phase Result

Phase 38 is complete. Repository plugin applicability is now described as a
producer-side evidence contract, represented by registry/applicability
fixtures, attached to autonomous batch output as a sidecar, covered by
cross-ecosystem static examples, and validated on a pinned local FastMCP
checkout.

The real FastMCP run shows current repository profile selection choosing
`generic.single_package.v0`, while plugin applicability remains review
evidence and does not change drafting, parser behavior, profile scoring, or
registry authority.

## Boundary

Phase 38 does not load third-party plugin code, execute plugins, run plugin
code, clone or fetch repositories, install dependencies, execute harvested
code, invoke package managers, run AI, accept packages, accept relations,
publish registry metadata, remove `preview_only`, or treat plugin decisions as
registry truth.

## Next Planning Note

No Phase 38 task remains selected. The next phase should be defined explicitly
before starting another Flow branch.
