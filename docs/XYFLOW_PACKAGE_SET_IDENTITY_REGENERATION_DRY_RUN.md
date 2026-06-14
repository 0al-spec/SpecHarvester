# Xyflow Package-Set Identity Regeneration Dry Run

Status: P32-T3 recorded dry-run evidence.

This report records a bounded xyflow-only run of the P32 deferred candidate
regeneration path. It follows the operator procedure in
[`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
and records whether the deferred xyflow package-set candidates can re-enter
candidate-layer review.

## Input

The run used the limited popular-library source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

The operator verified the local checkout before the dry run:

```text
repository id: xyflow
checkout: /Users/egor/Development/GitHub/xyflow
revision: a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd
worktree: clean
```

Source manifest validation was recorded at:

```text
.smoke/p32-deferred-regeneration/20260613T181500Z/source-manifest-validation.json
```

## Command

The dry run was scoped to `xyflow` only:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --select xyflow \
  --out .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

The static package-set viewer was rendered separately:

```bash
PYTHONPATH=src python -m spec_harvester render-package-set-site \
  --bundle-set .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/package-sets/xyflow \
  --output .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/viewer
```

The machine-readable summary fixture is:

```text
tests/fixtures/xyflow_package_set_identity_regeneration/p32-t3-xyflow-package-set-identity-regeneration.example.json
```

It uses:

```json
{
  "apiVersion": "spec-harvester.xyflow-package-set-identity-regeneration-dry-run/v0",
  "kind": "SpecHarvesterXyflowPackageSetIdentityRegenerationDryRun",
  "schemaVersion": 1
}
```

## Result

The dry run processed exactly one repository:

```text
selected: xyflow
skipped: flask, gin, cupertino, navigation-split-view, docc2context
```

It produced four preview candidates:

```text
xyflow.workspace
xyflow.react
xyflow.svelte
xyflow.system
```

The package-set identity is `xyflow.workspace`. The selected member packages
are `xyflow.react`, `xyflow.svelte`, and `xyflow.system`.

The relation proposal output recorded:

```text
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
xyflow.workspace contains xyflow.system
```

Bundle-set preflight passed:

```text
status: passed
warningCount: 0
errorCount: 0
```

```json
{
  "status": "passed",
  "candidateCount": 4,
  "candidatePreflightPassedCount": 4,
  "relationCount": 3,
  "warningCount": 0,
  "errorCount": 0
}
```

The static viewer rendered successfully with `status: ok`, `candidateCount: 4`,
and `relationCount: 3`.

All four member candidates retained `preview_only: true`, had clean
diagnostics, valid validation reports, and `authorReadyDraft.status:
author_ready_draft`.

## AI Proposal Notes

The live LM Studio enrichment pass completed cleanly:

```json
{
  "status": "completed",
  "proposalCount": 4,
  "warningCount": 0,
  "errorCount": 0
}
```

The AI draft proposal retained a warning-level `package_set_id_missing`
diagnostic. P32-T3 records that warning as proposal-only context rather than
registry truth. The deterministic package-set draft, relation proposals,
bundle-set preflight, and viewer evidence prove the actual
`xyflow.workspace` identity for this dry run.

## Candidate-Layer Decision

The recorded decision is:

```text
candidate_layer_review_required
selectedHandoffEligible: true
```

```json
{
  "status": "candidate_layer_review_required",
  "selectedHandoffEligible": true
}
```

Product verdict: the xyflow package-set identity blocker is resolved enough for
the regenerated xyflow candidates to re-enter candidate-layer review. They can
be included in the refreshed P32-T5 candidate-layer triage and selected
handoff evidence if no later review blocks them.

## Boundary

This dry run is producer evidence only. It does not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat AI output as registry truth.

SpecPM remains the validation, relation, acceptance, and registry authority.

## See Also

- [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
- [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
