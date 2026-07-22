# Controlled 50-100 Repository Corpus Plan

Status: P52-T1 plan.

P52-T1 defines the controlled path to 50-100 popular repositories. It is a
planning artifact, not a scrape, checkout acquisition, Codex run, AI run, or
registry decision.

The durable fixture is:

```text
tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.controlled-repository-corpus-plan/v0
kind: SpecHarvesterControlledRepositoryCorpusPlan
authority: producer_planning_evidence_only
```

## Starting Point

The plan is based on P51-T8:

```text
tests/fixtures/larger_curated_corpus_exit_decision/p51-t8-larger-curated-corpus-exit-decision.example.json
sha256:9c080b5f8f17d021894a3b2755177fefc56ac4d836aebd450098fbb09ee06ec9
```

P51-T8 made the 12-repository result ready for author review, but explicitly
left further expansion and registry promotion unapproved. P52-T1 therefore
plans a new controlled phase; it does not reinterpret prior evidence as live
execution approval.

## Rollout

The final target is 50-100 operator-curated repositories, reached only through
the following gates:

```text
P52-T2 Codex Spark external-model adapter contract
  -> P52-T3 five-repository calibration
  -> P52-T4 twenty-repository pilot
  -> P52-T5 50-100 source manifest and checkout readiness
  -> P52-T6 static-only gate
  -> P52-T7 Codex Spark proposal-only gate
  -> P52-T8 output triage and author handoff
  -> P52-T9 exit decision
```

The first two live stages are deliberately small. A five-repository calibration
proves the integration shape; a twenty-repository pilot reveals concurrency,
schema, and quality failure modes before the larger corpus is prepared.

## Codex Spark Boundary

`gpt-5.3-codex-spark` is planned as an external proposal-only worker invoked
through `codex exec`. It is not treated as an OpenAI-compatible HTTP provider.
P52-T2 must define a schema-validated external-model-output handoff from Codex
to SpecHarvester before any live model call.

Spark receives deterministic evidence inputs and can propose package-set or
enrichment content. Its response is validated before it is saved as proposal
evidence. It cannot accept packages or relations, publish registry metadata,
remove `preview_only`, or grant registry authority.

## Source Policy

Each future source must have an operator-provided pinned local checkout and
record its upstream URL, revision, ecosystem, repository shape, importance
signals, license/provenance evidence, and size budget. The corpus must cover
multiple ecosystems as well as single-package, workspace/monorepo,
documentation-heavy, framework, and library shapes.

Sources are excluded when their pinned revision or local checkout is missing,
license/provenance is unresolved, size budget is exceeded, content is only
generated/vendor material, or the source layout is unsafe or unreviewable.

## Quality Gates

| Measure | Required result |
| --- | ---: |
| Static completion | at least 95% |
| Codex Spark completion | at least 90% |
| Schema-valid output | at least 98% |
| Repository-specific candidates | at least 80% |
| Unsupported claims | at most 5% |
| Human-review sample | at least 10% and at least 10 candidates |

Failure to meet a threshold stops scale-out and requires a bounded follow-up;
it does not silently retry the entire corpus.

## Boundary

P52-T1 did not create or restore checkouts, clone or fetch repositories,
install dependencies, invoke package managers, execute harvested code, run
adapters, run Codex, or run AI. It did not accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, or treat
static, AI, planning, or adapter output as registry truth.

Raw prompts, raw provider responses, secrets, and chain-of-thought are not
persisted. A Phase 52 exit decision is required before any later authority
change can be considered.
