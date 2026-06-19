# P42-T5 Validation Report

## Verdict

Passed.

## Scope Validated

- Added
  `tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json`.
- Added a static
  `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport` fixture for
  P42-T5 input binding.
- Added synthetic output, diagnostics, and audit-record candidate files with
  byte sizes and SHA-256 digests.
- Added GitHub docs, DocC docs, roadmap/capabilities links, and regression
  coverage.
- Preserved fixture-only runtime state:
  - `adapterExecution: synthetic_fixture_only`;
  - `realAdapterProcessSpawned: false`;
  - `thirdPartyAdapterCodeLoaded: false`;
  - `executedAdapterCount: 0`;
  - `dependencyInstallation: not_allowed`;
  - `packageManagers: not_invoked`;
  - `networkAccess: none`;
  - `registryAuthority: false`.

## Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_synthetic_trusted_local_adapter_sandbox_run_fixture_is_documented -q
python -m json.tool tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json >/dev/null
python -m json.tool tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-runner-validation-report.example.json >/dev/null
python -m json.tool tests/fixtures/repository_plugins/synthetic_sandbox_run/trusted-local-adapter-output.example.json >/dev/null
python -m json.tool tests/fixtures/repository_plugins/synthetic_sandbox_run/trusted-local-adapter-diagnostics.example.json >/dev/null
python -m json.tool tests/fixtures/repository_plugins/synthetic_sandbox_run/trusted-local-adapter-audit-record.example.json >/dev/null
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
```

## Results

- Targeted synthetic sandbox run docs contract: `1 passed`.
- Docs contracts: `132 passed`.
- Full pytest: `820 passed, 1 skipped`.
- Coverage: `90.79%`, above the configured `90%` gate.
- JSON fixture validation: passed.
- Ruff check: passed.
- Ruff format check: passed.
- `git diff --check`: passed.
- Swift package manifest dump: passed.
- Swift docs build: passed.
- DocC static generation: passed.

## Notes

The P42-T5 fixture remains producer-side review evidence only. It records an
explicit synthetic approval and synthetic output/audit shape, but it does not
load third-party adapter code, spawn real adapter processes, install
dependencies, invoke package managers, use network access, execute harvested
repository code, run AI because of adapter execution, accept packages or
relations, publish registry metadata, remove `preview_only`, or treat synthetic
adapter output as registry truth.
