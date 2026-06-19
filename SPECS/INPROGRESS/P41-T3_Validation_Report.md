# P41-T3 Validation Report

## Scope

P41-T3 adds the first machine-readable
`SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture and documents its
review-only preflight boundary.

## Artifacts

- `tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`
- `docs/TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md`
- `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRunPreflightReportFixture.md`
- Updated request, readiness, index, capabilities, and roadmap docs.
- Updated `tests/test_docs_contracts.py`.

## Validation

- `python3 -m json.tool tests/fixtures/repository_plugins/trusted-local-adapter-run-preflight-report.example.json`: PASS.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_run_preflight_report_fixture_is_documented -q`: PASS, 1 passed.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`: PASS, 125 passed.
- `PYTHONPATH=src pytest -q`: PASS, 796 passed, 1 skipped.
- `PYTHONPATH=src ruff check .`: PASS.
- `PYTHONPATH=src ruff format --check src tests`: PASS after formatting
  `tests/test_docs_contracts.py`.
- `git diff --check`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`: PASS,
  796 passed, 1 skipped, total coverage 91%.

## Boundary Checks

- The preflight report references the P41-T2 run request fixture with a
  SHA-256 digest.
- The fixture records accepted checks for request identity, explicit operator
  opt-in, adapter references, declared input artifacts, read allowlists,
  output policy, resource budgets, environment policy, network policy,
  dependency policy, package manager policy, process policy, execution
  boundary, and non-authority statements.
- The fixture records rejected checks for unsafe paths, missing or mismatched
  digests, undeclared input artifacts, undeclared output paths, network access,
  dependency installation, package manager invocation, harvested code
  execution, AI execution, unbounded process execution, and unbounded outputs.
- The fixture records blocked checks for adapter execution, third-party
  adapter code loading, and registry authority requests.
- The fixture keeps `preflightPassIsExecutionPermission: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `executedAdapterCount: 0`, `appliedToDrafting: false`, and
  `registryAuthority: false`.
- No adapter loading, adapter execution, preflight CLI, runner, dependency
  installation, package manager invocation, harvested code execution, AI
  execution, package acceptance, relation acceptance, baseline seeding,
  registry publication, or `preview_only` removal was added.

## Verdict

PASS.
