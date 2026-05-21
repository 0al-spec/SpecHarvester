# P11-T3 OpenAI-Compatible Provider Adapter Boundary

Status: Archived
Created: 2026-05-21
Task: `P11-T3` Add an OpenAI-compatible provider adapter boundary for local
SpecNode execution, including LM Studio discovery, model listing, health
checks, timeout, retry, temperature, and token-budget policy.

## Problem

`P11-T1` defined the SpecHarvester-to-SpecNode job boundary and `P11-T2`
defined the deterministic `refine-preview` planning input. The next missing
contract is the provider adapter boundary that explains how local
OpenAI-compatible providers, especially LM Studio, are discovered and governed
without turning SpecHarvester into a model runtime.

Without a dedicated adapter contract, future implementation could blur
responsibilities between SpecHarvester and SpecNode, contact unapproved
endpoints, treat model availability as deterministic evidence, or omit timeout,
retry, temperature, and token-budget policy from usage receipts.

## Goals

- Define the `SpecNodeOpenAICompatibleProviderAdapter` boundary.
- Define LM Studio discovery defaults and explicit override behavior.
- Define provider health checks and model listing semantics.
- Define timeout, retry, temperature, max-output-token, and prompt-budget
  policy fields.
- Define usage receipt fields that record provider endpoint, model identity,
  policy, token usage, retries, and final status.
- Preserve the existing boundary: SpecHarvester prepares deterministic
  artifacts, SpecNode owns provider execution, and model output remains
  untrusted proposal metadata.
- Mirror the contract in DocC and add docs contract tests.

## Non-Goals

- Do not implement an HTTP client or invoke LM Studio.
- Do not add the `refine-preview` CLI implementation.
- Do not define final `candidatePatchProposal` schema details.
- Do not add real provider smoke tests.
- Do not weaken strict no-shell, no-filesystem, no-secret, and no raw-source
  authority boundaries.

## Design

- Add `docs/SPECNODE_PROVIDER_ADAPTER_CONTRACT.md` as the canonical
  provider-adapter contract.
- Add `Sources/SpecHarvester/Documentation.docc/SpecNodeProviderAdapterContract.md`
  as the DocC mirror.
- Update docs navigation and architecture/workflow references.
- Extend the SpecNode integration and refine-preview contracts with the P11-T3
  compatibility pointer.
- Add docs contract tests requiring the OpenAI-compatible adapter names,
  endpoint allowlist, discovery rules, health/model-listing behavior,
  generation policy, usage receipt, and authority limits.

## Deliverables

- GitHub provider adapter contract documentation.
- DocC mirror documentation.
- Navigation/reference updates.
- Documentation contract tests.
- Flow validation report.

## Acceptance Criteria

- Both GitHub docs and DocC define
  `SpecNodeOpenAICompatibleProviderAdapter`.
- The contract names LM Studio discovery, `/v1/models`, `/v1/chat/completions`,
  health checks, model listing, endpoint allowlist, and localhost-only defaults.
- The contract defines `timeoutPolicy`, `retryPolicy`, `generationPolicy`,
  `temperature`, `maxOutputTokens`, `promptBudget`, and provider usage receipt
  fields.
- The contract states that SpecHarvester does not contact providers and that
  SpecNode does not grant shell, filesystem, secret, raw-source, tool, or
  network-expansion authority to the model.
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
