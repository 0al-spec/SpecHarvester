# P16-T1 Quality Report Public Interface Coverage

Status: Planned
Task: `P16-T1`
Phase: Phase 16. Real Repository Signal Quality Hardening
Priority: P1
Effort: 2-4 hours
Dependencies: `P15-T4`, `P15-T5`, `P15-T6`

## Problem

P15-T4 showed that `flask` and `gin` generated `public-interface-index.json`
artifacts and ran public API analyzers, but `quality-report` still classified
their analyzer coverage as `weak`.  The current coverage derivation reads
`harvest.json` analyzer fields but does not count the colocated
`public-interface-index.json` artifact that the runner emits next to the
candidate.

## Goals

- Count a valid generated `public-interface-index.json` as deterministic
  analyzer evidence in `quality-report`.
- Keep report generation read-only and local-only.
- Preserve existing `harvest.json` analyzer detection behavior.
- Add regression coverage for a candidate with no analyzer fields in
  `harvest.json` but a generated public interface index artifact.

## Non-Goals

- Do not change public interface index generation.
- Do not change candidate drafting.
- Do not rerun the full real-repository matrix in this task.
- Do not change SpecPM evidence contracts.

## Deliverables

1. `quality-report` analyzer coverage logic that inspects candidate-local
   `public-interface-index.json`.
2. Regression tests proving the artifact is counted and reported in
   `analyzersUsed`.
3. Validation report with quality gate results.

## Acceptance Criteria

- A candidate with `harvest.json` and valid `public-interface-index.json` gets
  at least `partial` analyzer coverage.
- A candidate with both `harvest.json` analyzer evidence and
  `public-interface-index.json` can reach `strong` analyzer coverage.
- Missing, empty, or invalid public interface index artifacts do not create
  false analyzer coverage.
- Full Flow quality gates pass.
