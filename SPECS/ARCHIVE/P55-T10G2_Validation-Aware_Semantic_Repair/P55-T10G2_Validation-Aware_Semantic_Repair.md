# P55-T10G2 Validation-Aware Semantic Repair

## Objective

Make JSON repair understand deterministic semantic violations instead of
receiving only an unstructured error string.

## Deliverables

- A provider-neutral typed semantic-violation contract with stable code,
  prohibited values, and replacement constraints.
- Repair messages preserving the full original system prompt and request while
  adding bounded structured violation guidance.
- Targeted violations for generic-only intent contradiction, experimental-intent
  namespace/collision binding, and outcome-purpose specificity.
- Deterministic early failure when repaired output repeats the same semantic
  violation.
- Tests, documentation, validation, archive, and structured review evidence.

## Acceptance Criteria

- The original request, evidence, policy, roles, and bounded invalid output remain
  preserved exactly as in P55-T10D.
- Structured violation guidance contains no raw prompt, response, reasoning,
  credentials, or machine-local paths.
- The existing two provider attempts and one repair per attempt remain unchanged.
- Repeating the same semantic violation cannot consume an additional repair.
- Non-semantic parse and schema repair behavior remains backward compatible.
- Frozen P55 thresholds and proposal-only authority remain unchanged.
- Full configured quality gates pass with at least 90 percent coverage.

## Dependencies

- P55-T10D Semantic Repair Context Preservation.
- P55-T10F Generic Contradiction Gate.
- P55-T10G1 Outcome-Level Purpose Anchors.

## Non-Goals

- Running providers or the ten-repository calibration.
- Increasing provider or repair budgets.
- Acceptance, materialization, canonicalization, registry mutation, or publication.
