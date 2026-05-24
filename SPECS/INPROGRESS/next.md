# Next Task: P16-T1 — Quality Report Public Interface Coverage

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 2-4 hours
**Dependencies:** P15-T4, P15-T5, P15-T6
**Status:** In Progress

## Description

Count generated `public-interface-index.json` artifacts in structured
quality-report analyzer coverage so Python and Go candidates with executed
public API analyzers are not downgraded to `weak` coverage only because the
coverage derivation misses colocated interface-index evidence.

## Recently Archived

- P15-T5: Convert Validation Failures into Follow-Up Workplan Tasks (PASS, 2026-05-24)
- P15-T4: Local Validation Matrix (PASS, 2026-05-24)

## Next Step

Create the P16-T1 plan, then add a focused regression around `quality-report`
coverage derivation from generated public interface index artifacts.
