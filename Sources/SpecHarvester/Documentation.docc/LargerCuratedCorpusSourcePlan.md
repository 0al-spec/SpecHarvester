# Larger Curated Corpus Source Plan

Status: P51-T2 source plan.

P51-T2 authors the concrete larger curated corpus source plan and manifest
criteria for the Phase 51 sequence. It is based on P51-T1 planning evidence and
prepares P51-T3 checkout readiness verification. It does not run a larger
corpus batch.

Machine-readable fixture:

```text
tests/fixtures/larger_curated_corpus_source_plan/p51-t2-larger-curated-corpus-source-plan.example.json
```

Runnable source manifest:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-source-plan/v0
kind: SpecHarvesterLargerCuratedCorpusSourcePlan
authority: producer_larger_curated_corpus_source_plan_only
```

## Source Inputs

P51-T2 is derived from:

- `p51-t1-larger-curated-corpus-planning-phase.example.json`
- `inputs/p46-bounded-popular-library-pilot/repositories.yml`
- P50 restored-checkout rerun caveats carried through P51-T1

The source plan keeps the original six P46/P50 repositories and adds six
operator-curated local checkouts:

| Repository | Family | Shape |
| --- | --- | --- |
| `flask` | Python | single package |
| `gin` | Go | single package |
| `xyflow` | JavaScript/TypeScript | workspace/monorepo |
| `cupertino` | Swift | single package |
| `navigation-split-view` | Swift | single package |
| `docc2context` | Swift, documentation-heavy | single package |
| `fastapi` | Python, documentation-heavy | single package |
| `fastmcp` | Python | framework/runtime library |
| `specpm` | Python, Swift, documentation-heavy | tooling/workspace |
| `hypercode` | Swift, documentation-heavy | framework/workspace |
| `specnode` | Swift | framework/single package |
| `hyperprompt` | Swift, documentation-heavy | tooling/workspace |

The total repository count is 12, which is inside the P51-T1 target range of
10 to 16 repositories.

## Manifest Criteria

Every selected source must provide:

- stable `id`;
- `repository` URL;
- exact 40-character `revision`;
- operator-local `checkout`;
- expected `packageId`;
- ecosystem and shape `labels`.

The manifest is intentionally compatible with the existing
`read_repository_source_manifests` parser. Extended rationale lives in the JSON
fixture so the manifest can stay runnable data.

## Stop Conditions

P51-T3 must block readiness on:

- `missing_pinned_local_checkout`;
- `checkout_revision_mismatch`;
- `clone_or_fetch_required`;
- `dependency_installation_required_for_basic_evidence`;
- `harvested_code_execution_required`;
- `unclear_license_or_source_boundary`.

P51-T2 does not resolve these conditions. It defines them so P51-T3 can verify
them deterministically.

## Carried-Forward Caveats

P51-T2 preserves caveats from the restored six-repository evidence, including:

- `xyflow.partial_public_interface_index`;
- `xyflow.operator_checkout_origin_fork_mismatch`;
- `navigation-split-view.aiEnrichment.ai_json_repair_needed`;
- `docc2context.aiDraft.excluded_package_also_selected`;
- `docc2context.source_checkout_had_untracked_doccarchive`.

These are not registry blockers at source-plan time, but they remain review
evidence for P51-T7 triage and P51-T8 exit decision.

## Next Gate

P51-T2 selects P51-T3:

```text
Run the larger curated corpus checkout readiness gate
```

P51-T3 must resolve the manifest checkout paths without clone/fetch and compare
each observed local HEAD against the pinned revision before any static-only or
AI-enabled batch can run.

## Boundaries

P51-T2 does not run a larger corpus batch, run checkout readiness, clone or
fetch repositories, install dependencies, invoke package managers, execute
harvested code, run adapters, enable trusted local adapter execution, run AI,
persist raw prompts, persist raw provider responses, persist secrets, or
persist chain-of-thought.

P51-T2 does not accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, or treat source-plan output, AI output,
static output, or adapter output as registry truth.
