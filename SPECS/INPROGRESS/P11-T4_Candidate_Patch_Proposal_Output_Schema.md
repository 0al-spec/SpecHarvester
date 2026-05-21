# P11-T4 Candidate Patch Proposal Output Schema

Status: In Progress
Created: 2026-05-21
Task: `P11-T4` Define schema-validated model output for candidate patch
proposals, provenance, usage receipts, and rejection reasons before any
generated changes can be applied.

## Problem

`P11-T1` defines the SpecHarvester-to-SpecNode job boundary, `P11-T2` defines
compact model input, and `P11-T3` defines provider adapter policy. The next
missing contract is the shape of model output. Without a strict output schema,
future implementation could accept free-form text, direct file writes,
untraceable edits, or unsupported operations.

Model output must remain untrusted proposal metadata. SpecHarvester should be
able to validate a response structurally before showing it to a human reviewer
or applying any local edit.

## Goals

- Define `SpecNodeCandidatePatchProposal` as the only allowed patch proposal
  output.
- Define allowed proposal operations for candidate files.
- Define required provenance fields tying output to a job, preview plan,
  provider receipt, artifact digests, and source candidate state.
- Define `SpecNodeProposalUsageReceipt` and its relationship to
  `SpecNodeProviderUsageReceipt`.
- Define `SpecNodeRejectionReason` for safe refusal or inability to produce a
  valid proposal.
- Define validation and rejection rules before any generated change can be
  applied.
- Mirror the contract in DocC and add docs contract tests.

## Non-Goals

- Do not implement JSON Schema validation code.
- Do not implement model execution or provider calls.
- Do not apply generated patches.
- Do not define a full text-diff patch language.
- Do not allow direct writes to `specpm.yaml` or `specs/*.spec.yaml`.
- Do not make model output accepted registry truth.

## Design

- Add `docs/SPECNODE_PATCH_PROPOSAL_CONTRACT.md` as the canonical output
  contract.
- Add `Sources/SpecHarvester/Documentation.docc/SpecNodePatchProposalContract.md`
  as the DocC mirror.
- Update docs navigation and architecture/workflow references.
- Extend the SpecNode integration, refine-preview, and provider-adapter
  contracts with the P11-T4 compatibility pointer.
- Add docs contract tests requiring output kind names, allowed operations,
  provenance, usage receipt, rejection reason, and authority constraints.

## Deliverables

- GitHub patch proposal output contract documentation.
- DocC mirror documentation.
- Navigation/reference updates.
- Documentation contract tests.
- Flow validation report.

## Acceptance Criteria

- Both GitHub docs and DocC define `SpecNodeCandidatePatchProposal`.
- The contract defines `candidatePatchProposal`, `reviewNotes`,
  `SpecNodeProposalUsageReceipt`, and `SpecNodeRejectionReason`.
- The contract limits operations to schema-validated candidate metadata edits,
  not arbitrary shell, filesystem, Git, network, or provider actions.
- The contract ties each proposal to `SpecNodeRefinementJob`,
  `SpecHarvesterRefinePreviewPlan`, artifact digests, provider receipt, and
  candidate file digests.
- The contract states that SpecHarvester must validate the proposal and rerun
  SpecPM validation after any accepted edit.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
