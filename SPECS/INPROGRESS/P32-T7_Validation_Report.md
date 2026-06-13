# P32-T7 Validation Report

Task: `P32-T7 Limited Corpus Intake Readiness Decision`

## Scope

P32-T7 records a non-authoritative readiness decision for the bounded P30/P32
limited corpus. It uses committed P32-T5 producer evidence and the P32-T6
SpecPM consumer preflight result.

## Decision Artifact

```text
tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json
```

Identity:

```text
apiVersion: spec-harvester.limited-corpus-intake-readiness-decision/v0
kind: SpecHarvesterLimitedCorpusIntakeReadinessDecision
authority: producer_preview_evidence_only
```

## Result

The decision is:

```text
ready_for_author_maintainer_review_with_explicit_deferral
```

Selected candidates ready for author/maintainer review:

- `flask.core`
- `gin.core`
- `docc2context.core`
- `xyflow.workspace`
- `xyflow.react`
- `xyflow.svelte`
- `xyflow.system`
- `navigation_split_view.core`

Deferred candidate:

- `cupertino.core` remains deferred on `refined_summary_missing`.

## Evidence

- P32-T5 refreshed handoff fixture digest:
  `sha256:61a3aebcfdbc934288c18af272b2bdf4b1e64c86fe2092487f93f64b67097d02`.
- P32-T6 validation report digest:
  `sha256:39115673fe5042dbc9b0054a9c1292e24598c3fab83733aa012c5cfa56c99268`.
- SpecPM consumer gate:
  [`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140),
  revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

## Boundary

The decision remains review evidence only. It does not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, treat AI output as registry truth, or resolve
`cupertino.core`.

Broader autonomous scraping remains blocked behind a separate follow-up task.

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'limited_corpus_intake_readiness_decision or refreshed_candidate_layer_selected_handoff or autonomous_candidate_tech_debt_plan'`
  - `3 passed, 73 deselected`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed

## Verdict

PASS. The limited corpus is review-ready, not registry-accepted.
