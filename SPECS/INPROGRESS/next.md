# Next Task: P46-T6 Bounded Popular-Library Pilot Exit Decision

**Status:** Selected
**Branch:** `feature/P46-T6-bounded-popular-library-pilot-exit-decision`
**Phase:** Phase 46. Bounded Popular-Library Pilot After AI Draft Hardening
**Task:** `P46-T6`
**Depends On:** `P46-T5` Bounded Popular-Library Pilot Author Handoff Summaries

## Goal

Record the bounded pilot exit decision: proceed to a larger curated corpus,
run a targeted quality pass, or stop on a documented blocker.

## Context

P46-T5 produced author-facing handoff summaries for all six pilot
repositories. Reviewable static evidence is available for Flask, Gin, xyflow,
Cupertino, NavigationSplitView, and docc2context, but the exit decision must
account for do-not-promote AI sidecars:

- `gin.aiDraft`
- `docc2context.aiDraft`

The decision must also carry xyflow evidence gaps and unsupported enrichment
forward explicitly:

- `partial_public_interface_index`
- `operator_checkout_origin_fork_mismatch`
- `model_evidence_path_unsupported`

## Expected Deliverables

- Machine-readable exit decision fixture for the bounded pilot.
- Markdown and DocC documentation explaining the selected decision and rejected
  alternatives.
- Explicit treatment for static reviewability, do-not-promote AI sidecars,
  xyflow caveats, and larger-corpus readiness.
- Docs-contract coverage for decision identity, P46-T5 source artifact linkage,
  selected/rejected decision options, no-authority boundaries, and current
  next-task pointer.
- Validation report and archive artifacts for P46-T6.

## Boundaries

- Do not rerun the pilot.
- Do not run AI.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not treat AI output as registry truth.
- Do not treat static output as registry truth.
- Do not treat handoff output as registry truth.
- Do not treat exit-decision output as registry truth.
- Do not treat adapter output as registry truth.

## Recently Archived

- `P46-T5` Bounded Popular-Library Pilot Author Handoff Summaries: PASS on
  2026-06-20.
- `P46-T4` Bounded Popular-Library Pilot Output Triage: PASS on 2026-06-20.
- `P46-T3` Bounded Popular-Library Pilot AI-Enabled Run: PASS as evidence
  capture on 2026-06-20.

## Validation Expectations

- Validate any durable JSON fixture with `python3 -m json.tool` or equivalent.
- Run focused docs-contract tests for P46-T6 exit decision and current next
  task.
- Run formatting/lint/whitespace checks scaled to touched files.
