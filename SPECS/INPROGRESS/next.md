# Next Task: P17-T2 CLI Domain Command Objects

**Priority:** P1
**Phase:** Phase 17. Elegant Objects Refactoring Strategy
**Effort:** Medium
**Dependencies:** P17-T1
**Status:** Selected
**Stack Base:** codex/p33-t8-next-corpus-intake-readiness-decision

## Description

Split the CLI execution shell from domain command behavior by introducing
small command objects for selected `code-duplication-report`,
`architecture-lint`, and `procedural-style-report` flows while preserving
parser flags, JSON error output, report schemas, and exit-code behavior.

This task is a narrow EO refactoring slice. It must not change report payloads,
public CLI names, option names, defaults, trust-boundary text, or failure
semantics.

## Next Step

Run the PLAN command to generate the implementation-ready PRD.
