# P45-T3 Operational MVP Corpus Rerun After AI Draft Shape Fix

## Status

Archived as PASS on 2026-06-20.

## Motivation

P44-T4 proved that the bounded operational MVP corpus still runs, but it
resolved zero AI draft warnings. P45-T1 fixed safe package-set subject identity
normalization, and P45-T2 added an explicit pre-normalization validation guard.
The next step is to rerun the same bounded corpus and record whether the AI
draft layer is now clean enough for the later readiness decision in P45-T4.

## Goal

Re-run the bounded operational MVP corpus for xyflow, FastAPI, and Gin after the
AI draft shape fix, then compare warning counts, proposal counts, and
proposal-only boundaries against P44-T4.

## Deliverables

- Machine-readable post-fix rerun fixture under
  `tests/fixtures/operational_mvp_quality_hardening/`.
- GitHub documentation and DocC mirror for the post-fix rerun result.
- Docs-contract coverage for the fixture, docs, source artifact digests, warning
  comparison, and authority boundaries.
- Validation report for the task.
- Flow archive and review artifacts.

## Acceptance Criteria

- The rerun uses the same bounded pinned corpus as P44-T4: xyflow, FastAPI, and
  Gin.
- The fixture records source artifact references, including P44-T4 and the P45
  AI draft shape fix artifacts, with path, digest, API version, kind, and
  authority when available.
- Static-only and AI-enabled results record processed count, failures,
  preflight count, candidate count, relation count, AI draft proposal count, AI
  enrichment proposal count, and provider token totals.
- Repository comparisons record P44-T4 warning codes versus post-fix warning
  codes and classify whether warnings are resolved, changed, unchanged, or new.
- AI output remains proposal-only: no raw prompts, raw provider responses,
  secrets, or chain-of-thought are persisted; no AI enrichment is applied into
  registry truth.
- The task does not broaden the corpus, accept packages or relations, publish
  registry metadata, seed baselines, remove `preview_only`, enable trusted local
  adapter execution, execute harvested code, install dependencies, invoke
  package managers, or add Workplan tasks.

## Validation Plan

- Verify the pinned local checkouts match the P43/P44 revisions.
- Run `source-manifests` for the generated P45-T3 input manifest.
- Run static-only `autonomous-candidate-batch` over the bounded corpus.
- Probe local LM Studio at `http://127.0.0.1:1234/v1/models`.
- Run AI-enabled `autonomous-candidate-batch` with
  `openai/gpt-oss-20b` and bounded JSON repair.
- Parse the generated post-fix rerun fixture with `python3 -m json.tool`.
- Run focused docs-contract tests.
- Run lint, format, and whitespace checks for touched files.

## Non-Goals

- Do not broaden the corpus beyond xyflow, FastAPI, and Gin.
- Do not proceed to the P45-T4 readiness decision in this task.
- Do not add Workplan tasks.
- Do not call hosted AI services.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not accept packages, accept relations, publish registry metadata, seed
  baselines, remove `preview_only`, enable trusted local adapter execution, or
  treat AI output as registry truth.
