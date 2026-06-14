# Corpus Selection Policy

SpecHarvester is a bounded curated corpus builder, not an open-ended registry
crawler.

The policy for Phase 35 is to select important repositories and package
families intentionally before autonomous candidate generation runs. Raw
registry popularity search is useful context, but it is too noisy to be the
source of truth for harvesting.

## Selection Unit

The preferred selection unit is a repository or package family, not an isolated
registry search hit.

Good targets usually have public source, clear package-family identity, stable
license evidence, meaningful public API or behavior, enough static evidence for
local review, and a plausible author/maintainer review path.

For monorepos, the corpus plan should name both repository and package family.
For single-package repositories, the package family may match the package id.

## Importance Signals

Selection combines multiple signals:

- dependency centrality;
- registry usage;
- public API richness;
- ecosystem archetype coverage;
- release and maintenance health;
- source availability;
- license clarity;
- security and supply-chain relevance;
- author/maintainer review value.

No single ranking, including download count or GitHub stars, is sufficient.

## Exclusions and Deferrals

The policy excludes or defers noisy sources before drafting:

- internal utilities;
- types-only packages;
- generated-only packages;
- deprecated sources;
- examples and test fixtures;
- build tooling internals;
- registry search noise;
- sources without public pinned local checkouts;
- sources with unclear license evidence.

Deferral is not a permanent rejection. It means the source needs a more
specific corpus plan, classifier, or review policy before autonomous drafting.

## Ecosystem Scope

The first multi-ecosystem corpus should cover JavaScript/TypeScript, Python,
Rust, Go, and at least one additional ecosystem such as Java/Kotlin, .NET,
Swift, Ruby, or PHP.

Corpus plans should use per-ecosystem quotas so one registry or language family
does not consume the whole batch.

## Local-Only Boundary

Selected sources must already exist as pinned local checkouts.

This policy does not authorize SpecHarvester to clone repositories, fetch
remotes, install dependencies, run package scripts, run harvested tests,
execute harvested code, contact registries during harvesting, or access
secrets.

## Review Boundary

Selection means a source is worth attempting as producer evidence. It does not
accept packages, accept relations, seed baselines, remove `preview_only`,
publish registry metadata, create or merge SpecPM pull requests, treat AI
output as maintainer approval, treat AI output as upstream endorsement, or
treat generated output as registry truth.

## Follow-Up Work

Phase 35 continues with:

- `P35-T2`: `SpecHarvesterCorpusPlan`;
- `P35-T3`: candidate source classification;
- `P35-T4`: first multi-ecosystem seed corpus;
- `P35-T5`: explainable corpus selection report;
- `P35-T6`: selected corpus dry-run readiness.
