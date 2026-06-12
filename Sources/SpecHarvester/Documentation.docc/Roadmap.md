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
- <doc:XyflowPackageSetSmoke>
