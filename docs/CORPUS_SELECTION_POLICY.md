# Corpus Selection Policy

Status: planned policy for Phase 35.

SpecHarvester is a bounded curated corpus builder, not an open-ended registry
crawler. It should help operators produce author-ready starter packages for
important libraries, while leaving SpecPM acceptance, registry publication, and
maintainer decisions outside the harvester.

## Problem

Registry popularity search is a noisy source selection mechanism.

For example, an npm search for `react` sorted by downloads can mix:

- framework/runtime packages;
- unrelated high-download infrastructure packages;
- internal utilities;
- types-only packages;
- shims and compatibility packages;
- parsers and build tooling;
- generated artifacts;
- examples and test fixtures.

Those packages may be useful in an ecosystem map, but they are not all good
targets for author-ready SpecPM starter packages. A raw popularity crawl would
make SpecHarvester collect broad ecosystem plumbing instead of intentionally
selected libraries.

## Selection Unit

The primary selection unit is a repository or package family, not an isolated
registry search hit.

Preferred targets have:

- a public source repository;
- a clear package family or root project identity;
- stable license evidence;
- public API or user-facing behavior worth specifying;
- enough static evidence for local collection and review;
- a maintainer or author review path.

For monorepos, selection should name both the repository and the intended
package family, such as:

```text
repository: radix-ui/primitives
packageFamily: radix-ui.react-primitives
```

For single-package repositories, the package family can match the package id,
such as:

```text
repository: uuidjs/uuid
packageFamily: uuid.core
```

## Importance Signals

Selection should combine multiple signals. No single number, including
download count or GitHub stars, is sufficient.

Required signal names are: dependency centrality, registry usage, public API
richness, ecosystem archetype coverage, release and maintenance health, source
availability, license clarity, security and supply-chain relevance, and
author/maintainer review value.

| Signal | Meaning |
| --- | --- |
| Dependency centrality | Many downstream projects depend on the package or repository. |
| Registry usage | Downloads, dependents, or ecosystem registry prominence indicate real usage. |
| Public API richness | The project exposes a meaningful API, protocol, CLI, SDK, framework, parser, or runtime surface. |
| Ecosystem archetype coverage | The project represents a useful category such as framework, UI library, SDK, CLI, data layer, parser, runtime, or tooling interface. |
| Release and maintenance health | Recent releases, stable maintainers, issue hygiene, and active security handling make review useful. |
| Source availability | The source repository is public and can be pinned as a local checkout. |
| License clarity | License evidence is present and reviewable. |
| Security and supply-chain relevance | The project is central enough that bad metadata would matter downstream. |
| Author/maintainer review value | A generated starter spec would plausibly help an author or maintainer improve the package contract. |

## Ecosystem Quotas

Corpus plans should stay small and deliberately mixed. A batch should not spend
all of its capacity on one registry or one language family unless the task
explicitly says so.

The first multi-ecosystem seed corpus should include JavaScript/TypeScript,
Python, Rust, Go, and at least one additional ecosystem such as Java/Kotlin,
.NET, Swift, Ruby, or PHP.

Each selected ecosystem should include a small number of high-value targets
that exercise different repository shapes:

- single-package library;
- package-set or monorepo;
- framework or runtime;
- SDK or client library;
- CLI or tool surface;
- parser, schema, or data-layer library where relevant.

## Exclusion and Deferral Rules

Exclude or defer packages when they are poor author-ready starter package
targets for the current corpus.

Required exclusion class names are: internal utilities, types-only packages,
generated-only packages, deprecated sources, examples and test fixtures, build
tooling, and registry search noise.

| Class | Default decision | Reason |
| --- | --- | --- |
| Internal utility | Defer unless intentionally selected as part of a package-set | Usually not a standalone author-facing contract. |
| Types-only package | Defer to a dedicated type-definition archetype | It does not describe the runtime library itself. |
| Generated-only package | Defer | Static evidence can be misleading without generation provenance. |
| Deprecated source | Defer or reject | New starter specs should not privilege abandoned APIs without explicit rationale. |
| Examples and test fixtures | Exclude | They are evidence, not package targets. |
| Build tooling internals | Defer | Often implementation plumbing rather than public package intent. |
| Registry search noise | Exclude | Popularity search can return unrelated high-download packages. |
| Missing public source | Defer | SpecHarvester requires pinned local checkouts. |
| Unclear license | Defer | License evidence must be reviewable before corpus execution. |

Deferral is not a rejection of usefulness. It means the package needs a more
specific corpus plan, classifier, or review policy before autonomous drafting.

## Local Checkout Requirement

Corpus execution remains local-first. A selected source must have a pinned
local checkout before collection starts.

The policy does not authorize SpecHarvester to:

- clone repositories;
- fetch remotes;
- install dependencies;
- run package scripts;
- run harvested tests;
- execute harvested code;
- contact registries during harvesting;
- access secrets or private credentials.

Network-derived popularity or registry information can inform human selection,
but the harvesting run itself consumes local pinned checkouts.

## Required Selection Explanation

Every selected source should carry machine-readable rationale in the later
`SpecHarvesterCorpusPlan` work:

```json
{
  "repository": "example/library",
  "ecosystem": "npm",
  "packageFamily": "example.library",
  "selectedBecause": [
    "high_dependency_centrality",
    "public_api_rich",
    "framework_archetype"
  ],
  "excludedSubpackages": [
    {
      "name": "example-internal-test-utils",
      "reason": "test_fixture"
    }
  ]
}
```

The concrete planning contract is
[`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md).

## Review Boundary

Selection does not imply package quality, package acceptance, or registry
publication. It only says that a source is worth attempting as producer
evidence.

SpecHarvester may produce:

- collected static evidence;
- candidate package or package-set drafts;
- AI proposal artifacts;
- enriched preview candidate copies;
- validation and quality reports;
- selected/deferred handoff evidence.

SpecHarvester must not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- publish registry metadata;
- create or merge SpecPM pull requests without a separate trusted flow;
- treat AI output as maintainer approval;
- treat AI output as upstream project endorsement;
- treat generated output as registry truth.

## Follow-Up Tasks

This policy unlocks the rest of Phase 35:

- `P35-T2`: define
  [`SpecHarvesterCorpusPlan`](SPECHARVESTER_CORPUS_PLAN.md);
- `P35-T3`: define candidate source classification;
- `P35-T4`: create the first multi-ecosystem seed corpus;
- `P35-T5`: emit explainable corpus selection reports;
- `P35-T6`: run or document dry-run readiness for the selected corpus plan.
