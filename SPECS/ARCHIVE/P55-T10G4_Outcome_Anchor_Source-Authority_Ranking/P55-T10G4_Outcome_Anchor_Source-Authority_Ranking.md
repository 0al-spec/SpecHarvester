# P55-T10G4 Outcome Anchor Source-Authority Ranking

## Objective

Prevent generated candidate previews and package-boundary mechanics from
appearing as evidence of a repository's user-facing outcome. Rank the existing
digest-bound evidence so purpose anchors prefer descriptive manifest metadata
and pinned package-local or repository documentation.

## Deliverables

- A versioned, deterministic source-authority classification for outcome-anchor
  phrases.
- Anchor selection that prefers strong descriptive manifest and documentation
  evidence and excludes generated preview, member-package boundary, import,
  discovery, and module mechanics from satisfying outcome specificity.
- Fail-closed diagnostics that require reviewer attention when no strong
  outcome source exists, while retaining any weak source only as mechanics-only
  guidance.
- Validation that preserves candidate, profile, source-bundle, source-content,
  and anchor digest bindings.
- Targeted regression tests, user-facing task documentation, validation,
  archive, and review artifacts.

## Acceptance Criteria

- A pinned descriptive manifest or package-local/repository document outranks
  generated candidate and boundary wording deterministically.
- Weak generated preview, member-package boundary, import, discovery, and
  module phrases cannot make a purpose claim `specific`.
- If only weak generated wording exists, the input pack does not impose an
  unsatisfiable provider constraint and independent quality evaluation produces
  a reviewer-visible outcome rather than granting eligibility.
- Existing untrusted flags, evidence-content checks, digest bindings, bounded
  anchor count, and proposal-only execution boundaries remain intact.
- Existing valid anchor records remain readable or fail closed with a precise
  validation error; no silent authority upgrade is possible.
- Full configured tests, lint, formatting, Swift checks, and at least 90%
  coverage pass.

## Dependencies

- P55-T10G1 Outcome-Level Purpose Anchors.
- P55-T10G2 Validation-Aware Semantic Repair.
- P55-T10G3 ten-repository root-cause evidence.

## Non-Goals

- Running Codex 5.3 Spark, LM Studio, or the P55-T10G6 calibration.
- Altering attempt budgets, frozen quality thresholds, targets, or reviewer
  decision authority.
- Accepting, materializing, canonicalizing, publishing, or mutating SpecPM or
  registry truth.
