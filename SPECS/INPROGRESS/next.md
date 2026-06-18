# Next Task: P37-T4 Repository Profile Batch Integration

**Status:** In Progress
**Branch:** `feature/P37-T4-repository-profile-batch-integration`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T3 Repository Profile Detection CLI

## Recently Archived

- `P37-T3` added the opt-in `repository-profile-detect` CLI/report surface.
- The command emits `SpecHarvesterRepositoryProfileDetection` with
  `apiVersion: spec-harvester.repository-profile-detection/v0`,
  `kind: SpecHarvesterRepositoryProfileDetection`,
  `schemaVersion: 1`, and
  `authority: producer_profile_selection_only`.
- The command supports `--selection auto`, `--selection none`, and explicit
  profile ids such as `--selection custom.vendor_profile.v0`.
- The command reads only CLI arguments and optional source manifest metadata.
- The command can write JSON to stdout and optionally to `--output`.
- The command records candidate profiles, rejected profiles, diagnostics,
  non-authority statements, and advisory downstream hints.
- It does not collect source files, run analyzers, invoke package managers,
  run AI, draft packages, publish registry metadata, accept packages or
  relations, remove `preview_only`, or treat plugin decisions as registry
  truth.
- It does not run AI.
- It does not draft packages.
- It does not treat plugin decisions as registry truth.

## Current Task

`P37-T4` connects repository profile selection to autonomous candidate batch as
an explicit decision layer.

The integration should:

- add an explicit `auto | none | <profile-id>` repository profile selection
  option to autonomous candidate batch;
- preserve backwards-compatible generic behavior when selection is disabled,
  low confidence, ambiguous, or not configured;
- emit or attach the `SpecHarvesterRepositoryProfileDetection` artifact for
  each processed repository;
- keep profile decisions producer-side evidence only;
- avoid treating advisory hints as registry truth;
- avoid changing package acceptance, relation acceptance, or `preview_only`.

## Motivation

- P37-T1 defined the contract.
- P37-T2 defined the machine-readable artifact shape.
- P37-T3 provided a narrow standalone CLI/report surface.
- P37-T4 should make autonomous runs explain why profile selection was applied
  or why they fell back to generic behavior.

## Non-Goals

This task must not implement a general plugin registry or ecosystem-specific
profile plugins.

It must not clone/fetch repositories beyond existing autonomous batch source
manifest behavior, install dependencies, execute harvested code, invoke
package managers, run AI solely for profile selection, publish registry
metadata, accept packages or relations, remove `preview_only`, or treat AI
output or plugin decisions as registry truth.

## Planned Follow-Ups

- `P37-T5` Define generic workspace/member discovery hints produced by
  profiles.
- `P37-T6` Add cross-ecosystem profile fixtures proving the subsystem is not
  language-specific.
- `P37-T7` Re-run a real repository with profile auto-selection and compare it
  against manual targeting.

## Boundary

Repository profile selection in autonomous batch remains producer-side
evidence only. It can explain and record profile decisions, but it does not
publish registry metadata, accept packages or relations, seed baselines, remove
`preview_only`, or treat AI output or plugin decisions as registry truth.
It does not treat AI output or plugin decisions as registry truth.
