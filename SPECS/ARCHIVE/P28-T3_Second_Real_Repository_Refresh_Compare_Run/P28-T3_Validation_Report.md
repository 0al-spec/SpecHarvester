# P28-T3 Validation Report

Verdict: PASS
Date: 2026-06-12

## Source

- Repository: `https://github.com/TanStack/query`
- Local checkout: `/tmp/specharvester-p28-t3-tanstack-query-source`
- Revision: `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
- SpecHarvester branch: `codex/p28-t3-second-refresh-compare`
- SpecPM branch used for consumer-side compare: `main`
- SpecPM commit used: `3228a2e`

## SpecHarvester Run

Run root:

```text
/tmp/specharvester-p28-t3-tanstack-query-refresh
```

Commands:

```bash
PYTHONPATH=src python3 -m spec_harvester source-manifests \
  /tmp/specharvester-p28-t3-tanstack-query-refresh/inputs

PYTHONPATH=src python3 -m spec_harvester collect-batch \
  /tmp/specharvester-p28-t3-tanstack-query-refresh/inputs \
  --out /tmp/specharvester-p28-t3-tanstack-query-refresh/candidates \
  --emit-workspace-inventory \
  --report /tmp/specharvester-p28-t3-tanstack-query-refresh/batch-validation.json

PYTHONPATH=src python3 -m spec_harvester draft-package-set \
  /tmp/specharvester-p28-t3-tanstack-query-refresh/candidates/tanstack-query/workspace-inventory.json \
  --out /tmp/specharvester-p28-t3-tanstack-query-refresh/package-set

PYTHONPATH=src python3 -m spec_harvester draft-package-set \
  /tmp/specharvester-p28-t3-tanstack-query-refresh/candidates/tanstack-query/workspace-inventory.json \
  --out /tmp/specharvester-p28-t3-tanstack-query-refresh/package-set-member \
  --role workspace \
  --role member_package

PYTHONPATH=src python3 -m spec_harvester preflight-bundle-set \
  /tmp/specharvester-p28-t3-tanstack-query-refresh/package-set-member

PYTHONPATH=src python3 -m spec_harvester render-package-set-site \
  --bundle-set /tmp/specharvester-p28-t3-tanstack-query-refresh/package-set-member \
  --output /tmp/specharvester-p28-t3-tanstack-query-refresh/viewer-member

PYTHONPATH=src python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set /tmp/specharvester-p28-t3-tanstack-query-refresh/package-set-member \
  --fresh-generated-root /tmp/specharvester-p28-t3-tanstack-query-refresh/fresh-generated-member \
  --source-repository https://github.com/TanStack/query \
  --source-revision feb1efd804c1262106f72c8adc1d82a8ce9cfbb0 \
  --run-label p28-t3-tanstack-query-member-refresh \
  --output /tmp/specharvester-p28-t3-tanstack-query-refresh/fresh-candidate-refresh-run-member.json
```

Observed result:

- `source-manifests`: `ok`, repository count `1`
- `collect-batch`: `ok`, collected count `1`
- workspace inventory: `100` package manifests, `1` workspace manifest,
  diagnostics `0`
- default `draft-package-set`: `ok`, candidate count `1`, relation count `0`,
  skipped count `99`
- default skipped roles: `38` `member_package`, `61` `example_package`
- explicit member-package draft: `ok`, candidate count `39`, relation count
  `38`, skipped count `61`
- explicit member-package skipped roles: `61` `example_package`
- `preflight-bundle-set`: `passed`, candidates `39`, relations `38`, errors
  `0`, warnings `0`
- `render-package-set-site`: `ok`, candidates `39`, relations `38`
- `fresh-candidate-refresh-run`: `prepared`
- fresh run id: `fresh-candidate-refresh-d23e0a3eaeb57876`
- fresh generated contract files: `78`

## SpecPM Compare

Command run from `/Users/egor/Development/GitHub/0AL/SpecPM`:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle prepare-refresh-decision \
  --root . \
  --fresh-generated-root /tmp/specharvester-p28-t3-tanstack-query-refresh/fresh-generated-member \
  --package tanstack_query.workspace \
  --package tanstack_query.angular_cli_20 \
  --package tanstack_query.angular_query_experimental \
  --package tanstack_query.angular_query_persist_client \
  --package tanstack_query.eslint_plugin_query \
  --package tanstack_query.lit_query \
  --package tanstack_query.lit_vite \
  --package tanstack_query.preact_query \
  --package tanstack_query.preact_query_devtools \
  --package tanstack_query.preact_query_persist_client \
  --package tanstack_query.query_async_storage_persister \
  --package tanstack_query.query_broadcast_client_experimental \
  --package tanstack_query.query_codemods \
  --package tanstack_query.query_core \
  --package tanstack_query.query_devtools \
  --package tanstack_query.query_persist_client_core \
  --package tanstack_query.query_sync_storage_persister \
  --package tanstack_query.query_test_utils \
  --package tanstack_query.react_next_14 \
  --package tanstack_query.react_next_15 \
  --package tanstack_query.react_next_16 \
  --package tanstack_query.react_query \
  --package tanstack_query.react_query_devtools \
  --package tanstack_query.react_query_next_experimental \
  --package tanstack_query.react_query_persist_client \
  --package tanstack_query.react_vite \
  --package tanstack_query.react_webpack_4 \
  --package tanstack_query.react_webpack_5 \
  --package tanstack_query.solid_query \
  --package tanstack_query.solid_query_devtools \
  --package tanstack_query.solid_query_persist_client \
  --package tanstack_query.solid_vite \
  --package tanstack_query.svelte_query \
  --package tanstack_query.svelte_query_devtools \
  --package tanstack_query.svelte_query_persist_client \
  --package tanstack_query.svelte_vite \
  --package tanstack_query.vue_query \
  --package tanstack_query.vue_query_devtools \
  --package tanstack_query.vue_vite \
  --package-id tanstack_query.workspace \
  --version 0.1.0 \
  --source-repository https://github.com/TanStack/query \
  --source-revision feb1efd804c1262106f72c8adc1d82a8ce9cfbb0 \
  --run-label p28-t3-tanstack-query-member-refresh \
  --output /tmp/specharvester-p28-t3-tanstack-query-refresh/refresh-decision-member.json \
  --json
```

Observed result:

- prepare report: `failed`
- refresh decision summary: `manual_review_required`
- `updateNeeded`: `true`
- reason: `refresh_prepare_requires_review`
- package count: `39`
- generated contract files in decision: `0`
- digest verified count: `0`
- errors: `40`
- warnings: `78`
- first error:
  `refresh_decision_prepare_current_contract_files_missing`
- no `refresh-decision-member.json` was written

The failure is expected for a new package-set with no current SpecPM generated
baseline. The helper produced structured review evidence and refused to write
an invalid refresh decision artifact.

## Product Verdict

The producer-side package-set refresh handoff is not `xyflow`-specific:
TanStack/query produced a valid 39-candidate package-set with relation evidence,
preflight passed, viewer render passed, and a fresh generated root was
prepared.

The run also exposes two follow-ups:

- Default package-set role selection is too narrow for generic monorepos:
  TanStack/query needs explicit `member_package` selection to produce useful
  scoped members.
- SpecPM `prepare-refresh-decision` is a refresh compare helper for packages
  that already have current generated artifacts. A first-submission or
  seeded-baseline workflow is needed for new repositories before a
  preflightable refresh decision can be emitted.

## Boundary Checks

- No harvested package scripts were executed.
- No package managers were run.
- SpecHarvester did not mutate SpecPM.
- SpecPM compare was read-only and wrote only local `/tmp` reports.
- The failed prepare did not leave an invalid `refresh-decision-member.json`.
