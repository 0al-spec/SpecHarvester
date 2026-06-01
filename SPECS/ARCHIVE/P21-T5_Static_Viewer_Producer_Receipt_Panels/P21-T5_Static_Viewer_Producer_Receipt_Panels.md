# P21-T5 — Static Viewer Producer Receipt Panels

**Status:** In Progress
**Priority:** P1
**Phase:** Phase 21. Producer Candidate Bundle Contract
**Date:** 2026-06-02
**Stack Base:** `feature/P21-T4-candidate-bundle-preflight-verifier`

## Problem

Generated candidate bundles now include `producer-receipt.json`,
`validation-report.json`, and `diagnostics.json`, and P21-T4 adds local
preflight verification. The static viewer still focuses on `specpm.yaml` and
BoundarySpec YAML, so reviewers cannot quickly inspect producer provenance,
input evidence, output hashes, validation status, diagnostics, privacy caveats,
or the human review boundary from the rendered site.

## Goals

- Load `producer-receipt.json`, `validation-report.json`, and
  `diagnostics.json` as read-only bundle evidence when present.
- Add renderer payload fields for producer identity, subject, input provenance,
  output hashes, validation summary, diagnostics summary, privacy/security
  caveats, and human review status.
- Add static HTML/JS panels that present this evidence without implying SpecPM
  acceptance or public index publication.
- Preserve local-only renderer behavior: no package code execution, no network
  calls, no mutation of candidate bundles.
- Keep missing or unreadable producer artifacts as renderer diagnostics rather
  than registry acceptance decisions.

## Non-Goals

- Do not implement SpecPM-side enforcement.
- Do not merge, approve, publish, or promote generated candidates.
- Do not run package managers, build systems, harvested scripts, or external
  validators from the viewer.
- Do not make viewer diagnostics authoritative; they remain reviewer ergonomics.

## Deliverables

- Static renderer payload support for producer receipt and producer reports.
- Browser-safe viewer panels for receipt provenance, hashes, validation,
  diagnostics, privacy/security notes, and review boundary.
- Regression tests for payload shape and generated HTML/JS/CSS hooks.
- Validation report with exact quality gate results.

## Acceptance Criteria

- Rendering a candidate with producer artifacts includes a `producer` payload.
- The viewer shows producer identity/version, package subject, review status,
  output digests, validation report status, diagnostics status, privacy notes,
  security notes, and trust-boundary text.
- Missing producer artifacts do not break existing static rendering behavior.
- Viewer language states that generated evidence is review material, not
  automatic SpecPM acceptance.
- Existing tests, lint, format, coverage, Swift manifest, and DocC build pass.
