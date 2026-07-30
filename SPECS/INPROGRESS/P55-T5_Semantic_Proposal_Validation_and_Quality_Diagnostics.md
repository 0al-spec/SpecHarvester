# P55-T5 Semantic Proposal Validation and Quality Diagnostics

## Objective

Add a deterministic, provider-neutral quality gate for P55-T4 semantic
proposals and freeze the numerical policy that P55-T9 and P55-T10 must evaluate
without redefining it.

## Dependencies

- P55-T1 semantic-author product and authority contract.
- P55-T2 semantic-author schemas and cross-record invariants.
- P55-T3 bounded semantic-author input packs.
- P55-T4 provider-neutral semantic-author pass.

## Deliverables

- A deterministic semantic proposal quality evaluator producing hard errors,
  review warnings, stable metrics, and a proposal-only eligibility verdict.
- Revalidation of P55-T2 schema, candidate/source/proposal digests, exact
  evidence bindings, and experimental intent state.
- Candidate YAML checks for package capability namespace ownership and exact
  `specpm.yaml` versus BoundarySpec capability/intent consistency.
- Claim checks for provider-specific authoring language and unsupported
  quantitative statements.
- Generic intent, duplicate intent, experimental/observed overlap, and
  near-duplicate claim warnings.
- A versioned, digest-bound frozen threshold policy covering purpose accuracy,
  evidence support, schema validity, and reviewer edit burden.
- Valid, rejected, warning, stale-policy, and malformed-input tests plus GitHub
  Markdown and DocC documentation.

## Diagnostic Semantics

Hard errors make a proposal ineligible for P55-T9 calibration or later
materialization. They include schema or identifier failure, candidate/source
digest drift, unknown evidence, capability namespace violations,
manifest/BoundarySpec inconsistency, non-experimental novel intent IDs,
provider-specific authority wording, and quantitative claims whose numeric
facts do not occur in their cited evidence.

Warnings require reviewer attention but do not silently reject an otherwise
valid proposal. They include generic intents, duplicate or overlapping intent
decisions, and lexically near-duplicate claims. Diagnostics are sorted and
deterministic; provider identity cannot change severity or thresholds.

## Frozen Threshold Policy

The policy is canonical JSON with a SHA-256 calculated over the policy record
excluding its own digest field. It freezes these P55-T9/P55-T10 pass gates:

- purpose accuracy rate: at least `0.85`;
- evidence-supported claim rate: at least `0.95`;
- schema-valid proposal rate: exactly `1.0`;
- reviewer edit burden rate: at most `0.25`.

Calibration artifacts may reference and evaluate this digest but cannot change
the values. Any threshold change requires a separate reviewed policy revision.

## Acceptance Criteria

- Repeated evaluation of the same pack, proposal, and policy is byte-identical.
- Every required hard error and warning category has a focused regression test.
- Clean, warning, and rejected verdicts are distinguishable and remain
  proposal-only.
- The frozen policy digest is verified before evaluation and appears in every
  report.
- Full tests pass with at least 90% total coverage; Ruff, formatting, diff, Swift
  manifest, and DocC checks pass.

## Non-Goals

- Provider invocation, model comparison, or live calibration.
- Reviewer decisions, candidate materialization, SpecPM mutation, canonical
  intent creation, registry acceptance, or publication.
