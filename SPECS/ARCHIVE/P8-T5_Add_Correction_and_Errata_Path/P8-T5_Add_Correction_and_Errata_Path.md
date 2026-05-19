# P8-T5 - Add Correction and Errata Path for Accepted Updates

Branch: `feature/P8-T5-correction-and-errata-path`
Review subject: `p8_t5_correction_and_errata_path`

## Problem

The current accepted-package update flow can produce proposals against an already
accepted `package_id@version` that only fixes metadata/canonicalization issues.
Without an explicit correction path, this can resemble an in-place mutation and
lacks a deterministic audit note for why the same version was changed.

## Goals

- Add an explicit correction mode to the proposal command that requires operator
  confirmation.
- Prevent silent same-version accepted package proposal generation when upstream
  artifacts are unchanged.
- Ensure correction proposals are auditable with explicit reason notes.
- Preserve existing upstream update behavior for version changes and true upstream
  drift.

## Non-Goals

- Automating version bump decisions.
- Modifying `promote` behavior.
- Introducing cross-repository mutation or SpecPM write operations.

## Deliverables

1. CLI/API updates:
   - Add `--allow-correction` flag and `--correction-note` (repeatable) to
     `accepted-package-update-proposal`.
   - If candidate package version equals existing accepted version and upstream
     revision is unchanged, require correction mode (`--allow-correction` + at
     least one `--correction-note`), otherwise reject.
   - In correction mode set `updateKind` to `correction` and include structured
     correction evidence.
2. Proposal model updates:
   - Add `correction` block when enabled:
     - `enabled: true`
     - `reason`: correction notes array
     - `source: "manual_review"`
   - Keep `oldPackageVersion == newPackageVersion` in correction proposals.
3. Reporting updates:
   - Clarify correction flow in docs and CLI help text.
4. Validation:
   - Add tests for:
     - rejection when correction is required but not provided;
     - successful correction path with explicit notes;
     - upstream-driven updates remain unchanged in behavior.

## Acceptance Criteria

- Same-version updates are rejected unless correction mode with notes is explicit.
- Correction path produces deterministic proposal records with correction evidence.
- Upstream-change proposal semantics remain stable.
- All checks pass: ruff, ruff format check, tests.

---
**Archived:** 2026-05-19
**Verdict:** PASS
