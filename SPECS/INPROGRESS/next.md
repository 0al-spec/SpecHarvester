# Next Task: P47-T2 Execute Targeted Pilot Quality Pass

**Status:** Selected
**Branch:** `feature/P47-T2-execute-targeted-pilot-quality-pass`
**Phase:** Phase 47. Targeted Pilot Quality Follow-Up
**Task:** `P47-T2`
**Last Archived:** `P47-T1` Targeted Pilot Quality Follow-Up Plan
**Depends On:** `P47-T1` Targeted Pilot Quality Follow-Up Plan

## Goal

Execute the targeted quality pass planned by P47-T1 while keeping all output
proposal-only and keeping the larger curated corpus blocked.

## Context

P47-T1 records the targeted quality follow-up plan selected after the P46-T6
exit decision. The larger curated corpus remains blocked until Phase 47
executes targeted repair or explicit disposition work, runs the bounded rerun
gate, and records an exit decision.

## Carry-Forward Blockers

Repair or explicitly dispose the do-not-promote AI sidecars:

- `gin.aiDraft`
- `docc2context.aiDraft`

Resolve or explicitly exclude the unsupported AI sidecar:

- `xyflow.aiEnrichment`

Resolve or explicitly accept xyflow caveats:

- `partial_public_interface_index`
- `operator_checkout_origin_fork_mismatch`
- `model_evidence_path_unsupported`

## Expected Deliverables

- Targeted quality pass evidence for `gin.aiDraft` and
  `docc2context.aiDraft`.
- Explicit xyflow caveat disposition evidence.
- Durable fixture and documentation showing what was repaired, accepted, or
  still blocked.
- Validation report and archive artifacts for P47-T2.

## Boundaries

- Do not approve a larger curated corpus.
- Do not treat regenerated or accepted AI sidecars as registry truth.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories unless the P47-T2 plan explicitly
  verifies already-pinned local checkout inputs.
- Do not execute harvested code.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat plan output as registry truth.
- Do not treat adapter output as registry truth.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P47-T2 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
