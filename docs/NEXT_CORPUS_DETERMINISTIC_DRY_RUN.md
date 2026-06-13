# Next-Corpus Deterministic Dry Run

Status: P33-T3 deterministic producer evidence.

This page records the deterministic `--skip-ai` run over the P33 next bounded
corpus. It validates the P33-T2 source manifest before any live local-model
drafting, enrichment, selected handoff, or SpecPM preflight work.

The machine-readable companion fixture is:

```text
tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.next-corpus-deterministic-dry-run/v0",
  "kind": "SpecHarvesterNextCorpusDeterministicDryRun",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Corpus

Corpus id: `p33-next-bounded-corpus`.

Source manifest:

```text
inputs/p33-next-corpus/repositories.yml
```

| Repository | Manifest package id | Revision |
| --- | --- | --- |
| `serena` | `serena.core` | `892ef9cf19e2c154a75cb58f4b34c8589eada346` |
| `transmission` | `transmission.core` | `98fdf2dc0bfc77e537992ce50fa310b1c3ac636a` |
| `mcpm-sh` | `mcpm.core` | `3a21496dbddffa8b352797aaa498fd4f4d094161` |
| `specgraph` | `specgraph.core` | `2a3e247337acb8102bd4b1d00781c095acc59b16` |
| `specpm` | `specpm.core` | `8a5ce3dece3d18bf8f601a5a599520bd520c7839` |

SpecHarvester did not clone repositories, fetch remote state, execute harvested
code, install dependencies, run package scripts, publish registry metadata,
accept packages, accept relations, seed baselines, remove `preview_only`, or
call an AI provider.

## Deterministic Results

The deterministic `--skip-ai` path processed all five repositories.

| Repository | Candidates | Candidate ids | Relations | Preflight | Author-ready decision |
| --- | ---: | --- | ---: | --- | --- |
| `serena` | `1` | `serena.core` | `0` | `passed` | `stop_for_author_review` |
| `transmission` | `1` | `transmission.core` | `0` | `passed` | `stop_for_author_review` |
| `mcpm-sh` | `1` | `mcpm.system` | `0` | `passed` | `stop_for_author_review` |
| `specgraph` | `1` | `specgraph.system` | `0` | `passed` | `stop_for_author_review` |
| `specpm` | `1` | `specpm.core` | `0` | `passed` | `stop_for_author_review` |

Aggregate summary:

- repositories: `5`;
- collected repositories: `5`;
- generated preview candidates: `5`;
- relation proposals: `0`;
- passed bundle-set preflights: `5`;
- skipped package records: `0`;
- AI draft and AI enrichment: `skipped` for all repositories.

Every repository can proceed to P33-T4 live local-model review. In short, the
deterministic result is ready for P33-T4 live local-model review.

## Candidate-Layer Notes

The batch is healthy enough for P33-T4 live local-model draft/enrichment, but it
is not a SpecPM intake decision.

Two package-id review signals were observed:

- `mcpm-sh`: the source manifest package ID hint is `mcpm.core`, while
  deterministic package-set drafting produced `mcpm.system`.
- `specgraph`: the source manifest package ID hint is `specgraph.core`, while
  deterministic package-set drafting produced `specgraph.system`.

Both findings are recorded as
`package_id_hint_changed_by_package_set_selection`. They are not P33-T3
blockers because collection, drafting, preflight, and author-ready stop policy
all passed. P33-T5 should decide whether each generated package ID is accepted,
deferred for regeneration, or adjusted by a manifest/drafter policy change.

## Product Verdict

Verdict: `ready_for_live_local_model_next_corpus`.

The deterministic P33 next-corpus run produced valid starter package candidates
for all five repositories. This proves the bounded corpus is ready for P33-T4
live local-model review.

This is not a claim that generated specs are final or accepted. The generated
candidate packages remain valid starter packages for author and maintainer
review. SpecPM remains the validation, acceptance, relation, baseline, and
registry authority.

## Commands

Manifest preview:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/p33-next-corpus
```

Deterministic gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p33-next-corpus \
  --out /tmp/specharvester-p33-t3.QV2pVD/deterministic \
  --skip-ai
```

Recorded digests:

```text
inputs/p33-next-corpus/repositories.yml        sha256:72f3064da9f455c069a5fef6eb25321b74a7e075c5287edcede108a0f4cbed75
autonomous-candidate-batch-report.json        sha256:ffcf06735fac8945f8633250b5761af3a233aca7450ce1a18e858aaccfced282
reports/batch-validation-report.json          sha256:ef177176f518d3a5ae9db9ef28b6ed8ac59376cd1f02653a6d0f69b230ab550d
```

## Non-Authority Boundary

The deterministic dry run cannot:

- execute live local-model draft or enrichment providers;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

See also:

- [`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md)
- [`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
