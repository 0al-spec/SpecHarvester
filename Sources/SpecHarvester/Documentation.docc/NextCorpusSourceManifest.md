# Next-Corpus Source Manifest

Status: P33-T2 source fixture for the next bounded corpus.

P33-T2 records `SpecHarvesterNextCorpusSourceManifestFixture` with
`apiVersion: spec-harvester.next-corpus-source-manifest/v0`.

The source manifest is `inputs/p33-next-corpus/repositories.yml`, and the
companion fixture is
`tests/fixtures/next_corpus_source_manifest/p33-t2-next-corpus-source-manifest.example.json`.

## Selected Corpus

The fixture contains exactly five repositories:

- `serena` as `serena.core` with expected shape
  `single_python_agent_toolkit`;
- `transmission` as `transmission.core` with expected shape
  `multi_component_c_cxx_application`;
- `mcpm-sh` as `mcpm.core` with expected shape
  `mixed_javascript_python_registry_tool`;
- `specgraph` as `specgraph.core` with expected shape
  `javascript_spec_graph_tool`;
- `specpm` as `specpm.core` with expected shape
  `swift_python_registry_tooling`.

Every entry uses an exact pinned revision and a local checkout path. The
fixture does not use mutable `ref` values.

## Boundary

P33-T2 does not run collection, drafting, local-model enrichment,
candidate-layer triage, or SpecPM preflight.

Reading the manifest must not clone repositories, fetch remote state, install
dependencies, execute harvested repository code, run package scripts, or
perform network discovery. In short: no network discovery is allowed for this
fixture.

The fixture does not accept packages, accept relations, create a SpecPM pull
request, publish registry metadata, seed baselines, remove `preview_only`, or
treat AI output as registry truth.

P33-T3 deterministic collection and draft evidence is recorded in
<doc:NextCorpusDeterministicDryRun>. The next step is P33-T4: live local-model
draft/enrichment dry run over this same source manifest.

## Source

Canonical source:
`docs/NEXT_CORPUS_SOURCE_MANIFEST.md`
