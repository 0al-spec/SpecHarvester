# P13-T2 Clean-Context Semantic Review Pass

Status: Planned
Task: `P13-T2`
Phase: Phase 13. Prompted Refinement Quality Loop
Priority: P1
Effort: 8 hours
Dependencies: `P13-T1`

## Problem

`SpecNodeRefinementResult` validation currently proves structural safety: schema
shape, authority limits, evidence references, and proposal-only patch semantics.
It does not prove that the model understood the target package intent or that
its proposal is semantically useful.

This matters for weak local models. A first-pass prompt can produce a valid
JSON proposal that still describes SpecHarvester or SpecPM generation rather
than the target repository. The next safety layer must review the generated
proposal with a clean context so the reviewer is not contaminated by the first
model transcript, ad-hoc prompt wording, or provider logs.

## Goals

- Define a versioned `SpecNodeSemanticReviewContract`.
- Define a typed `SpecNodeSemanticReviewJob` assembled only from deterministic
  artifacts, the generated `SpecNodeRefinementResult`, and a fixed rubric.
- Define a typed `SpecNodeSemanticReviewResult` with verdict and findings.
- Ensure the review pass cannot mutate candidates or emit patch operations.
- Add validation helpers that reject unknown findings, unknown evidence
  references, mutation attempts, and inconsistent verdicts.
- Mirror the contract in GitHub docs and DocC.
- Add tests for the contract documentation and deterministic validation rules.

## Non-Goals

- Do not implement feedback retry orchestration; that belongs to `P13-T3`.
- Do not call LM Studio, OpenAI, or any provider in tests.
- Do not apply semantic review findings automatically.
- Do not make semantic review a replacement for structural validation,
  SpecPM validation, or human review.
- Do not include first-pass prompt transcripts, chain-of-thought, provider logs,
  raw source files, or arbitrary user prompts in the review job.

## Deliverables

- `docs/SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`
- `Sources/SpecHarvester/Documentation.docc/SpecNodeSemanticReviewContract.md`
- Cross-links from existing SpecNode docs, architecture, workflow, and DocC root.
- `build_specnode_semantic_review_job(...)` for deterministic review inputs.
- `validate_specnode_semantic_review_result(...)` for typed review outputs.
- Unit tests for valid review jobs/results and invalid mutation/finding cases.
- Docs contract tests for GitHub docs and DocC mirror coverage.

## Acceptance Criteria

- Semantic review input uses clean context only:
  deterministic artifact bundle, preview plan, refinement result digest/content,
  and fixed review rubric.
- Review output is schema-like typed data with `verdict` and `findings`.
- Allowed verdicts are bounded to `approve`, `needs_revision`, and `reject`.
- Finding codes are from a repository-owned taxonomy, including wrong package
  intent, unsupported claims, missing evidence references, confidence
  overstatement, unsafe negative claims, schema/policy mismatch, and authority
  boundary violations.
- Review results cannot contain patch operations, candidate mutation fields, or
  retry directives.
- Findings must reference known deterministic evidence IDs, artifact IDs,
  preview-plan references, or the reviewed refinement result.
- `approve` cannot contain blocking findings.
- `needs_revision` and `reject` must contain at least one finding.
- Python tests, docs tests, lint, format, coverage, Swift package manifest, and
  Swift DocC target build pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
