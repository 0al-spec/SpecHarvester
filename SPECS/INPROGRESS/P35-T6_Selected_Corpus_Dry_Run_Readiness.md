# P35-T6 Selected Corpus Dry-Run Readiness

## Summary

Add a selected corpus dry-run readiness report for the Phase 35 seed corpus.
The report verifies whether the selected P35-T4 sources are ready to enter an
`autonomous-candidate-batch` dry run by checking local checkout requirements,
package-family targets, expected analyzer coverage, and stop conditions.

## Motivation

P35-T4 selected a bounded seed corpus and P35-T5 explained the choices. Before
any autonomous collection starts, SpecHarvester needs a durable readiness
artifact that says whether those selected sources can be run safely. If pinned
local checkouts are missing or unverified, the correct result is not to run the
batch; it is to stop with an explicit operator action.

## Deliverables

- `docs/SELECTED_CORPUS_DRY_RUN_READINESS.md`.
- DocC mirror `SelectedCorpusDryRunReadiness`.
- Fixture
  `tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json`.
- Links from the seed corpus plan, explainable report, capabilities, README,
  roadmap, and DocC navigation.
- Regression coverage for identity, selected source coverage, package-family
  targets, analyzer expectations, stop conditions, readiness status, operator
  action items, and non-authority statements.

## Readiness Decision

The expected P35-T6 fixture should be conservative: the planned seed corpus has
review pins, but this task does not inspect real local checkouts. Therefore the
readiness report should record `blocked_pending_local_checkouts` until an
operator provides and verifies real pinned source checkouts.

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

- The readiness report is documented in GitHub Markdown and DocC.
- The fixture references the P35-T4 seed corpus plan and P35-T5 explainable
  report.
- The fixture covers `react`, `fastapi`, `serde`, `gin`, and
  `swift-argument-parser`.
- Every selected source has a package-family target, required analyzer list,
  stop conditions, and readiness status.
- Missing or unverified pinned local checkouts block readiness.
- Tests validate the report shape and docs links.
- Flow archive and review artifacts are created.
- Phase 35 is marked complete after archive if no P35 tasks remain.

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
