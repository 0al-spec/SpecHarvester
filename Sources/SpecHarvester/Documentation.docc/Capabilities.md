# Capabilities

Status: current product capability map.

SpecHarvester is a producer pipeline for turning pinned public repository
checkouts into reviewable SpecPM candidate packages. Its current goal is to
produce a valid, evidence-backed starter package that an author or maintainer
can review, correct, and hand off to SpecPM.

```text
local repository checkout
  -> bounded evidence
  -> candidate package or package-set draft
  -> optional local AI proposal
  -> validation, quality report, and static viewer
  -> selected/deferred handoff evidence
  -> SpecPM-side preflight and maintainer review
```

## Current Support

| Capability | Current support | Related docs |
| --- | --- | --- |
| Static evidence collection | Allowlisted metadata, file digests, provenance, and analyzer-policy records from local checkouts. | <doc:Workflow>, <doc:TrustBoundary> |
| Deterministic single-package drafting | `specpm.yaml`, `specs/*.spec.yaml`, validation reports, diagnostics, receipts, quality reports, and preview output. | <doc:ProducerCandidateBundle>, <doc:SinglePackageCandidateFallback> |
| Workspace and package-set drafting | Workspace/member discovery, aggregate package-set candidates, scoped member packages, and `contains` relation proposals. | <doc:WorkspaceInventory>, <doc:PackageSetDrafting>, <doc:PackageRelationProposals> |
| Package-set preflight and viewer | Member bundle checks, relation proposal checks, evidence digest checks, and static package-set review pages. | <doc:BundleSetPreflight>, <doc:PackageSetViewer> |
| Author-ready quality reporting | `author_ready_draft`, `needs_regeneration`, and `blocked` verdicts with hard gates, dimensions, and action items. | <doc:AuthorReadyDraftQualityBar>, <doc:AuthorReadyDraftQualityReport> |
| Local AI proposals | LM Studio/OpenAI-compatible proposal-only package-set drafting and enrichment. | <doc:PackageSetAIDraftProposal>, <doc:PackageSetAIEnrichment> |
| AI-enriched preview candidate copies | Clean AI enrichment proposals can be applied into copied preview candidates with patch reports for review. | <doc:AIEnrichmentCandidatePatch> |
| Selected/deferred candidate triage | Review-ready candidates are separated from candidates needing regeneration, repair, or explicit deferral. | <doc:SelectedCandidateHandoffProposal>, <doc:DeferredCandidateRegenerationRunbook> |
| SpecPM handoff evidence | Portable JSON/Markdown review evidence that SpecPM can preflight without rerunning SpecHarvester. | <doc:SpecPMHandoff>, <doc:SelectedCandidateHandoffPreflightExpectations> |
| Bounded corpus runs | Important multi-ecosystem repository/package-family targets selected with explicit importance signals and exclusion rules, recorded in a machine-readable corpus plan, explainable selection report, and dry-run readiness gate, then operator-selected local checkout batches with deterministic and optional live local-model paths. | <doc:CorpusSelectionPolicy>, <doc:SpecHarvesterCorpusPlan>, <doc:MultiEcosystemSeedCorpusPlan>, <doc:ExplainableCorpusSelectionReport>, <doc:SelectedCorpusDryRunReadiness>, <doc:AutonomousCandidateBatch> |
| Operational MVP validation | Phase 43 validates whether the current pipeline produces valid, repository-specific starter packages over a bounded pinned multi-ecosystem corpus before broader autonomous scraping or real adapter execution. P43-T2 adds the machine-readable `SpecHarvesterOperationalMVPValidationPlan` fixture; P43-T3 adds the companion `SpecHarvesterOperationalMVPValidationReport` fixture for per-repository result, quality, stop-policy, and handoff readiness fields; P43-T4 records the real local static-only baseline over xyflow, FastAPI, and Gin pinned checkouts; P43-T5 records the live local LM Studio AI-enabled comparison while keeping all AI draft/enrichment output proposal-only; P43-T6 adds author handoff summaries for valid, reviewable, manual-correction, and do-not-promote outcomes. | <doc:OperationalMVPValidationPlan>, <doc:OperationalMVPValidationPlanFixture>, <doc:OperationalMVPValidationReportFixture>, <doc:OperationalMVPStaticOnlyBaseline>, <doc:OperationalMVPAIEnabledComparison>, <doc:OperationalMVPAuthorHandoffSummaries>, <doc:AuthorReadyDraftQualityReport>, <doc:AutonomousCandidateBatch> |
| Repository parsing profile hook | Opt-in path classification for language/framework parser profiles, with `python.web_framework.v0` validated on FastAPI to separate public interface evidence from semantic usage/documentation evidence. | <doc:RepositoryParsingPluginContract>, <doc:FastAPIParserProfileRerun> |
| Repository profile detection evidence | Opt-in `repository-profile-detect` command and `autonomous-candidate-batch --repository-profile-selection` sidecar artifacts that emit `SpecHarvesterRepositoryProfileDetection` from static evidence before parser path classification, plus a generic discovery hint vocabulary, cross-ecosystem fixture coverage, real FastMCP comparison evidence, and harvested-manifest fallback evidence when workspace inventory is empty. | <doc:RepositoryProfileSelectionContract>, <doc:RepositoryProfileDiscoveryHints>, <doc:RepositoryProfileCrossEcosystemFixtures>, <doc:RepositoryProfileRealRunFastMCP>, <doc:AutonomousCandidateBatch>, <doc:RepositoryParsingPluginContract> |
| Repository plugin subsystem contract | Planned language- and framework-agnostic plugin subsystem contract plus machine-readable `SpecHarvesterRepositoryPluginRegistry`, `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`, and `SpecHarvesterRepositoryPluginApplicabilityReport` fixtures. Autonomous candidate batch can copy applicability reports as `repositoryPluginApplicability` sidecar producer evidence, cross-ecosystem fixtures cover single-package, workspace, documentation-heavy, nested, and ambiguous repository shapes, a real FastMCP run proves the sidecar path on a pinned local checkout, and Phase 39 now has a deterministic static evaluator helper, `repository-plugin-applicability-detect` CLI, opt-in `autonomous-candidate-batch --repository-plugin-registry --repository-plugin-static-evidence-envelope` integration, and a real FastMCP/FastAPI/xyflow validation fixture that derives applicability reports without executing plugins, reading repository source files, or changing parser/profile behavior. | <doc:RepositoryPluginSubsystemContract>, <doc:RepositoryPluginRegistryFixture>, <doc:RepositoryPluginStaticEvidenceEnvelopeFixture>, <doc:RepositoryPluginApplicabilityReportFixture>, <doc:RepositoryPluginCrossEcosystemFixtures>, <doc:RepositoryPluginRealRunFastMCP>, <doc:RepositoryPluginMultiRepositoryStaticEvaluatorValidation>, <doc:StaticRepositoryPluginApplicabilityEvaluator>, <doc:AutonomousCandidateBatch>, <doc:RepositoryParsingPluginContract>, <doc:RepositoryProfileSelectionContract> |
| Repository plugin adapter contract | Phase 40 defines the language- and framework-agnostic boundary for future adapter manifests, preflight reports, execution policy, sandbox expectations, and review-only adapter output evidence while keeping static applicability as the default safe path. P40-T2 adds the first machine-readable `SpecHarvesterRepositoryPluginAdapterManifest` fixture, P40-T3 adds the first `SpecHarvesterRepositoryPluginAdapterPreflightReport` fixture, P40-T4 documents disabled-by-default execution policy, P40-T5 connects explicit adapter evidence to autonomous batch as `repositoryPluginAdapterEvidence`, P40-T6 records a static cross-ecosystem adapter fixture matrix, and P40-T7 records real local adapter-contract validation over FastMCP, FastAPI, xyflow, and Gin while preserving `adapterExecution: not_run`. | <doc:RepositoryPluginAdapterContract>, <doc:RepositoryPluginAdapterManifestFixture>, <doc:RepositoryPluginAdapterPreflightReportFixture>, <doc:RepositoryPluginAdapterExecutionPolicy>, <doc:AutonomousCandidateBatch>, <doc:RepositoryPluginAdapterCrossEcosystemFixtureMatrix>, <doc:RepositoryPluginAdapterRealLocalValidation>, <doc:RepositoryPluginSubsystemContract>, <doc:StaticRepositoryPluginApplicabilityEvaluator> |
| Trusted local adapter runtime readiness | Phase 41 plans the safe path from adapter contracts toward future trusted local execution: explicit operator opt-in, run request fixtures, preflight fixtures, disabled no-execution runner skeleton, review-only batch evidence handoff, and real local readiness validation. P41-T2 adds `SpecHarvesterTrustedLocalAdapterRunRequest` as a machine-readable fixture for adapter manifest/preflight references, declared input artifacts, safe read allowlists, output policy, resource budgets, and non-authority statements. P41-T3 adds `SpecHarvesterTrustedLocalAdapterRunPreflightReport` as the review-only fixture for request identity, digest, path, output, budget, policy, execution-boundary, rejected unsafe-shape, blocked runtime-request, and warning checks. P41-T4 adds `trusted-local-adapter-runner-skeleton` and `SpecHarvesterTrustedLocalAdapterRunReport`, validating request/preflight linkage while preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`, and `registryAuthority: false`. P41-T5 connects that report to `autonomous-candidate-batch --trusted-local-adapter-run-report` as copied `trustedLocalAdapterRunEvidence` with source/copied digests and no-execution boundary fields. P41-T6 records real local readiness validation over FastMCP, FastAPI, xyflow, and Gin, preserving `adapterProcessSpawned: false`, zero execution counters, and explicit operator-provided sidecar evidence. It does not enable adapter execution. | <doc:TrustedLocalAdapterRuntimeReadiness>, <doc:TrustedLocalAdapterRunRequestFixture>, <doc:TrustedLocalAdapterRunPreflightReportFixture>, <doc:TrustedLocalAdapterRunnerSkeleton>, <doc:TrustedLocalAdapterRealLocalReadinessValidation>, <doc:AutonomousCandidateBatch>, <doc:RepositoryPluginAdapterExecutionPolicy>, <doc:RepositoryPluginAdapterRealLocalValidation> |
| Trusted local adapter runtime sandbox | Phase 42 defines the sandbox/runtime boundary required before any trusted local adapter process can run: explicit operator approval, adapter package identity, process isolation, sealed environment, dependency isolation, network-deny-by-default policy, output digests, audit records, and review-only authority. P42-T1 is documentation-only and keeps `adapterExecution: not_run`. P42-T2 adds the machine-readable `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture with adapter package identity, sandbox policy identity, approval requirements, filesystem/environment/network/dependency policy, output verification, audit requirements, and no-execution/non-authority statements. P42-T3 adds the machine-readable `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture with sandbox contract identity/digest linkage, accepted/rejected/blocked checks, no-execution state, and review-only non-authority statements. P42-T4 adds `trusted-local-adapter-sandbox-runner-validation` and `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`, validating sandbox contract/preflight linkage while preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`, `adapterProcessSpawned: false`, `executedAdapterCount: 0`, and `registryAuthority: false`. P42-T5 adds `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun` as an explicitly approved synthetic run fixture with approval binding, synthetic output candidates, output digests, audit records, and no real adapter process execution. P42-T6 adds `synthetic-trusted-local-adapter-sandbox-run-verifier` and `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` for deterministic fixture/link/output/audit verification while still preserving no real adapter execution and no registry authority. P42-T7 adds `real-local-trusted-adapter-sandbox-run-readiness` and `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` for future real-run review prerequisites while still refusing adapter code loading and process spawning. P42-T8 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` as a request-only fixture for future real-run review, verifier/readiness evidence requirements, scoped approval, runtime/output/audit policy, and non-authority statements without granting execution permission. P42-T9 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport` for request identity/digest, verifier/readiness requirements, rejected unsafe shapes, blocked execution drift, and review-only non-authority statements. P42-T10 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport` for request/preflight linkage validation while preserving disabled execution, no adapter code loading, no process spawning, no network access, no registry authority, and no adapter output acceptance. P42-T11 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff` for packaging P42-T8/P42-T9/P42-T10 artifacts as portable review evidence while preserving no execution permission, no operator approval, no registry authority, and no adapter output truth. P42-T12 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate` for validating the P42-T11 handoff and recording runtime prerequisites while preserving no runtime implementation, no runtime invocation, and no execution permission. P42-T13 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding` for binding one future local adapter run approval scope while preserving no execution permission, no registry authority, no consumed approval, and no adapter output truth. P42-T14 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport` for validating the P42-T13 approval binding through a disabled invocation skeleton while preserving no runtime invocation, no approval consumption, no registry authority, and no adapter output truth. P42-T15 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff` for packaging P42-T13 approval binding and P42-T14 disabled invocation evidence as portable review material while preserving no execution permission, no approval consumption, and no registry authority. P42-T16 adds `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewPacket` for packaging the P42-T15 handoff and implementation prerequisites as review material while preserving no runtime implementation, no runtime invocation, no approval consumption, and no registry authority. P42-T17 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationSkeleton` for recording the disabled future runtime surface from the P42-T16 review packet while preserving no adapter code loading, no adapter import, no process spawning, no runtime invocation, no approval consumption, and no registry authority. P42-T18 adds `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationSkeletonVerifierReport` for verifying the P42-T17 skeleton identity, digest, disabled surface, check counts, execution boundary, and non-authority statements while preserving no runtime invocation, no approval consumption, and no registry authority. | <doc:TrustedLocalAdapterRuntimeSandboxPlan>, <doc:TrustedLocalAdapterSandboxContractFixture>, <doc:TrustedLocalAdapterSandboxPreflightReportFixture>, <doc:TrustedLocalAdapterSandboxRunnerValidation>, <doc:TrustedLocalAdapterSyntheticSandboxRunFixture>, <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier>, <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestPreflightFixture>, <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRunnerSkeleton>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunnerEvidenceHandoff>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewGate>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxOperatorApprovalBinding>, <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeInvocationSkeleton>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeInvocationEvidenceHandoff>, <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewPacket>, <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeImplementationSkeleton>, <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeImplementationSkeletonVerifier>, <doc:TrustedLocalAdapterRuntimeReadiness>, <doc:TrustedLocalAdapterRealLocalReadinessValidation> |
| Optional CodeGraph input boundary | Pre-existing CodeGraph artifact normalization and offline pinned interface compatibility checks. | <doc:CodeGraphSourceGraphAdapter>, <doc:CodeGraphCompatibilityGuard> |

## Product Boundary

The current product quality target is:

```text
valid starter package, not final accepted spec
```

An author-ready draft should provide valid SpecPM files, evidence links,
digests, diagnostics, quality verdicts, author action items, and static review
output. It can still require author edits.

It must not hide failed validation, fabricate evidence, remove `preview_only`,
or present AI output as registry truth.

## SpecPM Boundary

SpecHarvester produces review evidence. SpecPM remains the validator, registry
authority, and public-index publisher.

Passing preflight means the bundle is internally consistent enough for review.
It does not accept the package into the registry.

## Corpus Selection Boundary

<doc:CorpusSelectionPolicy> defines how SpecHarvester chooses important
libraries across ecosystems before autonomous candidate generation. Source
selection is a curated operator decision over repositories and package
families, not an open-ended registry crawl.

<doc:SpecHarvesterCorpusPlan> defines the machine-readable plan shape for
selected, deferred, and rejected source decisions before any autonomous batch
run starts.

<doc:CandidateSourceClassifierPlan> defines how package-like units inside
selected repositories should be classified before drafting.

<doc:MultiEcosystemSeedCorpusPlan> records the first bounded seed set across
JavaScript/TypeScript, Python, Rust, Go, and Swift. It is a plan for future
local-checkout runs, not permission to clone repositories or publish registry
metadata.

<doc:ExplainableCorpusSelectionReport> explains selected, deferred, and
rejected seed sources, quota decisions, and the downstream command plan before
any readiness check or autonomous batch.

<doc:SelectedCorpusDryRunReadiness> records that the Phase 35 seed corpus is
blocked until operator-provided pinned local checkouts are verified.

<doc:RepositoryParsingPluginContract> defines the Phase 36 plugin contract for
repository path classification. <doc:FastAPIParserProfileRerun> records the
first practical profile run. <doc:RepositoryProfileSelectionContract> defines
the Phase 37 contract and the `repository-profile-detect` CLI report surface
plus autonomous batch sidecar evidence for selecting repository profile
plugins before path classification. The profile keeps documentation,
tutorials, examples, and tests available as semantic usage evidence while
keeping public interface indexes focused on package surfaces intended for
consumers.

<doc:RepositoryProfileDiscoveryHints> defines generic path-role hints such as
`package_set_root`, `member_package`, `example_package`, `internal_utility`,
and `evidence_only`.

<doc:RepositoryProfileCrossEcosystemFixtures> records workspace-shaped,
single-package, nested-package, and ambiguous multi-signal fixtures for the
same generic profile selection contract.

<doc:RepositoryProfileRealRunFastMCP> records the first real FastMCP
auto-selection comparison. The run passed, but auto-selection fell back to
`generic.repository.v0`; manual `fastmcp_slim` targeting produced a much
narrower public interface index. P37-T8 adds harvested manifest fallback
evidence when workspace inventory has no manifest records.

<doc:RepositoryPluginSubsystemContract> defines the Phase 38 contract that
turns parser profiles, repository profiles, future evidence producers,
topology helpers, and review surfaces into explicit plugin roles with
registration metadata, applicability reports, deterministic selection
boundaries, and producer-side authority limits.

<doc:RepositoryPluginRegistryFixture> records the first machine-readable
`SpecHarvesterRepositoryPluginRegistry` fixture for declared plugin contracts.
The fixture is not plugin execution, not registry acceptance, and not accepted
package truth.
<doc:RepositoryPluginApplicabilityReportFixture> records the first
machine-readable `SpecHarvesterRepositoryPluginApplicabilityReport` fixture for
selected, rejected, fallback, and blocked plugin decisions from static
evidence.
<doc:AutonomousCandidateBatch> can copy that report as
`repositoryPluginApplicability` sidecar producer evidence with
`appliedToDrafting: false` and `registryAuthority: false`.
<doc:RepositoryPluginCrossEcosystemFixtures> records static applicability
examples for manifest-backed single-package, workspace, documentation-heavy,
nested package root, and ambiguous mixed repository shapes.
<doc:RepositoryPluginRealRunFastMCP> records a real FastMCP plugin evidence
run. The run shows current profile selection choosing
`generic.single_package.v0` and autonomous batch recording
`repositoryPluginApplicability` as sidecar evidence with
`appliedToDrafting: false` and `registryAuthority: false`.

<doc:RepositoryPluginMultiRepositoryStaticEvaluatorValidation> records the
P39-T6 real FastMCP, FastAPI, and xyflow validation through the standalone
static evaluator and the P39-T5 batch auto-sidecar path.

<doc:StaticRepositoryPluginApplicabilityEvaluator> defines the Phase 39 helper,
`repository-plugin-applicability-detect` CLI, and opt-in
`autonomous-candidate-batch --repository-plugin-registry
--repository-plugin-static-evidence-envelope` integration for deriving
`SpecHarvesterRepositoryPluginApplicabilityReport` from static evidence such as
source manifest metadata, `harvest.json`, `workspace-inventory.json`,
`repository-profile-detection.json`, public-interface indexes, and operator
labels.

<doc:RepositoryPluginStaticEvidenceEnvelopeFixture> records the P39-T2
`SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` fixture, including safe
relative evidence paths, SHA-256 digests, `evidenceKinds[]`, advisory signals,
and non-authority boundaries.
<doc:RepositoryPluginAdapterContract> records the P40-T1 adapter contract.
<doc:RepositoryPluginAdapterManifestFixture> records the P40-T2
`SpecHarvesterRepositoryPluginAdapterManifest` fixture.
<doc:RepositoryPluginAdapterPreflightReportFixture> and
<doc:AutonomousCandidateBatch> record the P40-T5 opt-in batch sidecar path for
adapter manifest/preflight evidence as `repositoryPluginAdapterEvidence` with
copied paths, SHA-256 digests, allowed/rejected/fallback/blocked counts,
`appliedToDrafting: false`, `registryAuthority: false`, and
`adapterExecution: not_run`.
<doc:RepositoryPluginAdapterCrossEcosystemFixtureMatrix> records the P40-T6
static adapter fixture matrix across manifest-backed single packages,
workspaces, documentation-heavy repositories, nested package roots, and
ambiguous mixed layouts without loading third-party adapter code.

## Non-Goals

SpecHarvester does not clone or discover repositories during documented corpus
runs, execute harvested code, install harvested dependencies, run harvested
package scripts, access secrets, accept packages, accept relations, seed
baselines, remove `preview_only`, or publish directly into the SpecPM public
registry.

## Maturity

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
