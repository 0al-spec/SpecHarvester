# Next Task: P12-T2 Go Public Interface Evidence

**Status:** IN PROGRESS

**Updated:** 2026-05-21

## Description

Add a deterministic Go public interface analyzer or manifest-plus-source
fallback for `go.mod` projects, producing compact package/function/type evidence
without executing `go`, package scripts, tests, or network probes.

## Recently Archived

- `P12-T1` Accepted common public license filenames such as `LICENSE.txt` in
  strict public mode while preserving the hard failure for repositories with no
  license-like file.
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

## Parked

- `P11-T1` SpecNode Integration Contract remains parked until deterministic
  popular-repository smoke hardening is complete.

## Newly Observed Smoke Gaps

- `gin-gonic/gin` is detected as Go from `go.mod`, but public interface
  extraction is still `manifest_only`.
- Generated Flask/Gin intents are too generic for popular web frameworks.
- SpecPM validation warns on `kind: public_interface_index` because the SpecPM
  evidence-kind vocabulary does not yet include that generated artifact type.
- SpecPM validation warns on `provides.capabilities.intentIds` because the
  generated evidence support target is not declared by the current BoundarySpec
  support-target grammar.

## Next Step

Execute `P12-T2` through Flow and PR: add deterministic Go public interface
evidence or a manifest-plus-source fallback, rerun the Gin smoke path, and
capture validation evidence.
