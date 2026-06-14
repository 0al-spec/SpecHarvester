# Next Task: P34-T2 Autonomous Batch AI Enriched Preview Output

**Priority:** High
**Phase:** Phase 34. AI-Enabled Candidate Curation
**Effort:** Medium
**Dependencies:** P34-T1, P29-T5, P33-T4
**Status:** Selected
**Active Branch:** TBD
**Last Archived:** P34-T1 AI Enrichment Candidate Patch Proposal

## Recently Archived

- `P34-T1` added `apply-ai-enrichment-proposal`, a deterministic helper that
  reads a clean `SpecHarvesterPackageSetAIEnrichmentProposal`, copies a
  generated candidate bundle into an enriched preview candidate copy, applies
  supported summary, capability, and interface enrichments, refreshes producer
  receipt digests, and writes `ai-enrichment-candidate-patch.json` with
  before/after digests, provider provenance, applied changes, skipped changes,
  and non-authority boundary statements.
- The helper rejects failed or warning-bearing proposal reports, package id
  drift between the proposal and `specpm.yaml`, unresolved package diagnostics,
  output paths inside the source bundle, and report paths that would mutate the
  source candidate.
- The FastAPI live LM Studio smoke was re-run through the helper. The enriched
  `fastapi.core` preview candidate produced patch `status: prepared`, applied
  `8` changes with `0` skipped changes, preserved `previewOnly: true`, kept
  `sourceMutated: false`, passed producer preflight with zero diagnostics, and
  passed SpecPM validation with only the expected `preview_only_package`
  warning. The enriched candidate includes repository-specific capabilities
  such as `fastapi.core.http_routing`,
  `fastapi.core.middleware_support`,
  `fastapi.core.request_response_context`, and
  `fastapi.core.openapi_generation`.
- `P20-T8` cleaned up stale DocC warnings by converting
  `AcceptedPackageUpdateProposals` from a symbol-page heading into a normal
  documentation article and by changing literal command references in
  `RealRepositoryQualityReport` from DocC symbol-style double-backtick markup
  to inline code markup. DocC static generation now completes with no
  `warning:` output for `AcceptedPackageUpdateProposals`,
  `python -m spec_harvester quality-report`, or `specpm validate`.

## Description

P34-T1 made AI enrichment practically applicable through an explicit operator
command. P34-T2 should make that useful in autonomous corpus runs by adding an
opt-in mode that applies clean AI enrichment proposals into copied enriched
preview candidates and emits `ai-enrichment-candidate-patch.json` reports
beside the usual proposal-only artifacts.

The default autonomous batch behavior must remain proposal-only. Enriched
preview output is allowed only when the proposal is completed, clean, package
aligned, and diagnostic-free for the selected package.

## Boundary

P34-T2 must not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- mutate source candidates;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as maintainer approval;
- treat AI output as upstream project endorsement;
- replace SpecPM validation.

## Next Step

Plan P34-T2 as a separate PR. Start by tracing
`autonomous-candidate-batch` output layout and deciding where an opt-in
enriched preview root and patch summary should appear in the batch report.
