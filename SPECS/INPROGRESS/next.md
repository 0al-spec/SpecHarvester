# Next Task: P17-T5 Collector and Drafter Vertical Slice Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** Large
**Dependencies:** P17-T4
**Status:** Selected
**Last Archived:** P17-T4 Public API Analyzer Pipeline Objects

## Recently Archived

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
- `P17-T2` split selected CLI report execution bodies into
  `src/spec_harvester/cli_report_commands.py`. The completed slice introduced
  `CodeDuplicationReportCommand`, `ArchitectureLintCommand`, and
  `ProceduralStyleReportCommand` for `code-duplication-report`,
  `architecture-lint`, and `procedural-style-report` while preserving parser
  flags, JSON error output, report schemas, trust-boundary text, and exit-code
  behavior. The procedural-style smoke recorded behaviorRichClassCount: 3 for
  the new command-object slice.

## Description

Refactor collector and drafter behavior in thin vertical slices, adding
characterization tests before moving repository profile, license inference,
semantic evidence, intent profile, package draft assembly, or artifact-writing
logic.

This is the next Phase 17 EO refactoring slice after report and analyzer seams.
Keep the scope especially narrow because collector and drafter behavior touches
generated candidate package content.

## Next Step

Run the BRANCH and PLAN commands for P17-T5.
