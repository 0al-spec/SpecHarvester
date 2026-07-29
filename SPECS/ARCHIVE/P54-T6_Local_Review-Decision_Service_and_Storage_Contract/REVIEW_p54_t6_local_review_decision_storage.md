## REVIEW REPORT - P54-T6 Local Review Decision Storage

**Scope:** `origin/main..HEAD`

### Summary Verdict

- [x] Approve

### Critical Issues

None.

### Secondary Issues

- [Medium, resolved] Restart validation initially accepted a valid current
  decision after its immutable history copy had been removed. `current()` now
  requires the digest-addressed history record and verifies byte equality.

### Architectural Notes

- Client input cannot select a filesystem path. Candidate IDs and packet digests
  must match the schema-valid catalog before persistence.
- History is written before atomically publishing current state, so an
  interrupted first phase can be retried without losing predecessor evidence.
- Replacements use optimistic concurrency through the exact canonical current
  SHA-256; stale or silent overwrite is rejected.
- The HTTP surface binds only to loopback and gates writes with exact Origin,
  bounded body size, content type, and constant-time CSRF comparison.
- Decisions retain evidence-only authority and cannot invoke SpecPM, registry,
  package managers, models, or harvested code.

### Tests

- Focused decision service and docs-contract checks pass.
- Full suite, coverage threshold, Ruff, Swift manifest, and DocC target passed
  during EXECUTE.

### Next Steps

FOLLOW-UP skipped: the only review finding was fixed and covered in this task.
P54-T7 may build reviewer actions and portable exchange on this storage API.
