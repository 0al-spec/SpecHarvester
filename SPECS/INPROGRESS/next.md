# Next Task: P35-T3 Candidate Source Classifier Plan

**Status:** In Progress
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T3` Add a candidate source classifier plan
**Branch:** `feature/P35-T3-source-classifier-plan`
**Last Archived:** P35-T2 SpecHarvesterCorpusPlan

## Recently Archived

- `P35-T2` added [`SPECHARVESTER_CORPUS_PLAN.md`](../../docs/SPECHARVESTER_CORPUS_PLAN.md)
  and the DocC mirror `SpecHarvesterCorpusPlan`.
- The contract defines `apiVersion: spec-harvester.corpus-plan/v0`,
  `kind: SpecHarvesterCorpusPlan`, `schemaVersion: 1`, and
  `authority: producer_corpus_plan_only`.
- The fixture
  `tests/fixtures/corpus_plan/p35-t2-corpus-plan.example.json` records
  selected, deferred, and rejected source decisions across npm, PyPI, crates,
  Go, and Swift.
- The plan shape records source status, ecosystem, repository, package family,
  categories, local checkout expectations, selected/deferred/rejected reason
  codes, excluded subpackages, expected analyzer coverage, stop conditions, and
  non-authority statements.

## Context

P35-T2 defined how to represent selected, deferred, and rejected corpus sources.
P35-T3 should define how SpecHarvester classifies package-like source units
before drafting so package-set roots, primary packages, plugins, examples,
tooling, type-only packages, generated artifacts, internal utilities, and
deprecated sources are handled consistently.

## Motivation

- Corpus plans can declare selected and excluded sources, but later automation
  still needs a deterministic classification vocabulary.
- Without a classifier plan, package-set drafting can accidentally promote
  examples, internal utilities, types-only packages, generated artifacts, or
  build tooling as primary package candidates.
- The classifier should make decisions explainable before autonomous candidate
  generation runs.

## Goal

Document the candidate source classifier plan for Phase 35.

## Proposed Scope

- Define source classes:
  - `package_set_root`;
  - `primary_package`;
  - `plugin_package`;
  - `example_package`;
  - `tooling_package`;
  - `types_only_package`;
  - `generated_artifact`;
  - `internal_utility`;
  - `deprecated_source`;
  - `evidence_only`.
- Define classifier inputs:
  - corpus plan source entries;
  - repository source manifests;
  - workspace inventory;
  - package manifests;
  - static evidence paths;
  - explicit operator overrides.
- Define output shape for classification evidence.
- Preserve local-only, non-authority boundaries.

## Acceptance

- The plan explains which source classes may become primary candidates and
  which must remain excluded, deferred, or evidence-only.
- The plan describes how classification results should feed `P35-T4` seed
  corpus planning and later explainable reports.
- The plan does not implement a classifier yet unless the task explicitly
  chooses a small documentation-only fixture.
- The boundary remains local-first and does not authorize clone/fetch,
  dependency installation, harvested code execution, registry publication,
  acceptance, or `preview_only` removal.
