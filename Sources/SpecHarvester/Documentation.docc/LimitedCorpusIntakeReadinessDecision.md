# Limited Corpus Intake Readiness Decision

This page mirrors `docs/LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`.

Status: P32-T7 recorded intake readiness for the bounded P30/P32 corpus.

The fixture is:

```text
tests/fixtures/limited_corpus_intake_readiness_decision/p32-t7-limited-corpus-intake-readiness-decision.example.json
```

Its identity is `SpecHarvesterLimitedCorpusIntakeReadinessDecision` with
`apiVersion: spec-harvester.limited-corpus-intake-readiness-decision/v0`,
`schemaVersion: 1`, and `authority: producer_preview_evidence_only`.

## Inputs

P32-T7 records a decision from committed evidence only:

- P32-T5 refreshed selected handoff;
- P32-T6 SpecPM consumer preflight validation;
- SpecPM PR [0al-spec/SpecPM#140](https://github.com/0al-spec/SpecPM/pull/140)
  at revision `8a5ce3dece3d18bf8f601a5a599520bd520c7839`.

It does not run a new harvest, call LM Studio, or regenerate candidate bundles.

## Decision

The decision is
`ready_for_author_maintainer_review_with_explicit_deferral`.

The selected preview candidates are ready for author/maintainer review:
`flask.core`, `gin.core`, `docc2context.core`, `xyflow.workspace`,
`xyflow.react`, `xyflow.svelte`, `xyflow.system`, and
`navigation_split_view.core`.

`cupertino.core` remains deferred until `refined_summary_missing` is resolved
by regenerated enrichment or author-curated summary evidence.

## SpecPM Gate Result

The P32-T5 fixture passed
`specpm producer-bundle preflight-selected-candidate-handoff` with eight
selected candidates, one deferred candidate, zero warnings, zero errors, and
three source digests verified.

## Expansion Boundary

The limited corpus is ready to stop regeneration loops and move to review, but
broader autonomous scraping still requires a separate follow-up task with its
own source manifest, bounded repository count, validation gate, and stop
conditions.

## Non-Authority Boundary

The decision does not accept packages, accept relations, seed baselines, remove
`preview_only`, publish registry metadata, create a SpecPM pull request, treat
AI output as registry truth, replace author or maintainer review, or resolve
`cupertino.core`.

Short form: the limited corpus is review-ready, not registry-accepted.

See also <doc:AutonomousCandidateTechDebtPlan>,
<doc:RefreshedCandidateLayerSelectedHandoff>, and <doc:SpecPMHandoff>.
