# Deferred Candidate Regeneration Runbook

Status: P32-T2 operator runbook for deferred candidate regeneration.

This runbook turns the P31-T5 regeneration requirements into a safe operator
procedure. It is for the six deferred P30 candidates only:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`;
- `cupertino.core`;
- `navigation_split_view.core`.

It does not run regeneration by itself. It defines the inputs, commands,
expected artifacts, stop conditions, and review boundaries that P32-T3 and
P32-T4 must follow.

## Inputs

Use only operator-provided local public checkouts recorded in the limited
corpus source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

Before any regeneration command, verify the source manifest:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries
```

The operator must verify:

- every selected checkout path exists;
- every checkout is a git worktree;
- every checkout matches the pinned revision in the manifest;
- every checkout is clean enough for the run policy;
- output roots are fresh, reviewable, and outside accepted registry sources;
- local provider use is explicit and bounded when AI proposal commands are
  enabled.

## Output Root

Use a dedicated run root per attempt:

```text
.smoke/p32-deferred-regeneration/<attempt-id>/
```

The run root should preserve:

- `source-manifest-validation.json`;
- deterministic collect output;
- `workspace-inventory.json` where available;
- `package-set-draft.json`;
- `package-relation-proposals.json`;
- `package-set-ai-draft-proposal.json` when AI draft is enabled;
- `package-set-ai-enrichment-proposal.json` when AI enrichment is enabled;
- member candidate bundles;
- `producer-receipt.json`;
- `validation-report.json`;
- `diagnostics.json`;
- `author-ready-draft-quality-report.json`;
- `bundle-set-preflight.json`;
- static viewer output;
- refreshed candidate-layer triage;
- selected handoff evidence only for candidates that pass hard gates.

## Regeneration Classes

### Package-Set Identity Regeneration

Affected candidates:

- `xyflow.workspace`;
- `xyflow.react`;
- `xyflow.svelte`;
- `xyflow.system`.

Use this class when the blocker is `package_set_identity_regeneration` or
`package_set_id_missing`.

Safe command shape:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out .smoke/p32-deferred-regeneration/<attempt-id>/xyflow \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

For dry-run request inspection without calling a provider, use the lower-level
proposal commands:

```bash
PYTHONPATH=src python -m spec_harvester package-set-ai-draft-proposal \
  .smoke/p32-deferred-regeneration/<attempt-id>/xyflow/collected/xyflow/workspace-inventory.json \
  --source-checkout ../../../../xyflow \
  --request-output .smoke/p32-deferred-regeneration/<attempt-id>/xyflow/ai-draft/request.json

PYTHONPATH=src python -m spec_harvester package-set-ai-enrichment-proposal \
  --bundle-set .smoke/p32-deferred-regeneration/<attempt-id>/xyflow/package-sets/xyflow \
  --source-checkout ../../../../xyflow \
  --request-output .smoke/p32-deferred-regeneration/<attempt-id>/xyflow/ai-enrichment/request.json
```

Expected proof:

- package-set identity remains `xyflow.workspace`;
- member ids remain `xyflow.react`, `xyflow.svelte`, and `xyflow.system`;
- relation proposals preserve:

```text
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
xyflow.workspace contains xyflow.system
```

- `bundle-set-preflight.json` reports `passed`;
- producer preflight warning count is `0`;
- producer preflight error count is `0`;
- static viewer output is present;
- `preview_only` remains intact;
- `registryAcceptanceDecision.status` remains `external_required`.

### Warning-Bearing Enrichment Regeneration

Affected candidate:

- `cupertino.core`.

Use this class when the blocker is
`warning_bearing_enrichment_regeneration` or `refined_summary_missing`.

Safe command shape:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out .smoke/p32-deferred-regeneration/<attempt-id>/cupertino \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

If model regeneration still lacks a refined summary, the operator may attach
author-curated summary evidence instead of looping the model. That evidence
must be recorded as review evidence and must not be treated as registry
acceptance.

Expected proof:

- enrichment diagnostics no longer include `refined_summary_missing`; or
- author-curated summary evidence explicitly resolves the missing summary gap;
- producer preflight warning count is `0`;
- producer preflight error count is `0`;
- static viewer output is present;
- `preview_only` remains intact;
- `registryAcceptanceDecision.status` remains `external_required`.

### Identity-Drift Resolution

Affected candidate:

- `navigation_split_view.core`.

Use this class when the blocker is `identity_drift_resolution`,
`package_set_id_missing`, or `package_id_hint_mismatch`.

Before regeneration, choose the canonical package id. P32-T4 chooses
`navigation_split_view.core` for the current source manifest because it matches
the generated and validated candidate identity; `navigation-split-view.core`
is retained only as historical drift evidence unless a maintainer explicitly
aliases it later.

```text
navigation-split-view.core
navigation_split_view.core
```

The decision must record:

- chosen canonical id;
- rejected or aliased non-canonical id;
- reason for the decision;
- source manifest update requirement, if any;
- impact on existing candidate paths and digests.

Safe command shape after the canonical id decision:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out .smoke/p32-deferred-regeneration/<attempt-id>/navigation-split-view \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Expected proof:

- generated `specpm.yaml` package id matches the canonical id;
- candidate bundle path matches the canonical id policy;
- non-canonical id is rejected or explicitly aliased;
- producer preflight warning count is `0`;
- producer preflight error count is `0`;
- static viewer output is present;
- `preview_only` remains intact;
- `registryAcceptanceDecision.status` remains `external_required`.

## Stop Conditions

Stop the affected candidate and keep it deferred when any of these conditions
is true:

- checkout path is missing;
- checkout is not a git worktree;
- checkout revision does not match the source manifest;
- checkout is dirty when clean input is required;
- source manifest validation fails;
- deterministic collection fails;
- `workspace-inventory.json` is missing for a package-set regeneration;
- package-set identity is still missing;
- relation endpoints are not in the selected member set;
- `package_id_hint_mismatch` remains unresolved;
- `refined_summary_missing` remains unresolved and no author-curated summary
  evidence exists;
- JSON repair is exhausted;
- AI proposal diagnostics contain unsupported evidence paths or package id
  drift;
- producer preflight has warnings or errors;
- static viewer output is missing;
- evidence digests are missing or do not match the files being reviewed.

Stopped candidates must stay in `needs_regeneration`, `blocked`, or
`not_for_intake`. They must not be selected for handoff.

## Re-Entry Criteria

A regenerated candidate can re-enter candidate-layer triage only when:

- all required evidence roles are present;
- `authorReadyDraft.status` is `author_ready_draft`;
- producer preflight is `passed`;
- warning count is `0`;
- error count is `0`;
- static viewer status is `ok`;
- evidence digests are reviewable;
- `preview_only` remains intact;
- registry acceptance remains `external_required`.

The refreshed triage must use the existing states:

- `candidate_layer_review_required`;
- `needs_regeneration`;
- `blocked`;
- `not_for_intake`.

Only candidates classified as `candidate_layer_review_required` may enter a
future selected handoff dry run.

P32-T3 records the xyflow package-set identity regeneration result in
[`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md).
That dry run classifies `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`,
and `xyflow.system` as `candidate_layer_review_required` with
`selectedHandoffEligible: true`.
P32-T4 records the single-package regeneration result in
[`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md).
That dry run keeps `cupertino.core` at `needs_regeneration` because
`refined_summary_missing` remains unresolved, and classifies
`navigation_split_view.core` as `candidate_layer_review_required` with
`selectedHandoffEligible: true`.
P32-T5 records the refreshed selected handoff result in
[`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md).
It includes the P30 selected candidates plus the eligible regenerated xyflow
and NavigationSplitView candidates, while keeping `cupertino.core` deferred.

## Non-Authority Boundary

This runbook cannot:

- clone repositories;
- fetch updates;
- install dependencies;
- execute harvested code;
- run package managers;
- run builds or tests;
- publish registry metadata;
- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- create or merge a SpecPM pull request;
- treat AI output as registry truth;
- replace author or SpecPM maintainer review.

See also:

- [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
- [`DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`](DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md)
- [`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md)
- [`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md)
- [`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md)
- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
- [`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
