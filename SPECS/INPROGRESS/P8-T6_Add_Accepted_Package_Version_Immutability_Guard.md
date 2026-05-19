# P8-T6 - Add Accepted Package Version Immutability Guard for Update Proposals

Branch: `feature/P8-T6-accepted-package-version-immutability-guard`
Review subject: `p8_t6_accepted_package_version_immutability_guard`

## Problem

`accepted-package-update-proposal` can produce proposal payloads for an already
accepted `package_id@version` without guaranteeing that the same-version mutation
is explicitly marked as correction. This can silently rewrite an immutable
registry evidence path when upstream revision or metadata changes without explicit
operator intent.

## Goals

- Treat proposal generation against an existing `package_id@version` as mutable only
  via explicit correction flow.
- Require `--allow-correction` and at least one `--correction-note` for any proposal
  where candidate and prior accepted package versions are identical and content
  differs.
- Ensure exact-version matches, not only latest accepted versions, are considered when
  applying the immutability guard.
- Keep correction behavior deterministic: emit `updateKind: correction` and correction
  evidence when allowed.

## Non-Goals

- Changing how `promote` writes accepted packages.
- Automatically bumping versions or choosing upstream drift strategies.
- Additional proposal workflow policy in SpecPM CI.

## Deliverables

1. Proposal logic updates:
   - Update prior accepted record lookup to prefer exact package version match for
     immutability checks when available.
   - Update correction preflight logic so same-version candidate mutations always
     require correction mode, independent of upstream revision stability.
   - Keep error messaging explicit that the package version is immutable.
2. Tests:
   - Reject same-version updates when upstream hash/metadata/capability changed and
     correction is not enabled.
   - Verify candidate targeting older accepted version is also blocked unless correction.
   - Verify same-version updates with `--allow-correction` still produce correction
     artifacts.
   - Keep regression coverage for existing metadata-only correction behavior.
3. Documentation:
   - Update CLI help text and proposal docs to describe strict same-version correction
     policy.

## Acceptance Criteria

- Any proposal targeting an already accepted `packageId@version` with content changes
  requires explicit correction mode and rationale notes.
- Exact accepted-version matches are detected even when a newer version for the same
  package exists.
- Preflight fails with a clear message when correction is required but missing.
- Existing accepted metadata correction flow for same version remains functional when
  correction flags are present.
- `ruff`, `ruff format`, and relevant tests pass.
