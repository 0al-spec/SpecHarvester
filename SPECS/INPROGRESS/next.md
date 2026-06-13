# Next Task: P33-T3 Deterministic Next-Corpus Dry Run

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P33-T3 Deterministic Next-Corpus Dry Run
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T2 Next-Corpus Source Manifest Fixture

## Recently Archived

- `P33-T1` recorded the bounded corpus expansion plan in
  `docs/BOUNDED_CORPUS_EXPANSION_PLAN.md`,
  `<doc:BoundedCorpusExpansionPlan>`, and
  `tests/fixtures/bounded_corpus_expansion_plan/p33-t1-bounded-corpus-expansion-plan.example.json`.
  The fixture identity is `SpecHarvesterBoundedCorpusExpansionPlan` with
  `apiVersion: spec-harvester.bounded-corpus-expansion-plan/v0`. It caps the
  next batch at a five-repository limit, requires a source manifest, defines
  deterministic and live-model validation gates, candidate-layer triage,
  SpecPM-side selected handoff preflight, stop conditions, and keeps the result
  as review evidence only. It does not accept packages, does not accept
  relations, and does not remove `preview_only`.
- `P33-T2` recorded the next-corpus source manifest fixture in
  `docs/NEXT_CORPUS_SOURCE_MANIFEST.md`,
  `<doc:NextCorpusSourceManifest>`,
  `inputs/p33-next-corpus/repositories.yml`, and
  `tests/fixtures/next_corpus_source_manifest/p33-t2-next-corpus-source-manifest.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusSourceManifestFixture` with
  `apiVersion: spec-harvester.next-corpus-source-manifest/v0`. It selects
  `serena`, `transmission`, `mcpm-sh`, `specgraph`, and `specpm`, records exact
  pinned revisions, allows no network discovery, and remains review evidence
  only. It does not clone, does not fetch, does not install dependencies, and
  does not execute harvested code.

## Current Selection

Implement `P33-T3`: run the deterministic collection and draft dry run over
`inputs/p33-next-corpus/repositories.yml` without AI.

The dry run must record:

- candidate counts;
- relation counts, if any;
- preflight outcomes;
- blocker classes;
- source manifest digest;
- whether every repository can proceed to live local-model review.

## Boundaries

This task must not run live local-model calls, clone repositories, fetch remote
state, install dependencies, execute harvested code, run package scripts,
publish registry metadata, accept packages, accept relations, seed baselines,
remove `preview_only`, or treat AI output as registry truth.

It must not accept packages and must not publish registry metadata.
