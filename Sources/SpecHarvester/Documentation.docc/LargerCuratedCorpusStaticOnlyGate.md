# Larger Curated Corpus Static-Only Gate

Status: P51-T4 real local static-only gate.

P51-T4 runs the 12-source P51 larger curated corpus manifest in deterministic
static-only mode. It is the required gate before the P51-T5 AI-enabled
proposal-only run.

The source manifest is:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The durable fixture is:

```text
tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-static-only-gate/v0
kind: SpecHarvesterLargerCuratedCorpusStaticOnlyGate
authority: producer_static_preview_evidence_only
```

## What Was Run

Run root:

```text
/tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z
```

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p51-larger-curated-corpus \
  --out /tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

The source manifest digest was:

```text
sha256:7676d9d5069f223c33c3e3650c76a60897ada6bed05034dfb5f94dba1d4be79a
```

The batch report digest was:

```text
sha256:2f6bd4e6f8762463d1698be5bfa3369e7fbdae8214d3cbb8b552a15855e73823
```

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | passed |
| Processed repositories | 12 |
| Failed repositories | 0 |
| Passed preflights | 12 |
| Candidate packages | 15 |
| Relation proposals | 3 |
| Preflight warnings | 0 |
| Repository profile detections | 12 |
| Repository profile selected | 10 |
| Repository profile fallback | 2 |
| Author-ready drafts | 15 |
| AI draft proposals | 0 |
| AI enrichment proposals | 0 |
| Trusted local adapter sidecars | 0 |

In prose: all 12 repositories processed successfully, all preflights passed,
15 preview candidates were produced, three relation proposals were preserved,
and no AI or adapter output was produced.

## Repository Results

| Repository | Status | Candidates | Relations | Profile decision | Interface status |
| --- | --- | ---: | ---: | --- | --- |
| Flask | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Gin | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| xyflow | passed | 4 | 3 | selected `generic.package_set.v0` | partial, 29 diagnostics |
| Cupertino | passed | 1 | 0 | fallback | complete |
| NavigationSplitView | passed | 1 | 0 | fallback | complete |
| docc2context | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| FastAPI | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| FastMCP | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| SpecPM | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Hypercode | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| SpecNode | passed | 1 | 0 | selected `generic.single_package.v0` | complete |
| Hyperprompt | passed | 1 | 0 | selected `generic.single_package.v0` | complete |

xyflow produced the relation proposals:

- `xyflow.workspace.contains.xyflow.react`
- `xyflow.workspace.contains.xyflow.svelte`
- `xyflow.workspace.contains.xyflow.system`

## Carry-Forward Triage

Two non-blocking caveats remain visible for P51-T6 triage:

- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`

The caveats did not block P51-T4 because the static-only batch passed and the
source revisions had already matched the P51-T3 readiness gate.

## Gate Decision

P51-T4 passed and allows the P51-T5 AI-enabled proposal-only gate.

P51-T5 must keep all AI output proposal-only. It must not persist raw prompts,
raw provider responses, secrets, or chain-of-thought, and it must not accept
packages, accept relations, publish registry metadata, seed baselines, or
remove `preview_only`.

## Boundary

P51-T4 did not run AI, enable trusted local adapter execution, run adapter
code, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, accept packages or relations, publish
registry metadata, seed baselines, remove `preview_only`, persist raw prompts,
persist raw provider responses, persist secrets, or persist chain-of-thought.

The run does not treat static output as registry truth, does not treat AI
output as registry truth, and does not treat adapter output as registry truth.
All generated candidates and relations remain preview review evidence requiring
SpecPM maintainer review.
