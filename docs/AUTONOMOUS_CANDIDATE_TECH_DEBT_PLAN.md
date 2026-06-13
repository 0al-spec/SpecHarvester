# Autonomous Candidate Technical Debt Plan

Status: Planned follow-up for Phase 29.

This plan records the technical debt found while running
`autonomous-candidate-batch` against the local popular-library corpus:

- `/Users/egor/Development/GitHub/flask`
- `/Users/egor/Development/GitHub/gin`
- `/Users/egor/Development/GitHub/xyflow`

The deterministic run passed for all three repositories, but Flask and Gin
produced `0` package-set candidates because they are single-package repositories
rather than workspaces. The live LM Studio run also showed that local model
output can occasionally fail JSON parsing on real corpus input.

## Boundary

The objective is still a valid starter package, not a final accepted
specification.

SpecHarvester should improve producer-side preview evidence. It must not:

- clone repositories;
- execute harvested code;
- install dependencies;
- publish SpecPM registry content;
- remove `preview_only`;
- treat AI output as registry truth;
- replace author or maintainer review.

## P29-T3 Corpus Baseline and Gap Report

Motivation:

- The first practical corpus run showed useful behavior that is not yet
  captured as a durable artifact.
- Operators need a repeatable baseline before changing fallback or model retry
  behavior.

Goal:

- Record the Flask, Gin, and xyflow autonomous batch outcomes as a machine-readable
  or documented baseline with candidate counts, relation counts, preflight
  status, author-ready stop-policy status, and AI status.

Acceptance:

- The baseline records deterministic `--skip-ai` outcomes.
- The baseline records a live LM Studio outcome when the local model is
  available.
- The report explicitly marks Flask and Gin as `single_package_fallback_needed`.
- The report explicitly marks malformed model JSON as `ai_json_repair_needed`.
- No generated preview candidate is promoted to SpecPM acceptance.

Artifact:

- [`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md)
  records the Flask/Gin/xyflow baseline as
  `SpecHarvesterAutonomousCandidateCorpusBaseline`.

## P29-T4 Single-Package Candidate Fallback

Motivation:

- Many popular libraries are single-package repositories.
- Flask and Gin collected useful evidence and public interface indexes, but the
  package-set drafter produced `0` candidates because there was no workspace
  topology to draft.

Goal:

- When package-set drafting produces no selected member candidates, create one
  preview single-package candidate from harvest metadata, repository source
  manifest hints, README/license evidence, and `public-interface-index.json`.

Acceptance:

- Flask produces a preview candidate for `flask.core`.
- Gin produces a preview candidate for `gin.core`.
- The fallback does not create `contains` relations.
- The fallback emits producer receipt, validation report, diagnostics, and
  author-ready quality report artifacts like other preview candidates.
- The fallback preserves the producer boundary: `preview_only`,
  `producer_preview_evidence_only`, and no registry mutation.

Artifact:

- [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md)
  documents the implemented fallback and its
  `single_package_source_manifest_fallback` selection reason.

## P29-T5 LM Studio JSON Repair and Retry

Motivation:

- Local models can return prose, fenced content, partial JSON, or malformed JSON
  under real corpus load.
- A single malformed response should not make the operator lose the deterministic
  harvest and package draft artifacts.

Goal:

- Add a bounded JSON repair/retry path for local LM Studio/OpenAI-compatible
  proposal generation.

Acceptance:

- Invalid JSON is recorded as a structured diagnostic without persisting raw
  model response text.
- The provider receives at most a small bounded number of repair prompts.
- Successful repair records provider usage and a repair-attempt count.
- Exhausted repair attempts leave the repository as reviewable deterministic
  evidence with AI status `failed` or `needs_regeneration`, not silent success.
- The batch report identifies `ai_json_repair_needed` and does not leak secrets,
  raw prompts, raw responses, or chain-of-thought.
- Package-set AI draft and enrichment proposal receipts record
  `jsonRepairNeeded`, `jsonRepairAttemptCount`, and `jsonRepairStatus`; the
  autonomous batch report exposes `diagnosticCodes` and `jsonRepair` summaries
  for AI proposal records.

## P29-T6 Corpus Quality Gate After Fallbacks

Motivation:

- The autonomous runner should be judged on a mixed corpus, not only on
  package-set-friendly monorepos.

Goal:

- Re-run the local corpus after P29-T4 and P29-T5 and record whether the MVP is
  ready for larger popular-library scraping.

Acceptance:

- Flask, Gin, and xyflow all produce at least one preview candidate.
- Deterministic preflight passes for all repositories.
- Live LM Studio mode either completes proposal generation or emits structured,
  bounded AI diagnostics without corrupting deterministic artifacts.
- The report separates product quality findings from registry acceptance.
- Follow-up work is created only for remaining concrete blockers.

## Suggested Order

1. `P29-T3` baseline and gap report.
2. `P29-T4` single-package candidate fallback.
3. `P29-T5` LM Studio JSON repair/retry.
4. `P29-T6` corpus quality gate.

This order keeps the observed failure mode reproducible before implementation,
then fixes deterministic coverage, then fixes model robustness, then rechecks
the mixed corpus.
