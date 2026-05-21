# Next Task: P11-T5 SpecNode-Compatible Provider Smoke Coverage

**Status:** SELECTED

**Updated:** 2026-05-22

## Description

Add integration smoke coverage using a local SpecNode-compatible provider with
weak-model drafting inputs, while preserving deterministic fallback when no
provider is available.

## Recently Archived

- `P11-T4` Defined schema-validated model output for
  `SpecNodeCandidatePatchProposal`, `SpecNodeCandidatePatchOperation`,
  proposal provenance, usage receipts, review notes, and
  `SpecNodeRejectionReason` before any generated change can be applied.
- `P11-T3` Defined the OpenAI-compatible provider adapter boundary for local
  SpecNode execution, including LM Studio discovery, endpoint allowlisting,
  health checks, model listing, timeout, retry, temperature, token-budget
  policy, usage receipts, and authority limits.
- `P11-T2` Defined the deterministic `SpecHarvesterRefinePreviewPlan` contract
  with compact model input sections, artifact digests, prompt-budget controls,
  excluded raw content, and DocC/GitHub documentation contract coverage.
- `P11-T1` Defined the `SpecHarvesterSpecNodeArtifactBundle` and
  `SpecNodeRefinementJob` contract for future SpecNode-assisted candidate
  refinement without granting the model shell, filesystem, raw source, secret,
  or direct mutation authority.
- `P12-T6` Promoted Flask/Gin popular-repository smoke coverage into committed
  synthetic tests and mirrored the reproducible real-checkout recipe in GitHub
  docs and DocC.
- `P12-T5` Removed the unsupported
  `provides.capabilities.intentIds` evidence support target, remapped semantic
  evidence to declared SpecPM support targets, and added CI coverage for
  `semantic_intent_static_evidence` validation.
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

- None.

## Newly Observed Smoke Gaps

- No currently open avoidable SpecPM validation warning remains from
  `PublicInterfaceIndex` evidence kind or semantic evidence support targets.

## Next Step

Implement `P11-T5` through Flow and PR: add integration smoke coverage using a
local SpecNode-compatible provider with weak-model drafting inputs, while
preserving deterministic fallback when no provider is available.
