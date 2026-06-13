# Next Task: P33-T4 Live Local-Model Next-Corpus Dry Run

**Status:** Selected
**Selected:** 2026-06-14
**Task:** P33-T4 Live Local-Model Next-Corpus Dry Run
**Phase:** Phase 33. Bounded Corpus Expansion Planning
**Last Archived:** P33-T3 Deterministic Next-Corpus Dry Run

## Recently Archived

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
- `P33-T3` recorded the deterministic next-corpus dry run in
  `docs/NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`,
  `<doc:NextCorpusDeterministicDryRun>`, and
  `tests/fixtures/next_corpus_deterministic_dry_run/p33-t3-next-corpus-deterministic-dry-run.example.json`.
  The fixture identity is `SpecHarvesterNextCorpusDeterministicDryRun` with
  `apiVersion: spec-harvester.next-corpus-deterministic-dry-run/v0`. It processed
  five repositories, produced five preview candidates, zero relation proposals,
  and five bundle-set preflights. It recorded `mcpm.system` and
  `specgraph.system` package-id review signals and is ready for P33-T4 live
  local-model review. It remains review evidence only, does not accept
  packages, does not accept relations, and does not remove `preview_only`.

## Current Selection

Implement `P33-T4`: run the next-corpus live local-model draft/enrichment dry
run over the same five repositories in `inputs/p33-next-corpus/repositories.yml`.

The live local-model run must record:

- provider receipts;
- bounded JSON repair outcomes;
- candidate counts;
- relation counts, if any;
- AI draft/enrichment status;
- package-id review signals carried forward from P33-T3;
- whether every repository can proceed to candidate-layer triage.

## Boundaries

This task must not clone repositories, fetch remote state, install
dependencies, execute harvested code, run package scripts, publish registry
metadata, accept packages, accept relations, seed baselines, remove
`preview_only`, create a SpecPM pull request, or treat AI output as registry
truth.

It must not accept packages and must not publish registry metadata.
