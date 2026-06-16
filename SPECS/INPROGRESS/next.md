# Next Task: P37-T1 Repository Profile Selection Contract

**Status:** In Progress
**Branch:** `feature/P37-T1-repository-profile-selection-contract`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P36-T4 FastAPI AI-Enabled Parser Profile Rerun

## Recently Archived

- `P36-T4` reran FastAPI with `--parser-profile python.web_framework.v0`
  and live LM Studio model `openai/gpt-oss-20b`.
- Baseline public interface evidence had `1121` entrypoints, `6009` symbols,
  and `454` `docs_src/*` entrypoints.
- Profiled public interface evidence had `48` entrypoints, `298` symbols, and
  `0` `docs_src/*` entrypoints.
- FastAPI package entrypoints stayed at `48`, proving the profile removed
  tutorial evidence without dropping the package surface.
- The candidate reported `author_ready_draft`.
- AI draft and AI enrichment artifacts had warning-level gaps, so the result
  is closer to registry-review quality on evidence boundary but is not a clean
  registry handoff.
- The durable report fixture is
  `tests/fixtures/fastapi_parser_profile_rerun/p36-t4-fastapi-parser-profile-rerun.example.json`.
- Phase 36 proved that parser profiles can improve evidence boundaries, but
  profile choice still requires explicit operator selection.
- A practical FastMCP dry run showed the next gap: generic collection can
  over-include docs/examples, while manually targeted member packages produce
  better author-ready starter packages.

## Current Task

`P37-T1` documents a language- and framework-agnostic repository profile
selection contract.

The task must define the shared selection model:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

The contract should cover:

- static detection inputs such as manifests, workspace files, package
  metadata, lock/workspace files, directory layout, and allowlisted metadata;
- candidate profile scoring and confidence levels;
- explicit CLI and manifest overrides;
- `auto`, `none`, and explicit profile selection modes;
- ambiguous, low-confidence, conflicting, and unsupported profile handling;
- fallback to generic behavior when auto-selection is not safe;
- a replayable `SpecHarvesterRepositoryProfileDetection` decision artifact;
- non-authority boundaries for generated profile decisions.

## Motivation

- SpecHarvester should not guess repository shape through hidden heuristics.
- Language/framework plugins may provide evidence, but the core selection
  subsystem must decide and record why a plugin was or was not applied.
- FastMCP is a useful motivating case, but the contract must remain reusable
  for Python, JavaScript/TypeScript, Rust, Go, Swift, JVM, and future
  ecosystems.

## Non-Goals

This task does not implement a detector or a new ecosystem parser. It only
defines the contract and workplan surface for the subsystem.

It must not:

- clone/fetch repositories;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run AI;
- draft packages;
- publish registry metadata;
- accept packages or relations;
- remove `preview_only`;
- treat AI output or plugin decisions as registry truth.

## Planned Follow-Ups

- `P37-T2` Add a machine-readable
  `SpecHarvesterRepositoryProfileDetection` fixture format.
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

Repository profile selection remains producer-side evidence only. It does not
publish registry metadata, accept packages or relations, seed baselines,
remove `preview_only`, or accept plugin decisions as registry truth. It does
not treat AI output as registry truth.
