# Real Repository Validation Runner

Status: Phase 15 plan

Use this local-only runner to execute the real-repository refinement flow from a single
entry point and produce a compact execution report at `run-report.json`.

```bash
python3 scripts/run_real_repository_validation.py --help
```

## Purpose

`scripts/run_real_repository_validation.py` orchestrates:

- manifest validation (`source-manifests`) against local input manifests;
- deterministic batch collection (`collect-batch`);
- per-package drafting (`draft`);
- optional SpecNode contract boundary execution;
- optional SpecPM validation;
- optional governance and triage reporting;
- `draft-summary.json` summaries consumed by `quality-report`.

The runner is purely deterministic orchestration glue. It does not implement
SpecNode runtime, provider discovery, model execution, scheduling, or lifecycle
management.

## Inputs and Defaults

- `--inputs` (default: `.smoke/inputs`)
  Directory containing source manifest files.
- `--out` (default: `.smoke/output/real-repository-validation`)
  Output root for candidates and generated reports.
- `--select`
  One or more repository IDs to narrow processing.
- `--strict-exit`
  Treat optional SpecNode/governance/smoke failures as fatal.

## Command Template Options

- `--emit-interface-indexes`
  Passes `--emit-interface-indexes` to `collect-batch`.
- `--analyzer-cache-dir`
  Path for analyzer cache.
- `--skip-specpm-validation`
  Skip per-package `specpm validate`.
- `--no-specnode-artifacts`
  Skip `specnode-artifact-bundle.json` / preview plan writes.
- `--specnode-command`
  Optional SpecNode-compatible template string. Supports:
  `{candidate}`, `{bundle}`, `{preview_plan}`, `{result}`.
- `--skip-governance-reports`
  Skip `governance-*` and smoke summary generation.
- `--skip-smoke-triage`
  Skip `smoke-triage-summary`.
- `--specpm-command`
  Template for per-package SpecPM validation; default
  `python -m specpm.cli validate {candidate} --json`.
- `--strict-exit`
  Keep optional steps fatal and stop immediately on first optional failure.
- `--dry-run`
  Render commands and produce report without executing any command.

## Common Invocation

```bash
python3 scripts/run_real_repository_validation.py \
  --inputs .smoke/inputs \
  --out .smoke/output/real-repository-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/analyzer-cache \
  --specnode-command \
  "python3 -m specnode_refiner run \
   --candidate {candidate} \
   --bundle {bundle} \
   --preview-plan {preview_plan} \
   --result {result}"
```

## Optional Output

- `--output <path>` writes the execution report JSON to a chosen file.
- Without `--output`, the runner writes `<out>/run-report.json`.
- Each drafted candidate receives `draft-summary.json`, derived from the
  generated `specpm.yaml` and `specs/*.spec.yaml` artifacts. This is the compact
  quality-report input and avoids relying on a non-existent raw `draft.json`
  command output.

Build the structured quality report after a run with:

```bash
python -m spec_harvester quality-report \
  --run-report .smoke/output/real-repository-validation/run-report.json \
  --candidates-root .smoke/output/real-repository-validation \
  --output .smoke/output/real-repository-validation/quality-report.json
```

## Status Semantics

- `status: ok`
  Required steps succeeded; optional failures (if any) were disabled.
- `status: degraded`
  One or more optional steps failed in non-strict mode.
- exit code `2` and `status: error` are returned for fatal failures.

## Failure Routing

- Non-fatal optional steps are captured in `nonFatalFailures` and `package`
  sections.
- Fatal failures abort immediately and return an error report.

## Safety Rules

- No package script execution.
- No dependency installation.
- No raw repository tests, builds, or execution.
- No package manager network operations.
- Generated `.smoke/output/*` artifacts remain local and uncommitted.
