# P32-T2 Deferred Candidate Regeneration Runbook

**Status:** Planned
**Selected:** 2026-06-13
**Phase:** Phase 32. Autonomous Deferred Candidate Regeneration and Intake Readiness

## Motivation

P31-T5 defines what must be regenerated before deferred P30 candidates can
enter selected handoff. P32-T1 records the overall work plan. The remaining gap
is operational: an operator needs a safe, repeatable runbook before running
xyflow package-set identity regeneration, Cupertino enrichment repair, or
NavigationSplitView identity-drift repair.

Without a runbook, the next regeneration pass could become ad-hoc command
chaining, unbounded local model calls, or accidental broad scraping.

## Goal

Document the deferred candidate regeneration runbook that maps each blocker
class to safe local inputs, commands, expected artifacts, stop conditions,
candidate-layer triage outcomes, and non-authority boundaries.

## Deliverables

- Add a GitHub docs page for the deferred candidate regeneration runbook.
- Add a DocC mirror page and link it from the root topics.
- Link the runbook from the autonomous candidate tech-debt plan, deferred
  regeneration requirements, selected candidate handoff, roadmap, docs index,
  and SpecPM handoff docs.
- Add docs-contract tests that pin blocker classes, candidate ids, command
  surfaces, expected artifacts, stop conditions, and non-authority boundaries.
- Archive Flow artifacts and leave the next pointer on P32-T3.

## Acceptance Criteria

- The runbook covers `package_set_identity_regeneration`,
  `warning_bearing_enrichment_regeneration`, and `identity_drift_resolution`.
- The runbook names all six deferred P30 candidates:
  `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
  `cupertino.core`, and `navigation_split_view.core`.
- The runbook requires local pinned checkouts, source manifest verification,
  bounded local model calls, and reviewable output roots.
- The runbook lists expected artifacts such as collect output, workspace
  inventory, package-set draft, package relation proposals, AI draft/enrichment
  proposals, bundle-set preflight, static viewer output, author-ready quality
  reports, refreshed triage, and selected handoff evidence.
- The runbook defines stop conditions for missing checkout, revision mismatch,
  dirty input, producer preflight warnings/errors, missing viewer output,
  identity drift, unresolved enrichment warnings, exhausted JSON repair, or
  missing evidence digests.
- The runbook explicitly states that it does not clone repositories, fetch
  updates, execute harvested code, install dependencies, publish registry
  metadata, accept packages, accept relations, seed baselines, remove
  `preview_only`, create a SpecPM pull request, or treat AI output as registry
  truth.
- Project documentation tests pass.

## Non-Goals

- No actual regeneration run.
- No LM Studio invocation.
- No new CLI behavior.
- No SpecPM repository change.
- No selected handoff proposal rerun.
- No registry publication or acceptance decision.
