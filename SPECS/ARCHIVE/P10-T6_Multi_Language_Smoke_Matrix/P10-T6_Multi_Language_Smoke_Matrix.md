# P10-T6 Multi-Language Smoke Matrix

Status: In Progress
Created: 2026-05-20
Task: `P10-T6` Add a reproducible multi-language smoke matrix covering local
repositories and synthetic fixtures for npm, SPM, Gradle/Maven, Go modules,
Composer, CMake, Xcode/CocoaPods, RubyGems, Python packaging, and at least one
documentation-first manifest-poor repository.

## Problem

SpecHarvester now has broad manifest-first ecosystem detection, optional
analyzer orchestration, language-neutral semantic extraction, and local smoke
fixture documentation. The project still lacks a compact, deterministic smoke
matrix that verifies those capabilities across the supported ecosystem spread in
one reviewable test surface.

Without this matrix, regressions can hide in ecosystems that are not represented
by ordinary unit fixtures, and reviewer confidence depends on ad hoc local
repository runs.

## Goals

- Add a deterministic multi-language smoke matrix that exercises supported
  manifest-first ecosystem detectors without executing repository code.
- Cover npm, SPM, Gradle/Maven, Go modules, Composer, CMake, Xcode/CocoaPods,
  RubyGems, Python packaging, and a documentation-first manifest-poor fixture.
- Verify `ProjectProfile` languages, ecosystems, analyzer plans, diagnostics,
  and documentation semantic fallback behavior.
- Keep fixtures synthetic, compact, and committed only as tests or docs, not as
  generated candidate outputs.
- Document how operators can use the smoke matrix alongside local adjacent
  repository checkouts under `~/Development/GitHub`.

## Non-Goals

- Do not clone repositories.
- Do not execute package managers, build systems, package scripts, tests,
  language servers, or network probes.
- Do not commit generated smoke outputs under `.smoke/`.
- Do not require optional external classifiers or Tree-sitter packages.
- Do not make the smoke matrix an acceptance decision for public SpecPM
  registry publication.

## Proposed Shape

- Add Python test fixtures that create tiny synthetic repositories in `tmp_path`.
- Run `collect_local_repository` and verify:
  - expected `ProjectProfile.languages`;
  - expected `ProjectProfile.ecosystems`;
  - expected analyzer plan ids/statuses;
  - no false execution/network behavior;
  - expected documentation-first semantic fallback for a manifest-poor repo.
- Add docs describing the smoke matrix scope and how it maps to local real
  repository checks.
- Add DocC mirror coverage and docs contract tests.

## Acceptance Criteria

- A single test or small test group covers all target ecosystem families.
- The matrix verifies at least:
  - npm JavaScript/TypeScript package evidence;
  - SwiftPM package evidence;
  - Gradle/Maven Java/Kotlin evidence;
  - Go module evidence;
  - Composer PHP evidence;
  - CMake C/C++ evidence;
  - Xcode/CocoaPods Objective-C/iOS evidence;
  - RubyGems/Bundler evidence;
  - Python packaging evidence;
  - documentation-first manifest-poor semantic extraction.
- The matrix remains deterministic and local-only.
- Documentation explains that generated smoke outputs remain ignored and should
  not be committed.
- Flow validation gates pass and coverage stays at or above the configured
  threshold.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
