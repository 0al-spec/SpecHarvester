# Next Task: P12-T5 Evidence Support Target Contract Alignment

**Status:** IN_PROGRESS

**Updated:** 2026-05-21

## Description

Remove or remap generated evidence support targets that the current SpecPM
BoundarySpec support-target grammar does not declare, including
`provides.capabilities.intentIds`, so generated candidates validate without
avoidable advisory warnings.

## Recently Archived

- `P12-T4` Kept `kind: public_interface_index` for SpecPM `0.2.0+`, added
  explicit `PublicInterfaceIndex` artifact metadata to BoundarySpec evidence,
  and added CI coverage that validates a candidate containing
  `public-interface-index.json`.
- `P12-T3` Added deterministic web-framework domain intent inference from
  documentation hints and public interface indexes so Flask/Gin candidates now
  include web framework, routing, middleware, and request/response context
  intents instead of only generic API/tooling claims.
- `P12-T2` Added deterministic Go public interface evidence for `go.mod`
  projects without executing `go`, package scripts, tests, builds, or network
  probes.
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

## Parked

- `P11-T1` SpecNode Integration Contract remains parked until deterministic
  popular-repository smoke hardening is complete.

## Newly Observed Smoke Gaps

- SpecPM validation warns on `provides.capabilities.intentIds` because the
  generated evidence support target is not declared by the current BoundarySpec
  support-target grammar.

## Next Step

Implement `P12-T5` through Flow and PR: align generated evidence `supports`
targets with the current SpecPM BoundarySpec support-target grammar.
