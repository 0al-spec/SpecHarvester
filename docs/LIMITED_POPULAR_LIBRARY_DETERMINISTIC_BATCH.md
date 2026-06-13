# Limited Popular-Library Deterministic Batch

Status: P30-T2 deterministic producer evidence.

This page records the deterministic `--skip-ai` run over the P30 limited
popular-library corpus. It validates the committed source manifest before any
live LM Studio or SpecPM handoff work.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json
```

Its contract identity is:

```json
{
  "apiVersion": "spec-harvester.limited-popular-library-deterministic-batch/v0",
  "kind": "SpecHarvesterLimitedPopularLibraryDeterministicBatch",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Corpus

Corpus id: `p30-limited-popular-libraries`.

Source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

| Repository | Manifest package id | Revision |
| --- | --- | --- |
| Flask | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |
| Cupertino | `cupertino.core` | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` |
| NavigationSplitView | `navigation-split-view.core` | `2c88df50b8f587560b91f6027e9ea275aee17060` |
| docc2context | `docc2context.core` | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` |

SpecHarvester did not clone repositories, fetch updates, execute harvested
code, install dependencies, publish registry metadata, accept packages, accept
relations, seed baselines, remove `preview_only`, or call an AI provider.

## Deterministic Results

The deterministic `--skip-ai` path processed all six repositories.

| Repository | Candidates | Candidate ids | Relations | Preflight | Author-ready decision |
| --- | ---: | --- | ---: | --- | --- |
| Flask | `1` | `flask.core` | `0` | `passed` | `stop_for_author_review` |
| Gin | `1` | `gin.core` | `0` | `passed` | `stop_for_author_review` |
| xyflow | `4` | `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system` | `3` | `passed` | `stop_for_author_review` |
| Cupertino | `1` | `cupertino.core` | `0` | `passed` | `stop_for_author_review` |
| NavigationSplitView | `1` | `navigation_split_view.core` | `0` | `passed` | `stop_for_author_review` |
| docc2context | `1` | `docc2context.core` | `0` | `passed` | `stop_for_author_review` |

Aggregate summary:

- repositories: `6`;
- collected repositories: `6`;
- generated preview candidates: `9`;
- relation proposals: `3`;
- passed bundle-set preflights: `6`;
- skipped package records: `7`, all from the xyflow workspace package-set
  selection;
- AI draft and AI enrichment: `skipped` for all repositories.

## Candidate-Layer Notes

The batch is healthy enough for P30-T3 live LM Studio comparison, but it is not
a SpecPM intake decision.

One candidate-layer review item was observed:

- `package_id_hint_mismatch`: `navigation-split-view.core` in the source manifest became
  `navigation_split_view.core` in deterministic drafting. P30-T4 should decide
  whether this is acceptable normalization, a manifest fix, or a generator
  naming-policy issue.

xyflow remained the only package-set case in this corpus. It produced
`xyflow.workspace` plus `xyflow.react`, `xyflow.svelte`, and `xyflow.system`
with three producer-observed `contains` relation proposals.

## Product Verdict

Verdict: `ready_for_live_lm_studio_limited_corpus`.

The deterministic P30 limited corpus run produced valid starter package
candidates for all six repositories. This proves the bounded corpus is ready
for P30-T3 live LM Studio comparison.

This is not a claim that generated specs are final or accepted. The generated
candidate packages remain valid starter packages for author and maintainer
review. SpecPM remains the validation, acceptance, relation, baseline, and
registry authority.

## Commands

Manifest preview:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries
```

Deterministic gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out /tmp/specharvester-p30-t2.7rNeq2/deterministic \
  --skip-ai
```

Recorded report digests:

```text
autonomous-candidate-batch-report.json sha256:f2e6ad92cb9a6686e8d7bf333b173aeb91dd7d3005c955da7dece5cda620500c
batch-validation-report.json           sha256:ef81c8a2f8a4b7a720f19112bd46b72c96e5c9ff07695c9591221950e58c29f5
```

## Non-Authority Boundary

The deterministic batch cannot:

- execute AI draft or enrichment providers;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- replace author or SpecPM maintainer review.

See also:

- [`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md)
- [`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md)
- [`AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`](AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
