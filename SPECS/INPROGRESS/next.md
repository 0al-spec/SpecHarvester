# Next Task: P35-T1 Corpus Selection Policy

**Status:** In Progress
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T1` Document the corpus selection policy
**Branch:** `feature/P35-T1-corpus-selection-policy`
**Last Archived:** P34-T2 Autonomous Batch AI Enriched Preview Output

## Context

Phase 34 made AI-enabled autonomous batch output useful for review: clean
package-set AI enrichment proposals can now be applied into copied enriched
preview candidates while preserving `preview_only` and keeping SpecPM as the
acceptance boundary.

The next risk is corpus quality. Registry search results such as npm
`react` sorted by downloads mix real author-facing libraries with ecosystem
plumbing, internal utilities, type packages, shims, parsers, generated
artifacts, and unrelated high-download packages. Without a selection policy,
SpecHarvester would drift toward broad crawling instead of producing strong
author-ready starter packages for important libraries.

## Motivation

- Autonomous harvesting should target important libraries and package families,
  not every popular package returned by a registry search.
- The corpus must cover more than JavaScript/TypeScript while staying bounded
  and explainable.
- Operators need to know why a repository was selected, which subpackages are
  in scope, which sources are excluded, and which evidence must exist before a
  harvesting run starts.

## Goal

Document a corpus selection policy that defines how SpecHarvester chooses
important multi-ecosystem repository/package-family targets for autonomous
candidate generation.

## Proposed Scope

- Define library importance signals:
  - dependency centrality;
  - registry usage;
  - public API richness;
  - ecosystem archetype coverage;
  - release and maintenance health;
  - source availability and license clarity;
  - security and supply-chain relevance;
  - author/maintainer review value.
- Define exclusion and deferral rules for:
  - internal utilities;
  - types-only packages;
  - generated-only packages;
  - deprecated sources;
  - examples and test fixtures;
  - build tooling;
  - registry search noise.
- Define ecosystem quota expectations for a small curated corpus across
  JavaScript/TypeScript, Python, Rust, Go, and at least one additional
  ecosystem.
- Preserve local-only operation: no clone/fetch, dependency installation,
  harvested code execution, registry publication, package acceptance, relation
  acceptance, `preview_only` removal, or AI-as-registry-truth.

## Expected Follow-Ups

- `P35-T2` Define `SpecHarvesterCorpusPlan`.
- `P35-T3` Add candidate source classifier plan.
- `P35-T4` Create the first multi-ecosystem seed corpus plan.
- `P35-T5` Add explainable corpus selection report.
- `P35-T6` Run or document selected corpus plan dry-run readiness.

## Acceptance

- The policy clearly says SpecHarvester is a bounded curated corpus builder,
  not an open-ended crawler.
- The policy covers non-JS ecosystems and avoids npm-specific assumptions.
- The policy defines why sources are selected and why noisy packages are
  excluded or deferred.
- The policy preserves the producer-evidence boundary: selected corpus entries
  do not imply SpecPM acceptance, registry publication, or maintainer approval.
