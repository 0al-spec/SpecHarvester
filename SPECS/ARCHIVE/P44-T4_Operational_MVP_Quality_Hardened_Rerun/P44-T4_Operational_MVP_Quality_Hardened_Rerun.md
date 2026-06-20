# P44-T4 Operational MVP Quality-Hardened Rerun

## Status

Archived as PASS on 2026-06-20.

## Motivation

P43 proved that the bounded operational MVP corpus can produce static-only and
AI-enabled proposal output, but P43-T7 selected `needs_quality_hardening`.
P44-T1 through P44-T3 clarified warning causes, reviewed proposal quality, and
accepted xyflow caveats for bounded rerun purposes. P44-T4 must record whether
the post-hardening evidence is materially cleaner than the P43 baseline.

## Goal

Produce a durable quality-hardened rerun comparison for the bounded corpus:
xyflow, FastAPI, and Gin.

## Deliverables

- Machine-readable `SpecHarvesterOperationalMVPQualityHardenedRerun` fixture.
- Static-only and AI-enabled rerun summary for all three repositories.
- Comparison against P43-T4/P43-T5/P43-T6/P44-T1/P44-T2/P44-T3 source
  artifacts.
- Explicit status for warnings, proposal-only AI sidecars, manual-correction
  caveats, and registry-authority boundaries.
- GitHub documentation, DocC mirror, navigation links, and docs-contract
  coverage.
- Validation report for this task.

## Acceptance Criteria

- The fixture references all source artifacts by path, digest, API version,
  kind, and authority.
- Static-only and AI-enabled rerun results preserve the bounded corpus lineage.
- AI output remains proposal-only and no raw prompts, raw provider responses,
  secrets, or chain-of-thought are persisted.
- The comparison records whether P44 hardening changed warning ambiguity,
  proposal usefulness, do-not-promote output, and xyflow manual-correction
  visibility.
- The fixture does not accept packages, relations, AI output, adapter output, or
  registry truth.

## Non-Goals

- Do not broaden the corpus beyond xyflow, FastAPI, and Gin.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not enable trusted local adapter execution or run adapter code.
- Do not approve bounded popular-library scraping; that is P44-T5.
