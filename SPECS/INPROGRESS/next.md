# Next Task: P37-T6 Cross-Ecosystem Profile Fixtures

**Status:** In Progress
**Branch:** `feature/P37-T6-cross-ecosystem-profile-fixtures`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T5 Generic Profile Discovery Hints

## Recently Archived

- `P37-T5` defined `SpecHarvesterRepositoryProfileHintVocabulary`.
- The generic vocabulary uses
  `apiVersion: spec-harvester.repository-profile-hints/v0`,
  `kind: SpecHarvesterRepositoryProfileHintVocabulary`,
  `schemaVersion: 1`, and
  `authority: producer_profile_hint_vocabulary_only`.
- The fixture lives at
  `tests/fixtures/repository_profile_detection/generic-hint-vocabulary.example.json`.
- The vocabulary contains 13 stable hints:
  `package_set_root`, `member_package`, `meta_package`, `primary_package`,
  `cli_package`, `bridge_package`, `plugin_package`, `example_package`,
  `test_package`, `documentation_source`, `generated_artifact`,
  `internal_utility`, and `evidence_only`.
- Current repository profile detection now emits canonical ids for
  `package_set_root`, `member_package`, and `documentation_source`.
- Current hint emission rejects unknown built-in generic hint ids.
- GitHub docs, DocC, capabilities, roadmap, and repository profile selection
  docs link the vocabulary.
- Repository profile hints remain producer-side evidence only: they do not
  accept packages, do not accept relations, do not remove `preview_only`, do
  not publish registry metadata, or treat profile hints as registry truth.

## Current Task

`P37-T6` adds cross-ecosystem profile fixtures proving the repository profile
selection subsystem is not language-specific.

The fixture set should cover:

- one workspace-shaped repository;
- one single-package repository;
- one nested-package repository;
- one ambiguous multi-signal repository.

## Motivation

P37-T5 made the generic hint vocabulary stable. The next missing proof is that
profile selection and discovery hints work across repository shapes instead of
encoding one language, package manager, or framework layout.

## Non-Goals

This task must not implement ecosystem-specific plugins, change package-set
drafting semantics, accept packages or relations, remove `preview_only`, or
publish registry metadata.

It must not treat profile decisions or profile hints as registry truth.

## Planned Follow-Ups

- `P37-T7` Re-run a real repository with profile auto-selection and compare it
  against manual targeting.

## Boundary

Cross-ecosystem profile fixtures are static producer-side evidence. They may
exercise profile selection and hints, but they do not mutate source candidates,
accept registry state, or replace maintainer review.
