# P35-T5 Explainable Corpus Selection Report

## Summary

Add an explainable corpus selection report for the Phase 35 seed corpus. The
report turns the P35-T4 seed plan into a reviewable decision artifact that
summarizes selected, deferred, and rejected sources, importance signals,
exclusion reasons, quota decisions, and the downstream command plan without
running collection, drafting, AI enrichment, or SpecPM handoff.

## Motivation

The seed corpus plan is machine-readable, but reviewers need a compact artifact
that explains why each source is in or out of the corpus. This report should
make corpus selection auditable before a dry-run readiness check starts.

## Deliverables

- `docs/EXPLAINABLE_CORPUS_SELECTION_REPORT.md`.
- DocC mirror `ExplainableCorpusSelectionReport`.
- Fixture
  `tests/fixtures/explainable_corpus_selection_report/p35-t5-selection-report.example.json`.
- Links from the seed corpus plan, corpus plan, capabilities, README, roadmap,
  and DocC navigation.
- Regression coverage for identity, seed-plan reference, selected/deferred/
  rejected source decisions, importance signals, exclusion reasons, quota
  decisions, command plan, and non-authority statements.

## Report Shape

The report should use a machine-readable identity such as:

```json
{
  "apiVersion": "spec-harvester.corpus-selection-report/v0",
  "kind": "SpecHarvesterCorpusSelectionReport",
  "schemaVersion": 1,
  "authority": "producer_selection_report_only"
}
```

It should reference the P35-T4 seed plan fixture and summarize the same source
set without duplicating every analyzer expectation from the seed plan.

## Non-Goals

- No clone/fetch.
- No dependency installation.
- No harvested code execution.
- No collection or drafting.
- No AI enrichment.
- No SpecPM handoff.
- No registry publication, package acceptance, relation acceptance, baseline
  seeding, `preview_only` removal, or AI output as registry truth.

## Acceptance Criteria

- The report is documented in GitHub Markdown and DocC.
- The fixture references the P35-T4 seed corpus plan.
- The fixture records all five selected sources and the deferred/rejected
  decisions from P35-T4.
- The fixture includes quota decisions for npm, PyPI, crates, Go, and Swift.
- The fixture includes downstream autonomous-batch command plan metadata.
- Tests validate the report shape and docs links.
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
