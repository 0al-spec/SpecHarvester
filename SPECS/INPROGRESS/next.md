# Next Task: P17-T6 SpecNode Refinement Orchestration Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** Large
**Dependencies:** P17-T5
**Status:** Selected
**Active Branch:** `codex/p17-t6-specnode-refinement-orchestration-objects`
**Last Archived:** P17-T5 Collector and Drafter Vertical Slice Objects

## Recently Archived

- `P17-T5` moved single-package draft bundle materialization behind
  `SinglePackageDraftBundle` while preserving `DraftOptions`,
  `draft_spec_package`, generated `specpm.yaml`, boundary specs,
  `harvest.json`, optional public interface indexes, producer validation and
  diagnostics reports, author-ready quality reports, producer receipts,
  wrapper result fields, output roles, digests, and the receipt self-hash
  boundary. The procedural-style smoke recorded behaviorRichClassCount: 1 and
  reduced `drafter.py` topLevelFunctionSpan from 1665 to 1550.
- `P17-T4` moved the Python, Go, and JavaScript/TypeScript public API analyzer
  entry pipelines behind `PythonPublicApiAnalyzer`, `GoPublicApiAnalyzer`, and
  `JavaScriptTypeScriptPublicApiAnalyzer` objects while preserving analyzer
  ids, versions, confidence values, cache payloads, diagnostics, evidence
  records, wrapper signatures, and `PublicInterfaceIndex` validation behavior.
  The procedural-style smoke recorded behaviorRichClassCount: 3 and reduced
  analyzer topLevelFunctionSpan from 1085 to 927.
- `P17-T3` moved accepted candidate diff report behavior behind
  `AcceptedCandidateDiffReport`, `PackageDiffSource`,
  `AcceptedPackageVersions`, `CandidateComparison`, `PackageRecordDiff`, and
  `AcceptedCandidateDiffReportWriter` while preserving the
  `SpecHarvesterAcceptedCandidateDiffReport` schema, issue codes, comparison
  statuses, trust-boundary text, CLI output behavior, and downstream imports.
  The procedural-style smoke recorded behaviorRichClassCount: 4 and reduced
  accepted diff topLevelFunctionSpan from 204 to 87.

## Description

Refactor SpecNode refinement orchestration after the report, analyzer,
collector, and drafter seams are stable, keeping SpecHarvester-side provider,
validation, retry, and unavailable-result objects inside the existing SpecNode
contract boundary.

This is the final Phase 17 EO refactoring slice. Keep the scope narrow and do
not change the SpecNode artifact contracts, provider API, JSON schema
validation, retry semantics, or unavailable-result behavior while introducing
behavior-rich orchestration objects.

## Next Step

Run the BRANCH and PLAN commands for P17-T6.
