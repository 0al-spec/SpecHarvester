# Next Task: P52-T2 Codex Spark External-Model Adapter Contract

**Status:** Selected
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T1` Controlled 50-100 Repository Corpus Plan

## Objective

Define the Codex Spark external-model adapter contract before any live model
call. The contract must turn deterministic SpecHarvester evidence into a
schema-validated `codex exec` handoff with bounded receipts and proposal-only
output.

## Deliverable Boundary

P52-T2 defines an adapter contract and fixtures only. It must isolate a future
Codex invocation from original repository checkouts, require read-only and
ephemeral execution, require a JSON Schema for the final message, and route
only a validated final JSON output through SpecHarvester's existing external
`--model-output` boundary. It must not invoke Codex or change the LM Studio
OpenAI-compatible provider path.

## Source Evidence

P52-T2 takes its planning authority from the P52-T1 fixture:

```text
tests/fixtures/controlled_repository_corpus_plan/p52-t1-controlled-repository-corpus-plan.example.json
```

P52-T1 requires a standalone Codex Spark adapter contract before the
five-repository calibration. It does not approve any live model call by itself.

## Boundaries

- Do not create, restore, clone, or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code, adapters, Codex, or AI during planning.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static, AI, AI-enriched, planning, triage, handoff, or adapter
  output as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
