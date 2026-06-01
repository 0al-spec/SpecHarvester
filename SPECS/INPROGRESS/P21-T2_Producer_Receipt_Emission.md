# P21-T2 — Producer Receipt Emission

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02

## Problem

SpecHarvester can draft candidate package files, but generated candidate
bundles do not yet include `producer-receipt.json`. That means reviewers cannot
machine-check which generator, inputs, configuration, output files, validation
state, diagnostics state, privacy state, and human review boundary produced a
candidate.

P21-T1 documented the expected SpecPM handoff shape. P21-T2 must implement the
first runtime artifact while preserving the self-hash boundary:
`producer-receipt.json` must not appear in receipt `outputs[]`.

## Goals

- Emit `producer-receipt.json` during candidate draft generation.
- Use the SpecPM `generated_spec_package_v0` receipt profile:
  `apiVersion: specpm.receipts/v0`, `kind: SpecPMProducerReceipt`,
  `schemaVersion: 1`.
- Record subject package ID, version, API version, package root, and boundary
  spec paths.
- Record SpecHarvester producer identity and version.
- Record input evidence references for `harvest.json`, optional
  `public-interface-index.json`, and generation configuration.
- Record generated output roles and SHA-256 digests for `specpm.yaml`,
  `specs/*.spec.yaml`, and other generated evidence files when present.
- Exclude `producer-receipt.json` from `outputs[]`.
- Record validation and diagnostics status placeholders compatible with P21-T3.
- Default public handoff `humanReview` to required for
  `public_index_acceptance`.
- Add regression tests for required fields, digests, deterministic ordering, and
  excluded receipt self-hash.

## Non-Goals

- Do not emit `validation-report.json` or `diagnostics.json`; that remains
  P21-T3.
- Do not implement candidate bundle preflight verification; that remains
  P21-T4.
- Do not extend the static viewer; that remains P21-T5.
- Do not change SpecPM or accepted package publication behavior.
- Do not embed raw source bodies, private prompts, secrets, credentials, or
  local-only private paths in the receipt.

## Deliverables

- A producer receipt emission module or object following the local Elegant
  Objects style guidance.
- Draft command integration that writes `producer-receipt.json` into candidate
  output directories.
- Tests covering receipt shape, output digests, input references, review
  defaults, and self-hash exclusion.
- Validation report with exact quality gate results.

## Acceptance Criteria

- Drafted candidates contain `producer-receipt.json`.
- The receipt uses `apiVersion: specpm.receipts/v0`,
  `kind: SpecPMProducerReceipt`, and
  `receiptProfile: generated_spec_package_v0`.
- `outputs[]` includes SHA-256 digests for generated candidate files and does
  not include `producer-receipt.json`.
- `humanReview.status` defaults to `required` and
  `humanReview.requiredFor` includes `public_index_acceptance`.
- `privacy.secretsIncluded` is `false`.
- Receipt output is deterministic for the same generated candidate inputs,
  except for explicitly time-based fields if they are included.
- Existing tests, lint, format, coverage, Swift manifest, and DocC build pass.
