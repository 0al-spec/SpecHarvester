# P5-T1 Add Duplicate Intent and Capability Claim Report

Status: Planned
Selected: 2026-05-18
Branch: `feature/P5-T1-add-duplicate-intent-and-capability-claim-report`
Review subject: `p5_t1_duplicate_intent_capability_claim_report`

## Objective

Add an advisory governance report that detects duplicate `intent.*` and
capability claims across generated candidate and accepted package metadata, so
maintainers can review overlap and avoid conflicting declarations before accepted
source promotion.

## Deliverables

- Implement deterministic extraction of package identity and claim sets from
  package metadata (`specpm.yaml`) under accepted and candidate directories.
- Detect duplicate intents and duplicate capabilities, including source provenance
  (`accepted` vs `candidate`) and claimant package IDs.
- Add a CLI command:
  - `governance-report`
  - inputs: `--accepted-root`, `--candidates-root`, optional `--output`
  - output: deterministic JSON report with stable ordering and duplicate sections.
- Add regression tests for parsing and duplicate aggregation.
- Document the report command in operator docs and mirror it in DocC.

## Acceptance Criteria

- Report generation does not execute external commands, network, or analyzers.
- Running report with valid roots writes deterministic duplicate summaries in JSON.
- Duplicate detection includes:
  - exact claim identity match across all scanned sources,
  - source tag on each claimant,
  - claimant package identity and version.
- Empty/invalid roots produce clear errors in CLI/API output.
- New behavior is covered by `pytest` tests.
- Coverage is preserved above 90%.
