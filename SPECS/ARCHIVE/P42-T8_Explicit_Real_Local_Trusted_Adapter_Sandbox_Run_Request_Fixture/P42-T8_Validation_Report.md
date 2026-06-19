# P42-T8 Validation Report

## Verdict

Passed.

## Implemented Scope

- Added
  `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture.
- The fixture records:
  - P42-T6 verifier report contract requirements;
  - P42-T7 readiness report contract requirements;
  - scoped future operator approval requirements;
  - adapter package identity and digest;
  - target repository identity and revision;
  - sandbox policy identity and version;
  - runtime, filesystem/output, audit, rollback, and review policy;
  - no-execution request boundary;
  - non-authority statements.
- Added GitHub docs and DocC docs.
- Linked the new fixture from docs index, DocC root, capabilities, roadmap,
  sandbox plan, verifier docs, and readiness docs.
- Added docs-contract regression coverage for fixture shape, safe paths,
  approval scope, execution boundary, non-authority statements, and links.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_trusted_adapter_sandbox_run_request_fixture_is_documented -q
```

Result: `1 passed`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `135 passed`.

```bash
python -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request.example.json >/dev/null
```

Result: passed.

```bash
PYTHONPATH=src pytest -q
```

Result: `843 passed, 1 skipped`.

```bash
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed; `131 files already formatted`.

```bash
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
```

Result: `843 passed, 1 skipped`; total coverage `90.47%`.

```bash
swift package --allow-writing-to-directory ./.docc-build \
  generate-documentation \
  --target SpecHarvesterDocs \
  --disable-indexing \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester \
  --output-path ./.docc-build
```

Result: generated documentation archive at `./.docc-build`.

## Notes

- `.docc-build` was removed after local generation.
- P42-T8 remains request-only evidence. It does not grant execution
  permission, operator approval, registry authority, package/relation
  acceptance, baseline seeding, publication authority, or adapter output truth.
