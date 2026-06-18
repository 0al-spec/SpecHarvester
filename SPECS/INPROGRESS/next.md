# Next Task: P37-T3 Repository Profile Detection CLI

**Status:** In Progress
**Branch:** `feature/P37-T3-repository-profile-detection-cli`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T2 Repository Profile Detection Fixture

## Recently Archived

- `P37-T2` added the machine-readable fixture
  [`generic-package-set.example.json`](../../tests/fixtures/repository_profile_detection/generic-package-set.example.json).
- The fixture records
  `apiVersion: spec-harvester.repository-profile-detection/v0`,
  `kind: SpecHarvesterRepositoryProfileDetection`,
  `schemaVersion: 1`, and
  `authority: producer_profile_selection_only`.
- The fixture demonstrates a high-confidence `auto` selection of
  `generic.package_set.v0`, a `generic.repository.v0` fallback, rejected
  lower-confidence profiles, diagnostics, and advisory downstream hints.
- The fixture records `package_set_root`, `member_package`, and
  `documentation_source` hints without treating them as registry truth.
- Docs, DocC, and docs-contract tests now validate the fixture shape and
  non-authority boundary.

## Current Task

`P37-T3` implements an opt-in repository profile detection CLI/report surface
that emits a `SpecHarvesterRepositoryProfileDetection` artifact.

The command should:

- read only static repository evidence already available from operator input;
- accept `auto | none | <profile-id>` selection mode;
- accept optional CLI override metadata;
- emit the detection artifact shape introduced in P37-T2;
- preserve explicit fallback to `generic.repository.v0`;
- report candidate profiles, rejected profiles, diagnostics, non-authority
  statements, and advisory downstream hints;
- remain deterministic and reviewable.

## Motivation

- P37-T1 defined the selection contract.
- P37-T2 made the artifact shape concrete.
- P37-T3 should provide the first narrow executable surface so operators can
  generate the artifact deliberately before it is wired into autonomous batch
  behavior.

## Non-Goals

This task must not connect profile selection to autonomous candidate batch
behavior.

It must not clone/fetch repositories, install dependencies, execute harvested
code, invoke package managers, run AI, draft packages, collect source files,
publish registry metadata, accept packages or relations, remove `preview_only`,
or treat AI output or plugin decisions as registry truth.

## Planned Follow-Ups

- `P37-T4` Connect repository profile selection to autonomous candidate batch
  as `auto | none | <profile-id>`.
- `P37-T5` Define generic workspace/member discovery hints produced by
  profiles.
- `P37-T6` Add cross-ecosystem profile fixtures proving the subsystem is not
  language-specific.
- `P37-T7` Re-run a real repository with profile auto-selection and compare it
  against manual targeting.

## Boundary

Repository profile detection remains producer-side evidence only. It does not
publish registry metadata, accept packages or relations, seed baselines, remove
`preview_only`, or treat AI output or plugin decisions as registry truth.

It does not clone or fetch repositories.
It does not run AI.
It does not draft packages.
It does not treat AI output or plugin decisions as registry truth.
