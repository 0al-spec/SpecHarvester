# P52-T3 Five-Repository Controlled Calibration

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T3`
**Depends On:** `P52-T2` Codex Spark External-Model Adapter Contract

## Goal

Run one bounded calibration over five operator-provided pinned local checkouts:
Flask, Gin, xyflow, FastAPI, and FastMCP. Produce static-only evidence first,
then compare two proposal-only model paths against the same deterministic
package-set draft inputs:

- LM Studio `openai/gpt-oss-20b` as a local OpenAI-compatible control; and
- Codex `gpt-5.3-codex-spark` through the P52-T2 read-only external-model
  contract and schema-validated `--model-output` handoff.

For the LM Studio control, SpecHarvester must request a JSON-object schema in
the OpenAI-compatible API payload. This is request-side structured output, not
a schema pasted into LM Studio's Chat Template field.

## Deliverables

- Add a five-source P52 manifest with the verified local revisions.
- Add a bounded runner that creates static requests, stages only compact
  allowlisted evidence for Codex, validates its final JSON Schema, and invokes
  the existing external `--model-output` seam.
- Add narrow LM Studio structured-output compatibility for the existing draft
  and enrichment requests: `response_format.type: json_schema` with a
  JSON-object schema, sent only for the `lm_studio` provider name.
- Run the static-only baseline before either model path.
- Record durable, proposal-only calibration evidence with per-repository status,
  schema validity, repository specificity, unsupported claims, timing/usage
  receipts, warnings, failures, and quality-threshold decision.
- Document the results in GitHub Markdown and DocC, indexes, capability map,
  and roadmap; add focused regression coverage.
- Create Flow validation, archive, and review artifacts.

## Acceptance Criteria

- Exactly five existing, clean pinned local checkouts are used; no checkout is
  cloned, fetched, restored, or modified.
- Static-only evidence completes before LM Studio or Codex Spark is invoked.
- Codex receives no original checkout, writable add-directory, network/provider
  endpoint, dependency installation path, package manager, harvested code, or
  adapter code; it uses `read-only`, `ephemeral`, `ignore-user-config`, final
  response schema, and last-message output flags.
- Only schema-valid Codex final messages can enter
  `package-set-ai-draft-proposal <inventory> --model-output <message>`.
- LM Studio and Codex results remain separate proposal-only sidecars; neither
  can accept packages/relations, publish metadata, seed baselines, remove
  `preview_only`, or become registry truth.
- LM Studio's request payload uses `response_format.type: json_schema`, while
  its Chat Template remains untouched. The existing semantic/evidence
  validation stays authoritative after the provider returns a JSON object.
- No raw prompts, raw model responses, secrets, Codex session state, or
  chain-of-thought is persisted.
- The report evaluates the P52 thresholds: static >=95%, Codex completion
  >=90%, schema validity >=98%, repository specificity >=80%, and unsupported
  claims <=5%; it explicitly states whether P52-T4 is unlocked.

## Non-Goals

- Do not run a twenty-repository pilot or a 50-100 corpus gate.
- Do not add repository acquisition, dependency installation, package-manager,
  harvested-code, adapter, registry, or acceptance behavior.
- Do not alter non-LM-Studio OpenAI-compatible provider payloads or a user's
  LM Studio Chat Template. The only provider-path change is the request-side
  JSON-object schema required for the local control run.

## Validation Plan

- Run focused tests for the P52 calibration runner and documentation contract.
- Assert the LM Studio draft and enrichment wire payloads carry the JSON Schema
  and that other provider names retain their existing payload shape.
- Validate every durable JSON artifact with `python -m json.tool`.
- Run Flow gates from `.flow/params.yaml`, including full pytest, Ruff,
  coverage >=90%, Swift package/DocC build, and `git diff --check`.

---
**Archived:** 2026-07-22
**Verdict:** PASS
