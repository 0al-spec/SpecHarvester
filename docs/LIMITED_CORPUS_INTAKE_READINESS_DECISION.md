# Limited Corpus Intake Readiness Decision

Status: P32-T7 recorded intake readiness for the bounded P30/P32 corpus.

The machine-readable fixture is:

```text
tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json
```

Its identity is:

```json
{
  "apiVersion": "spec-harvester.limited-corpus-intake-readiness-decision/v0",
  "kind": "SpecHarvesterLimitedCorpusIntakeReadinessDecision",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

## Inputs

P32-T7 does not run a new harvest, does not call LM Studio, and does not
regenerate candidate bundles. It records a decision from two committed inputs:

- P32-T5 refreshed selected handoff:
  `tests/fixtures/refreshed_candidate_layer_selected_handoff/p32-t5-refreshed-candidate-layer-selected-handoff.example.json`;
- P32-T6 SpecPM consumer preflight validation:
  `SPECS/ARCHIVE/P32-T6_SpecPM_Selected_Candidate_Handoff_Preflight/P32-T6_Validation_Report.md`.

The SpecPM consumer gate was merged in
[`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140) at
revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

## Decision

The limited corpus decision is:

```text
ready_for_author_maintainer_review_with_explicit_deferral
```

The selected preview candidates are ready for author/maintainer review:

| Candidate | Disposition |
| --- | --- |
| `flask.core` | `ready_for_author_maintainer_review` |
| `gin.core` | `ready_for_author_maintainer_review` |
| `docc2context.core` | `ready_for_author_maintainer_review` |
| `xyflow.workspace` | `ready_for_author_maintainer_review` |
| `xyflow.react` | `ready_for_author_maintainer_review` |
| `xyflow.svelte` | `ready_for_author_maintainer_review` |
| `xyflow.system` | `ready_for_author_maintainer_review` |
| `navigation_split_view.core` | `ready_for_author_maintainer_review` |

`cupertino.core` remains deferred until `refined_summary_missing` is resolved
by regenerated enrichment or author-curated summary evidence.

## SpecPM Gate Result

The P32-T5 fixture passed
`specpm producer-bundle preflight-selected-candidate-handoff` with:

- `selectedCandidateCount: 8`;
- `deferredCandidateCount: 1`;
- `digestVerifiedCount: 3`;
- `warningCount: 0`;
- `errorCount: 0`.

This proves the handoff is internally consistent review evidence. It does not
make the generated candidates accepted SpecPM packages.

## Expansion Boundary

The limited corpus is ready to stop regeneration loops and move to review, but
broader autonomous scraping is not automatically allowed. Any next corpus
expansion must be planned as a separate follow-up task with its own source
manifest, bounded repository count, validation gate, and stop conditions.

## Non-Authority Boundary

This decision does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as registry truth;
- replace author or maintainer review;
- resolve `cupertino.core`.

Short form: the limited corpus is review-ready, not registry-accepted.
