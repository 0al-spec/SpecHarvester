# P54-T3 Deterministic Local Candidate Review Catalog

## Objective

Implement a deterministic, bounded catalog generator for validated P53-T14
portable handoff archives.

## Dependencies

- P54-T1 Workbench product and threat-model contract.
- P54-T2 candidate review schema bundle.
- Retained P53-T14 100-candidate portable handoff archive and digest.

## Deliverables

- Reusable Python catalog generator and CLI command.
- Safe tar reader with archive digest, entry type, path, size, count, and total
  payload checks.
- Packet validation and deterministic catalog ordering.
- Readiness, warning, correction, ecosystem, package-shape, and preflight
  facets that conform to the P54-T2 catalog schema.
- Unit/adversarial tests, documentation, and a catalog generated from the
  retained 100-candidate archive.

## Acceptance

- The generator reads archive members without extracting them to disk.
- Absolute paths, traversal, links, special files, duplicate packet identities,
  malformed JSON, digest drift, and resource-limit violations fail closed.
- Every item is bound to the SHA-256 of its exact `packet.json` bytes.
- Repeated runs over identical bytes produce byte-identical catalog output.
- The retained corpus produces exactly 100 schema-valid catalog items.
- No candidate content executes and no review, SpecPM, or registry state changes.
