# P52-T8 Triage Phase 52 Static, Spark, and Enriched Preview Output into Author Handoff

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T8`
**Depends On:** `P52-T7`

## Goal

Classify the 50-repository Phase 52 output into selected, deferred, and
`do_not_promote` buckets using only already produced artifacts from `P52-T6`
and `P52-T7`, then prepare durable author-handoff evidence for maintainer
review.

## Inputs

- `tests/fixtures/final_corpus_static_only_gate/p52-t6-final-corpus-static-only-gate.example.json`
- `tests/fixtures/final_corpus_codex_spark_gate/p52-t7-final-corpus-codex-spark-gate.example.json`
- `inputs/p52-final-corpus/repositories.yml`

## Deliverables

- Add a durable machine-readable triage fixture under
  `tests/fixtures/final_corpus_output_triage/p52-t8-final-corpus-output-triage.example.json`.
- Add documentation file:
  `docs/P52_T8_Output_Triage.md`.
- Add an execution + quality report:
  `SPECS/INPROGRESS/P52-T8_Validation_Report.md`.
- Update review artifacts and archive state through standard FLOW steps.

## Classification Rules

- `selected_for_author_review`: evidence suitable for human review.
- `deferred`: evidence remains useful but requires explicit disposition before
  registry promotion.
- `do_not_promote`: evidence is blocked or currently unsafe for promotion.

## Expected Behavior

- Triages all 50 repositories.
- Classifies static package results from `P52-T6`.
- Classifies Codex Spark sidecars from `P52-T7`.
- Records whether enriched preview outputs are currently ready for selected,
  deferred, or do-not-promote handoff.
- Carries forward visible caveats into `P52-T9`.

## Acceptance Criteria

- The triage artifact records stable source artifact digests for both P52-T6 and
  P52-T7 inputs.
- The triage artifact contains `repositoriesTriaged: 50` and a `classification`
  entry for every repository outcome.
- `doNotPromoteReasonCount` and carried-forward caveat lists are included.
- The task does not rerun a corpus, execute adapters, invoke package managers,
  run harvested code, accept packages or relations, publish registry metadata,
  seed baselines, or remove `preview_only`.
- Raw prompts, raw provider responses, secrets, session state, and chain-of-thought
  are not persisted.

## Boundaries

- Do not clone/fetch repositories.
- Do not install dependencies.
- Do not execute package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, AI output, or triage output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.


---

**Archived:** 2026-07-26
**Verdict:** PASS
