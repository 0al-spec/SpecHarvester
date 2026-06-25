# Larger Curated Corpus Output Triage

Status: P51-T7 triage report.

P51-T7 classifies the P51 larger curated corpus output after the P51-T5
AI-enabled proposal-only gate and the P51-T6 Hyperprompt repair. It does not
rerun the corpus, run AI, or change registry truth.

The durable fixture is:

```text
tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-output-triage/v0
kind: SpecHarvesterLargerCuratedCorpusOutputTriage
authority: producer_triage_evidence_only
```

## Source Evidence

P51-T7 uses these existing artifacts:

- P51-T4 static-only gate:
  `tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json`
- P51-T5 AI-enabled gate:
  `tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json`
- P51-T6 Hyperprompt fallback:
  `tests/fixtures/hyperprompt_ai_draft_single_package_fallback/p51-t6-hyperprompt-ai-draft-single-package-fallback.example.json`
- Source manifest:
  `inputs/p51-larger-curated-corpus/repositories.yml`

## Classification Vocabulary

P51-T7 uses three classifications:

- `selected_for_author_review`: evidence is suitable for human review, but is
  not registry acceptance.
- `deferred`: evidence remains useful, but a caveat, warning, or explicit exit
  decision must be handled before promotion.
- `do_not_promote`: evidence must not be used as registry-promotion input in
  its current form.

## Summary

| Metric | Count |
| --- | ---: |
| Repositories triaged | 12 |
| Static candidate packages | 15 |
| Selected static packages | 11 |
| Deferred static packages | 4 |
| Relation proposals | 3 |
| Deferred relation proposals | 3 |
| AI draft sidecars | 12 |
| AI draft selected for author review | 6 |
| AI draft deferred | 6 |
| AI draft superseded do-not-promote sidecars | 1 |
| AI enrichment sidecars | 12 |
| AI enrichment selected for author review | 8 |
| AI enrichment deferred | 3 |
| AI enrichment do-not-promote | 1 |
| AI-enriched preview prepared packages | 8 |
| AI-enriched preview skipped packages | 7 |
| Carried-forward caveats | 4 |
| Registry-promotion blockers | 5 |

## Static Package Triage

P51-T7 selects 11 static packages for author review:

```text
flask.core
gin.core
cupertino.core
navigation_split_view.core
docc2context.core
fastapi.core
fastmcp.core
specpm.core
hypercode.core
specnode.core
hyperprompt.core
```

The four `xyflow` static packages are deferred:

```text
xyflow.react
xyflow.svelte
xyflow.system
xyflow.workspace
```

They remain useful evidence, but `xyflow.partial_public_interface_index` and
`xyflow.operator_checkout_origin_fork_mismatch` must stay visible for P51-T8.

The three relation proposals are also deferred:

```text
xyflow.workspace.contains.xyflow.react
xyflow.workspace.contains.xyflow.svelte
xyflow.workspace.contains.xyflow.system
```

They should not be promoted before the `xyflow` package evidence is explicitly
disposed.

## AI Draft Triage

Six AI draft sidecars are selected for author review:

```text
xyflow.aiDraft
fastapi.aiDraft
fastmcp.aiDraft
hypercode.aiDraft
specnode.aiDraft
hyperprompt.aiDraft
```

`hyperprompt.aiDraft` uses the P51-T6 fallback evidence, not the failed P51-T5
sidecar. It remains warning-level and proposal-only with:

```text
ai_json_repair_needed
ai_json_repair_exhausted
package_set_subject_metadata_missing
single_package_deterministic_fallback_applied
```

The failed P51-T5 `hyperprompt.aiDraft` sidecar is explicitly classified as
`do_not_promote` and superseded by P51-T6.

Six AI draft sidecars are deferred because they carry warning diagnostics and
`continue_generation` stop-policy decisions:

```text
flask.aiDraft
gin.aiDraft
cupertino.aiDraft
navigation-split-view.aiDraft
docc2context.aiDraft
specpm.aiDraft
```

## AI Enrichment And Preview Triage

Eight AI enrichment sidecars are selected for author review:

```text
gin.aiEnrichment
cupertino.aiEnrichment
docc2context.aiEnrichment
fastapi.aiEnrichment
fastmcp.aiEnrichment
specpm.aiEnrichment
hypercode.aiEnrichment
hyperprompt.aiEnrichment
```

Three AI enrichment sidecars are deferred:

```text
flask.aiEnrichment
xyflow.aiEnrichment
navigation-split-view.aiEnrichment
```

`specnode.aiEnrichment` is `do_not_promote` because it carries
`model_evidence_path_unsupported`.

All AI-enriched preview copies remain `preview_only`. Prepared preview copies
are deferred review evidence, not registry input. Skipped preview copies are
`do_not_promote` in their current form.

## Caveats Carried Forward

P51-T7 carries four caveats into P51-T8:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`
- `hyperprompt.single_package_deterministic_fallback_applied`

These caveats do not block P51-T8 exit decision. They do block registry
promotion until a maintainer explicitly disposes them.

## Gate Decision

P51-T7 passes as output triage. It allows P51-T8 to record the larger curated
corpus exit decision because all output layers are classified and the previous
Hyperprompt hard blocker is superseded by P51-T6 fallback evidence.

P51-T7 does not approve a larger curated corpus expansion by itself. P51-T8
must still decide whether to proceed, run another targeted pass, or stop on a
documented blocker.

## Boundary

P51-T7 did not rerun the larger corpus, run AI, run adapters, enable trusted
local adapter execution, clone or fetch repositories, install dependencies,
invoke package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The triage does not treat static output as registry truth, AI output as
registry truth, enriched preview output as registry truth, triage output as
registry truth, or adapter output as registry truth.
