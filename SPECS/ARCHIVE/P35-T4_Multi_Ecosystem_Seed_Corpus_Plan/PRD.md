# P35-T4 Multi-Ecosystem Seed Corpus Plan

## Summary

Create the first bounded multi-ecosystem seed corpus plan for autonomous
SpecHarvester runs. The task turns the Phase 35 policy, corpus-plan shape, and
source-classification plan into a concrete reviewable corpus artifact without
running collection, drafting, AI enrichment, or SpecPM handoff.

## Motivation

SpecHarvester needs a practical seed corpus before autonomous scraping can be
credible. A popularity list alone would pull in registry noise, internal helper
packages, type-only packages, and duplicate package families. P35-T4 defines a
small curated plan that tells the harvester what to try first, why each source
is selected, and where the run must stop for maintainer review.

## Deliverables

- `docs/MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md` documenting the seed corpus plan.
- DocC mirror `MultiEcosystemSeedCorpusPlan`.
- Machine-readable fixture
  `tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`.
- Links from corpus policy, corpus plan, classifier plan, capabilities,
  README, roadmap, and DocC navigation.
- Regression coverage proving the plan is bounded, multi-ecosystem,
  non-authoritative, and aligned with P35-T2/P35-T3.

## Seed Corpus Boundaries

The seed plan should include selected sources across JavaScript/TypeScript,
Python, Rust, Go, and Swift. It should also record deferred or rejected sources
so the corpus is explainable rather than a raw popularity scrape.

Selected sources must include:

- ecosystem;
- repository;
- package family;
- selected-because reason codes from the corpus plan vocabulary;
- source-classification expectations from the classifier plan;
- local checkout expectation with pinned revision required;
- expected analyzer coverage;
- stop conditions.

## Non-Goals

- No cloning or fetching new repositories.
- No dependency installation.
- No harvested code execution.
- No draft package generation.
- No AI enrichment.
- No SpecPM proposal or registry publication.
- No package acceptance, relation acceptance, baseline seeding, or
  `preview_only` removal.

## Acceptance Criteria

- The fixture uses `SpecHarvesterCorpusPlan` identity and references the
  P35-T2/P35-T3 contracts.
- At least five ecosystems are represented in selected sources.
- Every selected source has local checkout expectations and stop conditions.
- Deferred and rejected sources are present with reason codes.
- The documentation explicitly states that the plan is review evidence and not
  registry authority.
- Tests validate the fixture shape, selected/deferred/rejected decisions,
  reason-code use, source-classification expectations, and current next task.
- Flow archive and review artifacts are created.

## Validation Plan

Run:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift build --target SpecHarvesterDocs
swift package dump-package >/dev/null
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester
rm -rf .docc-build
```
