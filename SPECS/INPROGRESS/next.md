# Next Task: P19-T1 — Static Spec Renderer

**Status:** Pending
**Suggested:** 2026-05-29

## Recently Archived

- P18-T1: Swift Public API Analyzer (PASS, 2026-05-29)

## Rationale

SpecHarvester now produces richer generated SpecPM candidate packages, but
reviewers still inspect `specpm.yaml` and `specs/*.spec.yaml` mostly as raw
YAML. A deterministic static HTML/JS renderer gives reviewers a browser-safe
candidate preview while keeping SpecPM as the validation and registry authority.

## Next Step

Implement `P19-T1` as a small extractable static site generator for local
candidate directories, with tests and documentation covering the trust boundary
and future standalone-repository extraction path.
