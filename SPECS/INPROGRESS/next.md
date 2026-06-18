# Next Task: P37-T5 Generic Profile Discovery Hints

**Status:** Planned
**Branch:** `feature/P37-T5-generic-profile-discovery-hints`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T4 Repository Profile Batch Integration

## Recently Archived

- `P37-T4` connected repository profile selection to
  `autonomous-candidate-batch` as producer-side evidence.
- The batch now accepts `--repository-profile-selection none|auto|<profile-id>`.
- The default mode remains `none` and preserves generic drafting behavior.
- Each processed repository gets a
  `SpecHarvesterRepositoryProfileDetection` artifact under
  `reports/repository-profile-detections/<repository-id>/repository-profile-detection.json`.
- Batch reports now include top-level `repositoryProfileSelection` and
  per-repository `repositoryProfileDetection` summaries.
- `auto` mode derives static evidence from existing `workspace-inventory.json`
  and can select `generic.package_set.v0` from root workspace plus member
  manifest evidence.
- Explicit profile ids are recorded as CLI overrides.
- Advisory hints remain evidence only:
  `advisoryHintsAppliedToDrafting: false`.
- The integration does not accept packages, accept relations, publish registry
  metadata, remove `preview_only`, or treat plugin decisions as registry truth.
- It does not treat plugin decisions as registry truth.

## Current Task

`P37-T5` defines generic workspace/member discovery hints produced by
repository profiles.

The hint vocabulary should cover:

- package-set root;
- member packages;
- meta packages;
- primary packages;
- CLI packages;
- bridge packages;
- plugin packages;
- example packages;
- test packages;
- documentation sources;
- generated artifacts;
- internal utilities;
- evidence-only sources.

## Motivation

P37-T4 records profile decisions and preserves generic drafting. The next
missing layer is a stable hint vocabulary that can make profile output useful
without making profile decisions authoritative.

Hints should let future repository profiles say "this path is probably an
example package" or "this path is probably a primary package" while keeping
review, drafting, and registry acceptance explicit.

## Non-Goals

This task must not implement ecosystem-specific plugins, change package-set
drafting semantics, accept packages or relations, remove `preview_only`, or
publish registry metadata.

It must not treat profile hints as registry truth.

## Planned Follow-Ups

- `P37-T6` Add cross-ecosystem profile fixtures proving the subsystem is not
  language-specific.
- `P37-T7` Re-run a real repository with profile auto-selection and compare it
  against manual targeting.

## Boundary

Repository profile hints are producer-side evidence. They may explain and
prepare future selection/drafting decisions, but they do not mutate source
candidates, accept registry state, or replace maintainer review.
