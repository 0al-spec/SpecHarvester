# Next Task: P37-T2 Repository Profile Detection Fixture

**Status:** In Progress
**Branch:** `feature/P37-T2-repository-profile-detection-fixture`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T1 Repository Profile Selection Contract

## Recently Archived

- `P37-T1` added [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](../../docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md)
  and the DocC mirror `RepositoryProfileSelectionContract`.
- The contract defines the language- and framework-agnostic selection model:

  ```text
  detect candidates -> score evidence -> select or fallback -> record decision
  ```

- The contract defines static inputs, `auto | none | <profile-id>` selection
  modes, override precedence, confidence levels, fallback behavior, generic
  workspace/member hints, and non-authority boundaries.
- The future decision artifact is
  `SpecHarvesterRepositoryProfileDetection` with
  `apiVersion: spec-harvester.repository-profile-detection/v0` and
  `authority: producer_profile_selection_only`.
- Docs, DocC, capabilities, roadmap, and docs-contract tests now reference the
  repository profile selection contract.

## Current Task

`P37-T2` adds a machine-readable
`SpecHarvesterRepositoryProfileDetection` fixture format.

The fixture should record:

- repository identity and source manifest metadata;
- selection mode and override source;
- selected profile id or `null`;
- fallback profile id;
- candidate profiles with confidence, evidence paths, reason codes,
  conflicts, and recommended actions;
- rejected profiles and reason codes;
- diagnostics with severity, code, message, and evidence paths;
- non-authority statements;
- advisory downstream hints produced by the selected profile.

## Motivation

- P37-T1 documents the contract, but implementation needs a concrete fixture
  before code can safely emit or validate profile selection reports.
- The fixture should make profile selection replayable and reviewable without
  introducing a detector implementation yet.

## Non-Goals

This task must not implement runtime profile detection or change autonomous
candidate batch behavior.

It must not clone/fetch repositories, install dependencies, execute harvested
code, invoke package managers, run AI, draft packages, publish registry
metadata, accept packages or relations, remove `preview_only`, or treat AI
output or plugin decisions as registry truth.

## Planned Follow-Ups

- `P37-T3` Implement an opt-in repository profile detection CLI/report
  surface that emits the detection artifact only.
- `P37-T4` Connect repository profile selection to autonomous candidate batch
  as `auto | none | <profile-id>`.
- `P37-T5` Define generic workspace/member discovery hints produced by
  profiles.
- `P37-T6` Add cross-ecosystem profile fixtures proving the subsystem is not
  language-specific.
- `P37-T7` Re-run a real repository with profile auto-selection and compare it
  against manual targeting.

## Boundary

Repository profile detection fixtures remain producer-side evidence only. They
do not publish registry metadata, accept packages or relations, seed baselines,
remove `preview_only`, or treat AI output or plugin decisions as registry
truth.

It does not treat AI output or plugin decisions as registry truth.
It does not publish registry metadata.
