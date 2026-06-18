# Next Task: P38-T4 Repository Plugin Batch Integration

**Status:** Planned
**Branch:** `feature/P38-T4-repository-plugin-batch-integration`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P38-T3 Repository Plugin Applicability Report Fixture

## Recently Archived

- `P38-T3` added the machine-readable repository plugin applicability report
  fixture at
  `tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
- The fixture defines `SpecHarvesterRepositoryPluginApplicabilityReport` with
  authority `producer_plugin_applicability_only`.
- Each plugin decision carries `decisionAuthority:
  producer_plugin_applicability_only` and `pluginOutputAuthority:
  producer_side_evidence_only`.
- The fixture reads the P38-T2 `SpecHarvesterRepositoryPluginRegistry` fixture
  as declared plugin contract input and records selected, rejected, fallback,
  and blocked decisions from static evidence.
- The fixture records diagnostics with `plugin_selected`, `plugin_fallback`,
  `plugin_rejected_low_confidence`, and
  `plugin_blocked_required_evidence_missing`.
- Applicability output remains sidecar producer evidence. It must not execute
  plugins, must not run AI, must not accept packages, must not accept
  relations, must not publish registry metadata, must not remove
  `preview_only`, and must not treat plugin decisions as registry truth.

## Current Task

`P38-T4` should connect plugin registry and applicability output to autonomous
candidate batch as sidecar producer evidence.

The integration reads registry and applicability fixtures while preserving
existing parser and repository profile behavior by default. It attaches
applicability decisions as reviewable evidence for later candidate review.

## Motivation

P38-T2 and P38-T3 define the registry and applicability report shapes, but
autonomous candidate batch still does not expose those decisions in its batch
artifacts. P38-T4 should make the evidence visible without giving plugin
decisions registry authority.

## Non-Goals

P38-T4 must not implement plugin execution, must not run plugins, must not
load third-party code, must not change parser profile behavior, must not change
repository profile scoring, must not run package managers, must not install
dependencies, must not invoke AI, must not accept packages, must not accept
relations, must not publish registry metadata, must not remove `preview_only`,
and must not treat plugin decisions as registry truth.

## Planned Deliverables

- Add an autonomous candidate batch sidecar evidence path for repository plugin
  registry/applicability output.
- Preserve existing parser profile and repository profile behavior unless a
  high-confidence plugin decision is explicitly selected in future work.
- Add docs and DocC updates for the batch integration boundary.
- Add regression coverage for sidecar evidence emission and non-authority
  guarantees.
- Archive the task through Flow.

## Boundary

Plugin applicability decisions can become batch-visible producer evidence.
They are not plugin execution, package acceptance, relation acceptance,
registry publication, accepted package truth, or permission to remove
`preview_only`.
