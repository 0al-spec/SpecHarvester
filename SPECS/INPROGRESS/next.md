# Next Task: P10-T4 ProjectProfile Analyzer Orchestration

**Status:** SELECTED

**Updated:** 2026-05-20

## Description

Wire `ProjectProfile` into analyzer orchestration so `collect-batch` can
recommend or emit public-interface indexes from existing static analyzers,
including Python `ast` and JavaScript/TypeScript export analyzers, before
`draft` runs.

## Recently Archived

- `P10-T3` Evaluate and integrate trusted language classification and
  vendored/generated-file filtering from established tools such as GitHub
  Linguist-compatible classifiers, `go-enry`, `Syft`, `ScanCode`, and
  Universal Ctags where licensing and deterministic operation are acceptable.
- `P10-T2` Add manifest-first ecosystem detectors for Swift/SPM, JavaScript and
  TypeScript package managers, Python, Java/Kotlin, Go, PHP, C/C++,
  Objective-C/iOS, Ruby, and Rust without executing package code.
- `P10-T1` Define a deterministic `ProjectProfile` schema for language,
  package ecosystem, package manager, manifest, confidence, provenance, and
  analyzer-plan evidence.

## Next Step

Plan `P10-T4`, then implement analyzer orchestration that consumes
`ProjectProfile.analyzerPlan` to emit existing static public-interface indexes
before drafting without executing harvested package code or installing
dependencies.
