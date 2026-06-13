# Xyflow Package-Set Identity Regeneration Dry Run

This page mirrors
`docs/XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`.

Status: P32-T3 recorded dry-run evidence.

P32-T3 ran the deferred candidate regeneration path for `xyflow` only, using
the procedure in <doc:DeferredCandidateRegenerationRunbook>.

## Input and Command

The run used `inputs/limited-popular-libraries/repositories.yml` and verified
the local xyflow checkout at revision
`a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.

The scoped command was:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --select xyflow \
  --out .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

The viewer command was:

```bash
PYTHONPATH=src python -m spec_harvester render-package-set-site \
  --bundle-set .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/package-sets/xyflow \
  --output .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/viewer
```

The recorded fixture is
`tests/fixtures/xyflow_package_set_identity_regeneration/p32-t3-xyflow-package-set-identity-regeneration.example.json`.

It uses `SpecHarvesterXyflowPackageSetIdentityRegenerationDryRun` with
`apiVersion: spec-harvester.xyflow-package-set-identity-regeneration-dry-run/v0`.

## Result

The dry run processed `xyflow` and skipped `flask`, `gin`, `cupertino`,
`navigation-split-view`, and `docc2context`.

It produced:

```text
xyflow.workspace
xyflow.react
xyflow.svelte
xyflow.system
```

The package-set identity is `xyflow.workspace`.

The relation evidence records:

```text
xyflow.workspace contains xyflow.react
xyflow.workspace contains xyflow.svelte
xyflow.workspace contains xyflow.system
```

Bundle-set preflight reports `status: passed`, `candidateCount: 4`,
`relationCount: 3`, `warningCount: 0`, and `errorCount: 0`.

The static viewer reports `status: ok`, `candidateCount: 4`, and
`relationCount: 3`.

All four member candidates keep `preview_only: true`,
`authorReadyDraft.status: author_ready_draft`, clean diagnostics, and valid
validation reports.

## Decision

The candidate-layer decision is `candidate_layer_review_required` with
`selectedHandoffEligible: true`.

The AI draft proposal retained the proposal-only warning
`package_set_id_missing`, but the deterministic package-set draft, relation
proposals, bundle-set preflight, and viewer evidence prove `xyflow.workspace`
for this dry run.

## Boundary

This dry run is producer evidence only. It does not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat AI output as registry truth.

See also <doc:DeferredCandidateRegenerationRunbook>,
<doc:AutonomousCandidateTechDebtPlan>,
<doc:SelectedCandidateHandoffProposal>, and <doc:SpecPMHandoff>.
