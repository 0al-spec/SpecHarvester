# P34-T1 AI Enrichment Candidate Patch Proposal

## Summary

Turn clean package-set AI enrichment proposals into reviewable enriched
candidate copies and patch reports.

SpecHarvester already produces `SpecHarvesterPackageSetAIEnrichmentProposal`
artifacts through local LM Studio/OpenAI-compatible providers. Those artifacts
contain useful repository-specific summaries and capabilities, but they remain
sidecar JSON. This task adds a deterministic apply helper that can turn clean
proposal evidence into a separate review candidate without mutating the
generated source bundle or implying SpecPM acceptance.

## Motivation

- AI-enabled usage is now the preferred operator path for candidate review.
- FastAPI smoke showed the deterministic draft is valid, while the LM Studio
  enrichment proposal provides better repository-specific capability shape.
- Operators need a safe handoff step between "model suggested improvements" and
  "maintainer reviews an enriched candidate diff".

## Deliverables

1. Add a CLI command for applying one proposal from
   `package-set-ai-enrichment-proposal.json` to a generated candidate bundle.
2. Write an enriched candidate copy under an explicit output directory.
3. Emit a machine-readable patch report that records inputs, applied changes,
   skipped fields, non-authority boundaries, and evidence digests.
4. Preserve `preview_only: true` and never mutate the source bundle.
5. Add docs and DocC coverage for the AI-enabled review path.
6. Add regression tests for success, warning rejection, unsupported evidence
   rejection, source-bundle immutability, and CLI output.

## Acceptance Criteria

- The helper rejects proposal reports with `status` other than `completed`
  unless an explicit future override is added.
- The selected proposal must have `status: proposed`, a matching package id,
  and no unsupported evidence diagnostics for that package.
- Applied changes are limited to:
  - package summary;
  - boundary `intent.summary`;
  - primary capability summary;
  - additive model-proposed capabilities;
  - additive model-proposed interface summaries.
- Evidence links are preserved from the proposal and recorded in the patch
  report.
- The source candidate bundle remains byte-for-byte unchanged.
- The enriched copy remains preview material and carries non-authority metadata.
- Local tests, lint, format, diff-check, Swift docs build, and DocC generation
  pass or record unrelated warnings.

## Non-Goals

- No SpecPM registry acceptance.
- No package or relation acceptance.
- No baseline seeding.
- No `preview_only` removal.
- No raw prompt or raw model response persistence.
- No automatic application of warning-bearing proposals.
- No model call in the apply helper.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_ai_enrichment_candidate_patch.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- DocC static generation command from `.github/workflows/docs.yml`
- Local smoke using the FastAPI LM Studio run artifact when available.
