# P21-T1 — Producer Candidate Bundle Output Planning

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02

## Problem

SpecPM now documents a Producer Candidate Bundle Contract for generated package
candidates. SpecHarvester already plans P21 implementation tasks, but its local
documentation does not yet pin the bundle layout, receipt profile, digest
expectations, review boundary, or rejection diagnostics that the implementation
must satisfy.

Without this alignment, later code could generate "mostly valid" YAML while
missing provenance, output hashes, diagnostics, privacy caveats, or explicit
human review state.

## Goals

- Document the SpecHarvester-facing candidate bundle output plan.
- Pin the minimum bundle layout: `specpm.yaml`, `specs/*.spec.yaml`,
  `producer-receipt.json`, `validation-report.json`, and `diagnostics.json`.
- Pin the receipt profile and required top-level handoff fields used by the
  SpecPM contract.
- Document output digest expectations, including the rule that
  `producer-receipt.json` is excluded from `outputs[]` to avoid self-hashing.
- Document the review boundary: SpecHarvester generates candidates, SpecPM
  validates shape, maintainers approve acceptance, and public index publishing
  requires approved review or explicit maintainer override.
- Document rejection diagnostics expected from future preflight validation.

## Non-Goals

- Do not emit `producer-receipt.json`; that remains `P21-T2`.
- Do not emit `validation-report.json` or `diagnostics.json`; that remains
  `P21-T3`.
- Do not implement a bundle verifier; that remains `P21-T4`.
- Do not extend the static viewer; that remains `P21-T5`.
- Do not change SpecPM itself.

## Deliverables

- SpecHarvester documentation describing the candidate bundle output plan.
- Documentation contract tests that guard the required layout, receipt profile,
  output digest boundary, review boundary, and rejection diagnostics.
- Validation report with exact quality gate results.

## Acceptance Criteria

- The documentation names the SpecPM Producer Candidate Bundle Contract as the
  upstream handoff target.
- The documentation lists the required bundle files and receipt fields.
- The documentation states that generated outputs are hashed, while
  `producer-receipt.json` is not listed in `outputs[]`.
- The documentation states that producer output is evidence, not acceptance or
  publication authority.
- The documentation identifies expected preflight rejection diagnostics for
  missing files, malformed receipt, digest mismatch, invalid review status,
  evidence gaps, unstable IDs, privacy leaks, and namespace/version overlap.
- Targeted documentation contract tests pass.
