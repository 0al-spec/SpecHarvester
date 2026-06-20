# P44-T1 Operational MVP Warning Triage

## Status

Planned.

## Motivation

P43-T7 selected `needs_quality_hardening` before broader bounded
popular-library scraping. The immediate blocker is not provider availability:
P43-T5 ran local LM Studio successfully and produced proposal-only AI draft and
enrichment sidecars for xyflow, FastAPI, and Gin.

The unresolved question is why all three repositories reported the same
`package_set_id_missing` AI draft diagnostic while enrichment completed cleanly.
P44-T1 must classify that warning cause before later P44 tasks review proposal
quality, resolve xyflow caveats, rerun the corpus, or make a post-hardening
readiness decision.

## Goal

Record a durable warning triage artifact that explains the P43-T5
`package_set_id_missing` diagnostics per repository and separates draft-layer
shape issues from package-set identity drift, missing draft context, expected
producer-side boundaries, and unrelated manual-correction caveats.

## Deliverables

- Machine-readable `SpecHarvesterOperationalMVPWarningTriage` fixture under
  `tests/fixtures/operational_mvp_quality_hardening/`.
- GitHub documentation and DocC mirror for the warning triage.
- Navigation links from docs index, DocC root, capabilities, and roadmap.
- Docs-contract coverage for fixture identity, source digests, per-repository
  classifications, follow-up guidance, and non-authority boundaries.
- Validation report for this task.

## Acceptance Criteria

- The fixture references the current P43-T5 AI-enabled comparison and P43-T7
  exit report by path, digest, API version, kind, and authority.
- The fixture records one warning triage entry each for xyflow, FastAPI, and
  Gin.
- Each entry classifies the `package_set_id_missing` warning cause using the
  P44 categories: missing draft context, package-set identity drift, AI proposal
  shape, or expected producer-side boundary.
- The triage keeps AI enrichment output proposal-only and does not promote it
  to accepted SpecPM truth.
- The triage records follow-up guidance for P44-T2, P44-T3, P44-T4, and P44-T5.
- Documentation and tests prove that the task does not clone/fetch
  repositories, install dependencies, invoke package managers, execute
  harvested code, run AI, enable trusted local adapter execution, accept
  packages or relations, publish registry metadata, seed baselines, remove
  `preview_only`, or treat AI output as registry truth.

## Non-Goals

- Do not rerun the operational MVP corpus.
- Do not call LM Studio or hosted AI services.
- Do not inspect or persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not apply AI enrichment proposals.
- Do not fix xyflow public-interface or fork-origin caveats; those remain
  separate P44 follow-ups.
