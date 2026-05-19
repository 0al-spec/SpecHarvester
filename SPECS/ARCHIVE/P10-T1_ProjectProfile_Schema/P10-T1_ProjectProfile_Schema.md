# P10-T1 ProjectProfile Schema

Status: In Progress
Created: 2026-05-19
Task: `P10-T1` Define a deterministic `ProjectProfile` schema for language,
package ecosystem, package manager, manifest, confidence, provenance, and
analyzer-plan evidence.

## Problem

SpecHarvester can collect package manifests and public interface indexes, but it
does not yet expose a stable repository-level profile that summarizes what kind
of project was found before draft generation. This makes future language
detectors and analyzer orchestration harder to review because each feature would
need to invent its own evidence shape.

## Goals

- Define a versioned `ProjectProfile` data shape that can be emitted inside
  harvest snapshots.
- Capture deterministic evidence for languages, ecosystems, package managers,
  manifests, confidence, diagnostics, and recommended static analyzers.
- Keep the schema local-only and evidence-first: no package execution,
  dependency installation, build invocation, or network probing.
- Add validation tests around the schema contract and initial profile generation
  from existing manifest evidence.

## Non-Goals

- Do not implement broad multi-language manifest detection beyond evidence that
  SpecHarvester already collects.
- Do not integrate external tools such as Linguist, `go-enry`, `Syft`,
  `ScanCode`, Universal Ctags, or Tree-sitter in this task.
- Do not automatically run analyzers during batch collection.
- Do not change SpecPM candidate drafting behavior beyond carrying the profile
  as evidence.

## Proposed Schema

`projectProfile` will be embedded in `SpecHarvesterEvidenceSnapshot` and include:

- `schemaVersion`: integer schema marker.
- `languages`: ranked language entries with `id`, `confidence`, `reason`, and
  evidence paths.
- `ecosystems`: ranked package ecosystem entries with package manager and
  manifest evidence.
- `manifests`: detected manifest records with path, ecosystem, package manager,
  digest, and parser identifier.
- `analyzerPlan`: recommended static analyzer entries with analyzer id,
  language/ecosystem target, status, reason, and evidence paths.
- `diagnostics`: ambiguity or missing-evidence notes.

## Acceptance Criteria

- Harvest snapshots include a deterministic `projectProfile` object.
- Swift/SPM and JavaScript/npm evidence already available from package manifests
  appears in the profile with evidence paths and confidence reasons.
- Unknown or README-only repositories receive an empty or low-confidence profile
  with diagnostics rather than invented language claims.
- Analyzer recommendations are advisory only and do not execute analyzers.
- Existing snapshot consumers continue to work when `projectProfile` is present.
- Tests cover Swift, JavaScript, mixed/unknown evidence, and deterministic
  ordering.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
