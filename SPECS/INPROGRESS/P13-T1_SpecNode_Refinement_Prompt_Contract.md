# P13-T1 SpecNode Refinement Prompt Contract

Status: Planned
Task: `P13-T1`
Phase: Phase 13. Prompted Refinement Quality Loop

## Problem

Local LM Studio probing showed that `openai/gpt-oss-20b` can follow
`response_format.type: json_schema`, but semantic quality is prompt-sensitive.
A weak ad-hoc prompt can make the model describe SpecPM generation instead of
the target package behavior.

Prompt text must become a versioned, reviewable contract owned by the
repository. It must preserve the existing SpecNode trust boundary: the model
receives bounded deterministic `compactModelInput`, emits schema-bound proposal
data, and cannot invent evidence, mutate candidates, or expand authority.

## Goals

- Define a versioned `SpecNodeRefinementPromptContract` for first-pass
  refinement prompts.
- Specify deterministic prompt sections derived from
  `SpecHarvesterRefinePreviewPlan.compactModelInput`.
- Require strict output schema binding to `SpecNodeRefinementResult`.
- Define evidence-reference rules that reject unknown, collapsed, or invented
  references.
- Define negative-claim and confidence-calibration rules for weak models.
- Mirror the contract in GitHub docs and DocC.
- Add docs contract tests for the new contract and navigation links.

## Non-Goals

- Do not implement real SpecNode provider execution.
- Do not call LM Studio or any OpenAI-compatible endpoint in tests.
- Do not add semantic review pass execution; that belongs to `P13-T2`.
- Do not add retry orchestration; that belongs to `P13-T3`.
- Do not let prompt text override deterministic evidence, schema validation,
  SpecPM validation, or human review.

## Deliverables

- `docs/SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`
- `Sources/SpecHarvester/Documentation.docc/SpecNodeRefinementPromptContract.md`
- Links from docs index and DocC root topic.
- Cross-references from existing SpecNode refine-preview/provider/patch/smoke
  docs where useful.
- Tests in `tests/test_docs_contracts.py` that assert the contract includes:
  - `SpecNodeRefinementPromptContract`
  - `promptContractVersion`
  - `compactModelInput`
  - `SpecNodeRefinementResult`
  - `response_format.type: json_schema`
  - evidence-reference allowlist rules
  - negative-claim policy
  - confidence calibration
  - forbidden task self-description such as `generate_specpm`
  - no chain-of-thought, provider logs, raw source, or arbitrary prompts.

## Acceptance Criteria

- Prompt contract is deterministic and versioned.
- Prompt sections are derived only from allowed preview-plan fields.
- Prompt contract requires the model to infer target package behavior, not the
  SpecHarvester or SpecPM generation task.
- Evidence references must match known artifact IDs, evidence IDs, operation
  IDs, or explicitly generated prompt-local evidence IDs.
- Confidence values must be calibrated from evidence coverage, not model
  self-assurance.
- Direct candidate mutation remains forbidden; output remains proposal-only.
- Documentation builds under SwiftPM DocC target.
- Python docs-contract tests, lint, format, coverage, and Swift docs checks
  pass.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
