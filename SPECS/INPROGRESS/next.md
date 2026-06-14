# Next Task: P35-T2 SpecHarvesterCorpusPlan

**Status:** Planned
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T2` Define a machine-readable `SpecHarvesterCorpusPlan`
**Last Archived:** P35-T1 Corpus Selection Policy

## Recently Archived

- `P35-T1` added [`CORPUS_SELECTION_POLICY.md`](../../docs/CORPUS_SELECTION_POLICY.md)
  and the DocC mirror `CorpusSelectionPolicy`.
- The policy establishes SpecHarvester as a bounded curated corpus builder,
  not an open-ended registry crawler.
- The policy defines repository/package-family selection units, importance
  signals, ecosystem quotas, exclusion and deferral rules, pinned local
  checkout requirements, and the producer-evidence boundary.
- The policy preserves local-only operation: no clone/fetch, dependency
  installation, harvested code execution, registry publication, package or
  relation acceptance, `preview_only` removal, or AI output as registry truth.

## Context

P35-T1 defined the semantics of source selection. P35-T2 should turn those
semantics into a machine-readable planning contract that later tasks can use
for seed corpus planning, source classification, explainable reports, and
dry-run readiness checks.

## Motivation

- Operators need a stable artifact that records why each repository or package
  family is selected before harvesting runs.
- The plan should be reviewable before local collection, deterministic
  drafting, AI enrichment, or SpecPM handoff checks execute.
- Later automation should not infer corpus scope from raw npm/PyPI/crates.io
  search results or ad hoc notes.

## Goal

Define `SpecHarvesterCorpusPlan`, a versioned machine-readable format for
curated source batches.

## Proposed Scope

- Define document identity:
  - `apiVersion`;
  - `kind`;
  - `schemaVersion`;
  - corpus name;
  - producer-evidence authority boundary.
- Define source entries:
  - ecosystem;
  - repository;
  - package family;
  - category;
  - pinned local checkout path or required checkout reference;
  - selected-because reason codes;
  - excluded or deferred subpackage reason codes;
  - expected analyzer coverage;
  - stop conditions.
- Define summary fields:
  - per-ecosystem quotas;
  - selected/deferred/rejected counts;
  - non-authority statements;
  - downstream autonomous-batch command plan.
- Add a fixture or example corpus plan that can be used by `P35-T4`.

## Acceptance

- The schema is ecosystem-neutral and does not assume npm as the default.
- Every selected source explains why it exists in the corpus.
- Every excluded or deferred source uses a reviewable reason code.
- The plan remains local-first and does not authorize clone/fetch, dependency
  installation, harvested code execution, registry publication, acceptance, or
  `preview_only` removal.
- Docs and tests make the contract visible from the primary entrypoints.
