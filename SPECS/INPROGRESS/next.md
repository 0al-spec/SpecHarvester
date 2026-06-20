# Next Task: P45-T2 AI Draft Proposal Validation Guard

**Status:** Selected
**Branch:** `feature/P45-T2-ai-draft-proposal-validation-guard`
**Phase:** Phase 45. Operational MVP AI Draft Shape Hardening
**Task:** `P45-T2`
**Depends On:** `P45-T1` AI Draft Proposal Subject Identity Fix

## Goal

Add a deterministic AI draft proposal validation guard that reports missing
package-set subject identity and unknown excluded-package references before
provider output is accepted as proposal evidence.

## Context

P45-T1 normalized safe AI draft subject identity cases: missing
`packageSet.packageId` now uses deterministic request identity, and
single-package unknown exclusions can be ignored as model-side noise. P45-T2
should make the remaining validation boundary explicit and deterministic so
truly ambiguous provider output still surfaces before later P45 reruns.

## Expected Deliverables

- A deterministic validation guard for AI draft proposal subject identity.
- Regression coverage for invalid or ambiguous provider output.
- Documentation or fixture updates needed to preserve the Phase 45 warning
  lineage.

## Boundaries

- Do not broaden the corpus.
- Do not rerun the bounded operational MVP corpus; that belongs to `P45-T3`.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not treat AI output as registry truth.
- Do not add new Workplan tasks.

## Recently Archived

- `P45-T1` AI Draft Proposal Subject Identity Fix: PASS on 2026-06-20.

## Validation Expectations

- Run focused tests for the AI draft proposal validation guard.
- Run docs-contract tests if documentation or fixtures change.
- Run formatting/lint/test gates scaled to the implementation surface.
