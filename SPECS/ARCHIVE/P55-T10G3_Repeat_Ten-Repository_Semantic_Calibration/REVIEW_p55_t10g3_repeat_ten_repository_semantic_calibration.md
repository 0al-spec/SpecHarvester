# Review: P55-T10G3 Repeat Ten-Repository Semantic Calibration

## Verdict

PARTIAL

## Findings

### P0: Generated preview descriptions can satisfy outcome anchors

Firecrawl, Angular, and Electron passed deterministic quality while the unchanged
supervisor rubric rejected their purposes. Their generated static package
descriptions contain phrases such as `generated preview`, `member package
boundary`, and import/module mechanics. P55-T10G1 currently treats those phrases
as outcome anchors at the same authority as pinned source documentation, so a
provider can exactly match a weak anchor and avoid `purpose_outcome_anchor_missing`.

Required follow-up: rank anchor provenance, classify generated candidate wording
as mechanics-only guidance, and require a source-document or descriptive-manifest
outcome when stronger evidence exists.

### P1: Capability namespace failure is outside typed semantic repair

Bitcoin now produces an accurate purpose and a terminal record, but independent
quality rejects it for `capability_namespace_violation` while it retains generic
repository-metadata intent reuse. P55-T10G2 covers experimental-intent namespace,
not capability identifier namespace, so the provider does not receive the exact
candidate prefix and prohibited identifier as typed replacement constraints.

Required follow-up: add validation-aware capability namespace repair without
changing the one-repair-per-attempt budget.

## Positive Evidence

- Completion improved from 8/10 to 10/10 and terminal failures fell to zero.
- Evidence support and schema-valid rates improved from 0.80 to 1.00.
- Generic reuse remains reduced from baseline seven to one.
- Excalidraw's previous namespace failure was repaired successfully.
- False novelty and duplicate experimental IDs or stems remain zero.

## Frozen Decision

Purpose accuracy 0.70 and reviewer edit burden 0.40 fail unchanged gates of 0.85
and 0.25. P55-T10H remains blocked. Thresholds and denominators must not change.

## Validation Evidence

- Python: 1411 passed, 1 skipped.
- Coverage: 90.01 percent.
- Ruff lint and format: PASS.
- Swift manifest and DocC target build: PASS.
- JSON, archive, privacy, boundary, and diff checks: PASS.

## Follow-Up

Create P55-T10G4 for anchor source-authority ranking, P55-T10G5 for typed
capability namespace repair, and P55-T10G6 for one exact frozen rerun. P55-T10H
may proceed only if G6 passes every unchanged gate.
