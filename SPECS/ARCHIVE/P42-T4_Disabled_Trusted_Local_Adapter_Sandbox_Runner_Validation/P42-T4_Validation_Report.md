# P42-T4 Validation Report

## Verdict

Passed.

## Scope Validated

- Added `trusted-local-adapter-sandbox-runner-validation`.
- Added
  `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport`.
- Validated `SpecHarvesterTrustedLocalAdapterSandboxContract` and
  `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` identity and digest
  linkage.
- Preserved disabled no-execution runtime state:
  - `adapterExecution: not_run`;
  - `adapterCodeLoaded: false`;
  - `adapterProcessSpawned: false`;
  - `executedAdapterCount: 0`;
  - `registryAuthority: false`.
- Added GitHub docs, DocC docs, roadmap/capabilities links, and regression
  tests.

## Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_sandbox_runner_validation_is_documented -q
PYTHONPATH=src pytest tests/test_trusted_local_adapter_sandbox_runner.py -q
PYTHONPATH=src ruff check src/spec_harvester/trusted_local_adapter_sandbox_runner.py src/spec_harvester/cli.py tests/test_trusted_local_adapter_sandbox_runner.py tests/test_docs_contracts.py
PYTHONPATH=src ruff format --check src/spec_harvester/trusted_local_adapter_sandbox_runner.py src/spec_harvester/cli.py tests/test_trusted_local_adapter_sandbox_runner.py tests/test_docs_contracts.py
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q
PYTHONPATH=src python -m pytest tests/test_trusted_local_adapter_sandbox_runner.py -q
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
PYTHONPATH=src python -m spec_harvester trusted-local-adapter-sandbox-runner-validation --contract tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-contract.example.json --preflight tests/fixtures/repository_plugins/trusted-local-adapter-sandbox-preflight-report.example.json --output /tmp/trusted-local-adapter-sandbox-runner-validation-report.json
```

## Results

- Targeted docs contract: `1 passed`.
- Targeted sandbox runner tests: `6 passed`.
- Docs contracts: `131 passed`.
- Full pytest: `819 passed, 1 skipped`.
- Coverage: `90.79%`, above the configured `90%` gate.
- Ruff check: passed.
- Ruff format check: passed.
- `git diff --check`: passed.
- Swift package manifest dump: passed.
- Swift docs build: passed.
- DocC static generation: passed.
- CLI smoke: passed, emitted
  `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport` with
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `adapterProcessSpawned: false`, and `executedAdapterCount: 0`.

## Notes

The new validation report remains producer-side review evidence only. It does
not load third-party adapter code, spawn adapter processes, install
dependencies, invoke package managers, use network access, run AI, accept
packages or relations, publish registry metadata, remove `preview_only`, or
treat adapter output as registry truth.
