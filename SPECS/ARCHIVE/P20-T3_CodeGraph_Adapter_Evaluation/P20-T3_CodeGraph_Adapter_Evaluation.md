# P20-T3 — CodeGraph Adapter Evaluation

**Status:** Planned
**Priority:** P1
**Phase:** Phase 20. Scoped Source Unit Harvesting
**Date:** 2026-05-31

## Problem

SpecHarvester can now harvest scoped repository roots, folders, and files, but
non-package source units still need richer deterministic source-graph evidence.
`codegraph` may provide useful multi-language graph extraction, but it must not
become a trusted default dependency until its output contract, license, runtime
behavior, and failure modes are understood.

## Goals

- Evaluate `codegraph` as an optional local evidence adapter for scoped source
  units.
- Record package/license/version signals and trust-boundary assumptions.
- Inspect CLI/output schema stability and whether output can be normalized into
  SpecHarvester evidence without executing harvested code.
- Measure a small local smoke run on representative repositories or fixtures
  when the tool can be installed safely.
- Produce a concrete integration recommendation and follow-up tasks, without
  adding a default production dependency.

## Non-Goals

- Do not add `codegraph` as a required runtime dependency.
- Do not execute harvested package scripts, build tools, or project code.
- Do not replace existing language-specific public API analyzers.
- Do not commit third-party generated graph output unless it is small,
  deterministic, and necessary as a fixture.

## Deliverables

- Evaluation artifact documenting license, install surface, CLI contract,
  output schema, trust policy, version capture, digest requirements, and
  integration recommendation.
- Optional smoke script or fixture only if it is small, deterministic, and
  valuable for future adapter work.
- Workplan follow-up tasks for any recommended integration, schema hardening,
  or rejected-risk mitigation.
- Validation report with exact commands and outcomes.

## Acceptance Criteria

- The evaluation clearly says whether `codegraph` is suitable for a future
  optional adapter.
- Any recommended adapter boundary keeps `codegraph` evidence explicitly
  untrusted and records analyzer version plus source digests.
- The evaluation identifies how scoped folder/file harvesting would consume
  normalized graph evidence without overclaiming package-manager ownership.
- Tests, lint, format, coverage, Swift manifest, and DocC gates are run or
  explicitly justified if skipped.
