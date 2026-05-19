# P10-T2 Manifest-First Ecosystem Detectors

Status: In Progress
Created: 2026-05-19
Task: `P10-T2` Add manifest-first ecosystem detectors for Swift/SPM,
JavaScript and TypeScript package managers, Python, Java/Kotlin, Go, PHP,
C/C++, Objective-C/iOS, Ruby, and Rust without executing package code.

## Problem

`ProjectProfile` exists, but it currently maps only `package.json` and
`Package.swift` evidence. SpecHarvester needs a broader manifest-first detector
matrix so weak-model drafting and later analyzer orchestration can start from
deterministic package evidence across common ecosystems.

## Goals

- Detect common ecosystem manifests using file names and parsed static metadata
  only.
- Extend `projectProfile` with deterministic language, ecosystem, package
  manager, parser, confidence, and analyzer-plan evidence.
- Cover the requested matrix: npm/pnpm/yarn/bun, SwiftPM, Python packaging,
  Maven/Gradle, Go modules, Composer, CMake/Meson/Autotools/Conan/vcpkg,
  Xcode/CocoaPods, RubyGems/Bundler, and Cargo.
- Preserve strict trust boundaries: no build execution, package manager
  execution, dependency installation, package scripts, or network probes.

## Non-Goals

- Do not integrate external classifiers such as Linguist, `go-enry`, `Syft`,
  `ScanCode`, Universal Ctags, or Tree-sitter.
- Do not parse full build DSLs. Minimal manifest metadata extraction is
  acceptable only when deterministic and local.
- Do not run language analyzers automatically; analyzer plan entries remain
  advisory.
- Do not change drafting behavior beyond richer snapshot evidence.

## Detector Matrix

- JavaScript/TypeScript: `package.json`, `pnpm-workspace.yaml`,
  `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock`,
  `bun.lock`, `bun.lockb`.
- Swift/SPM: `Package.swift`.
- Python: `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`.
- Java/Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`,
  `settings.gradle`, `settings.gradle.kts`, `gradle.properties`.
- Go: `go.mod`.
- PHP: `composer.json`, `composer.lock`.
- C/C++: `CMakeLists.txt`, `meson.build`, `configure.ac`, `configure.in`,
  `Makefile`, `conanfile.txt`, `conanfile.py`, `vcpkg.json`.
- Objective-C/iOS: `*.xcodeproj/project.pbxproj`, `*.xcworkspace`, `Podfile`,
  `Podfile.lock`.
- Ruby: `Gemfile`, `Gemfile.lock`, `*.gemspec`.
- Rust: `Cargo.toml`, `Cargo.lock`.

## Acceptance Criteria

- `collect_local_repository` includes manifest candidates from the detector
  matrix when they exist in the root repository or known safe package locations.
- `projectProfile.languages`, `projectProfile.ecosystems`,
  `projectProfile.manifests`, and `projectProfile.analyzerPlan` are populated
  deterministically from supported manifest evidence.
- Unsupported or ambiguous collected manifests produce diagnostics rather than
  invented claims.
- Tests cover each language/ecosystem family with synthetic fixtures.
- Existing JavaScript/npm and Swift/SPM behavior remains compatible with
  `P10-T1`.
- No harvested repository code, package scripts, build tools, dependency
  installers, or network probes are executed.

## Validation Plan

- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest tests/test_collector.py -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
