# P52-T2 Codex Spark External-Model Adapter Contract

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T2`
**Depends On:** `P52-T1` Controlled 50-100 Repository Corpus Plan

## Goal

Define the schema-validated, proposal-only boundary for a future Codex Spark
worker. The contract must transform deterministic SpecHarvester evidence into a
bounded `codex exec` invocation and accept only its final JSON message through
the existing external `--model-output` seam.

## Source Evidence

P52-T2 uses the P52-T1 fixture as its only planning authority:

```text
tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json
```

P52-T1 selected `gpt-5.3-codex-spark` as an external proposal-only worker,
not an OpenAI-compatible HTTP provider. It requires P52-T2 before the
five-repository calibration.

## Deliverables

- Add a durable `SpecHarvesterCodexSparkExternalModelAdapterContract` fixture.
- Define a future invocation profile using:
  - `codex exec --model gpt-5.3-codex-spark`;
  - `--sandbox read-only`;
  - `--ephemeral`;
  - `--ignore-user-config`;
  - `--output-schema`;
  - `--output-last-message`.
- Define the evidence-staging boundary: a future invocation receives a
  generated read-only evidence directory and no original repository checkout,
  writable add-directory, or network/provider endpoint.
- Define final-output validation, deterministic `--model-output` handoff,
  receipt fields, timeout/exit failure taxonomy, and rejection conditions.
- Add GitHub Markdown and DocC documentation, indexes, capability map, and
  roadmap linkage.
- Add focused docs-contract tests for source linkage, invocation invariants,
  privacy, authority, and P52-T3 next-state.
- Create validation, archive, and review artifacts through Flow.

## Acceptance Criteria

- The fixture references P52-T1 by path, digest, `apiVersion`, `kind`, and
  authority.
- The adapter is explicitly `codex_exec_external_model_output`, not an
  OpenAI-compatible HTTP provider and not a replacement for LM Studio.
- The invocation profile requires the selected model, read-only sandbox,
  ephemeral state, ignored user config, final response JSON Schema, and a
  final-message output file.
- The contract excludes original repository checkouts, `--add-dir`, writable
  agent workspaces, package manager/dependency actions, adapters, and live
  network/provider endpoints from a future invocation.
- Only validated final JSON can enter the existing `--model-output` path;
  malformed output, non-zero exit, timeout, missing output, schema failure,
  policy drift, and receipt mismatch are rejected as proposal-only failures.
- Receipts may retain model id, Codex CLI version, sandbox mode, schema digest,
  evidence digest, duration, exit status, and final-output digest. They must
  not retain raw prompts, raw model/provider responses, secrets, session state,
  or chain-of-thought.
- The task does not invoke Codex, run AI, create/restore/clone/fetch a
  repository, install dependencies, invoke package managers, execute harvested
  code, run adapters, accept packages or relations, publish registry metadata,
  seed baselines, remove `preview_only`, or treat output as registry truth.

## Non-Goals

- Do not implement a subprocess adapter or add a CLI command.
- Do not run the five-repository calibration.
- Do not modify the LM Studio/OpenAI-compatible provider implementation.
- Do not create schemas that expose raw source checkout content to Codex.
- Do not persist raw prompts, raw responses, or Codex session files.

## Validation Plan

- Validate the JSON fixture with `python -m json.tool`.
- Run focused docs-contract tests for the Codex Spark adapter contract.
- Run repository Flow gates from `.flow/params.yaml`:
  - `PYTHONPATH=src python -m pytest`
  - `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `swift package dump-package >/dev/null`
  - `swift build --target SpecHarvesterDocs`
- `git diff --check`

---
**Archived:** 2026-07-22
**Verdict:** PASS
