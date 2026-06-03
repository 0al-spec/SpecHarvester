# Next Task: P23-T2 Shared Cross-Repository Fixture Policy

**Phase:** Phase 23. SpecPM Intake Boundary Alignment
**Status:** P23-T1 complete; P23-T2 recommended next
**Updated:** 2026-06-04

## Recently Archived

- P22-T1: Candidate Bundle End-to-End Smoke (PASS, 2026-06-02)
- P23-T1: SpecPM proposal evidence links (implemented in current PR)

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

## Next Step

Define a shared cross-repository fixture policy so SpecPM contract examples and
SpecHarvester generated bundle examples cannot silently drift.
