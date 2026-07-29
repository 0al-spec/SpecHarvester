# P54-T6 Local Review-Decision Service and Storage Contract

## Objective

Implement a loopback-only local service and durable storage boundary for
schema-valid reviewer decisions without executing candidate content or granting
SpecPM/registry authority.

## Deliverables

- A catalog-bound decision store whose reads and writes remain inside one
  configured review workspace.
- Atomic current-decision writes plus immutable digest-addressed history.
- Optimistic replacement checks using the exact prior decision SHA-256.
- Restart-safe loading and validation of persisted current decisions.
- A bounded loopback HTTP surface with exact Origin and CSRF validation for
  writes.
- CLI integration, focused security/storage tests, and operator documentation.

## Acceptance

- Reject absolute/traversal paths, symlink escapes, malformed schema records,
  unknown candidate IDs, packet digest drift, invalid first/replacement prior
  digests, duplicate history conflicts, oversized requests, non-loopback binds,
  untrusted origins, and missing/incorrect CSRF tokens.
- Write a decision only after complete validation. Publish current and history
  records with same-filesystem atomic replacement and durable file flushes.
- Never silently overwrite a newer decision. A replacement must bind the SHA-256
  of the actual current record.
- A newly constructed store over the same workspace must return the same
  schema-valid current decision and digest.
- Candidate data remains inert evidence. The service does not accept packages,
  run SpecPM, mutate registry truth, or expose public-network authority.

## Dependencies

- P54-T2 Workbench JSON Schema.
- P54-T3 digest-bound candidate catalog.
- P54-T5 candidate detail evidence and browser boundary.

## Non-Goals

- Reviewer action controls, reason taxonomy UX, summaries, and import/export
  belong to P54-T7.
- SpecPM intake preflight belongs to P54-T8.
- Shared multi-user hosting, remote authentication, automatic acceptance, and
  publication remain out of scope.
