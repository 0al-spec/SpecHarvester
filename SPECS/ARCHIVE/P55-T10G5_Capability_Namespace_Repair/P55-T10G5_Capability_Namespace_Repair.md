# P55-T10G5 Capability Namespace Repair

## Objective

Make the existing validation-aware semantic JSON repair actionable when a
provider returns a capability ID outside the candidate namespace. The repair
message must carry the exact namespace, the rejected identifier, and a bounded
replacement shape so Codex 5.3 Spark and compatible providers can correct the
same deterministic failure without broader authoring changes.

## Deliverables

- A proposal-only `capabilityNamespaceRepairs` record carrying each rejected
  static capability ID and its candidate-scoped proposed replacement.
- A stable `ModelJsonSemanticViolation` for missing or invalid capability
  namespace repairs in semantic proposal transport validation.
- Repair guidance containing the candidate namespace, exact prohibited
  capability ID, and a replacement-ID shape that remains scoped to the
  candidate.
- Deterministic rejection when the repair repeats that same violation, using
  the existing two provider responses and one repair attempt only.
- Targeted Codex and LM Studio transport tests, user-facing task documentation,
  validation evidence, archive, and review artifacts.

## Acceptance Criteria

- A malformed capability ID outside `<candidateId>.` creates repair guidance
  with code, prohibited value, required namespace, and replacement shape.
- A repaired replacement capability ID under the exact candidate namespace
  succeeds without changing source evidence, static candidate YAML, original
  system prompt, initial provider request, or proposal-only authority.
- Repeating the same invalid capability ID returns the existing
  unchanged-semantic-violation failure after one repair attempt; no third
  provider request is made.
- Existing generic-intent, experimental-intent, purpose, schema, evidence,
  provider-attempt, repair-budget, privacy, materialization, SpecPM, registry,
  and publication boundaries remain unchanged.
- Full configured Python, lint, formatting, coverage, Swift manifest, and
  Swift documentation gates pass with coverage at least 90%.

## Test-First Plan

1. Add provider-transport regressions for a malformed capability ID followed
   by a valid repair, asserting the preserved message roles/request and exact
   semantic violation guidance.
2. Add repeated-violation coverage that counts provider calls and asserts the
   current single-repair budget terminates deterministically.
3. Implement one shared validator for candidate-YAML namespace evidence,
   proposed repair records, transport enforcement, and review-required quality
   diagnostics; leave generic JSON repair provider-neutral.
4. Run focused semantic repair and quality suites, then all configured gates;
   record only aggregate validation outcomes.

## Non-Goals

- Running a live provider or P55-T10G6 calibration.
- Altering frozen quality thresholds, target corpus, provider-attempt count, or
  repair budget.
- Accepting, materializing, canonicalizing, publishing, or mutating SpecPM or
  registry truth.

## Notes

- Update `docs/` with the capability-namespace repair contract once the
  implementation and tests stabilize.
- The follow-up P55-T10G6 calibration remains a separate task and consumes no
  evidence from this implementation run.

---
**Archived:** 2026-08-02
**Verdict:** PASS
