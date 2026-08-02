# P55-T10G5 Capability Namespace Repair

P55-T10G5 makes a static capability namespace defect actionable for a semantic
authoring provider without treating the provider as an editor of the candidate
package. The source candidate remains immutable and the provider can only add a
bounded proposal record for a reviewer.

## Repair Contract

When digest-bound `specpm.yaml` or a `*.spec.yaml` member declares a capability
outside the candidate ID namespace, the author request contains one
`capabilityNamespaceRepairRequirements` record for each prohibited ID. Every
record states:

- `candidateNamespace` and `requiredPrefix`;
- `prohibitedCapabilityId`; and
- a bounded `replacementIdPattern`.

The semantic proposal may respond with a matching
`capabilityNamespaceRepairs` record. Each record has the prohibited static ID
and exactly one replacement ID matching that candidate-scoped pattern. The
proposal must cover every violation once, and replacement IDs must be unique.

Transport validation uses the same candidate-YAML evidence as the independent
quality report. A missing, malformed, incomplete, duplicated, or out-of-scope
repair becomes `capability_namespace_violation`. The preserved JSON repair
request includes the stable violation code, exact rejected values, and exact
replacement constraints. If the repaired output returns the same violation,
the existing single-repair budget stops it deterministically; no third provider
request is made.

## Review and Authority

A syntactically valid repair proposal does not fix `specpm.yaml` or a boundary
file. Quality reports it as `capability_namespace_repair_proposed`, sets the
result to `review_required`, and makes it ineligible for calibration. A
reviewer must explicitly decide whether and how to edit the static candidate in
a later, separate materialization workflow.

The feature is provider-neutral. Simulated Codex 5.3 Spark CLI and LM Studio
OpenAI-compatible transports share the same validator, request preservation,
and repair budget. It does not invoke either provider, materialize a proposal,
mutate SpecPM or registry truth, or publish a package.
