# P52-T6 50-100 Repository Static-Only Gate

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T6`
**Depends On:** `P52-T5` Final 50-100 Repository Source Manifest and Checkout Readiness

## Goal

Run one deterministic static-only candidate batch over the approved P52-T5
50-repository corpus and prove that its completion rate meets the Phase 52 95%
minimum before any Codex Spark execution is allowed.

## Deliverables

- Add a deterministic P52-T6 gate command that consumes the P52-T5 readiness
  report and the exact final corpus manifest.
- Require a passing P52-T5 report, matching source ids, 50-100 sources, and no
  blocked readiness records before static collection begins.
- Reuse `run_autonomous_candidate_batch` with `skip_ai=True` and automatic
  repository-profile selection; do not introduce another collector or drafter.
- Emit a sanitized P52-T6 report with static completion metrics, every source
  outcome, failure diagnostics, static report digest, execution boundaries, and
  an explicit P52-T7 decision.
- Preserve generated packages as deterministic `preview_only` candidate
  evidence without acceptance, relation, publication, baseline, or registry
  authority.
- Add focused tests, a durable live report fixture, Markdown/DocC documentation,
  and validation evidence.

## Acceptance Criteria

- The gate processes every one of the 50 approved P52-T5 sources; no source is
  silently omitted, replaced, cloned, fetched, restored, or modified.
- Static collection and deterministic drafting complete for at least 95% of the
  corpus. The report records numerator, denominator, value, minimum, and pass
  status plus explicit failed repository ids.
- The underlying autonomous batch is invoked exactly once with `skip_ai=True`;
  no LM Studio, Codex Spark, model provider, enrichment, package manager,
  adapter, build, test, or harvested-code execution occurs.
- The P52-T5 readiness artifact is digest-bound and its source ids exactly match
  the manifest and the P52-T6 static results.
- P52-T7 is unlocked only when readiness, exact source coverage, the static-only
  execution boundary, and the 95% static completion threshold all pass. The
  underlying batch status may be `failed` when the explicitly recorded failure
  count remains within the threshold; no failure may be omitted.
- Generated package output remains `preview_only` producer evidence. No package
  or relation is accepted, registry metadata is published, baseline is seeded,
  or registry truth is changed.
- No raw prompts, raw provider responses, model stdout/stderr, secrets, session
  state, or chain-of-thought are persisted.

## Non-Goals

- Do not run P52-T7 Codex Spark, LM Studio, AI enrichment, author triage, or the
  Phase 52 exit decision.
- Do not acquire repositories, install dependencies, invoke package managers,
  run adapters, or execute harvested code.
- Do not promote, publish, or accept generated candidates.

## Validation Plan

- Run focused gate, CLI, failure-policy, digest-binding, and documentation tests.
- Run a live 50-source static-only gate into a disposable output directory and
  retain only the sanitized report fixture and artifact digests.
- Verify there are no AI/model/request/response artifacts in the static output.
- Validate durable JSON artifacts with `python -m json.tool`.
- Run Flow gates from `.flow/params.yaml`: full pytest with coverage >=90%,
  Ruff, Swift package/DocC build, and `git diff --check`.
