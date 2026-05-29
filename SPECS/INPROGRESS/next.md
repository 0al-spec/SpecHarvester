# Next Task: P18-T1 — Swift Public API Analyzer

**Status:** Selected
**Suggested:** 2026-05-29

## Task

Add a deterministic Swift public API analyzer that scans `.swift` sources for
`public` and `open` declarations, emits `PublicInterfaceIndex` evidence, and
plugs into project-profile analyzer orchestration without executing SwiftPM,
build tools, package scripts, or repository code.

## Rationale

SpecHarvester already has the shared public-interface schema, analyzer options,
orchestration registry, and drafter ingestion path, but Swift repositories only
contribute manifest and semantic evidence. Swift/SPM candidates need the same
deterministic public API signal currently available for Python, JavaScript,
TypeScript, and Go.

## Next Step

Create the P18-T1 task PRD, then implement the Swift analyzer and regression
coverage.
