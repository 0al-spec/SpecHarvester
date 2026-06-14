# Next-Corpus Source Manifest

Status: P33-T2 source fixture for the next bounded corpus.

This document records the first concrete input for Phase 33. It does not run
collection, drafting, local-model enrichment, candidate-layer triage, or SpecPM
preflight. It only defines which existing local checkouts are allowed to enter
the next dry-run sequence.

## Artifacts

- Source manifest:
  `inputs/p33-next-corpus/repositories.yml`
- Companion fixture:
  `tests/fixtures/next_corpus_source_manifest/p33-t2-next-corpus-source-manifest.example.json`
- Fixture kind:
  `SpecHarvesterNextCorpusSourceManifestFixture`
- Fixture API:
  `spec-harvester.next-corpus-source-manifest/v0`

## Selected Corpus

The fixture contains exactly five repositories:

| ID | Package ID | Expected package shape | Revision |
| --- | --- | --- | --- |
| `serena` | `serena.core` | `single_python_agent_toolkit` | `892ef9cf19e2c154a75cb58f4b34c8589eada346` |
| `transmission` | `transmission.core` | `multi_component_c_cxx_application` | `98fdf2dc0bfc77e537992ce50fa310b1c3ac636a` |
| `mcpm-sh` | `mcpm.core` | `mixed_javascript_python_registry_tool` | `3a21496dbddffa8b352797aaa498fd4f4d094161` |
| `specgraph` | `specgraph.core` | `javascript_spec_graph_tool` | `2a3e247337acb8102bd4b1d00781c095acc59b16` |
| `specpm` | `specpm.core` | `swift_python_registry_tooling` | `8a5ce3dece3d18bf8f601a5a599520bd520c7839` |

## Selection Rationale

The set is intentionally shape-diverse and bounded:

- `serena` adds a Python agent-tooling repository outside the Phase 30/32 web
  framework corpus.
- `transmission` adds a mature C/C++ CMake multi-component repository shape.
- `mcpm-sh` adds mixed JavaScript/Python registry tooling.
- `specgraph` adds JavaScript/TypeScript specification-graph tooling with
  existing local operator context.
- `specpm` adds the downstream registry-tooling repository as a controlled
  self-adjacent handoff-policy validation shape.

This selection is not a claim that these repositories are accepted SpecPM
packages or representative of every framework ecosystem.

## Manifest Requirements

Every source manifest entry has:

- stable repository ID;
- repository URL;
- exact pinned `revision`;
- local checkout path;
- package ID hint;
- review labels.

Each row records a pinned revision, and the fixture does not use mutable `ref`
values. The companion fixture records the source manifest digest so later dry
runs can prove they used the same input.

## Local-Only Policy

The manifest is operator-authored data. Reading it must not:

- clone repositories;
- fetch remote state;
- install dependencies;
- execute harvested repository code;
- run package scripts;
- perform network discovery.

In short: no network discovery is allowed for this fixture.

## Non-Authority Boundary

P33-T2 does not:

- accept packages;
- accept relations;
- create a SpecPM pull request;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth.

P33-T3 deterministic collection and draft evidence is recorded in
[`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md).
The next step is P33-T4: live local-model draft/enrichment dry run over this
same source manifest.
