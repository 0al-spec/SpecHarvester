# Deferred Candidate Regeneration Runbook

This page mirrors `docs/DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`.

Status: P32-T2 operator runbook for deferred candidate regeneration.

The runbook covers the six deferred P30 candidates:
`xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system`,
`cupertino.core`, and `navigation_split_view.core`.

It does not run regeneration. It defines safe local inputs, command shapes,
expected artifacts, stop conditions, re-entry criteria, and non-authority
boundaries before P32-T3 or P32-T4 can run.

## Inputs and Output Root

Use only operator-provided local public checkouts recorded in
`inputs/limited-popular-libraries/repositories.yml`.

Before regeneration, verify the manifest:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries
```

Each attempt should write to
`.smoke/p32-deferred-regeneration/<attempt-id>/` and preserve source manifest
validation, collect output, `workspace-inventory.json`, `package-set-draft.json`,
`package-relation-proposals.json`, `package-set-ai-draft-proposal` output,
`package-set-ai-enrichment-proposal` output, member bundles, producer receipts,
validation reports, diagnostics, `author-ready-draft-quality-report.json`,
`bundle-set-preflight.json`, static viewer output, refreshed triage, and
selected handoff evidence only for candidates that pass hard gates.

The command surfaces are `autonomous-candidate-batch`,
`package-set-ai-draft-proposal`, and `package-set-ai-enrichment-proposal`.

## Regeneration Classes

`package_set_identity_regeneration` applies to `xyflow.workspace`,
`xyflow.react`, `xyflow.svelte`, and `xyflow.system`. The run must preserve
`xyflow.workspace` as the package-set identity, keep the member ids stable, and
prove:

```text
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
xyflow.workspace contains xyflow.system
```

`warning_bearing_enrichment_regeneration` applies to `cupertino.core` when
`refined_summary_missing` remains unresolved. The operator must regenerate AI
enrichment or attach author-curated summary evidence.

`identity_drift_resolution` applies to `navigation_split_view.core` when
`package_id_hint_mismatch` or `package_set_id_missing` remains unresolved. The
operator must choose the canonical package id, record the rejected or aliased
non-canonical id, and regenerate under that policy.

## Stop Conditions

Keep the affected candidate deferred when checkout paths are missing, revisions
do not match, inputs are dirty, collection fails, package-set identity is still
missing, relation endpoints drift, package id hints still mismatch,
`refined_summary_missing` remains unresolved without author-curated summary
evidence, JSON repair is exhausted, unsupported evidence paths are cited,
producer preflight has warnings/errors, static viewer output is missing, or
evidence digests are unavailable.

Stopped candidates must remain `needs_regeneration`, `blocked`, or
`not_for_intake`.

## Re-Entry Criteria

A candidate can re-enter candidate-layer triage only when all required evidence
roles are present, `authorReadyDraft.status` is `author_ready_draft`, producer
preflight is `passed`, warning count is `0`, error count is `0`, static viewer
status is `ok`, evidence digests are reviewable, `preview_only` remains intact,
and registry acceptance remains `external_required`.

Refreshed triage must use `candidate_layer_review_required`,
`needs_regeneration`, `blocked`, or `not_for_intake`. Only
`candidate_layer_review_required` candidates may enter a future selected
handoff dry run.

P32-T3 records the xyflow package-set identity regeneration result in
<doc:XyflowPackageSetIdentityRegenerationDryRun>. That dry run classifies
`xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, and `xyflow.system` as
`candidate_layer_review_required` with `selectedHandoffEligible: true`.

## Non-Authority Boundary

The runbook cannot clone repositories, fetch updates, install dependencies,
execute harvested code, run package managers, run builds or tests, publish
registry metadata, accept packages, accept relations, seed baselines, remove
`preview_only`, create or merge a SpecPM pull request, treat AI output as
registry truth, or replace author or SpecPM maintainer review.

See also <doc:AutonomousCandidateTechDebtPlan>,
<doc:DeferredSelectedCandidateRegenerationRequirements>,
<doc:XyflowPackageSetIdentityRegenerationDryRun>,
<doc:LimitedPopularLibraryCandidateLayerTriage>,
<doc:LimitedPopularLibrarySelectedHandoffDryRun>,
<doc:SelectedCandidateHandoffProposal>, and <doc:SpecPMHandoff>.
