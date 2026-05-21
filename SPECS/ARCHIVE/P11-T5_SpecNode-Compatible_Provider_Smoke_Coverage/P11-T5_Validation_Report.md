# P11-T5 Validation Report

Date: 2026-05-22
Task: `P11-T5` SpecNode-Compatible Provider Smoke Coverage
Verdict: PASS

## Summary

Implemented executable SpecNode provider smoke coverage for generated candidate
workspaces. The new smoke harness builds a deterministic
`SpecHarvesterSpecNodeArtifactBundle`, `SpecHarvesterRefinePreviewPlan`, and
`SpecNodeRefinementJob`, validates local SpecNode-compatible provider-stub
output as `SpecNodeRefinementResult`, and returns a deterministic
`provider_unavailable` fallback when no provider is configured.

The implementation preserves the Phase 11 trust boundary: SpecHarvester does
not call LM Studio or any OpenAI-compatible endpoint, does not apply generated
patches, does not mutate candidate files during smoke runs, and treats model
output only as untrusted proposal metadata.

## Deliverables

- Added `spec_harvester.specnode_refinement` smoke harness and structural
  validator.
- Added integration smoke tests with local provider stub, provider-unavailable
  fallback, absent public-interface-index handling, and unsafe-output rejection.
- Added GitHub and DocC documentation for `SpecNodeProviderSmokeRun`.
- Updated adjacent SpecNode integration, refine-preview, provider adapter,
  patch proposal, architecture, workflow, and documentation index pages.
- Added documentation contract coverage for the smoke coverage page and links.

## Acceptance Results

- Synthetic candidate collection, drafting, job construction, provider-stub
  execution, and result validation pass.
- Provider-unavailable fallback returns deterministic
  `SpecNodeRejectionReason` with code `provider_unavailable`.
- Candidate files remain unchanged during provider success, provider fallback,
  and unsafe-output rejection tests.
- Compact input excludes raw repository source, raw documentation bodies,
  dependency directories, provider logs, secrets, and arbitrary prompts.
- Unsafe operations such as `shellCommand`, forbidden file targets, missing
  digests, invalid provenance, malformed receipts, and invalid rejection shapes
  are rejected before apply.
- Existing collection, drafting, validation, and smoke tests do not require a
  configured provider.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py -q`
  - PASS: 9 passed
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: included in full test run
- `PYTHONPATH=src python -m pytest`
  - PASS: 238 passed
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: 46 files already formatted
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 238 passed, total coverage 91.15%
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Notes

- The provider used in tests is an in-process SpecNode-compatible test double,
  not a real model provider.
- The structural validator is intentionally a smoke gate, not a full JSON
  Schema implementation.
- No generated proposal is applied to `specpm.yaml` or `specs/*.spec.yaml`.
