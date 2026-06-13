# Next Task: P17-T3 Report Builder Behavior Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** Medium
**Dependencies:** P17-T2
**Status:** Selected
**Last Archived:** P17-T2 CLI Domain Command Objects

## Recently Archived

- `P17-T2` split selected CLI report execution bodies into
  `src/spec_harvester/cli_report_commands.py`. The completed slice introduced
  `CodeDuplicationReportCommand`, `ArchitectureLintCommand`, and
  `ProceduralStyleReportCommand` for `code-duplication-report`,
  `architecture-lint`, and `procedural-style-report` while preserving parser
  flags, JSON error output, report schemas, trust-boundary text, and exit-code
  behavior. The procedural-style smoke recorded behaviorRichClassCount: 3 for
  the new command-object slice.

## Description

Refactor report builders behind behavior-rich report objects one output
contract at a time, starting with low-risk governance or accepted candidate
reports and preserving report schemas, issue codes, and markdown output.

This is the next Phase 17 EO refactoring slice after the CLI shell/domain
command split. Keep the scope narrow and add characterization tests before
moving mature report-building behavior.

## Next Step

Run the PLAN command to generate the implementation-ready PRD.
