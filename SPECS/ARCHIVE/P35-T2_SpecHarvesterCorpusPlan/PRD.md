# P35-T2 SpecHarvesterCorpusPlan

## Summary

Define the machine-readable `SpecHarvesterCorpusPlan` contract for curated
multi-ecosystem source batches.

P35-T1 documented corpus selection semantics. P35-T2 turns those semantics into
a stable JSON-shaped planning artifact that later tasks can use for source
classification, seed corpus planning, explainable selection reports, and
dry-run readiness checks.

## Motivation

- Operators need a reviewable artifact that records why each repository or
  package family is selected before harvesting runs.
- Later automation should not infer corpus scope from raw registry search
  results, screenshots, or ad hoc notes.
- The contract must preserve local-only boundaries and SpecPM non-authority
  semantics before any source collection, AI enrichment, or handoff is run.

## Deliverables

1. Add a GitHub docs page for `SpecHarvesterCorpusPlan`.
2. Add a DocC mirror for the same contract.
3. Add a machine-readable example fixture for the first shape of the plan.
4. Link the contract from primary docs, capabilities, roadmap, and corpus
   selection policy.
5. Add regression coverage that validates the fixture shape and required
   non-authority fields.
6. Update Flow planning so `P35-T3` becomes the next task.

## Contract Scope

The contract should define:

- document identity:
  - `apiVersion`;
  - `kind`;
  - `schemaVersion`;
  - `authority`;
  - `corpus.name`;
- source entries:
  - `id`;
  - `ecosystem`;
  - `repository`;
  - `packageFamily`;
  - `categories`;
  - pinned local checkout expectation;
  - selected-because reason codes;
  - excluded/deferred subpackages with reason codes;
  - expected analyzer coverage;
  - stop conditions;
- summary fields:
  - per-ecosystem quotas;
  - selected/deferred/rejected counts;
  - downstream autonomous-batch command plan;
  - non-authority statements.

## Acceptance Criteria

- The contract is ecosystem-neutral and does not assume npm as the default.
- Every selected source explains why it exists in the corpus.
- Every excluded or deferred source uses a reviewable reason code.
- The fixture includes at least JavaScript/TypeScript, Python, Rust, Go, and
  one additional ecosystem.
- The contract remains local-first and does not authorize clone/fetch,
  dependency installation, harvested code execution, registry publication,
  package or relation acceptance, baseline seeding, `preview_only` removal, or
  AI output as registry truth.
- Docs, DocC, roadmap, capabilities, Workplan, and `next.md` expose the
  contract and follow-up task boundary.

## Non-Goals

- No CLI parser or validator implementation in this task.
- No source classifier implementation.
- No live registry lookup.
- No repository clone/fetch.
- No corpus batch run.
- No SpecPM package or relation acceptance.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- DocC static generation command from `.github/workflows/docs.yml`
