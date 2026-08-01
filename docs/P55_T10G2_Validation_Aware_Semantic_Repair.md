# P55-T10G2 Validation-Aware Semantic Repair

P55-T10G2 extends bounded JSON repair with machine-readable semantic failure
guidance. The original system prompt, complete provider request, evidence roles,
policy context, and bounded invalid assistant output remain unchanged from
P55-T10D.

## Semantic Violation Contract

`ModelJsonSemanticViolation` carries:

- a stable lower-case violation `code`;
- bounded `prohibitedValues` that must not be repeated;
- provider-neutral `replacementConstraints` describing the permitted correction.

The repair message includes this record as `semanticViolation` alongside the
existing human-readable `validationError`. It contains no hidden reasoning,
credentials, raw durable prompt record, or machine-local path.

## Covered Violations

- `specific_purpose_generic_only_contradiction` instructs repair to remove
  generic-only reuse and permits at most one collision-bound experimental intent.
- `experimental_intent_identifier_not_collision_bound` supplies the required
  namespace, semantic-word count, and source-bundle suffix.
- `experimental_intent_identifier_leaks_candidate_namespace` prohibits candidate
  identity tokens in package-neutral experimental intent IDs.
- `purpose_restates_package_mechanics` prohibits mechanics-only purpose wording
  and supplies source-bound outcome terms.
- `purpose_outcome_anchor_missing` requires purpose overlap with a source-bound
  outcome anchor.

## Convergence and Budgets

If the repaired output repeats the same semantic violation code, repair returns
`unchanged_semantic_violation` immediately. It does not consume another repair,
even if a caller configured a larger generic repair limit.

The retained semantic campaign still uses two provider attempts and one repair
per provider attempt. P55-T5 thresholds and all proposal-only authority
boundaries remain unchanged.
