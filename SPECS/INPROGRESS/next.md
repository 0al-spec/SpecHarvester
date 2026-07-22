# Next Task: P52-T5 Final 50-100 Repository Source Manifest and Checkout Readiness

**Status:** Selected
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T4` Twenty-Repository Controlled Pilot

## Objective

Create the final 50-100 repository manifest and checkout-readiness evidence,
using pinned clean local checkouts, provenance, license, size, and stop-policy
metadata before any larger-corpus static or model gate.

## Preconditions

- P52-T3 is archived with a PASS verdict: five repositories passed the static,
  Codex completion, schema-validity, repository-specificity, and unsupported
  claim thresholds, and P52-T4 is unlocked.
- An operator supplies exactly twenty pinned local checkouts and an ingestible
  source manifest with matching revisions.
- Static-only collection completes before any LM Studio or Spark invocation.
- LM Studio is loaded locally, accepts `response_format.type: json_schema`, and
  provider-side sensitive request/response logging is disabled by the operator.
  The schema is sent by the client, not configured in the Chat Template.
- The `gpt-5.3-codex-spark` operator authorization is available at execution
  time; its P52-T2 read-only, ephemeral external-model handoff is preserved.

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
