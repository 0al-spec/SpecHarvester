# P41-T6 Validation Report

Task: Real Local Trusted-Adapter Readiness Validation

## Summary

Result: PASS

P41-T6 records a practical trusted local adapter readiness validation over four
existing pinned local checkouts: FastMCP, FastAPI, xyflow, and Gin. The run
generated a disabled `SpecHarvesterTrustedLocalAdapterRunReport`, attached it
to `autonomous-candidate-batch` through explicit
`--trusted-local-adapter-run-report` input, and preserved all no-execution and
non-authority boundaries.

## Real Local Run

Run root:

```text
/tmp/specharvester-p41-t6-20260619T061629Z
```

Command shape:

```bash
PYTHONPATH=src python3 -m spec_harvester trusted-local-adapter-runner-skeleton \
  --request tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json \
  --preflight tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json \
  --output /tmp/specharvester-p41-t6-20260619T061629Z/trusted-local-adapter-run-report.json

PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch \
  /tmp/specharvester-p41-t6-20260619T061629Z/inputs \
  --out /tmp/specharvester-p41-t6-20260619T061629Z/output \
  --skip-ai \
  --trusted-local-adapter-run-report \
  /tmp/specharvester-p41-t6-20260619T061629Z/trusted-local-adapter-run-report.json
```

Observed result:

| Repository | Shape | Revision | Result |
| --- | --- | --- | --- |
| FastMCP | nested package roots | `3b8538e2422a1c43fdb69661c610de7985b785f2` | passed, 1 candidate |
| FastAPI | documentation-heavy repository | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | passed, 1 candidate |
| xyflow | workspace/package-set | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | passed, 4 candidates, 3 relations |
| Gin | manifest-backed single package | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | passed, 1 candidate |

Batch summary:

- `status: passed`
- `processedCount: 4`
- `passedPreflightCount: 4`
- `trustedLocalAdapterRunEvidenceSidecarCount: 1`
- `ai.mode: disabled`
- `trustedLocalAdapterRunEvidence.status: recorded`
- `trustedLocalAdapterRunEvidence.runStatus: no_execution_report_emitted`

## Durable Artifacts

- Added
  `tests/fixtures/repository_plugins/trusted_local_adapter_real_runs/p41-t6-real-local-trusted-adapter-readiness-validation.example.json`.
- Added
  `docs/TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md`.
- Added DocC mirror
  `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRealLocalReadinessValidation.md`.
- Updated runtime readiness docs, capabilities, roadmap, docs index, and DocC
  root references.
- Added docs-contract regression coverage for the fixture, doc references,
  digests, repository revisions, and boundary counters.

## Boundary Verification

The durable fixture and real run preserve:

- `adapterExecution: not_run`
- `adapterCodeLoaded: false`
- `adapterProcessSpawned: false`
- `executedAdapterCount: 0`
- `dependencyInstallation: not_allowed`
- `packageManagers: not_invoked`
- `networkAccess: none`
- `harvestedCodeExecution: not_allowed`
- `aiExecution: not_run`
- `appliedToDrafting: false`
- `registryAuthority: false`

The run did not load third-party adapter code, run adapter processes, clone or
fetch repositories, install dependencies, invoke package managers, execute
harvested code, run AI because of the adapter sidecar, accept packages, accept
relations, seed baselines, publish registry metadata, remove `preview_only`, or
treat runner reports as registry truth.

## Commands

| Command | Result |
| --- | --- |
| Real local P41-T6 trusted runner + `autonomous-candidate-batch --skip-ai --trusted-local-adapter-run-report` over FastMCP, FastAPI, xyflow, and Gin | PASS |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_real_local_readiness_validation_fixture_and_docs -q` | PASS, `1 passed` |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` | PASS, `127 passed` |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q` | PASS, `32 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `809 passed, 1 skipped` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS |
| `git diff --check` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `PYTHONPATH=src pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q` | PASS, `809 passed, 1 skipped`, total coverage `90.89%` |
| `rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc` | PASS |

## Remaining Gap

This task intentionally does not implement real adapter execution. Future work
must still define sandboxed process execution, adapter package distribution,
dependency isolation, output verification, and explicit operator approval
before any adapter process can run.
