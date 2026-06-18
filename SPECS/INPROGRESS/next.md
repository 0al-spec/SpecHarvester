# Next Task: P37-T7 Real Repository Profile Auto-Selection Run

**Status:** Planned
**Branch:** `feature/P37-T7-real-repository-profile-auto-selection`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T6 Cross-Ecosystem Profile Fixtures

## Recently Archived

- `P37-T6` added cross-ecosystem repository profile detection fixtures.
- The fixture set lives under
  `tests/fixtures/repository_profile_detection/`.
- `cross-ecosystem-workspace.example.json` selects
  `generic.package_set.v0` with high confidence and emits
  `package_set_root`, `member_package`, and `documentation_source` hints.
- `cross-ecosystem-single-package.example.json` selects
  `generic.single_package.v0` with high confidence.
- `cross-ecosystem-nested-package.example.json` falls back to
  `generic.repository.v0` because nested manifests alone do not provide one
  high-confidence profile.
- `cross-ecosystem-ambiguous-multi-signal.example.json` falls back to
  `generic.repository.v0` because workspace/documentation signals are
  insufficient without enough member evidence.
- GitHub docs, DocC, capabilities, roadmap, and repository profile selection
  docs link `REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`.
- Cross-ecosystem fixtures remain producer-side evidence only: they do not
  implement ecosystem-specific plugins, accept packages, accept relations,
  publish registry metadata, remove `preview_only`, treat profile decisions as
  registry truth, or treat profile hints as registry truth.

## Current Task

`P37-T7` reruns a real repository with profile auto-selection and records a
quality comparison against manual targeting.

FastMCP may be used as the motivating validation case, but the report must
evaluate the generic subsystem:

- detection evidence;
- selected profile;
- confidence;
- overrides;
- public-interface precision;
- topology hints;
- author-ready output quality.

## Motivation

P37-T6 proves the contract with static fixtures. The next useful proof is a real
checkout run showing whether `--repository-profile-selection auto` improves or
at least explains the output compared with manual targeting.

## Non-Goals

This task must not implement ecosystem-specific plugins, change package-set
drafting semantics, accept packages or relations, remove `preview_only`, or
publish registry metadata.

It must not treat profile decisions, profile hints, manual targeting, or AI
output as registry truth.

## Planned Follow-Ups

- Decide whether Phase 37 is complete or whether another bounded profile
  selection task is needed before implementing ecosystem-specific plugins.

## Boundary

Real repository profile auto-selection output is producer-side evidence. It may
inform future profile plugin design, but it does not mutate source candidates,
accept registry state, or replace maintainer review.
