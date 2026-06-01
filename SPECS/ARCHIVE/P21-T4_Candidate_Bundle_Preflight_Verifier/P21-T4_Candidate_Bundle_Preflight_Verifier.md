# P21-T4 — Candidate Bundle Preflight Verifier

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02

## Problem

SpecHarvester now emits `producer-receipt.json`, `validation-report.json`, and
`diagnostics.json`, but there is no deterministic local verifier that checks the
candidate bundle before handoff. A malformed receipt, missing report, digest
drift, self-hash violation, or invalid review status can still reach proposal
automation unless reviewers catch it manually.

## Goals

- Add a local candidate bundle preflight verifier.
- Check required files: `specpm.yaml`, `specs/*.spec.yaml`,
  `producer-receipt.json`, `validation-report.json`, and `diagnostics.json`.
- Validate receipt API family, kind, schema version, and profile.
- Verify every `outputs[]` digest against generated bundle bytes.
- Reject `producer-receipt.json` in `outputs[]`.
- Verify `validation.reportDigest` and `diagnostics.digest`.
- Verify `humanReview.status` is valid and public handoff remains review-gated.
- Verify bundle-local receipt inputs exist and match their digest.
- Verify receipt subject metadata is aligned with `specpm.yaml` and referenced
  BoundarySpec paths.
- Expose a CLI command that prints a machine-readable preflight report.

## Non-Goals

- Do not make SpecPM accept or reject packages automatically.
- Do not run package code, package scripts, build tools, or network calls.
- Do not implement registry publishing or maintainer override workflows.
- Do not extend the static viewer; that remains P21-T5.

## Deliverables

- Preflight verifier module.
- CLI command for local preflight.
- Regression tests for valid bundles, missing files, digest mismatch,
  self-hash violation, invalid review status, malformed receipt profile, and
  missing bundle-local input evidence.
- Validation report with exact quality gate results.

## Acceptance Criteria

- Valid drafted candidate bundles pass preflight with status `passed`.
- Invalid bundles fail with stable diagnostic codes.
- The verifier returns non-zero through CLI when status is not `passed`.
- The verifier records no automatic acceptance authority.
- Existing tests, lint, format, coverage, Swift manifest, and DocC build pass.
