# Autonomous Candidate Technical Debt Plan

Status: Planned follow-up for Phase 29.

This page records the technical debt found while running
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

SpecHarvester should improve producer-side preview evidence. It must not clone
repositories, execute harvested code, install dependencies, publish SpecPM
registry content, remove `preview_only`, treat AI output as registry truth, or
replace author or maintainer review.

## Work Plan

`P29-T3 Corpus Baseline and Gap Report`

- Motivation: the first practical corpus run needs a durable baseline before
  changing fallback or model retry behavior.
- Goal: record Flask, Gin, and xyflow outcomes with candidate counts, relation
  counts, preflight status, author-ready stop-policy status, and AI status.
- Acceptance: mark Flask and Gin as `single_package_fallback_needed`, mark
  malformed model JSON as `ai_json_repair_needed`, and keep all output
  producer-side only.
- Artifact: <doc:AutonomousCandidateCorpusBaseline> records the Flask/Gin/xyflow
  baseline as `SpecHarvesterAutonomousCandidateCorpusBaseline`.

`P29-T4 Single-Package Candidate Fallback`

- Motivation: many popular libraries are single-package repositories; Flask and
  Gin collected useful evidence but produced no package-set candidates.
- Goal: create one preview single-package candidate from harvest metadata,
  source manifest hints, README/license evidence, and
  `public-interface-index.json` when package-set drafting selects no members.
- Acceptance: Flask produces `flask.core`, Gin produces `gin.core`, no
  `contains` relations are invented, and all artifacts remain `preview_only`.

`P29-T5 LM Studio JSON Repair and Retry`

- Motivation: local models can return prose, fenced content, partial JSON, or
  malformed JSON under real corpus load.
- Goal: add a bounded JSON repair/retry path for local LM
  Studio/OpenAI-compatible proposal generation.
- Acceptance: invalid JSON becomes a structured diagnostic, repair attempts are
  bounded, successful repair records attempt count, and raw prompts, raw
  responses, secrets, and chain-of-thought are not persisted.

`P29-T6 Corpus Quality Gate After Fallbacks`

- Motivation: the autonomous runner should be judged on a mixed corpus, not
  only on package-set-friendly monorepos.
- Goal: re-run the local corpus after P29-T4 and P29-T5 and decide whether the
  MVP is ready for larger popular-library scraping.
- Acceptance: Flask, Gin, and xyflow all produce at least one preview
  candidate, deterministic preflight passes, and live LM Studio mode either
  completes or emits structured bounded AI diagnostics.

## Suggested Order

1. `P29-T3` baseline and gap report.
2. `P29-T4` single-package candidate fallback.
3. `P29-T5` LM Studio JSON repair/retry.
4. `P29-T6` corpus quality gate.
