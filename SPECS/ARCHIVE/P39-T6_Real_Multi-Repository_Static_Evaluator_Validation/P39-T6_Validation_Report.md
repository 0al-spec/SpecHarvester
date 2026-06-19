# P39-T6 Validation Report

Task: Real Multi-Repository Static Evaluator Validation  
Date: 2026-06-19  
Verdict: PASS

## Summary

P39-T6 validates the Phase 39 repository plugin static evaluator on real local
checkouts and verifies the P39-T5 `autonomous-candidate-batch` auto-sidecar
path.

The run covered:

- `fastmcp` at `3b8538e2422a1c43fdb69661c610de7985b785f2`;
- `fastapi` at `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`;
- `xyflow` at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.

All three local checkouts were available and clean. The run did not clone,
fetch, install dependencies, invoke package managers, execute harvested code,
or invoke AI.

## Real Run Evidence

Durable fixture:

```text
tests/fixtures/repository_plugins/real_runs/p39-t6-multi-repository-static-evaluator-validation.example.json
```

Run root:

```text
/tmp/specharvester-p39-t6-static-evaluator-20260619T000000Z
```

Per repository, the validation ran:

1. `autonomous-candidate-batch --skip-ai --repository-profile-selection auto`
   to collect deterministic metadata and profile evidence.
2. `repository-plugin-applicability-detect` against a static evidence envelope
   derived from that metadata.
3. `autonomous-candidate-batch --repository-plugin-registry
   --repository-plugin-static-evidence-envelope` to verify batch auto-sidecar
   generation.

## Results

| Repository | Profile | Standalone evaluator | Batch sidecar | Selected | Blocked |
| --- | --- | --- | --- | ---: | ---: |
| `fastmcp` | `generic.single_package.v0` | passed | passed | 4 | 1 |
| `fastapi` | `generic.single_package.v0` | passed | passed | 4 | 1 |
| `xyflow` | `generic.package_set.v0` | passed | passed | 4 | 1 |

Every generated batch sidecar recorded:

- `sourceMode: auto_static_evaluator`;
- `appliedToDrafting: false`;
- `registryAuthority: false`.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_repository_plugin_multi_repository_static_evaluator_validation_docs tests/test_docs_contracts.py::test_repository_plugin_real_run_fastmcp_fixture_and_docs tests/test_docs_contracts.py::test_static_repository_plugin_applicability_evaluator_plan_is_documented -q
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_repository_plugin_multi_repository_static_evaluator_validation_docs -q
PYTHONPATH=src pytest -q
swift build --target SpecHarvesterDocs
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc
```

## Gate Results

- Targeted docs-contract tests: passed.
- Full tests: `782 passed, 1 skipped`.
- Coverage: `91.12%`, above the configured 90% threshold.
- Ruff check: passed.
- Ruff format check: passed.
- Whitespace check: passed.
- Swift docs build: passed.
- DocC static generation: passed.

## Boundaries

The validation remains producer-side evidence only. It does not:

- load third-party plugin code;
- execute plugins;
- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- invoke AI;
- change parser profile behavior;
- change repository profile scoring;
- accept packages or relations;
- publish registry metadata;
- remove `preview_only`;
- treat plugin decisions as registry truth.
