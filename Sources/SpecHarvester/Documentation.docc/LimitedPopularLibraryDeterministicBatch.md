# Limited Popular-Library Deterministic Batch

This page records the P30-T2 deterministic `--skip-ai` run over the limited
popular-library corpus.

The machine-readable companion fixture is:

```text
tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json
```

Its identity is
`SpecHarvesterLimitedPopularLibraryDeterministicBatch` with
`apiVersion: spec-harvester.limited-popular-library-deterministic-batch/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Corpus

The run used `inputs/limited-popular-libraries/repositories.yml`.

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

## Results

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
- skipped package records: `7`;
- AI draft and AI enrichment: `skipped`.

## Candidate-Layer Notes

The batch is ready for P30-T3 live LM Studio comparison, but it is not a SpecPM
intake decision.

NavigationSplitView produced one review item:
`package_id_hint_mismatch`. `navigation-split-view.core` in the source manifest
became `navigation_split_view.core` in deterministic drafting. P30-T4 should
decide whether this is acceptable normalization, a manifest fix, or a generator
naming-policy issue.

## Product Verdict

Verdict: `ready_for_live_lm_studio_limited_corpus`.

The deterministic P30 limited corpus run produced valid starter package
candidates for all six repositories. The generated output remains producer
preview evidence for author and maintainer review. SpecPM remains the
validation, acceptance, relation, baseline, and registry authority.

## Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries
```

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

See also <doc:LimitedPopularLibraryCorpusPlan>,
<doc:AutonomousCandidateCorpusQualityGate>, and
<doc:AutonomousCandidateIntakePolicy>.
