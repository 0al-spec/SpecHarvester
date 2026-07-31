# P55-T10A Experimental-Intent Decision Policy

## Objective

Define and implement a deterministic, evidence-grounded decision policy that
lets a semantic author distinguish justified observed-intent reuse from one
bounded experimental-intent proposal when generic observed metadata does not
express the documented user outcome.

## Dependencies

- P55-T2 semantic author schemas and experimental-intent records.
- P55-T4 provider-neutral semantic author pass.
- P55-T5 frozen semantic proposal quality policy and diagnostics.
- P55-T9A provider output conformance controls.
- P55-T10 retained-corpus baseline, including 48 generic-intent reuse cases and
  zero experimental-intent proposals.

## Deliverables

- A versioned, digest-bound experimental-intent decision policy that records:
  - the generic observed intents that require an explicit sufficiency decision;
  - required nearby-intent comparison, evidence, user need, and non-goals;
  - bounded identifier rules for visibly experimental, package-neutral IDs;
  - explicit reuse and novelty decision criteria;
  - unchanged proposal-only and non-canonical authority.
- Provider-neutral request integration for Codex 5.3 Spark and LM Studio.
- Fail-closed transport validation for policy binding, observed-intent
  comparison, experimental identifier shape, claim references, and evidence.
- Deterministic quality diagnostics that expose unjustified generic reuse,
  missing nearby comparison, malformed experimental identifiers, and false
  novelty without changing the frozen P55 quality thresholds.
- Unit tests, fixtures, operator documentation, and validation evidence.

## Execution Plan

1. Define a static decision policy and canonical SHA-256 representation.
2. Bind that policy into every provider request and explain the exact
   reuse-versus-experimental decision in the shared system prompt.
3. Validate decisions before a provider result enters the semantic pass.
4. Emit deterministic review diagnostics from the quality layer.
5. Verify reuse, justified novelty, false novelty, stale policy, provider
   neutrality, and authority boundaries with focused and full quality gates.

## Acceptance Criteria

- A generic observed intent cannot be silently reused: the proposal must cite
  an evidence-grounded rationale that explicitly compares semantic sufficiency.
- One proposal may contain at most one experimental intent. It must use a
  visibly non-canonical `intent.experimental.*` identifier with a bounded
  collision-resistant suffix, a purpose/user-need claim, at least one nearby
  observed intent, and at least one non-goal claim.
- Experimental nearby intent IDs must come from the request's observed intent
  set and must be represented by nearby-intent-difference claims.
- Existing observed intents remain reusable when evidence shows they express
  the user outcome; novelty is never required merely because a generic intent
  is present.
- False novelty, synonyms, package/vendor namespace leakage, stale policy
  bindings, and malformed identifiers fail validation or produce explicit
  deterministic diagnostics.
- The P55-T5 quality policy digest and numerical gates remain unchanged.
- No result receives acceptance, materialization, canonicalization, registry,
  or publication authority.
- Python tests pass with at least 90% coverage; Ruff lint and format, diff
  integrity, Swift manifest, and Swift documentation checks are recorded.

## Non-Goals

- Running the targeted repository calibration; that is P55-T10B.
- Reprocessing the 48 retained generic-intent cases; that is P55-T10C.
- Adding an intent to SpecPM canonical taxonomy or publishing any candidate.
- Automatically accepting, editing, materializing, or promoting a proposal.
- Changing the frozen P55 quality thresholds to make calibration pass.
