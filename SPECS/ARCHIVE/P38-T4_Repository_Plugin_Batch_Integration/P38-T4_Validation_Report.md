# P38-T4 Validation Report

## Task

P38-T4 Repository Plugin Batch Integration.

## Summary

PASS. The autonomous candidate batch can now copy a provided
`SpecHarvesterRepositoryPluginApplicabilityReport` into a stable
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`
sidecar path and record a discoverable `repositoryPluginApplicability` summary
with identity, digest, counts, diagnostic codes, and non-authority boundary
flags.

The integration remains sidecar producer evidence only. It does not execute
plugins, load third-party plugin code, change parser profile behavior, change
repository profile scoring, invoke AI, accept packages or relations, publish
registry metadata, or treat plugin decisions as registry truth.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q` | PASS, `17 passed` |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'autonomous_candidate_batch or repository_plugin or current_next_task'` | PASS, `4 passed, 106 deselected` |
| `PYTHONPATH=src pytest -q` | PASS, `763 passed, 1 skipped` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `763 passed, 1 skipped`, total coverage `91.16%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS, `120 files already formatted` |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Review Notes

- Default batch behavior records `repositoryPluginApplicability.status:
  not_provided` and `repositoryPluginApplicabilitySidecarCount: 0`.
- Provided sidecars are validated for identity and summary shape before being
  copied.
- The copied sidecar digest is recorded as SHA-256 over the exact copied JSON
  artifact.
- P38-T4 was rebased onto the post-review P38-T3 fixture semantics: topology
  decisions are not treated as selected when required declared input evidence is
  unavailable.
