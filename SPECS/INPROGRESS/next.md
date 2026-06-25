# Next Task: P50-T1 Record Restored-Checkout Rerun Evidence

**Status:** Selected
**Branch:** `feature/P50-T1-record-restored-checkout-rerun-evidence`
**Phase:** Phase 50. Restored-Checkout Rerun Follow-Up
**Task:** `P50-T1`
**Last Archived:** `P49-T4` Record docc2context Follow-Up Exit Decision
**Depends On:** `P49-T4` Record docc2context Follow-Up Exit Decision

## Goal

Record the restored-checkout same-scope rerun evidence after the six
operator-local checkout paths from the P46 manifest were restored.

## Context

P49-T4 selected:

```text
record_no_larger_corpus_readiness_due_to_operator_local_checkout_blocker
```

That decision was correct for the evidence then available: P49-T3 could not
reach static-only or AI-enabled execution because all six expected checkout
paths were missing.

The operator-local paths are now restored through symlinks:

- `/Users/egor/Development/GitHub/0AL/flask`
- `/Users/egor/Development/GitHub/0AL/gin`
- `/Users/egor/Development/GitHub/0AL/xyflow`
- `/Users/egor/Development/GitHub/0AL/cupertino`
- `/Users/egor/Development/GitHub/0AL/NavigationSplitView`
- `/Users/egor/Development/GitHub/0AL/docc2context`

The restored checkouts point to the pinned repositories under
`/Users/egor/Development/GitHub/` and match the P46 manifest revisions.

The local rerun evidence is under:

```text
/tmp/specharvester-p49-t3-rerun-after-checkout-restore-20260625T004309
```

Observed rerun result:

- static-only gate: `passed`
- AI-enabled gate: `passed`
- processed repositories: `6`
- failed repositories: `0`
- passed preflight: `6`
- AI draft proposals: `6`
- AI enrichment proposals: `6`
- raw prompts, raw provider responses, and chain-of-thought: not persisted

## Scope

- Add durable P50-T1 restored-checkout rerun evidence.
- Document static-only-before-AI ordering and same-scope P46 manifest reuse.
- Record remaining warning/caveat evidence without treating warnings as
  registry truth.
- Update the current next-state decision from checkout-blocked to
  larger-corpus planning reconsideration-ready.

## Expected Deliverables

- Durable P50-T1 restored-checkout rerun evidence fixture.
- GitHub and DocC documentation for the restored-checkout rerun.
- Workplan/next update to the selected post-rerun state.
- Focused docs-contract tests.
- Validation report and archive artifacts for P50-T1.

## Boundaries

- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, static output, rerun output, targeted follow-up
  output, exit-decision output, or adapter output as registry truth.

## Validation Expectations

- Validate the durable JSON fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P50-T1 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
