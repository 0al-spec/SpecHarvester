# Next Task: P52-T10 Add strict collector support for canonical dual-license filenames

**Status:** Selected
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T6` static-only gate evidence
**Started:** 2026-07-27
**Active Task:** `P52-T10` Add strict collector support for common root `LICENSE-APACHE`/`LICENSE-MIT` dual-license filenames and validate `actix-web` and `uv`.
**Branch:** feature/p52-t10-dual-license-collector

## Objective

Resolve the two known strict static false negatives without changing the historical P52-T6 evidence or granting registry authority.

## Preconditions

- The pinned `actix-web` and `uv` checkouts remain available under `P52Sources`.
- The collector remains strict and deterministic.
- No AI, adapter, package-manager, or registry operation is needed.
