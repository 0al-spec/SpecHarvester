# Next Task: P38-T6 Real Repository Plugin Evidence Run

**Status:** In Progress
**Branch:** `feature/P38-T6-real-repository-plugin-evidence-run`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T5 Repository Plugin Cross-Ecosystem Fixtures

## Recently Archived

- `P38-T5` added cross-ecosystem static
  `SpecHarvesterRepositoryPluginApplicabilityReport` fixtures under
  `tests/fixtures/repository_plugins/cross_ecosystem/`.
- The fixture matrix covers manifest-backed single-package, workspace or
  multi-package, documentation-heavy, nested package root, and ambiguous mixed
  repository shapes.
- Regression coverage verifies fixture identity, summary counts, decision
  sets, diagnostics, non-authority statements, docs links, DocC links, and that
  every selected plugin has all required declared `inputEvidenceKinds[]`
  available in `staticEvidence.evidenceKinds[]`.
- The matrix covers `selectedPlugins[]`, `rejectedPlugins[]`,
  `fallbackPlugins[]`, `blockedPlugins[]`, `plugin_selected`,
  `plugin_fallback`, `plugin_rejected_low_confidence`, and
  `plugin_blocked_required_evidence_missing`.
- The fixtures remain static producer-side review evidence. They do not load
  third-party plugin code, execute plugins, run plugin code, clone or fetch
  repositories, install dependencies, execute harvested code, invoke package
  managers, run AI, accept packages, accept relations, publish registry
  metadata, remove `preview_only`, or treat plugin decisions as registry truth.

## Current Task

`P38-T6` should run one real repository through the repository plugin evidence
path and compare the result with the current Phase 37 repository profile
selection behavior.

The run should use an already-available local checkout or an explicitly
operator-provided local checkout. It should record producer-side evidence only
and should not turn plugin decisions into registry authority.

## Motivation

P38-T2 through P38-T5 define the plugin registry, applicability report,
autonomous batch sidecar integration, and static cross-ecosystem fixtures. The
next risk is that the fixture matrix looks good but the path has not been
checked against a real repository shape. P38-T6 should produce one practical
comparison artifact without adding runtime plugin execution.

## Non-Goals

P38-T6 must not implement plugin execution, load third-party code, clone or
fetch repositories, run package managers, install dependencies, execute
harvested code, invoke AI, accept packages, accept relations, publish registry
metadata, remove `preview_only`, or treat plugin decisions as registry truth.

## Planned Deliverables

- Run one local real repository through the repository plugin evidence path.
- Compare repository plugin applicability evidence with Phase 37 repository
  profile selection behavior.
- Record the result as a static review artifact or fixture.
- Document the run in GitHub docs and DocC.
- Add regression coverage for artifact identity, boundary, and documentation.
- Archive the task through Flow.

## Boundary

The real-repository run is local, static producer-side evidence. It is not
plugin execution, runtime plugin loading, package acceptance, relation
acceptance, registry publication, accepted package truth, or permission to
remove `preview_only`.
