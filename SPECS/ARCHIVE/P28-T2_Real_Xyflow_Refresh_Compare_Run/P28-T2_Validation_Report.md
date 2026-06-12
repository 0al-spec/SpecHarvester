# P28-T2 Validation Report

Verdict: PASS
Date: 2026-06-12

## Source

- Repository: `https://github.com/xyflow/xyflow`
- Local checkout: `/Users/egor/Development/GitHub/xyflow`
- Revision: `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`
- SpecHarvester branch: `codex/xyflow-refresh-compare-run`
- SpecPM branch used for consumer-side compare:
  `codex/refresh-decision-ci-artifact`
- SpecPM commit used: `6642312ea850ba204aa3deeee4dc1b56efea1034`

## SpecHarvester Run

Run root:

```text
/tmp/specharvester-p28-t2-xyflow-refresh
```

Commands:

```bash
PYTHONPATH=src python3 -m spec_harvester collect-batch \
  /tmp/specharvester-p28-t2-xyflow-refresh/inputs \
  --out /tmp/specharvester-p28-t2-xyflow-refresh/candidates \
  --emit-workspace-inventory

PYTHONPATH=src python3 -m spec_harvester draft-package-set \
  /tmp/specharvester-p28-t2-xyflow-refresh/candidates/xyflow/workspace-inventory.json \
  --out /tmp/specharvester-p28-t2-xyflow-refresh/package-set

PYTHONPATH=src python3 -m spec_harvester preflight-bundle-set \
  /tmp/specharvester-p28-t2-xyflow-refresh/package-set

PYTHONPATH=src python3 -m spec_harvester render-package-set-site \
  --bundle-set /tmp/specharvester-p28-t2-xyflow-refresh/package-set \
  --output /tmp/specharvester-p28-t2-xyflow-refresh/viewer

PYTHONPATH=src python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set /tmp/specharvester-p28-t2-xyflow-refresh/package-set \
  --fresh-generated-root /tmp/specharvester-p28-t2-xyflow-refresh/fresh-generated \
  --source-repository https://github.com/xyflow/xyflow \
  --source-revision a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd \
  --run-label p28-t2-xyflow-refresh \
  --output /tmp/specharvester-p28-t2-xyflow-refresh/fresh-candidate-refresh-run.json
```

Observed result:

- `collect-batch`: `ok`
- `draft-package-set`: `ok`, candidate count `4`
- `preflight-bundle-set`: `passed`, candidate count `4`
- `render-package-set-site`: `ok`, candidate count `4`
- `fresh-candidate-refresh-run`: `prepared`, candidate count `4`
- fresh run id: `fresh-candidate-refresh-fee706cdce4d43e3`
- packages:
  - `xyflow.workspace`
  - `xyflow.react`
  - `xyflow.svelte`
  - `xyflow.system`

## SpecPM Compare

Commands run from `/Users/egor/Development/GitHub/0AL/SpecPM`:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle prepare-refresh-decision \
  --root . \
  --fresh-generated-root /tmp/specharvester-p28-t2-xyflow-refresh/fresh-generated \
  --package xyflow.workspace \
  --package xyflow.react \
  --package xyflow.svelte \
  --package xyflow.system \
  --package-id xyflow.workspace \
  --version 0.1.0 \
  --source-repository https://github.com/xyflow/xyflow \
  --source-revision a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd \
  --run-label p28-t2-xyflow-refresh \
  --output /tmp/specharvester-p28-t2-xyflow-refresh/refresh-decision.json \
  --json

PYTHONPATH=src python3 -m specpm.cli producer-bundle preflight-refresh-decision \
  --body /tmp/specharvester-p28-t2-xyflow-refresh/refresh-decision.json \
  --root . \
  --json
```

Observed result:

- prepare report: `passed`
- preflight report: `passed`
- decision id:
  `specpm-refresh-decision-draft-xyflow.workspace-0.1.0-a58568f11bc0-no_update_required`
- decision status: `no_update_required`
- `updateNeeded`: `false`
- reason: `no_contract_delta`
- package count: `4`
- generated contract files: `8`
- digest verified count: `8`
- errors: `0`
- warnings: `0`

## Product Verdict

The current SpecHarvester package-set generator can reproduce the current
SpecPM generated `xyflow` contract surface. The fresh run may produce newer
producer receipts, validation reports, diagnostics, or review artifacts, but
SpecPM correctly treats those as advisory/report-only or receipt-only deltas.

No registry update PR is justified by this run because `specpm.yaml` and
`specs/*.spec.yaml` match current generated contract files.

## Boundary Checks

- No harvested package scripts were executed.
- No package managers were run.
- SpecHarvester did not mutate SpecPM.
- SpecPM compare was read-only and wrote only local `/tmp` reports.
- `no_update_required` remains review evidence, not maintainer approval.
