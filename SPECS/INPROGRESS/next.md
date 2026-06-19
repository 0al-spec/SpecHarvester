# Next Task: P40-T5 Adapter Evidence Batch Integration

**Status:** Planned
**Branch:** `feature/P40-T5-adapter-evidence-batch-integration`
**Phase:** Phase 40. Repository Plugin Adapter Contract
**Last Archived:** P40-T4 Adapter Execution Policy

## Recently Archived

- `P40-T4` documented the disabled-by-default repository plugin adapter
  execution policy.
- The GitHub-facing documentation is
  `docs/REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`.
- The DocC mirror is
  `Sources/SpecHarvester/Documentation.docc/RepositoryPluginAdapterExecutionPolicy.md`.
- The policy defines `disabled`, `static_only`, `trusted_local_tool`, and
  `blocked` execution modes.
- `static_only` remains the only current safe mode.
- Future `trusted_local_tool` requires explicit operator opt-in, path
  allowlists, bounded resources, output digests, and denied ambient
  capabilities.
- The policy records deny-by-default rules: no dependency installation, no
  package manager invocation, no network discovery, no harvested code
  execution, no AI/model execution, and no registry write.
- Adapter output remains producer-side review evidence only.

## Task

Connect adapter manifest and preflight output to `autonomous-candidate-batch`
as review-only producer evidence.

## Why This Is Next

P40-T2 defines adapter manifests, P40-T3 defines adapter preflight reports, and
P40-T4 defines execution policy. The next step is to let batch output carry
operator-supplied adapter evidence as sidecar review data while keeping the
existing static evaluator path unchanged by default.

## Scope

- Add an opt-in batch evidence path for adapter manifest and preflight output.
- Keep the existing static evaluator path unchanged unless an operator
  explicitly supplies adapter evidence.
- Record adapter manifest path and digest in batch output.
- Record adapter preflight path and digest in batch output.
- Record selected, rejected, fallback, and blocked adapter counts.
- Record `appliedToDrafting: false`.
- Record `registryAuthority: false`.
- Record diagnostics as review-only producer evidence.
- Keep adapter output producer-side evidence only.

## Non-Goals

- Do not implement adapter loading or execution.
- Do not auto-run adapters.
- Do not change static plugin applicability defaults.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not treat adapter output as registry truth.

## Phase 40. Repository Plugin Adapter Contract

- [x] `P40-T1` Document a language- and framework-agnostic repository plugin
  adapter contract. The contract must define adapter identity, versioned
  manifests, declared input evidence, output artifacts, execution modes,
  sandbox expectations, diagnostics, and authority boundaries without making
  Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven,
  Gradle, or any other ecosystem normative.
- [x] `P40-T2` Add a machine-readable
  `SpecHarvesterRepositoryPluginAdapterManifest` fixture that records adapter
  ids, contract versions, supported roles, required and optional evidence
  kinds, declared outputs, execution mode, sandbox requirements, capability
  requests, and non-authority statements.
- [x] `P40-T3` Add a repository plugin adapter preflight report fixture that
  validates one or more adapter manifests against a static evidence envelope,
  records allowed, rejected, fallback, and blocked adapter decisions, and
  refuses unsafe execution or missing required evidence before any adapter code
  can run.
- [x] `P40-T4` Define adapter execution policy for future local adapters:
  default disabled execution, static-only mode, bounded local trusted mode,
  path allowlists, no dependency installation, no package manager invocation,
  no network discovery, no harvested code execution, and explicit operator
  opt-in for every non-static mode.
- [ ] `P40-T5` Connect adapter manifest and preflight output to
  `autonomous-candidate-batch` as review-only producer evidence while keeping
  the existing static evaluator path unchanged unless an operator explicitly
  supplies adapter evidence.
- [ ] `P40-T6` Record a cross-ecosystem adapter contract fixture matrix for
  manifest-backed single packages, workspaces, documentation-heavy
  repositories, nested package roots, and ambiguous mixed layouts without
  loading third-party adapter code.
- [ ] `P40-T7` Run a real local adapter-contract validation over existing
  pinned checkouts, comparing FastMCP, FastAPI, xyflow, and at least one
  additional ecosystem shape when available, while proving that adapters remain
  producer-side evidence only.

Motivation:

- Adapter manifests, preflight, and execution policy are now documented, but
  batch output cannot yet carry adapter evidence in a structured way.
- Operators need an explicit opt-in sidecar path before future real validation
  can compare adapter evidence across repositories.
- Batch integration must not imply adapter execution or registry authority.

Goal:

- Let `autonomous-candidate-batch` attach operator-supplied adapter manifest
  and preflight evidence as review-only producer evidence without changing the
  default static evaluator behavior.

Acceptance:

- Existing batch behavior remains unchanged without adapter evidence inputs.
- Adapter evidence inputs are opt-in and digest-recorded.
- Batch output records manifest/preflight paths, digests, counts, diagnostics,
  and non-authority boundaries.
- Adapter evidence remains `appliedToDrafting: false` and
  `registryAuthority: false`.
- The task does not execute adapters or treat adapter output as registry truth.

