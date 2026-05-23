# Real Repository Validation Runner

This DocC page mirrors
`docs/REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md` and documents the local-only
runner for real-repository refinement validation.

## Purpose

Use this workflow helper to execute deterministic real-repository checks from a
single command and generate a compact `run-report.json`.

`scripts/run_real_repository_validation.py` orchestrates SpecHarvester-owned phases:

- `source-manifests` validation,
- `collect-batch`,
- per-package `draft`,
- optional SpecNode-compatible command invocation,
- optional per-package SpecPM validation,
- optional governance and smoke triage summaries,
- per-candidate `draft-summary.json` files for `quality-report`.

## What the Runner Does Not Do

The runner does not implement SpecNode runtime, model execution, provider
discovery, scheduling, lifecycle orchestration, or provider-specific
capabilities. Those responsibilities remain in external SpecNode-compatible
implementations and contracts.

## Inputs and Execution

- `--inputs` points to local manifest files under `.smoke/inputs`.
- `--out` points to local output under `.smoke/output`.
- `--select` limits run scope to specific repository IDs.
- `--dry-run` renders planned commands without running them.
- `--strict-exit` makes optional failures fatal.
- `--output` overrides the default `<out>/run-report.json` execution report.

After the runner finishes, build the structured quality report with:

```bash
python -m spec_harvester quality-report \
  --run-report .smoke/output/real-repository-validation/run-report.json \
  --candidates-root .smoke/output/real-repository-validation \
  --output .smoke/output/real-repository-validation/quality-report.json
```

## Command Template Inputs

The optional `--specnode-command` template supports:

- `{candidate}`
- `{bundle}`
- `{preview_plan}`
- `{result}`

Use it only when an external SpecNode-compatible contract runtime is available.

## Status Model

- `ok` — all required steps passed.
- `degraded` — optional SpecNode/governance/smoke steps failed in non-strict mode.
- `error` — required or strict optional step failed.

## Safety Surface

The runner keeps runs local-only and does not execute harvested package scripts,
dependency installers, or repository tests/builds. Generated candidates and reports
remain on local `.smoke/output` artifacts for review.

`draft-summary.json` is derived from generated `specpm.yaml` and
`specs/*.spec.yaml` artifacts; it is a compact reporting artifact, not raw
repository source or model output.
