# P37-T4 Repository Profile Batch Integration

## Motivation

P37-T1 through P37-T3 defined repository profile selection as an explicit,
language- and framework-agnostic decision artifact. The autonomous candidate
batch still drafts packages through the existing generic path without recording
whether repository profile selection was disabled, attempted, selected, or
fell back.

This task connects that decision layer to autonomous batch runs so operators
can inspect profile selection evidence per repository without changing the
registry or treating advisory hints as truth.

## Goal

Add opt-in repository profile selection to autonomous candidate batch:

- `none` records a disabled decision artifact and preserves current behavior;
- `auto` derives static evidence from the collected repository artifacts and
  records the selected or fallback profile;
- explicit profile ids record operator override metadata;
- every processed repository gets a
  `SpecHarvesterRepositoryProfileDetection` artifact reference in the batch
  report.

The integration must remain producer-side evidence only. It must not accept
packages, accept relations, publish registry metadata, remove `preview_only`,
or use advisory hints as authoritative drafting input.

## Deliverables

- Add a repository profile selection option to autonomous candidate batch
  options and CLI.
- Emit a `repository-profile-detection.json` artifact for each processed
  repository.
- Attach a concise `repositoryProfileDetection` summary to each repository
  record in the autonomous candidate batch report.
- Derive static evidence paths from existing collected artifacts, especially
  `workspace-inventory.json`, without additional clone/fetch/install/build
  behavior.
- Preserve backwards-compatible generic behavior when selection is disabled,
  low confidence, ambiguous, or not configured.
- Update docs and DocC to describe the batch integration boundary.
- Add regression tests for disabled/default behavior, auto selection, explicit
  override, CLI wiring, and non-authority boundaries.

## Acceptance Criteria

- Autonomous candidate batch accepts `auto | none | <profile-id>` repository
  profile selection.
- The default mode is `none` and does not alter candidate drafting output.
- Each processed repository report includes:
  - profile detection artifact path;
  - selected profile id or `null`;
  - decision, confidence, and diagnostic codes.
- Auto mode can select `generic.package_set.v0` from existing workspace/member
  manifest evidence.
- Low-confidence or ambiguous evidence preserves generic fallback behavior.
- Explicit profile-id mode records `overrideSource: cli`.
- The generated detection artifact retains:
  - `apiVersion: spec-harvester.repository-profile-detection/v0`;
  - `kind: SpecHarvesterRepositoryProfileDetection`;
  - `schemaVersion: 1`;
  - `authority: producer_profile_selection_only`.
- Advisory hints are recorded only as evidence; they are not consumed as
  registry truth, package acceptance, relation acceptance, or `preview_only`
  removal.

## Non-Goals

- Do not implement a general plugin registry.
- Do not add ecosystem-specific profile plugins.
- Do not change package-set drafting semantics based on profile hints.
- Do not clone/fetch repositories beyond existing autonomous batch behavior.
- Do not install dependencies, execute harvested code, invoke package managers,
  or run AI solely for profile selection.
- Do not publish registry metadata, accept packages or relations, seed
  baselines, remove `preview_only`, or treat AI/plugin decisions as registry
  truth.

## Dependencies

- P37-T1 repository profile selection contract.
- P37-T2 repository profile detection fixture.
- P37-T3 `repository_profile_detection` module and CLI.
- Existing autonomous candidate batch collection and workspace inventory
  artifacts.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift build --target SpecHarvesterDocs`
