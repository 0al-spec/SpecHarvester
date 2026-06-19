# P41-T2 Validation Report

## Scope

P41-T2 adds the first machine-readable
`SpecHarvesterTrustedLocalAdapterRunRequest` fixture and documents its
producer-side request boundary.

## Artifacts

- `tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json`
- `docs/TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md`
- `Sources/SpecHarvester/Documentation.docc/TrustedLocalAdapterRunRequestFixture.md`
- Updated index, capabilities, roadmap, and readiness docs.
- Updated `tests/test_docs_contracts.py`.

## Validation

- `python3 -m json.tool tests/fixtures/repository_plugins/trusted-local-adapter-run-request.example.json`: PASS.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py::test_trusted_local_adapter_run_request_fixture_is_documented -q`: PASS, 1 passed.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`: PASS, 124 passed.
- `PYTHONPATH=src pytest -q`: PASS, 795 passed, 1 skipped.
- `PYTHONPATH=src ruff check .`: PASS.
- `PYTHONPATH=src ruff format --check src tests`: PASS after formatting
  `tests/test_docs_contracts.py`.
- `git diff --check`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.
- `PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q`: PASS,
  795 passed, 1 skipped, total coverage 91%.

## Boundary Checks

- The request fixture records explicit operator opt-in.
- The request fixture references Phase 40 adapter manifest and preflight
  report fixtures with SHA-256 digests.
- The request fixture records safe relative read allowlists, declared input
  artifacts, output policy, resource budgets, environment policy, network
  policy, dependency policy, package manager policy, process policy, and
  non-authority statements.
- The fixture keeps `requestIsExecutionPermission: false`,
  `adapterExecution: not_run`, `adapterCodeLoaded: false`,
  `appliedToDrafting: false`, and `registryAuthority: false`.
- No adapter loading, adapter execution, preflight implementation, runner,
  dependency installation, package manager invocation, harvested code
  execution, AI execution, package acceptance, relation acceptance, baseline
  seeding, registry publication, or `preview_only` removal was added.

## Verdict

PASS.
