# Next Task: P23-T3 SpecPM CI Preflight Gate Support

**Phase:** Phase 23. SpecPM Intake Boundary Alignment
**Status:** P23-T2 complete; P23-T3 recommended next
**Updated:** 2026-06-04

## Recently Archived

- P22-T1: Candidate Bundle End-to-End Smoke (PASS, 2026-06-02)
- P23-T1: SpecPM proposal evidence links (implemented in current PR)
- P23-T2: Shared cross-repository fixture policy (implemented in current PR)

## Phase 23 Status

SpecHarvester proposal artifacts and the trusted SpecPM proposal workflow now
explicitly include or link producer bundle evidence:

```text
producer-receipt.json
validation-report.json
diagnostics.json
producer preflight evidence
static viewer evidence
accepted-source diff
```

SpecHarvester now also documents the shared fixture policy for keeping SpecPM
contract examples and SpecHarvester generated bundle examples aligned by exact
commit SHA instead of mutable refs.

## Next Step

Add SpecHarvester-side support for any future optional SpecPM CI preflight gate
without making producer evidence registry authority.
