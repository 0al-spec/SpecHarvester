# Next Task: P35-T4 Multi-Ecosystem Seed Corpus Plan

**Status:** Planned
**Phase:** Phase 35. Curated Multi-Ecosystem Corpus Selection
**Task:** `P35-T4` Create the first multi-ecosystem seed corpus plan
**Last Archived:** P35-T3 Candidate Source Classifier Plan

## Recently Archived

- `P35-T3` added
  [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](../../docs/CANDIDATE_SOURCE_CLASSIFIER_PLAN.md)
  and the DocC mirror `CandidateSourceClassifierPlan`.
- The classifier plan defines
  `SpecHarvesterCandidateSourceClassificationPlan` with
  `apiVersion: spec-harvester.source-classification-plan/v0`,
  `schemaVersion: 1`, and `authority: producer_classification_plan_only`.
- The fixture
  `tests/fixtures/source_classifier_plan/p35-t3-source-classifier-plan.example.json`
  covers package-set root, primary package, plugin, example, tooling,
  type-only, generated, internal, deprecated, and evidence-only classes.
- The classifier plan records allowed actions: `select_primary`,
  `select_member`, `defer`, `exclude`, and `include_as_evidence_only`.

## Context

P35-T1 defined the selection policy, P35-T2 defined the corpus plan shape, and
P35-T3 defined source classification. P35-T4 should now create the first
bounded multi-ecosystem seed corpus plan that uses those contracts without
running collection or publishing registry metadata.

## Motivation

- The project needs a concrete seed corpus to avoid arguing only from abstract
  policy.
- The seed corpus should represent important libraries across ecosystems while
  remaining small enough for review.
- The plan must be explicit about selected, deferred, and rejected sources
  before autonomous candidate generation runs.

## Goal

Create the first multi-ecosystem seed corpus plan artifact for Phase 35.

## Proposed Scope

- Select a small bounded corpus across JavaScript/TypeScript, Python, Rust,
  Go, and at least one additional ecosystem.
- Use `SpecHarvesterCorpusPlan` fields and reason codes.
- Include source-classification expectations from P35-T3.
- Record selected, deferred, and rejected sources.
- Preserve local checkout requirements and non-authority boundaries.
- Do not run collection, drafting, AI enrichment, or SpecPM handoff in this
  task.

## Acceptance

- The seed plan is machine-readable and references the P35-T2/P35-T3 contract
  shape.
- Every selected source has an ecosystem, repository, package family,
  selected-because reason codes, local checkout expectation, expected analyzer
  coverage, and stop conditions.
- No source requires clone/fetch, dependency installation, harvested code
  execution, registry publication, package acceptance, relation acceptance,
  baseline seeding, `preview_only` removal, or AI output as registry truth.
- The plan does not require clone/fetch, dependency installation, harvested
  code execution, registry publication, package acceptance, relation
  acceptance, baseline seeding, `preview_only` removal, or AI output as
  registry truth.
- The next task remains `P35-T5` explainable corpus selection report.
