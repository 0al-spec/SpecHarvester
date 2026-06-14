# Next Task: Phase 35 Complete

**Status:** Complete
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Last Archived:** P35-T6 Selected Corpus Dry-Run Readiness

## Recently Archived

- `P35-T6` added
  [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](../../docs/SELECTED_CORPUS_DRY_RUN_READINESS.md)
  and the DocC mirror `SelectedCorpusDryRunReadiness`.
- The readiness fixture
  `tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json`
  defines `SpecHarvesterSelectedCorpusReadinessReport` with `apiVersion:
  spec-harvester.selected-corpus-readiness/v0`, `schemaVersion: 1`, and
  `authority: producer_readiness_report_only`.
- The report covers `react`, `fastapi`, `serde`, `gin`, and
  `swift-argument-parser`.
- The readiness verdict is `blocked_pending_local_checkouts`, with every
  selected source blocked by `local_checkout_not_verified`.
- The downstream `autonomous-candidate-batch` command gate is `allowed:
  false` until all selected sources have verified pinned local checkouts.

## Phase Summary

Phase 35 completed the curated multi-ecosystem corpus selection foundation:

- `P35-T1` documented the corpus selection policy.
- `P35-T2` defined `SpecHarvesterCorpusPlan`.
- `P35-T3` defined candidate source classification.
- `P35-T4` created the first bounded seed corpus.
- `P35-T5` added the explainable corpus selection report.
- `P35-T6` added the selected corpus dry-run readiness report.

## Result

SpecHarvester now has a bounded curated corpus planning path instead of an
open-ended registry crawl. The seed corpus is selected and explainable, but it
is blocked until operator-provided pinned local checkouts are verified.

The non-authority boundary remains explicit: the phase does not publish
registry metadata, does not accept packages or relations, does not seed
baselines, does not remove `preview_only`, and does not treat AI output as
registry truth.

## Suggested Next Step

Choose a new phase for operator-provided local checkout preparation and
readiness rerun, or pause corpus expansion until the selected repositories are
available locally at verified pinned revisions.
