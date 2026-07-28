# P54-T2 Local Candidate Review Workbench Schemas

## Objective

Define JSON Schema 2020-12 contracts for the review catalog, candidate detail,
static-versus-AI comparison, reviewer decision, reason taxonomy, and portable
export bundle.

## Deliverables

- Versioned schema bundle with reusable digest, authority, and identity types.
- Representative valid fixture covering all six records.
- Invalid fixtures for digest, disposition, reason, stale linkage, and authority.
- Runtime schema-validation tests.
- Documentation for compatibility and evolution rules.

## Acceptance

- Every candidate-bearing record binds a P53-T14 packet SHA-256.
- Decisions require reviewer, timestamp, reason code, packet digest, and
  prior-decision linkage.
- Export remains proposal/review evidence and cannot assert registry authority.
- Unknown fields are rejected in security-sensitive records.
- Schema evolution requires a new API version for breaking changes.
