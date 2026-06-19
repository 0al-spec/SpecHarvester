# Next Task: P39-T3 Deterministic Static Applicability Evaluator Helper

**Status:** Planned
**Branch:** `feature/P39-T3-deterministic-static-applicability-evaluator-helper`
**Phase:** Phase 39. Static Repository Plugin Applicability Evaluator
**Last Archived:** P39-T2 Static Plugin Evidence Envelope Fixture

## Recently Archived

- `P39-T2` added the machine-readable static plugin evidence envelope fixture
  in
  `tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
  The fixture records
  `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`,
  `spec-harvester.repository-plugin-static-evidence/v0`, source manifest
  metadata, `harvest.json`, `workspace-inventory.json`,
  `repository-profile-detection.json`, public-interface indexes, parser
  profile decisions, operator labels, safe relative paths, SHA-256 digests,
  `evidenceKinds[]`, advisory signals, `appliedToDrafting: false`,
  `registryAuthority: false`, and producer-side evidence that is not registry
  truth.
- `P39-T1` documented the static repository plugin applicability evaluator plan
  in `STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`. The plan defines a
  deterministic path from `SpecHarvesterRepositoryPluginRegistry` plus a
  static evidence envelope to
  `SpecHarvesterRepositoryPluginApplicabilityReport`, with
  selected/rejected/fallback/blocked decisions,
  `repository-plugin-applicability-detect` as the future CLI surface,
  `--repository-plugin-applicability` preserving explicit operator sidecar
  precedence, `appliedToDrafting: false`, `registryAuthority: false`, and
  producer-side evidence that is not registry truth.
- `P38-T6` recorded a real FastMCP plugin evidence run in
  `tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.
- Phase 38 is complete: repository plugin applicability is now described as a
  producer-side evidence contract, represented by registry/applicability
  fixtures, attached to autonomous batch output as a sidecar, covered by
  cross-ecosystem static examples, and validated on a pinned local FastMCP
  checkout.

## Current Task

`P39-T3` should implement the deterministic static applicability evaluator
helper.

The helper should read `SpecHarvesterRepositoryPluginRegistry` plus
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` and emit
`SpecHarvesterRepositoryPluginApplicabilityReport`.

## Motivation

P39-T1 defined the evaluator plan and P39-T2 defined the static evidence
envelope. The next step is deterministic selection logic that compares plugin
`inputEvidenceKinds[]` with available `evidenceKinds[]`, then emits selected,
rejected, fallback, and blocked plugin decisions with diagnostics.

## Non-Goals

P39-T3 must not add a CLI, must not change autonomous batch behavior, must not
load third-party plugin code, must not execute plugins, must not clone or fetch
repositories, must not install dependencies, must not invoke package managers,
must not execute harvested code, must not run AI, must not accept packages or
relations, must not publish registry metadata, must not remove `preview_only`,
and must not treat plugin decisions as registry truth.

## Planned Deliverables

- Add a deterministic evaluator helper module or domain object.
- Read the generic registry fixture and static evidence envelope fixture.
- Emit a `SpecHarvesterRepositoryPluginApplicabilityReport` shape with
  selected, rejected, fallback, and blocked plugin decisions.
- Preserve producer-side authorities and non-authority statements.
- Add regression coverage for required evidence matching, missing evidence
  blocking/fallback behavior, summary counts, diagnostics, and digest-safe
  references.
- Keep CLI exposure deferred to P39-T4.
- Archive the task through Flow.
