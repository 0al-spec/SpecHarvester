# P44-T2 Operational MVP AI Proposal Quality Review

## Status

Planned.

## Motivation

P44-T1 narrowed the shared P43-T5 `package_set_id_missing` warning to an AI
draft proposal shape issue. The enrichment sidecars still completed cleanly and
contain proposal-only author review material for xyflow, FastAPI, and Gin.

Before the project uses AI enrichment as a broader scraping quality baseline,
P44-T2 must classify proposal quality: useful suggestions, noisy suggestions,
unsupported claims, evidence gaps, and do-not-promote output.

## Goal

Record a durable AI proposal quality review artifact for the P43-T5 enrichment
proposals without applying AI output to accepted SpecPM truth.

## Deliverables

- Machine-readable `SpecHarvesterOperationalMVPAIProposalQualityReview`
  fixture under `tests/fixtures/operational_mvp_quality_hardening/`.
- Per-repository quality review for xyflow, FastAPI, and Gin.
- Follow-up guidance for generator changes, evidence tightening, author review,
  and do-not-promote handling.
- GitHub documentation, DocC mirror, navigation links, and docs-contract
  coverage.
- Validation report for this task.

## Acceptance Criteria

- The fixture references P43-T5 and P44-T1 by path, digest, API version, kind,
  and authority.
- The fixture records all six enrichment proposal members from P43-T5.
- Each repository has explicit counts for useful suggestions, noisy
  suggestions, unsupported claims, evidence gaps, and do-not-promote output.
- The fixture records that proposal output remains author-review evidence only.
- The task does not read or persist raw prompts, raw provider responses, secrets,
  or chain-of-thought.

## Non-Goals

- Do not apply AI enrichment proposals.
- Do not regenerate AI output.
- Do not fix the P44-T1 draft proposal shape issue.
- Do not resolve xyflow public-interface or fork-origin caveats.
- Do not approve bounded popular-library scraping.
