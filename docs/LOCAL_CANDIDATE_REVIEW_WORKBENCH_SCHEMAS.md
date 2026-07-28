# Local Candidate Review Workbench Schemas

P54-T2 defines JSON Schema 2020-12 records for the local review catalog,
candidate detail, static-versus-AI comparison, reviewer decision, reason
taxonomy, and portable export bundle.

The schema is `schemas/local-candidate-review-workbench-v0.schema.json`.
Candidate-bearing records bind a safe candidate identity to a 64-hex P53-T14
packet SHA-256. Decision records require disposition, reviewer, RFC 3339
timestamp, reason code, and nullable prior-decision digest.

Catalog records expose deterministic readiness, warning, correction, ecosystem,
package-shape, and preflight facets without changing candidate evidence.

Security-sensitive records reject unknown fields. Detail content is typed only
as inert text, JSON, or YAML. Export authority is fixed to
`portable_local_review_evidence_only` and registry mutation count is fixed to
zero.

The schema file accepts each versioned record as a standalone document as well
as the all-record fixture envelope. Consumers that combine a decision with a
reason taxonomy must also run `validate_decision_reason_compatibility`; JSON
Schema validates each record shape, while that semantic check enforces that the
reason exists and permits the selected disposition.

Breaking changes require a new API version. Additive changes are permitted only
where the current schema explicitly allows them; consumers must not silently
reinterpret unknown authority or decision fields.
