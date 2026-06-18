# Next Task: P38-T1 Repository Plugin Subsystem Contract

**Status:** In Progress
**Branch:** `feature/P38-T1-repository-plugin-subsystem-contract`
**Phase:** Phase 38. Repository Plugin Subsystem
**Last Archived:** P37-T8 Harvest Manifest Evidence for Repository Profile Detection

## Recently Archived

- Phase 37 is complete.
- P37-T8 closed the harvested-manifest evidence gap found by the real FastMCP
  profile selection run.
- Repository profile detection now uses `workspace-inventory.json` evidence
  first and falls back to static manifest paths from `harvest.json` when
  workspace inventory has no manifest records.
- Repository profile selection remains producer-side evidence only: it does not
  accept packages, accept relations, publish registry metadata, remove
  `preview_only`, or replace maintainer review.

## Current Task

`P38-T1` documents a language- and framework-agnostic repository plugin
subsystem contract.

The contract should unify the ideas from:

- parser profiles from Phase 36;
- repository profile selection from Phase 37;
- future language/framework evidence producers;
- deterministic applicability and selection boundaries.

## Motivation

The current system has useful hooks for parser profiles and repository
profiles, but a real autonomous library harvester needs a broader plugin
subsystem. That subsystem should let future plugins provide static evidence and
applicability signals without turning into hidden heuristics or
ecosystem-specific special cases.

## Non-Goals

This task must not implement plugin loading, execute plugin code, add
ecosystem-specific plugins, change parser profile behavior, change repository
profile scoring, run package managers, install dependencies, fetch network
data, invoke AI, accept packages, accept relations, publish registry metadata,
remove `preview_only`, or treat plugin output as registry truth.

## Planned Deliverables

- Add a GitHub-facing repository plugin subsystem contract.
- Add a DocC mirror and index links.
- Update capabilities, roadmap, and workplan references.
- Add docs-contract regression coverage.
- Archive the task through Flow.

## Boundary

Repository plugins are producer-side evidence producers and applicability
helpers. They can improve candidate generation and review, but they do not
replace SpecPM validation or maintainer acceptance.
