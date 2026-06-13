# P30-T3 Validation Report

Task: P30-T3 Live LM Studio Limited Corpus Batch

Date: 2026-06-13

Verdict: PASS

## Scope

P30-T3 records the live LM Studio/OpenAI-compatible run over the committed
P30 limited popular-library corpus. The task preserves the deterministic
P30-T2 baseline as the comparison point and records live AI draft/enrichment
output as producer preview evidence only.

## Recorded Evidence

- Fixture:
  `tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json`
- GitHub docs:
  `docs/LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/LimitedPopularLibraryLiveLMStudioBatch.md`
- Live run root:
  `/tmp/specharvester-p30-t3.f7iGn0/live-lm-studio`
- Batch report digest:
  `sha256:901e1fd2e81b03975fa7cd46d8a5a75b35b16a34512a41f264952a72909cd2c1`
- Batch validation report digest:
  `sha256:f21e068bd63f8fb413578541989ee4fbd6d78a21ecb9483c31ee3dc15fa5da69`

## Product Result

- Processed repositories: `6`
- Generated preview candidates: `9`
- Relation proposals: `3`
- Passed preflights: `6`
- AI draft proposals: `6`
- AI draft statuses: `2 completed`, `4 warning`
- AI enrichment proposals: `6`
- AI enrichment statuses: `5 completed`, `1 warning`
- JSON repair needed: `0`
- JSON repair exhausted: `0`
- Provider total tokens: `138700`
- Product verdict: `ready_for_candidate_layer_triage`

The live run is not SpecPM acceptance and does not accept packages, accept
relations, seed baselines, remove `preview_only`, or publish registry metadata.

## Candidate-Layer Findings for P30-T4

- `excluded_package_unknown`: Flask and Gin AI draft output.
- `package_set_id_missing`: xyflow and NavigationSplitView AI draft output.
- `refined_summary_missing`: Cupertino AI enrichment output.
- `package_id_hint_mismatch`: NavigationSplitView source manifest hint
  `navigation-split-view.core` normalized to generated id
  `navigation_split_view.core`.

## Validation Commands

```bash
rtk python -m json.tool tests/fixtures/limited_popular_library_live_lm_studio_batch/p30-t3-limited-popular-libraries.example.json
rtk env PYTHONPATH=src python -m spec_harvester source-manifests inputs/limited-popular-libraries
rtk env PYTHONPATH=src pytest tests/test_docs_contracts.py -q
rtk env PYTHONPATH=src pytest -q
rtk env PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
rtk env PYTHONPATH=src ruff check .
rtk env PYTHONPATH=src ruff format --check src tests
rtk git diff --check
rtk swift package dump-package
rtk swift build --target SpecHarvesterDocs
rtk swift package --allow-writing-to-directory /tmp/specharvester-p30-t3-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p30-t3-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

## Validation Results

- JSON fixture parse: passed.
- Source manifest preview: `status: ok`, `repositoryCount: 6`.
- Docs contract tests: `61 passed`.
- Full pytest: `629 passed, 1 skipped`.
- Coverage: `90.58%`, above the `90%` gate.
- Ruff check: passed.
- Ruff format check: passed.
- Git diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- DocC static generation: passed.

DocC emitted pre-existing unrelated warnings for
`AcceptedPackageUpdateProposals`, `quality-report`, and `specpm validate`
references. These warnings predate P30-T3 and did not fail documentation
generation.
