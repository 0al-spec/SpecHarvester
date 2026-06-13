# P33-T5 Validation Report: Next-Corpus Candidate-Layer Triage

Task: P33-T5 Next-Corpus Candidate-Layer Triage

Review subject: `p33_t5_next_corpus_candidate_layer_triage`

## Summary

Status: PASS.

P33-T5 recorded candidate-layer triage over the P33 next bounded corpus using
already archived P33-T3 deterministic evidence and P33-T4 live local-model
evidence. It selected three candidates for P33-T6 selected handoff preflight
and kept two candidates deferred.

## Inputs

P33-T5 did not run a new scrape and did not rerun LM Studio. It consumed:

```text
inputs/p33-next-corpus/repositories.yml
tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json
tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json
```

Recorded input digests:

```text
inputs/p33-next-corpus/repositories.yml                                                        sha256:72f3064da9f455c069a5fef6eb25321b74a7e075c5287edcede108a0f4cbed75
tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json sha256:3e8c4b69b33429b3fc2d339c0e119f53d06b52476e3b07648b736b5a46e2eba6
tests/fixtures/next_corpus_live_local_model_batch/p33-t4-next-corpus-live-local-model.example.json      sha256:1eaf50a41ae59e783f5714a1f3e0c32ab87bdc927a2d4404c8a168c345f2446f
```

## Triage Outcome

| Metric | Value |
| --- | ---: |
| preview candidates | `5` |
| relation proposals | `0` |
| selected for P33-T6 | `3` |
| deferred from P33-T6 | `2` |
| blocked | `0` |
| not-for-intake | `0` |

Selected candidates:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

Deferred candidates:

- `mcpm.system`;
- `specgraph.system`.

## Finding Outcome

| Finding | Classification | Candidates |
| --- | --- | --- |
| `ai_draft_no_proposal_subjects` | `candidate_layer_review_required` | `serena.core`, `transmission.core` |
| `ai_draft_warning_diagnostics` | `candidate_layer_review_required` | `specpm.core` |
| `ai_draft_warning_diagnostics` | `needs_regeneration` | `mcpm.system` |
| `package_id_hint_changed_by_package_set_selection` | `needs_regeneration` | `mcpm.system`, `specgraph.system` |

## Artifacts

- `tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json`
- `docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`
- `Sources/SpecHarvester/Documentation.docc/NextCorpusCandidateLayerTriage.md`

## Boundary Check

P33-T5 did not clone repositories, fetch remote state, install dependencies,
execute harvested repository code, run package scripts, rerun LM Studio, mutate
generated candidates, run SpecPM preflight, accept packages, accept relations,
seed baselines, remove `preview_only`, publish registry metadata, create a
SpecPM pull request, or treat model output as registry truth.

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
- docs contract tests: PASS, `82 passed`.
- full pytest: PASS, `658 passed, 1 skipped`.
- coverage gate: PASS, `90.56%`.
- ruff lint: PASS.
- ruff format check: PASS.
- diff check: PASS.
- Swift package dump: PASS.
- Swift docs build: PASS.
- DocC static generation: PASS.
