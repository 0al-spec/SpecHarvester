## REVIEW REPORT - P55-T2 AI Semantic-Author Schemas

**Scope:** `origin/main..HEAD`
**Files:** 18
**Date:** 2026-07-29

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None.

### Secondary Issues

None.

### Architectural Notes

- The JSON Schema 2020-12 bundle is versioned, package-included, and accepts
  both standalone P55 records and a complete fixture envelope.
- Request, proposal, observed-intent reuse, experimental intent, nearby-intent
  analysis, reviewer edit, and materialization-decision records have closed
  fields and explicit identities.
- Claim evidence is constrained to P55-T1 allowlisted evidence classes and
  safe repository-relative paths. It cannot contain an absolute or traversal
  path.
- Deterministic validation complements JSON Schema with candidate identity,
  source-bundle, proposal, reviewer-edit, nearby-analysis, and claim-reference
  consistency checks. Duplicate experimental intent IDs are rejected.
- Experimental intents are constrained to `intent.experimental.*`; materialized
  evidence remains `previewOnly: true` and `isRegistryTruth: false`.
- No provider transport, raw model material, credential, private path,
  acceptance, canonicalization, registry mutation, or publication field exists
  in the schema. P55-T2 invokes no provider or materializer.

### Tests

- Focused semantic-schema and documentation tests: `222 passed`.
- Full Python tests: `1184 passed, 1 skipped`.
- Total Python coverage: `90.04%`.
- Ruff lint and configured format checks passed.
- `git diff --check` passed.
- Swift package manifest and documentation target build passed with the
  existing unhandled DocC directory warning.

### Next Steps

- FOLLOW-UP is skipped because no actionable review findings remain.
- Continue with `P55-T3` Semantic Author Input Pack.
- Preserve allowlisted reads, exact source digests, bounded input sizes, and
  provider non-execution until P55-T4.
