# P30-T4 Validation Report

Task: P30-T4 Candidate-Layer Triage Report

Date: 2026-06-13

Verdict: PASS

## Scope

P30-T4 classifies the P30 limited popular-library generated preview packages
and findings before any selected SpecPM handoff dry run. It consumes the
recorded P30-T2 deterministic fixture and P30-T3 live LM Studio fixture.

## Recorded Evidence

- Fixture:
  `tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json`
- GitHub docs:
  `docs/LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/LimitedPopularLibraryCandidateLayerTriage.md`

## Product Result

- Preview candidates triaged: `9`
- `candidate_layer_review_required`: `3`
- `needs_regeneration`: `6`
- `blocked`: `0`
- `not_for_intake`: `0`
- Selected for P30-T5 dry-run handoff:
  - `flask.core`
  - `gin.core`
  - `docc2context.core`
- Deferred until regeneration or explicit approval:
  - `xyflow.workspace`
  - `xyflow.react`
  - `xyflow.svelte`
  - `xyflow.system`
  - `cupertino.core`
  - `navigation_split_view.core`
- Product verdict: `ready_for_selected_handoff_dry_run`

## Finding Classification

- `excluded_package_unknown`: `candidate_layer_review_required`, non-blocking
  model-output noise for Flask and Gin.
- `package_set_id_missing`: `needs_regeneration`, package-set AI draft
  identity drift.
- `refined_summary_missing`: `needs_regeneration`, enrichment quality drift.
- `package_id_hint_mismatch`: `needs_regeneration`, NavigationSplitView
  package identity policy issue.

## Validation Commands

```bash
rtk python -m json.tool tests/fixtures/limited_popular_library_candidate_layer_triage/p30-t4-limited-popular-libraries.example.json
rtk env PYTHONPATH=src pytest tests/test_docs_contracts.py -q
rtk env PYTHONPATH=src pytest -q
rtk env PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
rtk env PYTHONPATH=src ruff check .
rtk env PYTHONPATH=src ruff format --check src tests
rtk git diff --check
rtk swift package dump-package
rtk swift build --target SpecHarvesterDocs
rtk swift package --allow-writing-to-directory /tmp/specharvester-p30-t4-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p30-t4-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

## Validation Results

- JSON fixture parse: passed.
- Docs contract tests: `63 passed`.
- Full pytest: `631 passed, 1 skipped`.
- Coverage: `90.58%`, above the `90%` gate.
- Ruff check: passed.
- Ruff format check: passed.
- Git diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- DocC static generation: passed.

DocC emitted pre-existing unrelated warnings for
`AcceptedPackageUpdateProposals`, `quality-report`, and `specpm validate`
references. These warnings predate P30-T4 and did not fail documentation
generation.
