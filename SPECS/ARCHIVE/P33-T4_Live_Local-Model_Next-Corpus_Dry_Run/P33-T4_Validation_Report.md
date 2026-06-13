# P33-T4 Validation Report: Live Local-Model Next-Corpus Dry Run

Task: P33-T4 Live Local-Model Next-Corpus Dry Run

Review subject: `p33_t4_live_local_model_next_corpus_dry_run`

## Summary

Status: PASS.

P33-T4 recorded the live LM Studio dry run over the P33 next bounded corpus and
kept the output as producer preview evidence only. The run preserved the P33-T3
deterministic package shape and moved the corpus to P33-T5 candidate-layer
triage.

## Live Run

Provider availability was checked with:

```bash
curl -sS http://127.0.0.1:1234/v1/models
```

The local endpoint exposed `openai/gpt-oss-20b`, which was used for the live
run.

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p33-next-corpus \
  --out /tmp/specharvester-p33-t4.yQPfwg/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Run root:

```text
/tmp/specharvester-p33-t4.yQPfwg/live-lm-studio
```

Recorded digests:

```text
inputs/p33-next-corpus/repositories.yml        sha256:72f3064da9f455c069a5fef6eb25321b74a7e075c5287edcede108a0f4cbed75
autonomous-candidate-batch-report.json        sha256:cdf22a5ddec014e49c432925f1b71710140d8667954daba36684f8d9c12a1ff2
reports/batch-validation-report.json          sha256:993c8eb865a8f3aa35d35b84eb49ea06862062f0acca8eeb999fce11c27dec42
```

## Batch Outcome

| Metric | Value |
| --- | ---: |
| repositories processed | `5` |
| collected repositories | `5` |
| failed repositories | `0` |
| preview candidates | `5` |
| relation proposals | `0` |
| passed bundle-set preflights | `5` |
| AI draft proposals | `5` |
| AI enrichment proposals | `5` |
| JSON repair needed | `0` |
| JSON repair exhausted | `0` |
| draft provider tokens | `21251` |
| enrichment provider tokens | `55040` |
| total provider tokens | `76291` |

## Repository Outcome

| Repository | Candidate id | AI draft | AI enrichment | Findings |
| --- | --- | --- | --- | --- |
| `serena` | `serena.core` | `completed`, no proposal subjects | `completed` | `ai_draft_no_proposal_subjects` |
| `transmission` | `transmission.core` | `completed`, no proposal subjects | `completed` | `ai_draft_no_proposal_subjects` |
| `mcpm-sh` | `mcpm.system` | `warning` | `completed` | `package_id_hint_changed_by_package_set_selection`, `ai_draft_warning_diagnostics` |
| `specgraph` | `specgraph.system` | `completed` | `completed` | `package_id_hint_changed_by_package_set_selection` |
| `specpm` | `specpm.core` | `warning` | `completed` | `ai_draft_warning_diagnostics` |

## Artifacts

- `tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json`
- `docs/NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`
- `Sources/SpecHarvester/Documentation.docc/NextCorpusLiveLocalModelBatch.md`

## Boundary Check

P33-T4 did not clone repositories, fetch remote state, install dependencies,
execute harvested repository code, run package scripts, accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat model output as registry truth.

## Validation

The following gates were run during EXECUTE:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests inputs/p33-next-corpus
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvesterDocs \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Results:

- `source-manifests`: PASS.
- docs contract tests: PASS, `80 passed`.
- full pytest: PASS, `656 passed, 1 skipped`.
- coverage gate: PASS, `90.56%`.
- ruff lint: PASS.
- ruff format check: PASS.
- diff check: PASS.
- Swift package dump: PASS.
- Swift docs build: PASS.
- DocC static generation: PASS.
