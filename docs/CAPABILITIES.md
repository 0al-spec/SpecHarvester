# SpecHarvester Capabilities

Status: current product capability map.

SpecHarvester is a producer pipeline for turning pinned public repository
checkouts into reviewable SpecPM candidate packages. Its current goal is not to
write final registry truth. Its goal is to produce a valid, evidence-backed
starter package that an author or maintainer can review, correct, and hand off
to SpecPM.

Short form:

```text
local repository checkout
  -> bounded evidence
  -> candidate package or package-set draft
  -> optional local AI proposal
  -> validation, quality report, and static viewer
  -> selected/deferred handoff evidence
  -> SpecPM-side preflight and maintainer review
```

## What It Can Do Now

| Capability | Current support | Main docs |
| --- | --- | --- |
| Static evidence collection | Collect allowlisted metadata, file digests, provenance, and analyzer-policy records from local checkouts. | [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md), [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md) |
| Deterministic single-package drafting | Produce `specpm.yaml`, `specs/*.spec.yaml`, validation reports, diagnostics, receipts, quality reports, and preview output. | [`PRODUCER_CANDIDATE_BUNDLE.md`](PRODUCER_CANDIDATE_BUNDLE.md), [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md) |
| Workspace and package-set drafting | Detect workspace/member package shape, draft aggregate package-set candidates, draft scoped members, and emit `contains` relation proposals. | [`WORKSPACE_INVENTORY.md`](WORKSPACE_INVENTORY.md), [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md), [`PACKAGE_RELATION_PROPOSALS.md`](PACKAGE_RELATION_PROPOSALS.md) |
| Package-set preflight and viewer | Check member bundles, relation proposals, evidence digests, and render static review pages for package-set output. | [`BUNDLE_SET_PREFLIGHT.md`](BUNDLE_SET_PREFLIGHT.md), [`PACKAGE_SET_VIEWER.md`](PACKAGE_SET_VIEWER.md) |
| Author-ready quality reporting | Classify generated output as `author_ready_draft`, `needs_regeneration`, or `blocked`, with hard gates, review dimensions, and action items. | [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md), [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md) |
| Local AI draft and enrichment proposals | Use local OpenAI-compatible providers such as LM Studio for proposal-only package-set drafting and enrichment. | [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md), [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md) |
| AI-enriched preview candidate copies | Apply clean AI enrichment proposals into copied preview candidates with patch reports for review. | [`AI_ENRICHMENT_CANDIDATE_PATCH.md`](AI_ENRICHMENT_CANDIDATE_PATCH.md) |
| Selected/deferred candidate triage | Separate review-ready candidates from candidates that need targeted regeneration, repair, or explicit deferral. | [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md), [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md) |
| SpecPM handoff evidence | Emit portable JSON/Markdown review evidence that SpecPM can preflight without rerunning SpecHarvester. | [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md), [`SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`](SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md) |
| Bounded corpus runs | Select important multi-ecosystem repository/package-family targets with explicit importance signals and exclusion rules, record the machine-readable corpus plan, explainable selection report, and dry-run readiness gate, then run operator-selected local checkout batches with deterministic and optional live local-model paths. | [`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md), [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md), [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md), [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md), [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md) |
| Repository parsing profile hook | Opt-in path classification for language/framework parser profiles, with `python.web_framework.v0` validated on FastAPI to separate public interface evidence from semantic usage/documentation evidence. | [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md), [`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md) |
| Repository profile detection evidence | Opt-in `repository-profile-detect` command and `autonomous-candidate-batch --repository-profile-selection` sidecar artifacts that emit `SpecHarvesterRepositoryProfileDetection` from static evidence before parser path classification, plus a generic discovery hint vocabulary, cross-ecosystem fixture coverage, real FastMCP comparison evidence, and harvested-manifest fallback evidence when workspace inventory is empty. | [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md), [`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md), [`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md), [`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md), [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md) |
| Repository plugin subsystem contract | Planned language- and framework-agnostic plugin subsystem contract plus machine-readable `SpecHarvesterRepositoryPluginRegistry`, `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`, and `SpecHarvesterRepositoryPluginApplicabilityReport` fixtures. Autonomous candidate batch can copy applicability reports as `repositoryPluginApplicability` sidecar producer evidence, cross-ecosystem fixtures cover single-package, workspace, documentation-heavy, nested, and ambiguous repository shapes, a real FastMCP run proves the sidecar path on a pinned local checkout, and Phase 39 now has a deterministic static evaluator helper, `repository-plugin-applicability-detect` CLI, opt-in `autonomous-candidate-batch --repository-plugin-registry --repository-plugin-static-evidence-envelope` integration, and a real FastMCP/FastAPI/xyflow validation fixture that derives applicability reports without executing plugins, reading repository source files, or changing parser/profile behavior. | [`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md), [`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md), [`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md), [`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md), [`REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md), [`REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`](REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md), [`REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md`](REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md), [`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md), [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md), [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md) |
| Repository plugin adapter contract | Phase 40 defines the language- and framework-agnostic boundary for future adapter manifests, preflight reports, execution policy, sandbox expectations, and review-only adapter output evidence while keeping static applicability as the default safe path. P40-T2 adds the first machine-readable `SpecHarvesterRepositoryPluginAdapterManifest` fixture, P40-T3 adds the first `SpecHarvesterRepositoryPluginAdapterPreflightReport` fixture, P40-T4 documents disabled-by-default execution policy, P40-T5 connects explicit adapter evidence to autonomous batch as `repositoryPluginAdapterEvidence`, P40-T6 records a static cross-ecosystem adapter fixture matrix, and P40-T7 records real local adapter-contract validation over FastMCP, FastAPI, xyflow, and Gin while preserving `adapterExecution: not_run`. | [`REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`](REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md), [`REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md), [`REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md), [`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md), [`REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`](REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md), [`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md), [`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md), [`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md) |
| Trusted local adapter runtime readiness | Phase 41 plans the safe path from adapter contracts toward future trusted local execution: explicit operator opt-in, run request fixtures, preflight fixtures, disabled no-execution runner skeleton, review-only batch evidence handoff, and real local readiness validation. P41-T2 adds `SpecHarvesterTrustedLocalAdapterRunRequest` as a machine-readable fixture for adapter manifest/preflight references, declared input artifacts, safe read allowlists, output policy, resource budgets, and non-authority statements. P41-T3 adds `SpecHarvesterTrustedLocalAdapterRunPreflightReport` as the review-only fixture for request identity, digest, path, output, budget, policy, execution-boundary, rejected unsafe-shape, blocked runtime-request, and warning checks. P41-T4 adds `trusted-local-adapter-runner-skeleton` and `SpecHarvesterTrustedLocalAdapterRunReport`, validating request/preflight linkage while preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`, and `registryAuthority: false`. P41-T5 connects that report to `autonomous-candidate-batch --trusted-local-adapter-run-report` as copied `trustedLocalAdapterRunEvidence` with source/copied digests and no-execution boundary fields. P41-T6 records real local readiness validation over FastMCP, FastAPI, xyflow, and Gin, preserving `adapterProcessSpawned: false`, zero execution counters, and explicit operator-provided sidecar evidence. It does not enable adapter execution. | [`TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md), [`TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md), [`TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md`](TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md), [`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md), [`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md) |
| Trusted local adapter runtime sandbox | Phase 42 defines the sandbox/runtime boundary required before any trusted local adapter process can run: explicit operator approval, adapter package identity, process isolation, sealed environment, dependency isolation, network-deny-by-default policy, output digests, audit records, and review-only authority. P42-T1 is documentation-only and keeps `adapterExecution: not_run`. P42-T2 adds the machine-readable `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture with adapter package identity, sandbox policy identity, approval requirements, filesystem/environment/network/dependency policy, output verification, audit requirements, and no-execution/non-authority statements. P42-T3 adds the machine-readable `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture with sandbox contract identity/digest linkage, accepted/rejected/blocked checks, no-execution state, and review-only non-authority statements. P42-T4 adds `trusted-local-adapter-sandbox-runner-validation` and `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`, validating sandbox contract/preflight linkage while preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`, `adapterProcessSpawned: false`, `executedAdapterCount: 0`, and `registryAuthority: false`. P42-T5 adds `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun` as an explicitly approved synthetic run fixture with approval binding, synthetic output candidates, output digests, audit records, and no real adapter process execution. P42-T6 adds `synthetic-trusted-local-adapter-sandbox-run-verifier` and `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` for deterministic fixture/link/output/audit verification while still preserving no real adapter execution and no registry authority. P42-T7 adds `real-local-trusted-adapter-sandbox-run-readiness` and `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` for future real-run review prerequisites while still refusing adapter code loading and process spawning. P42-T8 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` as a request-only fixture for future real-run review, verifier/readiness evidence requirements, scoped approval, runtime/output/audit policy, and non-authority statements without granting execution permission. P42-T9 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport` for request identity/digest, verifier/readiness requirements, rejected unsafe shapes, blocked execution drift, and review-only non-authority statements. P42-T10 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport` for request/preflight linkage validation while preserving disabled execution, no adapter code loading, no process spawning, no network access, no registry authority, and no adapter output acceptance. P42-T11 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff` for packaging P42-T8/P42-T9/P42-T10 artifacts as portable review evidence while preserving no execution permission, no operator approval, no registry authority, and no adapter output truth. P42-T12 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate` for validating the P42-T11 handoff and recording runtime prerequisites while preserving no runtime implementation, no runtime invocation, and no execution permission. P42-T13 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding` for binding one future local adapter run approval scope while preserving no execution permission, no registry authority, no consumed approval, and no adapter output truth. P42-T14 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport` for validating the P42-T13 approval binding through a disabled invocation skeleton while preserving no runtime invocation, no approval consumption, no registry authority, and no adapter output truth. P42-T15 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff` for packaging P42-T13 approval binding and P42-T14 disabled invocation evidence as portable review material while preserving no execution permission, no approval consumption, and no registry authority. | [`TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md), [`TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md), [`TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_VERIFIER.md`](TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_VERIFIER.md), [`TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_SANDBOX_RUN_READINESS.md`](TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_SANDBOX_RUN_READINESS.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md), [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_SKELETON.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md), [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_SKELETON.md), [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_EVIDENCE_HANDOFF.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_EVIDENCE_HANDOFF.md), [`TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md), [`TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md`](TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md) |
| Optional CodeGraph input boundary | Normalize pre-existing CodeGraph artifacts into source graph evidence and check pinned interface compatibility offline. | [`CODEGRAPH_SOURCE_GRAPH_ADAPTER.md`](CODEGRAPH_SOURCE_GRAPH_ADAPTER.md), [`CODEGRAPH_COMPATIBILITY_GUARD.md`](CODEGRAPH_COMPATIBILITY_GUARD.md) |

## Repository Shapes

SpecHarvester currently has useful coverage for:

- manifest-backed single-package repositories;
- manifest-poor repositories with README/API-contract semantic hints;
- JavaScript/TypeScript package or workspace layouts;
- package-set or monorepo layouts where a workspace/root package should contain
  selected member packages;
- bounded local corpus runs over operator-selected checkouts.

The `xyflow` reference path is the current package-set calibration case:

```text
xyflow.workspace
  contains xyflow.react
  contains xyflow.svelte
  contains xyflow.system
```

The limited and next-corpus evidence pages record broader calibration runs. They
are evidence for pipeline quality, not permission to ingest arbitrary public
repositories into SpecPM automatically.

[`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md) defines the Phase 35
boundary for choosing important libraries across ecosystems. The policy treats
repository/package-family selection as a curated operator decision, not a raw
registry search crawl.

[`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md) defines the
machine-readable plan shape for selected, deferred, and rejected source
decisions before any autonomous batch run starts.

[`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md)
defines how package-like units inside selected repositories should be
classified before drafting.

[`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md)
records the first bounded seed set across JavaScript/TypeScript, Python, Rust,
Go, and Swift. It is a plan for future local-checkout runs, not permission to
clone repositories or publish registry metadata.

[`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md)
explains selected, deferred, and rejected seed sources, quota decisions, and
the downstream command plan before any readiness check or autonomous batch.

[`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md)
records that the Phase 35 seed corpus is blocked until operator-provided pinned
local checkouts are verified.

[`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md)
defines the Phase 36 plugin contract for repository path classification.
[`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md)
defines the Phase 37 contract and the `repository-profile-detect` CLI report
surface plus autonomous batch sidecar evidence for selecting repository
profile plugins before path classification.
[`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md)
defines generic path-role hints such as `package_set_root`, `member_package`,
`example_package`, `internal_utility`, and `evidence_only`.
[`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md)
records workspace-shaped, single-package, nested-package, and ambiguous
multi-signal fixtures for the same generic profile selection contract.
[`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md)
records the first real FastMCP auto-selection comparison. The run passed, but
auto-selection fell back to `generic.repository.v0`; manual `fastmcp_slim`
targeting produced a much narrower public interface index. P37-T8 adds
harvested manifest fallback evidence when workspace inventory has no manifest
records.
[`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md)
defines the Phase 38 contract that turns parser profiles, repository profiles,
future evidence producers, topology helpers, and review surfaces into explicit
plugin roles with registration metadata, applicability reports, deterministic
selection boundaries, and producer-side authority limits.
[`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md)
records the first machine-readable `SpecHarvesterRepositoryPluginRegistry`
fixture for declared plugin contracts. The fixture is not plugin execution,
not registry acceptance, and not accepted package truth.
[`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md)
records the first machine-readable
`SpecHarvesterRepositoryPluginApplicabilityReport` fixture for selected,
rejected, fallback, and blocked plugin decisions from static evidence.
[`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md) can copy
that report as `repositoryPluginApplicability` sidecar producer evidence with
`appliedToDrafting: false` and `registryAuthority: false`.
[`REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md)
records static applicability examples for manifest-backed single-package,
workspace, documentation-heavy, nested package root, and ambiguous mixed
repository shapes.
[`REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`](REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md)
records a real FastMCP plugin evidence run. The run shows current profile
selection choosing `generic.single_package.v0` and autonomous batch recording
`repositoryPluginApplicability` as sidecar evidence with `appliedToDrafting:
false` and `registryAuthority: false`.
[`REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md`](REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md)
records the P39-T6 real FastMCP, FastAPI, and xyflow validation through the
standalone static evaluator and the P39-T5 batch auto-sidecar path.
[`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md)
defines the Phase 39 helper, `repository-plugin-applicability-detect` CLI, and
opt-in `autonomous-candidate-batch --repository-plugin-registry
--repository-plugin-static-evidence-envelope` integration for deriving
`SpecHarvesterRepositoryPluginApplicabilityReport` from static evidence such as
source manifest metadata, `harvest.json`, `workspace-inventory.json`,
`repository-profile-detection.json`, public-interface indexes, and operator
labels.
[`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md)
records the P39-T2
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` fixture, including safe
relative evidence paths, SHA-256 digests, `evidenceKinds[]`, advisory signals,
and non-authority boundaries.
[`REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`](REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md)
records the P40-T1 adapter contract for future manifest, preflight, execution
policy, sandbox, and review-only output evidence layers.
[`REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md)
records the P40-T2 `SpecHarvesterRepositoryPluginAdapterManifest` fixture.
[`REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md)
and
[`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
record the P40-T5 opt-in batch sidecar path for adapter manifest/preflight
evidence as `repositoryPluginAdapterEvidence` with copied paths, SHA-256
digests, allowed/rejected/fallback/blocked counts, `appliedToDrafting: false`,
`registryAuthority: false`, and `adapterExecution: not_run`.
[`REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`](REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md)
records the P40-T6 static adapter fixture matrix across manifest-backed single
packages, workspaces, documentation-heavy repositories, nested package roots,
and ambiguous mixed layouts without loading third-party adapter code.
[`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md) records
the first practical profile run. The profile keeps documentation, tutorials,
examples, and tests available as semantic usage
evidence while keeping public interface indexes focused on package surfaces
intended for consumers.

## Author-Ready Draft Boundary

The current product quality target is:

```text
valid starter package, not final accepted spec
```

SpecHarvester should stop when remaining work is better done by the library
author, a maintainer, or a reviewing agent with project-specific context.

An author-ready draft should provide:

- valid SpecPM package files;
- bounded evidence links and digests;
- conservative intent and capability claims;
- diagnostics and validation output;
- quality report verdict and author action items;
- static review surface;
- handoff evidence for SpecPM-side preflight where relevant.

It is acceptable for a draft to require author edits. It is not acceptable for a
draft to hide failed validation, fabricate evidence, remove `preview_only`, or
present AI output as registry truth.

## AI and Local Model Boundary

Local model support is proposal-only.

SpecHarvester can use local OpenAI-compatible providers, including LM Studio, to
draft or enrich package-set candidates from compact evidence. The resulting AI
artifacts remain review evidence:

- provider receipts are provenance, not authority;
- raw prompts or responses are not persisted as registry truth;
- model JSON is schema checked and may pass through bounded repair;
- package identity, evidence paths, privacy flags, and interface kinds must
  still pass deterministic checks;
- clean enrichment proposals may be applied only into copied preview candidates
  through [`AI_ENRICHMENT_CANDIDATE_PATCH.md`](AI_ENRICHMENT_CANDIDATE_PATCH.md);
- accepted registry output still requires maintainer review.

## SpecPM Boundary

SpecHarvester produces reviewable candidate bundles. SpecPM remains the
validator, registry authority, and public-index publisher.

Passing SpecHarvester preflight or SpecPM-side handoff preflight means:

```text
the evidence is internally consistent enough for review
```

It does not mean:

```text
the package is accepted into the registry
```

Promotion requires a separate maintainer decision, accepted-source PR, and
SpecPM validation/indexing flow.

## What It Intentionally Does Not Do

SpecHarvester does not:

- clone or discover repositories on its own during documented corpus runs;
- execute harvested repository code;
- install harvested dependencies;
- run package scripts or tests from harvested projects;
- access secrets or private credentials;
- treat generated candidates as upstream-endorsed truth;
- accept packages, accept relations, seed baselines, or remove `preview_only`
  without an explicit maintainer flow;
- publish directly into the SpecPM public registry.

## Current Maturity

| Area | Maturity |
| --- | --- |
| Single-package deterministic candidate loop | Working MVP |
| Package-set drafting and relation proposals | Working MVP, calibrated on `xyflow` |
| Author-ready quality report | Working MVP |
| Static candidate and package-set viewer | Working review surface |
| Local LM Studio proposal path | Working, proposal-only |
| Selected/deferred handoff | Working review evidence path |
| SpecPM consumer preflight integration | Working for supported handoff artifacts |
| Curated multi-ecosystem corpus selection | Planned policy boundary |
| Repository parsing plugin profiles | Working explicit hook for one parser profile; broader selection still planned |
| Repository profile selection | Working standalone report, autonomous batch evidence layer, generic hint vocabulary, cross-ecosystem fixtures, real FastMCP evidence, and harvested-manifest fallback evidence |
| Repository plugin subsystem | Contract, registry fixture, applicability report fixture, and autonomous batch sidecar integration recorded; no plugin loading or plugin execution |
| Broad autonomous public-library scraping | Not ready; bounded local corpus only |
| Final accepted spec authoring | Out of scope for SpecHarvester |

## Operator Reading Path

For a practical path through the current system:

1. Start with [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md).
2. Check [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md) before adding analyzers or
   model providers.
3. Use [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md)
   to understand the stop policy.
4. Use [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md) and
   [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md) for monorepos.
5. Use [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
   and [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md) when preparing SpecPM review.
6. Use [`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md),
   [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md),
   [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md),
   [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md),
   [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md),
   and [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md)
   before running any larger corpus.
