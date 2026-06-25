# P51-T4 Larger Curated Corpus Static-Only Gate

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T4`
**Created:** 2026-06-25T13:31:00+03:00
**Depends On:** `P51-T3` Larger Curated Corpus Checkout Readiness Gate
**Reasoning Effort:** medium

## Goal

Run the larger curated corpus static-only gate over the 12 P51 selected sources
after checkout readiness has passed, and record durable evidence that decides
whether P51-T5 AI-enabled proposal-only execution is allowed.

## Context

P51-T2 authored the larger curated corpus source manifest:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

P51-T3 verified that all 12 operator-local checkouts are present, git-backed,
and revision-matched:

```text
tests/fixtures/larger_curated_corpus_checkout_readiness/p51-t3-larger-curated-corpus-checkout-readiness.example.json
```

P51-T4 is the deterministic static gate before any AI-enabled larger corpus
run. It may run the existing static `autonomous-candidate-batch --skip-ai`
path, but it must not run AI, adapters, package managers, dependency
installation, harvested code, clone/fetch, registry publication, or acceptance
flows.

## Deliverables

- Real static-only `autonomous-candidate-batch --skip-ai` output under a
  timestamped `/tmp` run root.
- Machine-readable P51-T4 static-only gate fixture under
  `tests/fixtures/larger_curated_corpus_static_only_gate/`.
- GitHub and DocC documentation explaining run inputs, run result, counts,
  diagnostics, caveats, and next gate.
- Contract tests proving fixture identity, P51-T3 readiness linkage, source
  manifest linkage, batch report digest, repository counts, preview output
  counts, no-AI boundaries, no-adapter boundaries, caveat carry-forward, and
  current next-task pointer.
- A validation report recording exact commands and results.

## Acceptance Criteria

- The run consumes `inputs/p51-larger-curated-corpus/repositories.yml`.
- The run uses `autonomous-candidate-batch --skip-ai
  --repository-profile-selection auto`.
- The run records processed, failed, preflight, candidate, relation, warning,
  repository-profile, static-output, and quality-gate counts for all 12
  selected repositories.
- AI draft proposals and AI enrichment proposals remain zero.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  produced or persisted.
- Trusted local adapter execution remains disabled and adapter sidecars do not
  become authority.
- `xyflow.operator_checkout_origin_fork_mismatch` and
  `docc2context.source_checkout_had_untracked_doccarchive` are carried forward
  as review evidence.
- If the static-only batch passes with no failed repositories, the fixture
  marks P51-T5 AI-enabled proposal-only gate as allowed.
- `SPECS/INPROGRESS/next.md` selects `P51-T5` after archival.

## Non-Goals

- Do not run AI.
- Do not enable trusted local adapter execution.
- Do not run adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat static output, readiness output, AI output, adapter output, or
  rerun output as registry truth.

## Validation Plan

- Parse the larger curated corpus source manifest through
  `spec_harvester source-manifests`.
- Run static-only `autonomous-candidate-batch` with
  `--repository-profile-selection auto`.
- Validate the durable fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P51-T4 and linked P51 artifacts.
- Run project quality gates from `.flow/params.yaml`.
