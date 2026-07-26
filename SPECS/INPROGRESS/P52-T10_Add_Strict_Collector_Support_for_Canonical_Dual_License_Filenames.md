# P52-T10 Add Strict Collector Support for Canonical Dual-License Filenames

## Objective

Correct the strict collector's root license filename allowlist for the two
canonical SPDX-adjacent Rust project files `LICENSE-APACHE` and `LICENSE-MIT`.
The correction must make the pinned P52 `uv` and `actix-web` checkouts produce
license evidence while retaining the strict policy for unrelated filenames.

## Acceptance Criteria

- `is_license_filename()` accepts root `LICENSE-APACHE` and `LICENSE-MIT`.
- Existing accepted `LICENSE` and `COPYING` filename variants continue to work.
- Arbitrary suffixed or third-party license names remain rejected.
- A targeted static collection validation over the pinned `uv` and `actix-web`
  checkouts completes without `missing_license_file`.
- Historical P52-T6 evidence remains recorded as 48/50; the new result is a
  follow-up correction, not a retroactive rewrite.
- No AI, adapters, package manager, repository code, registry, or SpecPM
  canonical package data is executed or mutated.

## Test-First Plan

1. Extend the collector filename helper test with the two canonical names and
   one near-miss rejection.
2. Update the allowlist implementation minimally and run the focused test.
3. Run static collection and batch validation against the two operator-provided
   pinned checkouts, recording sanitized outcome evidence.

## Implementation Plan

1. Define the two canonical no-extension filenames in the existing
   `license_files` policy module.
2. Preserve the extension filter and normal `LICENSE`/`COPYING` behaviour.
3. Add a durable targeted validation fixture and documentation explaining the
   correction and boundaries.
4. Run the configured Python, formatting, coverage, and Swift validation gates.

## Notes

P52-T8 remains a historical triage artifact. P52-T9 will consume the P52-T10
follow-up evidence and make the Phase 52 decision; this task does not select or
promote any candidate.
