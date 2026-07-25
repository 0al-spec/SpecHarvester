# P52-T7 Codex Spark Proposal-Only Gate

**Status:** Planned
**Phase:** Phase 52. Controlled Popular Repository Corpus with Codex Spark
**Task:** `P52-T7`
**Depends On:** `P52-T6` 50-100 Repository Static-Only Gate

## Objective

Run the approved 50-repository final corpus through a schema-validated Codex Spark
proposal-only control gate, preserving strict non-authority boundaries before any
larger-corpus proposal triage.

## Preconditions

- `P52-T6` report is passed with `decision.p52T7Unlocked == true`.
- The P52-T6 readiness input digest is provided and verified.
- P52-T6 manifest/revision/repository binding is still intact.
- The selected corpus still satisfies the 50-100 static-only scope.
- Boundaries from P52-T5/T6 remain enforced (local checkout only, proposal-only).

## Boundaries

- Do not clone, fetch, restore, or create repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code or adapters.
- Do not persist raw prompts, raw responses, secrets, or chain-of-thought.
- Do not accept packages or relations.
- Do not publish registry metadata or remove preview-only status.
- Do not treat any output as registry truth.

## Deliverables

- Implement a dedicated `P52-T7` executor that:
  - Validates and binds P52-T6 readiness by digest and source manifest fields
    (`id`, `repository`, `revision`).
  - Runs deterministic static-only batch with `skip_ai=True` on approved sources.
  - Runs Codex Spark control against per-repository inventory and schema.
  - Evaluates existing Phase 52 static/Codex quality metrics.
  - Produces a durable `final-corpus-codex-spark-gate-report.json` artifact.
- Add CLI command:
  - `final-corpus-codex-spark-gate` with `--readiness`,
    `--readiness-sha256`, `--out`, Codex options and `--skip-codex`.
- Add execution tests for:
  - readiness mismatch rejection (before static run)
  - Codex completion threshold blocking
  - schema/decision fields and artifact projection

## Acceptance Criteria

- The gate fails fast when manifest/revision/repository fields drift from P52-T6.
- Static-only boundary and readiness digest are bound to the exact approved
  manifest.
- Gate unlock condition is `p52T8Unlocked` and matches thresholds and control
  status.
- Codex receipts and schema flags are included without persistence of raw model
  content.
- Task does not execute package managers, adapters, harvested code, or mutate
  source/registry state.

## Plan Outputs

- `SPECS/INPROGRESS/P52-T7_Codex_Spark_Proposal-Only_Gate.md` (this file)
- `src/spec_harvester/final_corpus_codex_spark_gate.py`
- `src/spec_harvester/cli.py` CLI wiring
- `tests/test_final_corpus_codex_spark_gate.py`
- `SPECS/INPROGRESS/P52-T7_Validation_Report.md`
