# Next Task: P52-T6 50-100 Repository Static-Only Gate

**Status:** Selected
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T5` Final 50-100 Repository Source Manifest and Checkout Readiness

## Objective

Run deterministic static-only collection for the approved 50-repository P52-T5
corpus, preserving preview candidates and recording completion, failures, and
bounded receipts before any Codex Spark execution.

## Preconditions

- P52-T5 is archived with a PASS verdict and unlocks P52-T6.
- The P52-T5 manifest contains 50 clean local checkouts at matching immutable
  revisions with resolved provenance, license evidence, and size budgets.
- The static completion rate must meet the Phase 52 minimum of 95% before P52-T7
  can invoke Codex Spark.
- Repository failures remain explicit and subject to the recorded stop policy;
  no failed source is silently dropped or replaced.

## Boundaries

- Do not create, restore, clone, or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code or adapters.
- Do not invoke LM Studio, Codex Spark, or any other model.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static candidates or reports as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, session state,
  or chain-of-thought.
