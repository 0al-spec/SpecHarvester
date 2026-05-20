# Next Task: P11-T1 SpecNode Integration Contract

**Status:** READY

**Updated:** 2026-05-20

## Description

Define the SpecHarvester-to-SpecNode artifact bundle and typed job contract for
model-assisted candidate refinement without granting model output filesystem or
shell authority.

## Recently Archived

- `P10-T6` Add a multi-language smoke matrix covering local repositories and
  synthetic fixtures for npm, SPM, Gradle/Maven, Go modules, Composer, CMake,
  Xcode/CocoaPods, RubyGems, Python packaging, and a documentation-first
  manifest-poor repository.
- `P10-T5` Add language-neutral semantic extraction for documentation-first
  repositories so README/API-contract evidence can produce meaningful intent
  clusters even when no supported package manifest is present.
- `P10-T4` Wire `ProjectProfile` into analyzer orchestration so `collect-batch`
  can recommend or emit public-interface indexes from existing static
  analyzers, including Python `ast` and JavaScript/TypeScript export analyzers,
  before `draft` runs.
- `P10-T3` Evaluate and integrate trusted language classification and
  vendored/generated-file filtering from established tools such as
  GitHub Linguist-compatible classifiers, `go-enry`, `Syft`, `ScanCode`, and
  Universal Ctags where licensing and deterministic operation are acceptable.

## Next Step

Keep `P11-T1` parked until SpecNode integration work starts. For now, use the
completed smoke matrix and ignored `.smoke/` output directories for local
repository runs.
