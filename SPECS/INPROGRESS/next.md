# Next Task: P37-T8 Harvest Manifest Evidence for Repository Profile Detection

**Status:** In Progress
**Branch:** `feature/P37-T8-harvest-manifest-evidence-for-profile-detection`
**Phase:** Phase 37. Repository Profile Plugin Selection
**Last Archived:** P37-T7 Real Repository Profile Auto-Selection Run

## Recently Archived

- `P37-T7` recorded a real FastMCP auto-selection comparison in
  `tests/fixtures/repository_profile_real_runs/p37-t7-fastmcp-auto-selection-comparison.example.json`.
- The fixture uses `SpecHarvesterRepositoryProfileRealRunComparison` and is
  documented in `REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`.
- The real run used `--repository-profile-selection auto` for repository-wide
  input and `--repository-profile-selection none` for explicit manual
  `fastmcp_slim` targeting.
- Auto-selection passed as evidence but fell back to `generic.repository.v0`
  with low confidence.
- Manual `fastmcp_slim` targeting reduced public interface entrypoints from
  `772` to `260` and symbols from `9199` to `1563`.
- Both outputs remained `author_ready_draft`; the quality delta was public
  interface precision, not SpecPM acceptance.
- The verdict is `follow_up_required`: `harvest.json` saw `pyproject.toml`,
  but `workspace-inventory.json` had no manifest records, so profile detection
  lacked high-confidence manifest evidence.
- The result is producer-side evidence only. It does not accept packages, does
  not accept relations, does not publish registry metadata, does not remove
  `preview_only`, and does not treat profile decisions, profile hints, manual
  targeting, or AI output as registry truth.

## Current Task

`P37-T8` makes repository profile detection consume harvested package manifest
evidence when workspace inventory has no manifest records.

The implementation must remain language- and framework-agnostic. The goal is
not to recognize FastMCP. The goal is to let the generic profile detection layer
see already-collected static manifest paths such as root `pyproject.toml`,
`package.json`, `Cargo.toml`, `go.mod`, `Package.swift`, or equivalent future
manifest records when workspace inventory is empty.

## Motivation

P37-T7 showed that the current profile layer can explain fallback decisions, but
it can miss manifest evidence already present in `harvest.json`. That causes
auto-selection to fall back even when static package-manifest evidence exists.

## Non-Goals

This task must not implement a FastMCP-specific profile, Python-specific
profile, framework-specific profile, package manager execution, dependency
installation, network lookup, AI call, package acceptance, relation acceptance,
registry publication, `preview_only` removal, or SpecPM promotion.

It must not treat manifest evidence as registry truth. Manifest evidence remains
producer-side evidence for selecting or rejecting a profile.

## Planned Deliverables

- Extend repository profile detection input construction in autonomous batch so
  harvested package manifest paths can be used when workspace inventory has no
  manifest records.
- Add regression coverage for a root-manifest real-run shape without making
  FastMCP normative.
- Preserve fallback behavior for ambiguous, low-confidence, and conflicting
  evidence.
- Update docs and DocC to describe the manifest evidence fallback path.
- Record the validation result through Flow.

## Boundary

Repository profile selection remains producer-side evidence. It may improve
operator targeting, but it does not accept generated package claims or registry
state.
