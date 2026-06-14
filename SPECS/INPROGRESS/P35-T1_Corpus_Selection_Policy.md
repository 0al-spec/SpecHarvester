# P35-T1 Corpus Selection Policy

## Summary

Document the corpus selection policy that keeps autonomous harvesting bounded,
multi-ecosystem, and explainable.

Phase 34 made AI-enabled preview output useful for author-ready draft review.
P35-T1 defines the upstream selection boundary before running broader
autonomous batches: SpecHarvester should choose important repositories and
package families intentionally, not crawl every package returned by registry
search rankings.

## Motivation

- Registry search results mix important libraries with internal utilities,
  type packages, generated artifacts, shims, examples, tooling, and unrelated
  high-download packages.
- SpecHarvester needs a corpus policy that works across ecosystems instead of
  encoding npm-specific assumptions.
- Operators need a reviewable explanation for each selected source before
  local collection, drafting, AI enrichment, and SpecPM handoff checks run.

## Deliverables

1. Add a GitHub docs page for corpus selection policy.
2. Add a DocC mirror for the same policy.
3. Link the policy from primary docs, capabilities, roadmap, and Flow planning
   files.
4. Define importance signals, exclusion/deferral rules, ecosystem quotas,
   local checkout requirements, and non-authority boundaries.
5. Capture the follow-up task boundary for `SpecHarvesterCorpusPlan`, source
   classification, seed corpus planning, explainable selection reports, and
   dry-run readiness checks.
6. Add regression coverage proving the policy remains visible from primary
   documentation and retains the intended safety boundaries.

## Policy Scope

The policy must describe:

- importance signals:
  - dependency centrality;
  - registry usage;
  - public API richness;
  - ecosystem archetype coverage;
  - release and maintenance health;
  - source availability and license clarity;
  - security and supply-chain relevance;
  - author/maintainer review value;
- exclusion and deferral rules:
  - internal utilities;
  - types-only packages;
  - generated-only packages;
  - deprecated sources;
  - examples and test fixtures;
  - build tooling;
  - registry search noise;
- corpus bounds:
  - operator-selected sources;
  - per-ecosystem quotas;
  - pinned local checkout requirements;
  - repository/package-family selection rather than isolated package search
    hits;
- non-authority boundary:
  - no clone/fetch;
  - no dependency install;
  - no harvested code execution;
  - no registry publication;
  - no package or relation acceptance;
  - no `preview_only` removal;
  - no AI output as registry truth.

## Acceptance Criteria

- The policy clearly states that SpecHarvester is a bounded curated corpus
  builder, not an open-ended crawler.
- The policy covers JavaScript/TypeScript, Python, Rust, Go, and at least one
  additional ecosystem without treating npm as the default model.
- The policy explains how sources are selected, excluded, or deferred.
- The policy records follow-up artifacts required before practical corpus
  execution: corpus plan schema, source classifier, seed corpus, explainable
  selection report, and dry-run readiness check.
- Docs, DocC, roadmap, capabilities, Workplan, and `next.md` point to the
  policy or its task boundary.

## Non-Goals

- No implementation of the `SpecHarvesterCorpusPlan` schema in this task.
- No source classifier implementation.
- No new corpus run.
- No repository clone/fetch.
- No dependency installation.
- No harvested code execution.
- No SpecPM package or relation acceptance.
- No registry publication.
- No `preview_only` removal.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
