# Next Task: P52-T7 50-100 Repository Codex Spark Proposal-Only Gate

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Depends On:** `P52-T6` 50-100 Repository Static-Only Gate

## Objective

Run the approved 50-repository corpus through the schema-validated Codex Spark
proposal-only path, preserving bounded receipts, explicit failures, and
non-persistence before output triage.

## Preconditions

- P52-T6 is archived with a PASS verdict and explicitly unlocks P52-T7.
- All 50 approved sources produced static outcomes, with a 96% strict static
  completion rate against the required 95% minimum.
- The Codex Spark adapter contract and P52-T3/P52-T4 calibration evidence remain
  binding for schema validation, receipts, timeouts, and rejection policy.
- The two P52-T6 dual-license filename findings remain explicit and must not be
  silently omitted or treated as package-quality approval.

## Boundaries

- Do not create, restore, clone, or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code or adapters.
- Invoke only the approved read-only Codex Spark proposal path; do not invoke LM
  Studio or another model provider.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat static candidates, model proposals, or reports as registry truth.
- Do not persist raw prompts, raw provider responses, secrets, session state,
  or chain-of-thought.
