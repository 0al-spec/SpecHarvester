# P41-T5 Validation Report

Task: Trusted Local Adapter Run Evidence Handoff

## Summary

Result: PASS

P41-T5 adds an explicit `autonomous-candidate-batch
--trusted-local-adapter-run-report` input. The batch validates a disabled
`SpecHarvesterTrustedLocalAdapterRunReport`, copies it as review-only sidecar
producer evidence, records source/copied SHA-256 digests, and preserves the
no-execution/non-authority boundary.

## Functional Checks

- Added `trustedLocalAdapterRunEvidence` to
  `SpecHarvesterAutonomousCandidateBatchReport`.
- Added `trustedLocalAdapterRunEvidenceSidecarCount` to batch summary.
- Preserved the default static evaluator/no-sidecar path when no trusted run
  report is supplied.
- Preserved existing `repositoryPluginApplicability` and
  `repositoryPluginAdapterEvidence` sidecar behavior.
- Rejected authority-bearing trusted run reports.
- Rejected trusted run reports whose execution boundary attempts to record
  adapter execution.
- Rejected boolean values in trusted run numeric count fields.
- Added CLI coverage for `--trusted-local-adapter-run-report`.
- Updated GitHub docs and DocC mirrors for the handoff boundary.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q` | PASS, `32 passed` |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_trusted_local_adapter_runner.py -q` | PASS, `38 passed` |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_trusted_local_adapter_runner.py tests/test_docs_contracts.py -q` | PASS, `163 passed` |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_docs_contracts.py -q` | PASS, `158 passed` after boolean-count hardening and next-task helper update |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` | PASS, `126 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `807 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q` | PASS, `807 passed, 1 skipped`, total coverage `90.88%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS |
| `git diff --check` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc` | PASS |

## Advisory Checks

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester/autonomous_candidate_batch.py --path src/spec_harvester/cli.py` | PASS, `status: ok`, `issueCount: 0` |
| `PYTHONPATH=src python -m spec_harvester procedural-style-report --path src/spec_harvester/autonomous_candidate_batch.py --path src/spec_harvester/cli.py` | ADVISORY, `status: attention` |

The procedural-style advisory flags the already large `cli.py` and
`autonomous_candidate_batch.py` hotspot shape. This task follows the existing
sidecar pattern to keep the change reviewable, but the module remains a
candidate for future extraction once the trusted local adapter runtime boundary
stabilizes.

## Boundary Verification

The new sidecar records and tests preserve:

- `adapterExecution: not_run`
- `adapterCodeLoaded: false`
- `adapterProcessSpawned: false`
- `executedAdapterCount: 0`
- `appliedToDrafting: false`
- `registryAuthority: false`
- `adapterOutputAccepted: false`

The batch does not load adapter code, run adapter processes, install
dependencies, invoke package managers, execute harvested code, run AI because
of this sidecar, accept packages, accept relations, seed baselines, publish
registry metadata, remove `preview_only`, or treat the runner report as adapter
output truth.
