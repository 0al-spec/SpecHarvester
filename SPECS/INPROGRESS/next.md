# Next Task: P16-T8 — Evaluate Multi-Language Duplicate-Code Detector

**Priority:** P1
**Phase:** Phase 16. Real Repository Signal Quality Hardening
**Effort:** 4-8 hours
**Dependencies:** P16-T6, P16-T7, P16-T18
**Status:** Suggested
**Suggested:** 2026-05-28

## Description

Evaluate and integrate a multi-language duplicate-code detector backend such as
`jscpd` behind `SpecHarvesterCodeDuplicationReport`, including licensing,
deterministic JSON output, npm supply-chain, and CI ergonomics review before
enabling it as an advisory baseline.

## Recently Archived

- P16-T5: Rerun Representative Local Validation Matrix (PASS, 2026-05-28)
- P16-T4: Reduce Broad Duplicate Semantic Intent Claims (PASS, 2026-05-28)
- P16-T18: Duplicate-Code Practical-Minimum Audit (PASS, 2026-05-26)

## Rationale

P16-T5 confirmed that signal-quality advisory noise dropped from 12 total
issues in the P15-T4 baseline to 5 total issues after P16-T1 through P16-T4.
The remaining unchecked Phase 16 task is the multi-language duplicate-code
detector evaluation, which complements the existing builtin and pylint
duplicate-code backends.

## Next Step

Run SELECT for `P16-T8`, then evaluate the detector candidate licensing,
deterministic output shape, local-only execution behavior, and integration
boundary before enabling any advisory baseline.
