# Semantic Proposal Validation and Quality Diagnostics

P55-T5 adds a deterministic quality gate after the provider-neutral P55-T4
semantic-author pass. It does not call a model. It revalidates the proposal,
its P55-T3 input pack, candidate YAML, evidence bindings, and frozen calibration
policy before the proposal can enter P55-T9 calibration.

The report has three states:

- `eligible_for_calibration`: no deterministic findings;
- `review_required`: only generic, duplicate, or overlap warnings;
- `rejected`: one or more hard contract errors.

Hard errors cover malformed identifiers and proposal schema, stale candidate or
source digests, unknown evidence, package capability namespace violations,
`specpm.yaml`/BoundarySpec capability or intent drift, provider-specific
authority wording, and quantitative facts absent from the cited evidence.
Warnings expose generic intent reuse, duplicate intent decisions,
experimental/observed overlap, and near-duplicate claims for reviewer judgment.

## Frozen Calibration Policy

The digest-bound policy fixture freezes the Phase 55 corpus thresholds before
P55-T9:

| Metric | Gate |
| --- | --- |
| Purpose accuracy rate | `>= 0.85` |
| Evidence-supported claim rate | `>= 0.95` |
| Schema-valid proposal rate | `= 1.0` |
| Reviewer edit burden rate | `<= 0.25` |

The policy SHA-256 is calculated over canonical JSON excluding only its own
digest field. Calibration can reference and evaluate this policy, but cannot
rewrite it. A threshold change requires a separate reviewed policy revision.

## Authority Boundary

Quality evaluation emits evidence and diagnostics only. It does not invoke
Codex or LM Studio, execute repository code, install dependencies, make a
reviewer decision, materialize a candidate, mutate SpecPM or registry truth,
canonicalize an intent, or publish output.
