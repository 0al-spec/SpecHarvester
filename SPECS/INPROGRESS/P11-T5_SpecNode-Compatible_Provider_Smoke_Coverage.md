# P11-T5 SpecNode-Compatible Provider Smoke Coverage

Status: In Progress
Created: 2026-05-22
Task: `P11-T5` Add integration smoke coverage using a local SpecNode-compatible
provider with weak-model drafting inputs, while preserving deterministic
fallback when no provider is available.

## Problem

`P11-T1` through `P11-T4` define the SpecHarvester-to-SpecNode artifact bundle,
refine-preview plan, provider adapter boundary, and candidate patch proposal
output schema. The remaining Phase 11 gap is executable smoke coverage that
proves these contracts compose without requiring a real local model provider in
CI.

The coverage must exercise weak-model drafting inputs while preserving the trust
boundary: SpecHarvester remains deterministic evidence producer and validator,
SpecNode owns model execution, and model output remains untrusted proposal
metadata.

## Goals

- Add a deterministic smoke harness that builds a
  `SpecHarvesterSpecNodeArtifactBundle`, `SpecHarvesterRefinePreviewPlan`, and
  `SpecNodeRefinementJob` from a generated candidate workspace.
- Add a local in-process SpecNode-compatible provider test double that returns
  a controlled `SpecNodeRefinementResult`.
- Validate successful `candidatePatchProposal` output structurally before it is
  considered reviewable.
- Add deterministic fallback behavior for provider-unavailable scenarios.
- Prove that compact model input excludes raw repository source,
  documentation bodies, dependency directories, provider logs, secrets, and
  arbitrary prompts.
- Preserve existing commands and quality gates when no provider is configured.

## Non-Goals

- Do not call LM Studio or any real OpenAI-compatible endpoint from CI.
- Do not implement SpecNode itself.
- Do not make SpecHarvester own provider discovery or model execution.
- Do not apply generated patch operations to candidate files.
- Do not treat model output as accepted SpecPM registry truth.
- Do not add shell, filesystem, Git, package-manager, test-runner, build-tool,
  or network authority to model output.

## Design

- Add a small `specnode_refinement` module for deterministic smoke assembly and
  structural result validation.
- Build bundle artifacts from `harvest.json`, `specpm.yaml`,
  `specs/*.spec.yaml`, and optional `public-interface-index.json`.
- Build compact model input sections from existing deterministic artifacts:
  harvest summary, `ProjectProfile`, public-interface summary, semantic evidence
  hints, validation summaries, and draft candidate metadata.
- Represent provider integration as a typed local provider protocol in tests,
  not as an HTTP client to model infrastructure.
- Return a schema-shaped `provider_unavailable` rejection when no provider is
  configured or the provider test double reports unavailability.
- Add integration tests that run collection, drafting, smoke provider execution,
  fallback, and rejection of unsafe operations.
- Document the smoke coverage contract in GitHub docs and DocC.

## Deliverables

- Deterministic SpecNode smoke harness code.
- Integration smoke tests with a local SpecNode-compatible provider test double.
- Provider-unavailable fallback tests.
- Structural validation tests for unsafe model output.
- GitHub and DocC documentation for the smoke coverage boundary.
- Flow validation report.

## Acceptance Criteria

- A synthetic candidate can be collected, drafted, converted into a
  `SpecNodeRefinementJob`, passed through a local SpecNode-compatible provider
  stub, and validated as a `SpecNodeRefinementResult`.
- The provider-unavailable path returns a deterministic
  `SpecNodeRejectionReason` with code `provider_unavailable` and does not mutate
  candidate files.
- Compact model input contains bounded summaries and digests, not raw source,
  raw documentation bodies, provider logs, secrets, arbitrary prompts, or
  dependency directories.
- Unsafe outputs such as shell commands, provider calls, network fetches,
  full-file replacements, or operations outside `specpm.yaml` and
  `specs/*.spec.yaml` are rejected before apply.
- Existing `collect-local`, `collect-batch`, `draft`, validation, and smoke
  tests do not require a configured provider.
- Configured Flow quality gates pass with coverage at or above 90%.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_specnode_refinement_smoke.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `ruff check src tests`
- `ruff format --check src tests`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
