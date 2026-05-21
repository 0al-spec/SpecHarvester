# P11-T2 Refine Preview Planning Contract

Status: Archived
Created: 2026-05-21
Task: `P11-T2` Add a bounded `refine-preview` planning contract that packages
`harvest.json`, `ProjectProfile`, optional `PublicInterfaceIndex`,
`semanticEvidenceIndex`, validation reports, and draft candidate metadata as
compact model input.

## Problem

`P11-T1` defined the SpecHarvester-to-SpecNode trust boundary and typed job
envelope. The next missing contract is the concrete preview planning shape:
what compact model input SpecHarvester prepares before SpecNode is ever called.

Without this contract, future implementation work could accidentally pass raw
repository source, raw documentation bodies, oversized artifacts, or ambiguous
candidate state to a model. That would undermine the goal of using weak models
only after deterministic utilities have prepared bounded review material.

## Goals

- Define the `SpecHarvesterRefinePreviewPlan` contract.
- Define the `compactModelInput` sections produced from deterministic
  artifacts.
- Specify required and optional source artifacts and their digest constraints.
- Specify excluded content: raw repository source, raw documentation bodies,
  dependency directories, secrets, provider logs, and arbitrary prompts.
- Define size/token-budget controls and truncation behavior for weak-model
  input.
- Link the plan contract to the existing
  `SpecHarvesterSpecNodeArtifactBundle` and `SpecNodeRefinementJob` boundary.
- Mirror the contract in DocC and add docs contract tests.

## Non-Goals

- Do not implement the `refine-preview` CLI command.
- Do not call SpecNode or any provider.
- Do not define final `candidatePatchProposal` schema details.
- Do not apply model output or mutate candidate files.
- Do not change deterministic drafting, promotion, or SpecPM validation.

## Design

- Add `docs/SPECNODE_REFINE_PREVIEW_CONTRACT.md` as the canonical contract.
- Add `Sources/SpecHarvester/Documentation.docc/SpecNodeRefinePreviewContract.md`
  as the DocC mirror.
- Update docs navigation and architecture/workflow references.
- Extend `docs/SPECNODE_INTEGRATION_CONTRACT.md` and its DocC mirror with the
  P11-T2 compatibility pointer.
- Add docs contract tests for the new contract names, included sections,
  excluded content, and authority limits.

## Deliverables

- GitHub `refine-preview` planning contract documentation.
- DocC mirror documentation.
- Navigation/reference updates.
- Documentation contract tests.
- Flow validation report.

## Acceptance Criteria

- Both GitHub docs and DocC define `SpecHarvesterRefinePreviewPlan`.
- The contract includes `harvestSummary`, `projectProfile`,
  `publicInterfaceSummary`, `semanticEvidenceIndex`, `validationSummaries`,
  `draftCandidateMetadata`, `artifactDigests`, and `promptBudget`.
- The contract states `rawRepositorySource: excluded`,
  `documentationBodies: excluded`, `providerLogs: excluded`,
  `secretAccess: none`, `modelFilesystemAccess: none`, and
  `modelShellAccess: none`.
- The contract explains that `refine-preview` planning is deterministic and
  does not execute models.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

Archived: 2026-05-21
Verdict: PASS
