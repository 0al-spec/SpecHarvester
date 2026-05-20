# Next Task: P10-T6 Multi-Language Smoke Matrix

**Status:** SELECTED

**Updated:** 2026-05-20

## Description

Add a multi-language smoke matrix covering local repositories and synthetic
fixtures for npm, SPM, Gradle/Maven, Go modules, Composer, CMake,
Xcode/CocoaPods, RubyGems, and Python packaging.

## Recently Archived

- `P10-T5` Add language-neutral semantic extraction for documentation-first
  repositories so README/API-contract evidence can produce meaningful intent
  clusters even when no supported package manifest is present.
- `P10-T4` Wire `ProjectProfile` into analyzer orchestration so `collect-batch`
  can recommend or emit public-interface indexes from existing static
  analyzers, including Python `ast` and JavaScript/TypeScript export analyzers,
  before `draft` runs.
- `P10-T3` Evaluate and integrate trusted language classification and
  vendored/generated-file filtering from established tools such as GitHub
  Linguist-compatible classifiers, `go-enry`, `Syft`, `ScanCode`, and
  Universal Ctags where licensing and deterministic operation are acceptable.
- `P10-T2` Add manifest-first ecosystem detectors for Swift/SPM, JavaScript and
  TypeScript package managers, Python, Java/Kotlin, Go, PHP, C/C++,
  Objective-C/iOS, Ruby, and Rust without executing package code.

## Next Step

Create the P10-T6 PRD, then add reproducible multi-language smoke coverage
across supported manifest-first ecosystems and at least one documentation-first
manifest-poor repository.
