# Next Task: P52-T3 Five-Repository Controlled Calibration

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T2` Codex Spark External-Model Adapter Contract

## Objective

Run the first bounded Phase 52 calibration over exactly five
operator-provided, pinned local repository checkouts. Compare deterministic
static-only evidence with Codex Spark proposal-only output using the P52-T2
schema-validated external-model handoff and record the Phase 52 quality metrics.

## Preconditions

- P52-T2 is archived with a PASS verdict and its invocation profile is used
  without weakening the read-only, ephemeral, no-raw-persistence constraints.
- An operator supplies five pinned local checkouts and an ingestible source
  manifest with matching revisions.
- Static-only collection completes before any Spark invocation.
- LM Studio is loaded locally and accepts `response_format.type: json_schema`;
  the schema is sent by the client, not configured in the Chat Template.
- The `gpt-5.3-codex-spark` operator authorization is available at execution
  time; this pointer does not itself make a live model call.

## Boundaries

- Do not create, restore, clone, or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code or adapters.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static, AI, AI-enriched, calibration, or adapter output as
  registry truth.
- Do not persist raw prompts, raw provider responses, secrets, session state,
  or chain-of-thought.
