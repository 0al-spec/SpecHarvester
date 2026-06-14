# Bounded Corpus Expansion Plan

Status: Current plan for Phase 33 after the Phase 32 intake readiness decision.

`P33-T1` records `SpecHarvesterBoundedCorpusExpansionPlan` with
`apiVersion: spec-harvester.bounded-corpus-expansion-plan/v0`.

The next autonomous candidate expansion is capped at five repositories and
requires a pinned local source manifest before any scrape runs.

## Gates

The next expansion uses four gates:

1. Deterministic collection and draft gate.
2. Live local-model draft/enrichment gate with bounded JSON repair.
3. Candidate-layer triage gate.
4. SpecPM-side selected handoff preflight gate.

Each gate produces review evidence only. Passing a gate does not accept a
package, accept a relation, seed a baseline, remove `preview_only`, or publish
registry metadata. The next-corpus result stops at author/maintainer review
evidence unless a later SpecPM maintainer acceptance flow is explicitly opened.

P33-T2 records the next-corpus source manifest in
<doc:NextCorpusSourceManifest>. The source manifest is
`inputs/p33-next-corpus/repositories.yml`, and the companion fixture is
`SpecHarvesterNextCorpusSourceManifestFixture` with
`apiVersion: spec-harvester.next-corpus-source-manifest/v0`.

P33-T3 records the deterministic `--skip-ai` dry run in
<doc:NextCorpusDeterministicDryRun>. It processed all five repositories,
produced five preview candidates, produced zero relation proposals, passed five
bundle-set preflights, recorded package-id review signals for `mcpm-sh` and
`specgraph`, and is ready for P33-T4 live local-model review.

P33-T4 records the live local-model dry run in
<doc:NextCorpusLiveLocalModelBatch>. It used LM Studio with
`openai/gpt-oss-20b`, preserved the deterministic five preview candidates and
zero relation proposals, passed five bundle-set preflights, produced five AI
draft proposals and five AI enrichment proposals, required zero JSON repair
attempts, recorded `76291` provider tokens, and is ready for P33-T5
candidate-layer triage.

## Source Manifest

`P33-T2` must add the next-corpus source manifest fixture before any scrape
runs. The manifest must contain repository identifiers, local checkout paths,
pinned revisions, selection rationale, expected package shapes, and no network
discovery behavior.

## Stop Conditions

The run stops on missing or invalid source manifest data, repository counts
above five, unpinned or remote checkouts, deterministic preflight failures,
source digest drift, package identity drift, local model unavailability without
a fallback policy, JSON repair exhaustion, unclassified candidate-layer states,
or SpecPM-side preflight errors.

## Boundary

Phase 33 must not clone repositories, fetch remote state, install dependencies,
execute harvested repository code, run package scripts, publish SpecPM registry
content, accept packages, accept relations, seed baselines, remove
`preview_only`, treat AI output as registry truth, or create a SpecPM pull
request unless a later trusted handoff task explicitly requests it.

## Source

Canonical source:
`docs/BOUNDED_CORPUS_EXPANSION_PLAN.md`
