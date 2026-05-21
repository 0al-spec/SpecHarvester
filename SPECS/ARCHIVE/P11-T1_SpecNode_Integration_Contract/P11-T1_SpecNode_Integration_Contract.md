# P11-T1 SpecNode Integration Contract

Status: Archived
Created: 2026-05-21
Task: `P11-T1` Define the SpecHarvester-to-SpecNode artifact bundle and typed
job contract for model-assisted candidate refinement without granting model
output file-system or shell authority.

## Problem

SpecHarvester now produces compact deterministic evidence: `harvest.json`,
`ProjectProfile`, optional `public-interface-index.json`, semantic evidence,
validation reports, governance reports, and draft candidate metadata. The next
phase needs a bridge to SpecNode so weak local models can refine candidates
from those artifacts without reading raw repository source or gaining shell or
filesystem authority.

The boundary must be explicit before any provider adapter or refinement command
is implemented. Otherwise model integration risks becoming an untyped prompt
pipe with unclear provenance, unclear authority, and unsafe mutation paths.

## Goals

- Define the `SpecHarvesterSpecNodeArtifactBundle` contract.
- Define the `SpecNodeRefinementJob` typed job envelope.
- Specify required, optional, and forbidden artifacts.
- Specify path, digest, workspace, symlink, and authority constraints.
- Make clear that SpecHarvester remains the deterministic evidence producer and
  SpecNode owns provider discovery/model execution.
- Document that model output is untrusted proposal metadata and cannot mutate
  files directly.
- Mirror the contract in DocC and link it from the docs index/root topics.
- Add documentation contract tests that lock the security boundary terms.

## Non-Goals

- Do not implement a `refine-preview` command.
- Do not call SpecNode or any model provider.
- Do not discover LM Studio models or add OpenAI-compatible adapters.
- Do not define the final model patch output schema beyond named placeholder
  output kinds for later tasks.
- Do not change candidate generation, promotion, or SpecPM validation behavior.

## Design

- Add `docs/SPECNODE_INTEGRATION_CONTRACT.md` as the canonical GitHub-facing
  contract.
- Add `Sources/SpecHarvester/Documentation.docc/SpecNodeIntegrationContract.md`
  as the DocC mirror.
- Update `docs/README.md`, `docs/ARCHITECTURE.md`,
  `Sources/SpecHarvester/Documentation.docc/SpecHarvester.md`, and
  `Sources/SpecHarvester/Documentation.docc/HarvesterArchitecture.md`.
- Add a docs contract test requiring core terms such as
  `SpecHarvesterSpecNodeArtifactBundle`, `SpecNodeRefinementJob`,
  `modelFilesystemAccess: none`, `modelShellAccess: none`,
  `candidatePatchProposal`, `usageReceipt`, and explicit no-shell/no-filesystem
  boundaries.

## Deliverables

- GitHub contract documentation.
- DocC mirror documentation.
- Navigation/index updates.
- Documentation contract tests.
- Flow validation report.

## Acceptance Criteria

- Contract names and boundary terms are present in both GitHub docs and DocC.
- The contract defines bundle inputs, digest requirements, job policy fields,
  output authority, rejection conditions, and ownership split between
  SpecHarvester and SpecNode.
- Docs state that the model cannot run shell commands, mutate files, access raw
  repository source, access secrets, or expand network access.
- Existing full Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

---

**Archived:** 2026-05-21
**Verdict:** PASS
