# Larger Curated Corpus Exit Decision

Status: P51-T8 result.

P51-T8 records the exit decision for Phase 51 after the larger curated corpus
output triage. The decision is evidence-only: it does not approve further
larger corpus expansion, accept packages, accept relations, publish registry
metadata, seed baselines, remove `preview_only`, or treat exit-decision output
as registry truth.

The durable fixture is:

```text
tests/fixtures/larger_curated_corpus_exit_decision/p51-t8-larger-curated-corpus-exit-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-exit-decision/v0
kind: SpecHarvesterLargerCuratedCorpusExitDecision
authority: producer_exit_decision_evidence_only
```

Evidence input:

```text
tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json
```

Source digest:

```text
sha256:6c757fe4c65546404076a5b4b4d45d09b8f815859495fa467dc6a1e9cd9b8b11
```

## Decision

Selected outcome:

```text
complete_phase_51_with_author_review_evidence_no_further_expansion
```

P51-T7 classified all larger curated corpus output layers and found that no
larger curated corpus rerun is required for the exit decision. P51-T8 therefore
closes Phase 51 as author-review evidence ready.

That is a narrow decision. It means selected, deferred, and do-not-promote
evidence is now organized enough for a maintainer or author to review. It does
not mean registry promotion is allowed, and it does not approve further larger
corpus expansion.

## Evidence Summary

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

The selected static package evidence remains author-review evidence:

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

The deferred static packages and relation proposals remain visible:

```text
xyflow.react
xyflow.svelte
xyflow.system
xyflow.workspace
xyflow.workspace.contains.xyflow.react
xyflow.workspace.contains.xyflow.svelte
xyflow.workspace.contains.xyflow.system
```

The do-not-promote sidecar evidence remains visible:

```text
hyperprompt.aiDraft.p51-t5
specnode.aiEnrichment
```

## Rejected Alternatives

P51-T8 rejects another targeted pass before exit because P51-T7 classified all
output layers and set `largerCuratedCorpusRerunRequired` to false.

P51-T8 rejects stopping on a hard documented blocker because the previous
`hyperprompt.aiDraft` hard blocker is superseded by the P51-T6 deterministic
single-package fallback. The fallback remains proposal-only and carries
`hyperprompt.single_package_deterministic_fallback_applied`, but it is no
longer a hard runtime or AI draft blocker for the exit decision.

P51-T8 rejects approving further larger corpus expansion because P51-T7 still
records five registry-promotion blockers and no Phase 52 scope is selected.

## Carried-Forward Caveats

P51-T8 carries four caveats forward:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`
- `hyperprompt.single_package_deterministic_fallback_applied`

These caveats do not block the P51-T8 exit decision. They do block registry
promotion until a maintainer explicitly disposes them.

The fifth registry-promotion blocker is:

```text
specnode.model_evidence_path_unsupported
```

## Next State

Phase 51 is complete. There is no next task selected by P51-T8.

The practical follow-up is maintainer disposition of selected, deferred, and
do-not-promote evidence before any further expansion. Further expansion is not
approved, and registry promotion is not allowed.

## Boundary

P51-T8 did not rerun the larger corpus, run AI, run adapters, enable trusted
local adapter execution, clone or fetch repositories, install dependencies,
invoke package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The exit decision does not treat static output as registry truth, readiness
output as registry truth, AI output as registry truth, enriched preview output
as registry truth, repair output as registry truth, rerun output as registry
truth, planning output as registry truth, triage output as registry truth,
exit-decision output as registry truth, or adapter output as registry truth.
