# P52-T8 Output Triage

Status: P52-T8 triage report.

P52-T8 classifies the Phase 52 static, Codex Spark, and enriched-preview outputs
from the accepted 50-repository final corpus into selected, deferred, and
`do_not_promote` buckets. It does not rerun the corpus, execute adapters,
invoke package managers, accept packages or relations, or change registry truth.

The durable fixture is:

```text
tests/fixtures/final_corpus_output_triage/p52-t8-final-corpus-output-triage.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.phase-52-output-triage/v0
kind: SpecHarvesterPhase52OutputTriage
authority: producer_triage_evidence_only
```

## Source Evidence

P52-T8 uses these existing artifacts:

- P52-T6 static-only output:
  `tests/fixtures/final_corpus_static_only_gate/p52-t6-final-corpus-static-only-gate.example.json`
- P52-T7 Codex Spark gate output:
  `tests/fixtures/final_corpus_codex_spark_gate/p52-t7-final-corpus-codex-spark-gate.example.json`
- Source manifest:
  `inputs/p52-final-corpus/repositories.yml`

## Classification Vocabulary

- `selected_for_author_review`: evidence suitable for human review, not registry
  acceptance.
- `deferred`: evidence remains useful but requires explicit disposition before
  registry promotion.
- `do_not_promote`: evidence must not be used as registry-promotion input in
  current form.

## Summary

| Metric | Count |
| --- | ---: |
| Repositories triaged | 50 |
| Static candidate packages | 50 |
| Selected static packages | 48 |
| Deferred static packages | 2 |
| Relation proposals | 0 |
| AI draft sidecars | 50 |
| AI draft selected for author review | 50 |
| AI enrichment sidecars | 0 |
| AI-enriched preview prepared packages | 0 |
| Do-not-promote reason count | 2 |
| Registry-promotion blockers | 2 |

## Static Package Triage

`actix-web` and `uv` are carried as `deferred` because they fail static
readiness on canonical dual-license file variants (`LICENSE-APACHE`/`LICENSE-MIT`),
while static outputs for all other repositories are `selected_for_author_review`.

## Spark Draft Sidecars

All 50 `*.aiDraft` records are currently `selected_for_author_review` and are
proposal-only review evidence only.

## Enrichment and Preview Triage

No enriched preview artifacts are currently prepared from the triage boundary for
P52-T8; enriched preview handoff is deferred to follow-up remediation tasks.

## Caveats Carried Forward

- `actix-web.license_evidence_missing_file_names`
- `uv.license_evidence_missing_file_names`

These caveats do not block P52-T9 by themselves but must be explicitly tracked
in maintainer follow-up before registry promotion.

## Gate Decision

P52-T8 passes output triage as required evidence for the exit decision gate.
It does not grant expansion approval and does not approve any registry
promotion.

## Boundary

P52-T8 does not rerun the corpus, run AI providers, run adapters, clone or
fetch repositories, install dependencies, invoke package managers, execute harvested
code, accept packages or relations, publish registry metadata, seed baselines,
or remove `preview_only`.

It also does not persist raw prompts, raw provider responses, secrets,
or chain-of-thought.
