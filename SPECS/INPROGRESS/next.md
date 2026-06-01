# Next Task: P21-T2 — Producer Receipt Emission

**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Effort:** 4-8 hours
**Dependencies:** P21-T1
**Status:** Queued
**Suggested:** 2026-06-02

## Description

Emit `producer-receipt.json` for generated candidate bundles using the SpecPM
`generated_spec_package_v0` profile. The receipt should record producer
identity/version, subject package metadata, input evidence references,
configuration summary or digest, generated output roles, output SHA-256
digests, validation status, diagnostics status, privacy state, audit evidence,
and `humanReview` status.

## Recently Archived

- P21-T1: Producer Candidate Bundle Output Planning (PASS, 2026-06-02)
- P20-T4: Scoped Source Validation Fixtures (PASS, 2026-06-01)
- P20-T3: CodeGraph Adapter Evaluation (PASS, 2026-05-31)
- P20-T2: Tuist Manifest Parsing (PASS, 2026-05-31)
- P20-T1: Scoped Source Target Harvesting (PASS, 2026-05-31)

## Rationale

P21-T1 aligned SpecHarvester with the merged SpecPM producer receipt contract.
The next step is to generate the machine-readable `producer-receipt.json`
handoff artifact while preserving the self-hash boundary: generated outputs are
hashed in `outputs[]`, but `producer-receipt.json` is not listed there.

## Next Step

Run SELECT for `P21-T2`, identify the candidate bundle emission path, and add a
receipt emitter with tests for required fields, digest calculation, excluded
receipt self-hash, and public handoff `humanReview` defaults.
