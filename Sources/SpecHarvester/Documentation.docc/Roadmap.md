# Roadmap

SpecHarvester is in functional alpha as a bounded producer pipeline for
reviewable SpecPM candidate packages.

The canonical repository roadmap is `docs/ROADMAP.md`. This DocC page mirrors
the same direction for public documentation readers.

## Maturity Snapshot

SpecHarvester can run the current producer loop for selected public
repositories: collect static evidence, draft candidate bundles, validate them
with SpecPM, preflight bundle integrity, render review viewers, produce
package-set handoff artifacts, and optionally emit proposal-only AI enrichment
through local OpenAI-compatible providers such as LM Studio.

It is not a registry authority. It does not publish packages, accept package
relations, execute repository-owned scripts, crawl private repositories, or
treat model output as registry truth.

## Current Functional Alpha Baseline

SpecHarvester is usable today for:

- deterministic static evidence collection from allowlisted repository files;
- conservative `SpecPackage` and `BoundarySpec` candidate drafting;
- SpecPM validation before proposal or promotion;
- producer receipts, validation reports, and diagnostics reports;
- candidate bundle and bundle-set preflight;
- static candidate and package-set viewer output;
- monorepo workspace inventory;
- proposal-only LLM package-set draft selection from deterministic workspace
  inventory;
- package-set and scoped member candidate drafting;
- producer-observed package relation proposals;
- local `xyflow-package-set-smoke` package-set smoke coverage;
- package-set handoff proposal JSON and Markdown;
- fresh candidate refresh run export for SpecPM
  `prepare-refresh-decision` compare inputs;
- trusted SpecPM proposal workflow boundaries;
- proposal-only package-set AI enrichment.

## Milestones

### Producer Bundle Reliability

Generated candidate bundles include `specpm.yaml`, `specs/*.spec.yaml`,
`producer-receipt.json`, `validation-report.json`, and `diagnostics.json`.
Preflight checks required files, output hashes, report digests, stable IDs,
evidence links, and review status before a bundle is handed to SpecPM.

### SpecPM Handoff Boundary

SpecHarvester emits handoff evidence that SpecPM can review and preflight
without executing producer tools. Trusted workflow paths can attach evidence to
SpecPM review while keeping write credentials out of untrusted pull request
events. Handoff artifacts preserve a stable producer evidence layout for a
future optional SpecPM CI preflight gate and reference external SpecPM registry
acceptance decision records without writing maintainer approval into generated
receipts. Fresh candidate refresh runs export generated package-set bundles
into the `specpm-public-index-generated-root/v0` layout so SpecPM can compare
`<package_id>/<version>/specpm.yaml` and `specs/*.spec.yaml` contract files
mechanically. The real `xyflow` refresh compare run produced
`status: no_update_required`, `updateNeeded: false`, and
`reason: no_contract_delta` after verifying 8 generated contract-file digests.
The real `TanStack/query` refresh compare run produced a 39-candidate
package-set with 38 relation proposals and a structured SpecPM
missing-baseline result, confirming the producer handoff is not
`xyflow`-specific while keeping first-submission workflows separate from
refresh comparison. `--role-profile generic_monorepo` now selects
workspace/member package-set output for generic monorepos and reproduced the
useful TanStack/query 39-candidate / 38-relation shape without raw
`--role member_package` operator knowledge.
`SpecHarvesterBaselineSubmissionHandoff` records first-submission or
seeded-baseline review evidence when SpecPM reports
`refresh_decision_prepare_current_contract_files_missing`. The next boundary is
SpecPM-side intake policy for those handoff artifacts.

### Package Sets and Monorepo Discovery

Workspace inventory, package-set drafting, scoped member candidates, relation
proposals, bundle-set preflight, and package-set viewer output are implemented
for the `xyflow` reference shape. Aggregate packages such as `xyflow.workspace`
remain separate from scoped members such as `xyflow.react`, `xyflow.svelte`, and
`xyflow.system`. Package-set contract alignment is documented before runtime
monorepo discovery implementation, mapping SpecPM contracts to workspace
inventory, package-set candidates, scoped member packages, relation proposals,
bundle-set preflight, static viewer previews, and the `xyflow` smoke scenario.

### Proposal-Only AI Enrichment

Local OpenAI-compatible providers can suggest evidence-grounded summaries,
capabilities, interfaces, confidence, and evidence gaps for generated
package-set candidates. AI enrichment remains proposal evidence only and does
not mutate generated specs or accept registry content.

Clean proposals can also be applied deterministically into copied
AI-enriched preview candidates through `apply-ai-enrichment-proposal` and the
`autonomous-candidate-batch --apply-ai-enrichment` option. The copied
candidates keep `preview_only`, carry `ai-enrichment-candidate-patch.json`, and
remain producer review evidence rather than SpecPM acceptance.

### Author-Ready Valid Drafts

The active product-quality focus is to define when SpecHarvester should stop
drafting and hand a valid starter package to the repository author. The target
is an author-ready draft: valid under SpecPM, repository-specific,
evidence-backed, conservative, explicit about gaps, and cheaper for an author
to edit than to write from scratch. `author-ready-draft-quality-report.json`
now exposes an `authorReadyDraft` verdict, hard gates, dimensions, and author
action items. Package-set outputs also expose `authorReadyDraftSummary` so
operators can stop when remaining work is author-reviewable rather than
generator-fixable. Viewer and handoff outputs derive `authorReview` checklists,
weak claims, evidence gaps, recommended edits, and member action summaries from
the same evidence so authors can start review without reading raw JSON first.
The author-ready calibration matrix records estimated author edits, edit
categories, review priorities, and repeated generator gaps across real
repositories before broader intake is expanded.

See <doc:AuthorReadyDraftQualityBar> and
<doc:AuthorReadyDraftQualityReport>. See also
<doc:AuthorReadyCalibrationMatrix>.

### Multi-Repository Quality Calibration

The next practical focus is to run the current pipeline across 5-10 real
repositories from different ecosystems and repository shapes. Each run should
record package identity quality, summary quality, capability precision,
interface evidence, diagnostics, relation proposals, skipped packages, and any
gap between deterministic output, optional LM Studio enrichment, and human
review.

The P30 limited popular-library scraping batch completed this expansion with a
bounded source manifest, explicit stop conditions, deterministic and live run
commands, candidate-layer triage states, and non-authority boundaries. See
<doc:LimitedPopularLibraryCorpusPlan>.
The deterministic `--skip-ai` result is recorded in
<doc:LimitedPopularLibraryDeterministicBatch> with verdict
`ready_for_live_lm_studio_limited_corpus`.
The live LM Studio result is recorded in
<doc:LimitedPopularLibraryLiveLMStudioBatch> with verdict
`ready_for_candidate_layer_triage`: all six repositories processed, nine
preview candidates preserved, three relation proposals preserved, JSON repair
not needed, and model findings bounded to candidate review diagnostics.
The candidate-layer triage result is recorded in
<doc:LimitedPopularLibraryCandidateLayerTriage> with verdict
`ready_for_selected_handoff_dry_run`: `flask.core`, `gin.core`, and
`docc2context.core` are selected for P30-T5 dry-run handoff, while xyflow,
Cupertino, and NavigationSplitView candidates remain deferred until targeted
regeneration or package-identity fixes.
The selected handoff dry run is recorded in
<doc:LimitedPopularLibrarySelectedHandoffDryRun> with verdict
`selected_handoff_dry_run_ready`: `flask.core`, `gin.core`, and
`docc2context.core` have passing producer preflight reports, static viewer
digests, and `external_required` registry acceptance decisions while all
deferred candidates stay out of the handoff.

### Selected Candidate SpecPM Intake Handoff

The completed intake-handoff focus turns selected candidate dry-run evidence
into portable SpecPM review evidence while preserving the boundary that
SpecHarvester is only the producer of preview artifacts.

`SpecHarvesterSelectedCandidateHandoffProposal` records selected candidates,
deferred candidates, required evidence roles, producer preflight status, static
viewer status, and external registry acceptance decisions. Passing producer
preflight remains review evidence only. No proposal accepts packages, accepts
relations, seeds baselines, removes `preview_only`, publishes registry
metadata, or creates a SpecPM pull request.

See <doc:SelectedCandidateHandoffProposal>.
The helper command is `selected-candidate-handoff-proposal` and writes
`selected-candidate-handoff-proposal.json` plus
`selected-candidate-handoff-proposal.md` from the selected handoff dry-run
source evidence.

P31-T3 records the real selected candidate helper run in
`tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`
and <doc:SelectedCandidateHandoffProposalP31T3>. That artifact covers
`flask.core`, `gin.core`, and `docc2context.core` only; the deferred P30
candidates remain excluded until regeneration.

P31-T4 records downstream SpecPM-side preflight expectations in
<doc:SelectedCandidateHandoffPreflightExpectations>. The expected future
report is `SpecPMSelectedCandidateHandoffPreflightReport` with
`apiVersion: specpm.selected-candidate-handoff-preflight/v0`, and a pass means
internally consistent review evidence, not package acceptance.

P31-T5 records deferred selected-candidate regeneration requirements in
<doc:DeferredSelectedCandidateRegenerationRequirements> and the
`SpecHarvesterDeferredSelectedCandidateRegenerationRequirements` fixture with
`apiVersion: spec-harvester.deferred-selected-candidate-regeneration-requirements/v0`.
The requirements cover package-set identity regeneration, warning-bearing
enrichment regeneration, and identity-drift resolution before deferred
candidates can enter selected handoff.

P26-T3 records the package-set proposal intake checklist in
<doc:PackageSetProposalIntakeChecklist>. It names
`SpecHarvesterPackageSetHandoffProposal`,
`spec-harvester.package-set-handoff-proposal/v0`, the required evidence roles,
and the boundary between package member acceptance and relation acceptance.

### Autonomous Deferred Candidate Regeneration

The next planned focus is to convert the P30/P31 deferred candidate findings
into a bounded regeneration and intake-readiness sequence before any broader
popular-library scraping is attempted.

The sequence records the work plan, adds the deferred candidate regeneration
runbook in <doc:DeferredCandidateRegenerationRunbook>, reruns xyflow
package-set identity regeneration in
<doc:XyflowPackageSetIdentityRegenerationDryRun>, repairs or regenerates
`cupertino.core` and `navigation_split_view.core`, refreshes candidate-layer
triage and selected handoff evidence, coordinates SpecPM-side selected
candidate handoff preflight, and records a limited corpus intake readiness
decision.

P32-T4 records the single-package deferred regeneration dry run in
<doc:SinglePackageDeferredCandidateRegenerationDryRun>. It keeps
`cupertino.core` deferred because `refined_summary_missing` remains unresolved
and makes `navigation_split_view.core` eligible for refreshed candidate-layer
review under the canonical underscore id.
P32-T5 records the refreshed selected handoff in
<doc:RefreshedCandidateLayerSelectedHandoff>: eight candidates are ready for
SpecPM-side selected handoff preflight, while `cupertino.core` remains
deferred on `refined_summary_missing`.
P32-T6 records that the SpecPM preflight was merged in
[0al-spec/SpecPM#140](https://github.com/0al-spec/SpecPM/pull/140) and that the
P32-T5 fixture passes with eight selected candidates, one deferred candidate,
and three source digests verified.
P32-T7 records the intake readiness decision in
<doc:LimitedCorpusIntakeReadinessDecision>: the selected preview candidates are
ready for author/maintainer review, `cupertino.core` remains deferred, and
broader autonomous scraping requires a separate follow-up task.

The boundary remains unchanged: no clone/fetch/install/execute behavior, no
registry publication, no package or relation acceptance, no baseline seeding,
no `preview_only` removal, and no broad autonomous scraping before the limited
corpus is reviewable.

See <doc:AutonomousCandidateTechDebtPlan>.

### Bounded Corpus Expansion Planning

The next phase after Phase 32 is a bounded corpus expansion plan, not an
unbounded popular-framework crawl.

<doc:BoundedCorpusExpansionPlan> records `P33-T1`: the next corpus must have a
pinned local source manifest, a five-repository limit, deterministic and
live-model validation gates, candidate-layer triage, SpecPM-side selected
handoff preflight, stop conditions, and a non-authority boundary before any new
scrape runs.

<doc:NextCorpusSourceManifest> records `P33-T2`: the next source manifest is
`inputs/p33-next-corpus/repositories.yml`, contains `serena`, `transmission`,
`mcpm-sh`, `specgraph`, and `specpm`, and keeps all entries pinned by exact
revision.

<doc:NextCorpusDeterministicDryRun> records `P33-T3`: the deterministic
`--skip-ai` run processed all five repositories, produced five preview
candidates, zero relation proposals, five passing bundle-set preflights, and
package-id review signals for `mcpm-sh` and `specgraph`.

<doc:NextCorpusLiveLocalModelBatch> records `P33-T4`: the live LM Studio run
used `openai/gpt-oss-20b`, preserved the five preview candidates and zero
relation proposals, passed five bundle-set preflights, produced five AI draft
proposals and five AI enrichment proposals, required zero JSON repair attempts,
recorded `76291` provider tokens, and reached
`ready_for_candidate_layer_triage`.

<doc:NextCorpusCandidateLayerTriage> records `P33-T5`: selected candidates
`serena.core` and `specpm.core` are ready for P33-T6 selected handoff
preflight, while `transmission.core`, `mcpm.system`, and `specgraph.system`
remain deferred on package boundary, package identity, and AI draft evidence
findings.

<doc:NextCorpusSpecPMPreflightIntakeDecision> records `P33-T6`: the current
SpecPM selected handoff preflight rejects the P33-T5 candidate-layer triage
fixture with `selected_handoff_payload_missing`, so the next corpus needs a
durable selected handoff artifact before maintainer intake review.

<doc:NextCorpusDurableSelectedHandoff> records `P33-T7`: the durable selected
handoff artifact for `serena.core` and `specpm.core` passes SpecPM selected
handoff preflight with three deferred candidates and zero warnings or errors.

<doc:NextCorpusIntakeReadinessDecision> records `P33-T8`: the final Phase 33
decision status is
`ready_for_author_maintainer_review_with_explicit_deferral`. The selected
candidates `serena.core` and `specpm.core` are ready for author/maintainer
review, while `transmission.core`, `mcpm.system`, and `specgraph.system` remain
deferred.

The boundary remains unchanged: no clone/fetch/install/execute behavior, no
registry publication, no package or relation acceptance, no baseline seeding,
no `preview_only` removal, and no AI output as registry truth.

### Ecosystem Analyzer Depth

Future generator quality should come primarily from deterministic analyzer
improvements: richer JavaScript/TypeScript public interface extraction, broader
ecosystem profiles, analyzer version recording, source digests, and explicit
confidence. Package scripts, tests, and dependency installation remain outside
the default pipeline.

### Operator UX and Governance Reports

Operator reports should make review cheaper by surfacing namespace, upstream,
license, provenance, duplicate-intent, diagnostics, and evidence-quality risks
beside candidate bundles. These reports remain review aids and do not imply
SpecPM acceptance.

### Autonomous Candidate Harvest MVP

Operators need one cost-controlled runner for popular-library exploration. The
MVP path runs repository source manifests through deterministic collection,
workspace inventory, package-set drafting, bundle-set preflight, optional local
LM Studio AI draft/enrichment proposals, and one batch report.

Generated artifacts remain `preview_only` producer evidence. SpecHarvester does
not clone repositories, execute harvested code, install dependencies, publish
registry metadata, or accept packages. SpecPM remains the acceptance and
registry authority.

The first mixed corpus check exposed follow-up work: single-package repositories
such as Flask and Gin needed a fallback preview candidate path, and local LM
Studio/OpenAI-compatible output needed bounded JSON repair/retry. See
<doc:AutonomousCandidateTechDebtPlan>.

Before expanding autonomous corpus scraping, SpecHarvester documents the
SpecPM-facing candidate-layer review boundary in
<doc:AutonomousCandidateIntakePolicy>.
The current mixed-corpus baseline is recorded in
<doc:AutonomousCandidateCorpusBaseline>, including Flask/Gin
`single_package_fallback_needed` outcomes and the xyflow
`ai_json_repair_needed` LM Studio diagnostic.
The Flask/Gin deterministic fallback is documented in
<doc:SinglePackageCandidateFallback>.
The local model repair path records `ai_json_repair_needed`,
`ai_json_repair_exhausted`, provider receipt `jsonRepairStatus`, and batch
`jsonRepair` summaries without persisting raw prompts, raw responses, secrets,
or chain-of-thought.
The post-fallback quality gate is recorded in
<doc:AutonomousCandidateCorpusQualityGate> with verdict
`ready_for_limited_popular_library_scraping`.

### Curated Multi-Ecosystem Corpus Selection

Phase 35 records the next planning step: SpecHarvester should select important
library repositories and package families through a bounded, explainable corpus
plan rather than raw registry search results or open-ended crawling.

The planned work starts with `P35-T1`, <doc:CorpusSelectionPolicy>, which defines
importance signals, exclusion rules, ecosystem quotas, local checkout
requirements, and producer-evidence boundaries. `P35-T2` defines
<doc:SpecHarvesterCorpusPlan>, and `P35-T3` defines candidate source
classification through <doc:CandidateSourceClassifierPlan>. `P35-T4` records
the bounded seed corpus in <doc:MultiEcosystemSeedCorpusPlan>, and `P35-T5`
records selection explanations in <doc:ExplainableCorpusSelectionReport>.
`P35-T6` records dry-run readiness in <doc:SelectedCorpusDryRunReadiness>.

This phase explicitly covers JavaScript/TypeScript, Python, Rust, Go, and at
least one additional ecosystem. It also records why registry search noise such
as internal utilities, types-only packages, generated artifacts, deprecated
sources, examples, test fixtures, build tooling, and unrelated high-download
packages must be excluded or deferred before autonomous candidate generation.

The boundary remains unchanged: no clone/fetch/install/execute behavior, no
registry publication, no package or relation acceptance, no baseline seeding,
no `preview_only` removal, and no AI output as registry truth.

The Phase 35 seed corpus is blocked until operator-provided pinned local
checkouts are verified.

### Repository Parsing Plugin System

Phase 36 records the next precision layer after the FastAPI AI-enabled rerun:
repository parsing plugins should classify repository paths by evidence role
before public interface indexes are assembled.

`P36-T1` defines <doc:RepositoryParsingPluginContract>. The contract separates
public API evidence from semantic usage/documentation evidence, uses FastAPI
`docs_src/*` over-capture as the motivating case, and keeps the intended
Python web-framework parser profile reusable rather than repository-specific.

Completed follow-ups:

- `P36-T2`: add a machine-readable Python web-framework parser profile
  fixture;
- `P36-T3`: implement the first plugin-aware source classification hook;
- `P36-T4`: rerun FastAPI with the parser profile and compare evidence volume
  and claim quality.

The P36-T4 FastAPI rerun is recorded in
<doc:FastAPIParserProfileRerun>. It shows `docs_src/*` public interface
entrypoints dropping from `454` to `0` while FastAPI package entrypoints stay
at `48`. The output is closer to registry-review quality on evidence boundary,
but AI proposal artifacts still had warning-level gaps, so the result remains
an author-ready starter package rather than a clean registry handoff.

Plugin decisions remain producer-side evidence only: no registry publication,
no package or relation acceptance, no baseline seeding, no `preview_only`
removal, and no AI output as registry truth.

### Repository Profile Plugin Selection

Phase 37 plans the next layer after parser profiles: deciding which repository
profile plugin, if any, should be applied to a given checkout.

The planned work starts with `P37-T1`,
<doc:RepositoryProfileSelectionContract>, a language- and
framework-agnostic selection contract. The shared model is:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

Planned follow-ups:

- `P37-T2`: define a machine-readable
  `SpecHarvesterRepositoryProfileDetection` fixture format;
- `P37-T3`: add an opt-in detection CLI/report surface that emits profile
  decisions without collecting source, invoking AI, or drafting packages;
- `P37-T4`: connect profile selection to autonomous candidate batch through
  explicit `auto | none | <profile-id>` modes and sidecar
  `repository-profile-detection.json` artifacts;
- `P37-T5`: define generic workspace/member discovery hints for package-set
  roots, members, meta packages, primary packages, CLI/bridge packages,
  plugin packages, examples, tests, docs, generated artifacts, internal
  utilities, and evidence-only sources through
  <doc:RepositoryProfileDiscoveryHints> and
  `SpecHarvesterRepositoryProfileHintVocabulary`;
- `P37-T6`: add cross-ecosystem fixtures so the subsystem is not tied to one
  language or framework through
  <doc:RepositoryProfileCrossEcosystemFixtures>;
- `P37-T7`: rerun a real repository with profile auto-selection and compare
  it against manual targeting through
  <doc:RepositoryProfileRealRunFastMCP>;
- `P37-T8`: make repository profile detection consume harvested package
  manifest evidence when workspace inventory has no manifest records.

The motivating FastMCP dry run showed why this layer is needed: generic
repository-wide collection can over-include docs/examples, while manual member
targets can produce better author-ready starter packages. FastMCP remains a
validation case, not a hardcoded profile rule.

P37-T7 confirmed that finding on a real FastMCP checkout. Auto-selection passed
and explained its fallback, but it did not improve targeting: `harvest.json`
found `pyproject.toml`, `workspace-inventory.json` had no manifest records, and
manual `fastmcp_slim` targeting reduced public interface entrypoints from `772`
to `260`.

P37-T8 closes that generic evidence-routing gap by supplementing empty
workspace inventory evidence with already-collected static manifest paths from
`harvest.json`.

Selection decisions remain producer-side evidence only. Profile selection does
not clone or fetch repositories, install dependencies, execute harvested code,
invoke package managers, run AI, publish registry metadata, accept packages or
relations, remove `preview_only`, or accept plugin decisions as registry
truth. Profile selection does not treat AI output as registry truth.

### Repository Plugin Subsystem

Phase 38 turns parser profiles and repository profiles into a broader
language- and framework-agnostic plugin subsystem contract.

The first step is `P38-T1`, <doc:RepositoryPluginSubsystemContract>, which
defines plugin identity, plugin roles, registration metadata, static evidence
inputs, applicability reports, deterministic selection boundaries, output
artifact categories, diagnostics, and authority limits. The shared model is:

```text
register plugins -> collect static evidence -> evaluate applicability
  -> select, fallback, or block -> emit producer-side evidence
```

P38-T2 adds the first `SpecHarvesterRepositoryPluginRegistry` registry fixture
in <doc:RepositoryPluginRegistryFixture> and
`tests/fixtures/repository_plugins/generic-registry.example.json`.

P38-T3 adds the first `SpecHarvesterRepositoryPluginApplicabilityReport`
fixture in <doc:RepositoryPluginApplicabilityReportFixture> and
`tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
It records selected, rejected, fallback, and blocked plugin decisions from
static evidence without running plugin code.

P38-T4 connects registry/applicability output to <doc:AutonomousCandidateBatch>
as `repositoryPluginApplicability` sidecar producer evidence. The batch copies
the applicability report to
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`
and records path, digest, authority, summary counts, and diagnostic codes while
keeping `appliedToDrafting: false` and `registryAuthority: false`.

P38-T5 adds a cross-ecosystem static fixture matrix in
<doc:RepositoryPluginCrossEcosystemFixtures> and
`tests/fixtures/repository_plugins/cross_ecosystem/`. The matrix covers
manifest-backed single-package, workspace, documentation-heavy, nested package
root, and ambiguous mixed repository shapes while keeping plugin applicability
producer-side and language/framework agnostic.

P38-T6 records a real FastMCP plugin evidence comparison in
<doc:RepositoryPluginRealRunFastMCP> and
`tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.
The run shows current repository profile selection choosing
`generic.single_package.v0` and autonomous batch recording
`repositoryPluginApplicability` as sidecar evidence with
`appliedToDrafting: false` and `registryAuthority: false`.

Phase 39 starts with <doc:StaticRepositoryPluginApplicabilityEvaluator>. It
P39-T3 adds the deterministic helper, P39-T4 adds
`repository-plugin-applicability-detect`, and P39-T5 connects the same evaluator
to `autonomous-candidate-batch` through explicit
`--repository-plugin-registry` and
`--repository-plugin-static-evidence-envelope` opt-in inputs. Together they
derive `SpecHarvesterRepositoryPluginApplicabilityReport` from a static
evidence envelope rather than hand-authored sidecars. The helper, CLI, and
batch integration remain producer-side evidence only: they do not load plugins,
execute plugins, read repository source files, run package managers, install
dependencies, invoke AI, auto-attach generated reports to autonomous batch
output without explicit operator opt-in, accept packages or relations, publish
registry metadata, remove `preview_only`, or treat plugin decisions as registry
truth.

P39-T2 adds <doc:RepositoryPluginStaticEvidenceEnvelopeFixture> and
`tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
The fixture records `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`,
safe relative evidence paths, SHA-256 digests, `evidenceKinds[]`, advisory
signals, and `appliedToDrafting: false` / `registryAuthority: false` sidecar
boundaries as the bounded input to the P39-T3 helper, P39-T4 CLI, and P39-T5
batch opt-in path.

P39-T6 records a real multi-repository validation in
<doc:RepositoryPluginMultiRepositoryStaticEvaluatorValidation> and
`tests/fixtures/repository_plugins/real_runs/p39-t6-multi-repository-static-evaluator-validation.example.json`.
The run covers FastMCP, FastAPI, and xyflow local checkouts, exercises both
`repository-plugin-applicability-detect` and
`autonomous-candidate-batch --repository-plugin-registry
--repository-plugin-static-evidence-envelope`, and confirms that generated
sidecars remain `sourceMode: auto_static_evaluator`,
`appliedToDrafting: false`, and `registryAuthority: false`.

Phase 40 starts with `P40-T1`, <doc:RepositoryPluginAdapterContract>. The
phase turns the static plugin selection work into a language- and
framework-agnostic boundary for future adapter implementations: adapter
identity, versioned manifests, declared input evidence, output artifacts,
execution modes, sandbox expectations, diagnostics, and authority limits.
Static applicability remains the default safe path. Adapter execution stays
disabled until a future task adds explicit operator-controlled execution
policy, manifest preflight, and safe evidence handoff rules.

P40-T2 records the first machine-readable adapter manifest fixture in
<doc:RepositoryPluginAdapterManifestFixture> and
`tests/fixtures/repository_plugins/adapter-manifest.example.json`.
P40-T3 records the first adapter preflight report fixture in
<doc:RepositoryPluginAdapterPreflightReportFixture> and
`tests/fixtures/repository_plugins/adapter-preflight-report.example.json`,
covering allowed, rejected, fallback, and blocked adapter decisions without
loading or executing adapter code.
P40-T4 records the adapter execution policy in
<doc:RepositoryPluginAdapterExecutionPolicy>: execution is disabled by
default, `static_only` remains the only current safe mode, and future
`trusted_local_tool` requires explicit operator opt-in, path allowlists,
bounded resources, no dependency installation, no package manager invocation,
no network discovery, and no harvested code execution.
P40-T5 connects operator-supplied adapter manifest and preflight evidence to
<doc:AutonomousCandidateBatch> through
`--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight`. The batch records
`repositoryPluginAdapterEvidence` with copied paths, SHA-256 digests,
allowed/rejected/fallback/blocked counts, diagnostics, `appliedToDrafting:
false`, `registryAuthority: false`, and `adapterExecution: not_run` while
preserving the existing static evaluator path unless an operator explicitly
supplies adapter evidence.
P40-T6 records <doc:RepositoryPluginAdapterCrossEcosystemFixtureMatrix> and
`tests/fixtures/repository_plugins/adapter_cross_ecosystem/adapter-fixture-matrix.example.json`
as static adapter manifest/preflight expectations across manifest-backed
single packages, workspaces, documentation-heavy repositories, nested package
roots, and ambiguous mixed layouts without loading third-party adapter code.
P40-T7 records <doc:RepositoryPluginAdapterRealLocalValidation> and
`tests/fixtures/repository_plugins/adapter_real_runs/p40-t7-real-local-adapter-contract-validation.example.json`
as real local validation over FastMCP, FastAPI, xyflow, and Gin pinned
checkouts. The run maps real repository evidence to P40-T6 matrix categories
while preserving `adapterExecution: not_run`, `adapterCodeLoaded: false`,
`appliedToDrafting: false`, and `registryAuthority: false`.

Phase 41 starts with `P41-T1`, <doc:TrustedLocalAdapterRuntimeReadiness>.
P41-T2 adds <doc:TrustedLocalAdapterRunRequestFixture> and the
machine-readable `SpecHarvesterTrustedLocalAdapterRunRequest` fixture. P41-T3
adds <doc:TrustedLocalAdapterRunPreflightReportFixture> and the
machine-readable `SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture.
P41-T4 adds <doc:TrustedLocalAdapterRunnerSkeleton>, the
`trusted-local-adapter-runner-skeleton` CLI, and the machine-readable
`SpecHarvesterTrustedLocalAdapterRunReport` no-execution report. The phase
prepares a future trusted local adapter runtime without enabling execution yet.
P41-T5 connects the runner report to <doc:AutonomousCandidateBatch> through
`--trusted-local-adapter-run-report`, copying it as
`trustedLocalAdapterRunEvidence` with source/copied SHA-256 digests,
`adapterExecution: not_run`, `adapterCodeLoaded: false`,
`adapterProcessSpawned: false`, `executedAdapterCount: 0`,
`appliedToDrafting: false`, and `registryAuthority: false`. The remaining
follow-up is real local readiness validation over FastMCP, FastAPI, xyflow, and
Gin.

Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle,
and other ecosystems remain examples, not normative plugin rules. Repository
plugins and future adapters must not clone or fetch repositories, install
dependencies, execute harvested code, invoke package managers, run AI, publish
registry metadata, accept packages or relations, remove `preview_only`, or
treat plugin output as registry truth or treat adapter output as registry
truth.

## Non-Goals

SpecHarvester does not become the registry, the canonical package authority,
the package-set relation authority, or the execution runtime for harvested
repositories.

## References

- `docs/ROADMAP.md`
- <doc:HarvesterArchitecture>
- <doc:ProducerCandidateBundle>
- <doc:SpecPMHandoff>
- <doc:FreshCandidateRefreshRun>
- <doc:SpecPMPackageSetAlignment>
- <doc:PackageSetDrafting>
- <doc:BundleSetPreflight>
- <doc:AuthorReadyDraftQualityBar>
- <doc:PackageSetAIEnrichment>
- <doc:AutonomousCandidateBatch>
- <doc:AutonomousCandidateCorpusBaseline>
- <doc:SinglePackageCandidateFallback>
- <doc:LimitedPopularLibraryLiveLMStudioBatch>
- <doc:LimitedPopularLibraryCandidateLayerTriage>
- <doc:XyflowPackageSetSmoke>
