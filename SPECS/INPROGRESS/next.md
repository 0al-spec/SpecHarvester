# Next Task: P17-T4 Public API Analyzer Pipeline Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** Large
**Dependencies:** P17-T3
**Status:** Selected
**Last Archived:** P17-T3 Report Builder Behavior Objects

## Recently Archived

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

Refactor public API analyzer pipelines into language-specific analyzer objects
that use shared payload and option objects without hiding language-specific
parse, diagnostic, symbol, or evidence decisions.

This is the next Phase 17 EO refactoring slice after the accepted diff report
object seam. Keep the scope narrow and start with one language analyzer before
attempting broader analyzer orchestration changes.

## Next Step

Run the BRANCH and PLAN commands for P17-T4.
