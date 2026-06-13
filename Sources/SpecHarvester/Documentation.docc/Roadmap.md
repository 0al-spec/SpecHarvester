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

The P30 limited popular-library scraping batch starts this expansion with a
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
