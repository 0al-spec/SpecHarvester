# P53-T4 Mass Corpus Checkout Readiness Gate

**Status:** Planned
**Phase:** Phase 53. Mass Popular Repository Parsing and Candidate Production
**Task:** `P53-T4`
**Depends On:** `P53-T3` Mass Corpus Source Manifest

## Objective

Implement and run a fail-closed gate over the immutable P53 100-source corpus.
The gate must prove that every operator-provided checkout exists, is a clean Git
repository at its manifest revision, has a matching canonical origin, remains
within its declared size ceiling, and contains static license-file evidence.
Only a fully ready corpus can unlock P53-T5 static collection.

## Acceptance Criteria

- A P53-specific report schema records all 100 per-source outcomes, exact wave
  distribution, readiness totals, policy failures, and the `p53T5Unlocked`
  decision.
- The gate rejects missing checkout, remote-origin mismatch, revision mismatch,
  dirty worktree, unavailable tracked-size data, exceeded size, and unavailable
  license evidence without substituting or acquiring any source.
- A synthetic 100-checkout test demonstrates a passing result; focused tests
  demonstrate each blocking class and a live local run reports the actual
  machine state.
- The CLI exposes the gate with explicit inputs and output path. Documents make
  P53-T5 conditional on a passing report.

## Test-First Plan

1. Add failing tests for a complete 100-source passing corpus and for missing
   checkout, origin drift, position/wave drift, and license evidence failure.
2. Implement the narrow P53 reader and validator, reusing existing static Git
   and tracked-file helpers where their semantics match.
3. Run the gate against `inputs/p53-mass-corpus/` without creating sources, then
   record the sanitized outcome and all configured quality-gate results.

## Implementation Plan

1. Define the P53 report contract and validate manifest/metadata alignment,
   source ordering, exact 100-source requirement, and wave mapping.
2. Inspect only local checkout metadata and allowlisted static license filenames;
   aggregate every failure instead of stopping at the first source.
3. Add CLI and operator documentation, execute focused/full tests and quality
   gates, and retain the live diagnostic outside version control.

## Constraints And Non-Goals

- Do not create, restore, clone, fetch, or modify repositories. Checkouts are
  operator-provided and missing sources block the gate.
- Do not run static harvesting, Codex, LM Studio, adapters, package managers,
  or harvested code; do not persist raw prompts, responses, secrets, session
  state, stdout/stderr, or chain-of-thought.
- Do not accept packages or relations, publish registry metadata, remove
  `preview_only`, or treat readiness evidence as registry truth.
