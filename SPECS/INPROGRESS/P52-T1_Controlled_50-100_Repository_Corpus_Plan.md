# P52-T1 Controlled 50-100 Repository Corpus Plan

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T1`
**Depends On:** `P51-T8` Larger Curated Corpus Exit Decision

## Goal

Define the controlled planning contract for producing reviewable, proposal-only
SpecPM candidates from 50-100 popular repositories. The contract must use
staged calibration and quality gates before any corpus acquisition or live
Codex Spark execution is permitted.

## Source Evidence

P52-T1 uses the completed P51-T8 fixture as its planning authority:

```text
tests/fixtures/larger_curated_corpus_exit_decision/p51-t8-larger-curated-corpus-exit-decision.example.json
```

P51-T8 made author-review evidence available, but deliberately left further
expansion and registry promotion unapproved. This task authorizes a plan only,
not a corpus run or registry action.

## Deliverables

- Add a durable `SpecHarvesterControlledRepositoryCorpusPlan` fixture that
  records P51-T8 linkage, scope, staged gates, source policy, quality metrics,
  Codex Spark boundary, privacy requirements, and non-authority boundaries.
- Add GitHub Markdown and DocC documentation explaining the plan in operator
  terms.
- Extend Workplan Phase 52 with explicit follow-up tasks for:
  - Codex Spark external-model adapter contract;
  - five-repository calibration;
  - twenty-repository pilot;
  - 50-100 source manifest and checkout readiness;
  - static-only gate;
  - Codex Spark proposal-only gate;
  - output triage and author handoff;
  - exit decision.
- Update documentation indexes, capability map, and roadmap.
- Add focused documentation-contract tests for identity, source linkage, gate
  ordering, metric thresholds, privacy, authority, and current next-state.
- Create a validation report and complete Flow archive/review artifacts.

## Proposed Phase 52 Sequence

```text
P52-T1 plan
  -> P52-T2 Codex Spark external-model adapter contract
  -> P52-T3 five-repository calibration
  -> P52-T4 twenty-repository pilot
  -> P52-T5 50-100 source manifest and checkout readiness
  -> P52-T6 static-only gate
  -> P52-T7 Codex Spark proposal-only gate
  -> P52-T8 triage and author handoff
  -> P52-T9 exit decision
```

The 50-100 corpus execution gates must remain blocked until the five- and
twenty-repository calibration stages record their required evidence and an
operator provides pinned local checkouts.

## Acceptance Criteria

- The fixture references P51-T8 by path, digest, `apiVersion`, `kind`, and
  authority.
- The plan has a target range of 50-100 repositories but requires a staged
  five-repository calibration and twenty-repository pilot before scale-out.
- The source policy requires pinned operator-provided local checkouts, explicit
  selection rationale, ecosystem/repository-shape coverage, size limits,
  licensing/provenance evidence, and exclusion/stop rules.
- The gate order is explicit: adapter contract, calibration, pilot, source
  manifest/readiness, static-only, AI-enabled proposal-only, triage/handoff,
  exit decision.
- Codex Spark is defined as an external proposal-only worker. Its output must
  be schema-validated and passed to SpecHarvester only as external model output;
  it is not an OpenAI-compatible HTTP provider and cannot grant registry
  authority.
- The plan establishes measurable quality thresholds for static completion, AI
  completion, schema validity, repository specificity, unsupported claims, and
  sampled human review.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.
- The task does not clone/fetch repositories, install dependencies, invoke
  package managers, execute harvested code, run adapters, run Codex or AI,
  accept packages or relations, publish registry metadata, seed baselines,
  remove `preview_only`, or treat any output as registry truth.

## Non-Goals

- Do not implement the Codex Spark adapter.
- Do not select the final 50-100 repository list.
- Do not create or restore repository checkouts.
- Do not run the five-repository calibration, twenty-repository pilot, static
  gate, or AI-enabled gate.
- Do not change the existing LM Studio provider path.
- Do not change SpecPM registry acceptance or publication behavior.

## Validation Plan

- Validate the JSON fixture with `python -m json.tool`.
- Run focused docs-contract tests for the Phase 52 plan and next-state.
- Run repository Flow gates from `.flow/params.yaml`:
  - `PYTHONPATH=src python -m pytest`
  - `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `ruff format --check src tests`
  - `ruff check src tests`
  - `swift package dump-package >/dev/null`
  - `swift build --target SpecHarvesterDocs`
  - `git diff --check`
