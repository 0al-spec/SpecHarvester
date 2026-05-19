# Next Task: P8-T6 - Add accepted package version immutability guard for update proposals

**Priority:** P8
**Phase:** Accepted Specification Update Lifecycle
**Effort:** Medium
**Dependencies:** P8-T5
**Status:** SELECT

**Updated:** 2026-05-19
**Suggested Branch:** `feature/P8-T6-accepted-package-version-immutability-guard`

## Description

Add a strict preflight guard so proposals cannot silently mutate an already
accepted `package_id@version`. Same-version updates must use explicit correction
mode with rationale notes; all other same-version mutations should fail fast.

## Next Step

Run the PLAN command to create the P8-T6 implementation PRD.
