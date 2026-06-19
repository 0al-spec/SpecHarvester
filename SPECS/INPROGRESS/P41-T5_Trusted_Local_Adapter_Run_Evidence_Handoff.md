# P41-T5 Trusted Local Adapter Run Evidence Handoff

**Status:** Planned
**Branch:** `feature/P41-T5-trusted-local-adapter-run-evidence-handoff`
**Phase:** Phase 41. Trusted Local Adapter Runtime Readiness

## Motivation

P41-T4 made trusted local adapter runner output explicit and safe by emitting a
disabled no-execution `SpecHarvesterTrustedLocalAdapterRunReport`. That report
is useful only if downstream batch output can carry it as review evidence.

The important boundary is that attaching the report must not execute adapters,
load adapter code, change autonomous candidate drafting, or imply SpecPM
registry acceptance. It should work like the existing repository plugin
applicability and adapter evidence sidecars: visible, digested, reviewable, and
non-authoritative.

## Goal

Add an opt-in `autonomous-candidate-batch` evidence handoff for
`SpecHarvesterTrustedLocalAdapterRunReport` while preserving the default static
evaluator path and all no-execution/non-authority guarantees.

## Deliverables

- Add an `autonomous-candidate-batch` CLI input for a trusted local adapter run
  report.
- Validate the supplied report identity, schema version, authority, runner
  status, execution boundary, and required non-authority statements.
- Copy the report into batch output under a dedicated trusted-local-adapter run
  evidence sidecar directory.
- Record copied path, SHA-256 digest, report identity, runner status, and
  no-execution boundary in the batch report.
- Keep the sidecar explicitly separate from `repositoryPluginApplicability` and
  `repositoryPluginAdapterEvidence`.
- Update GitHub docs and DocC to explain the handoff boundary.
- Add regression coverage for the provided sidecar, default no-sidecar path, and
  invalid authority/boundary rejection.

## Acceptance Criteria

- When no trusted local adapter run report is supplied, batch output remains on
  the existing static evaluator path and records no trusted run evidence
  sidecar.
- When a valid report is supplied, batch output includes a copied report and a
  top-level review-only evidence record.
- The evidence record includes SHA-256 digests for the source and copied report,
  identity metadata, and no-execution fields.
- The record preserves:
  - `adapterExecution: not_run`
  - `adapterCodeLoaded: false`
  - `adapterProcessSpawned: false`
  - `executedAdapterCount: 0`
  - `appliedToDrafting: false`
  - `registryAuthority: false`
- Invalid or authority-bearing reports are rejected before batch output is
  emitted.
- Existing repository plugin applicability and adapter evidence sidecar tests
  keep passing.
- Documentation states that trusted local adapter run evidence is review-only
  producer evidence, not adapter output truth and not registry acceptance.

## Non-Goals

- Do not implement real adapter execution.
- Do not run adapter processes.
- Do not load third-party adapter code.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run AI because of this sidecar.
- Do not accept packages or relations.
- Do not seed baselines.
- Do not publish registry metadata.
- Do not remove `preview_only`.
- Do not replace static plugin applicability evaluation.

## Dependencies

- P41-T2 `SpecHarvesterTrustedLocalAdapterRunRequest`
- P41-T3 `SpecHarvesterTrustedLocalAdapterRunPreflightReport`
- P41-T4 disabled `SpecHarvesterTrustedLocalAdapterRunReport`
- Existing `autonomous-candidate-batch` sidecar pattern

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q`
- `PYTHONPATH=src pytest tests/test_trusted_local_adapter_runner.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- DocC static generation command from the project docs build path

## Review Notes

Review should focus on accidental authority creep:

- The batch command must not treat the report as adapter output.
- The batch command must not alter drafting from the sidecar.
- The copied sidecar must be hash-addressable review evidence.
- The report validator must reject changed execution boundaries instead of
  silently recording them.
