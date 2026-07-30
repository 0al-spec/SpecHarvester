# Semantic Proposal Validation and Quality Diagnostics

P55-T5 deterministically revalidates a P55-T4 semantic proposal against its
P55-T3 input pack, candidate YAML, exact evidence bindings, observed intents,
and a frozen calibration policy.

Hard errors reject malformed schemas or identifiers, stale bindings, unknown
evidence, capability namespace and manifest/BoundarySpec inconsistency,
provider-specific authority wording, and unsupported quantitative claims.
Generic, duplicate, and overlap signals remain explicit review warnings.

The digest-bound P55-T9 policy freezes purpose accuracy at `>= 0.85`, evidence
support at `>= 0.95`, schema validity at `= 1.0`, and reviewer edit burden at
`<= 0.25`. Calibration cannot redefine these values.

The evaluator does not invoke providers, materialize candidates, make reviewer
decisions, mutate SpecPM or registry truth, canonicalize intents, or publish.
