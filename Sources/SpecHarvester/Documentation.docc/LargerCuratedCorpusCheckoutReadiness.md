# Larger Curated Corpus Checkout Readiness

Status: P51-T3 readiness gate.

P51-T3 verifies that the 12 selected P51-T2 sources have operator-provided
pinned local checkouts before any static-only or AI-enabled larger corpus run.
It reads the P51-T2 source manifest, resolves local checkout paths, checks that
each path is a git repository, and compares observed `HEAD` with the pinned
manifest revision.

Machine-readable fixture:

```text
tests/fixtures/larger_curated_corpus_checkout_readiness/p51-t3-larger-curated-corpus-checkout-readiness.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-checkout-readiness/v0
kind: SpecHarvesterLargerCuratedCorpusCheckoutReadiness
authority: producer_larger_curated_corpus_checkout_readiness_only
```

## Inputs

P51-T3 is based on:

- `p51-t2-larger-curated-corpus-source-plan.example.json`;
- `inputs/p51-larger-curated-corpus/repositories.yml`.

The gate verifies the same 12 source ids selected by P51-T2:

```text
flask, gin, xyflow, cupertino, navigation-split-view, docc2context,
fastapi, fastmcp, specpm, hypercode, specnode, hyperprompt
```

## Result

The readiness gate passed.

| Metric | Value |
| --- | ---: |
| Selected sources | 12 |
| Manifest parsed | yes |
| Checkouts present | 12 |
| Git repositories | 12 |
| Revision matches | 12 |
| Missing checkouts | 0 |
| Revision mismatches | 0 |
| Blocking reasons | 0 |
| Sources with caveats | 2 |

P51-T4 static-only gate is allowed. P51-T5 AI-enabled gate remains blocked
until P51-T4 records passing static-only evidence.

## Caveats

Two non-blocking operator checkout caveats remain visible:

- `xyflow.operator_checkout_origin_fork_mismatch`;
- `docc2context.source_checkout_had_untracked_doccarchive`.

These caveats do not block P51-T4 because the checked revisions match the
manifest pins. They must remain visible for P51-T6 triage and P51-T7 exit
decision.

## Stop Conditions Checked

P51-T3 modeled readiness blockers for:

- `missing_pinned_local_checkout`;
- `checkout_revision_mismatch`;
- `clone_or_fetch_required`;
- `dependency_installation_required_for_basic_evidence`;
- `harvested_code_execution_required`;
- unclear checkout state.

None were present as blocking reasons in this run.

## Boundaries

P51-T3 ran the checkout readiness gate only. It did not run a larger corpus
batch, clone or fetch repositories, install dependencies, invoke package
managers, execute harvested code, run adapters, enable trusted local adapter
execution, run AI, persist raw prompts, persist raw provider responses, persist
secrets, or persist chain-of-thought.

P51-T3 does not accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, or treat readiness output, static output, AI
output, or adapter output as registry truth.
