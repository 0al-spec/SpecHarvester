# Next Task: P22-T1 Candidate Bundle End-to-End Smoke

**Phase:** Phase 22. Producer Bundle End-to-End Smoke
**Status:** Planned
**Updated:** 2026-06-02

## Motivation

Phase 21 added the producer receipt, validation report, diagnostics report,
preflight verifier, static viewer panels, and SpecPM handoff docs as separate
steps. The next gap is confidence that those pieces stay wired together through
one real local producer path.

## Goal

Add an end-to-end smoke that runs:

```text
local fixture repository -> collect -> draft -> preflight -> render
```

The smoke should assert that the generated candidate bundle passes producer
preflight and that the rendered static viewer payload exposes the same producer
identity, package identity, output hashes, diagnostics status, and human-review
boundary recorded in the bundle artifacts.

## Boundaries

- Do not add SpecPM registry acceptance policy in this task.
- Do not execute harvested repository code, install dependencies, or use
  network access.
- Do not commit generated candidate output; keep the smoke fixture and outputs
  test-local.

## Success Criteria

- The new smoke fails if receipt/report/viewer wiring drifts.
- Existing tests, lint, format, Swift manifest, and DocC build stay green.
