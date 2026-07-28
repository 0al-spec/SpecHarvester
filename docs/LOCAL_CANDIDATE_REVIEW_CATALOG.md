# Local Candidate Review Catalog

P54-T3 provides a deterministic catalog generator for the P53-T14 portable
handoff archive:

```bash
spec-harvester local-candidate-review-catalog \
  SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz \
  --expected-sha256 db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63 \
  --output review-workspace/catalog.json
```

The generator verifies the compressed archive digest, bounded archive and
expanded payload sizes, member count and types, safe relative paths, packet
identity, candidate and portable AI file digests, and aggregate preflight
metadata. It reads tar members without extracting them to the filesystem.

Catalog items are sorted by the frozen repository position and bind directly to
the SHA-256 of the exact `packet.json` bytes. They expose review readiness,
warning count, correction history, ecosystem, package shape, and producer
preflight status under the P54-T2 schema.

The retained 100-candidate corpus produces 100 ready-for-author-review items,
100 passed producer preflights, and two correction-history flags. Generation
does not execute candidate content or mutate review, SpecPM, or registry state.
