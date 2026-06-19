# P42-T6 Validation Report

## Verdict

Passed.

## Implemented Scope

- Added `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport`.
- Added `synthetic-trusted-local-adapter-sandbox-run-verifier` CLI.
- Verified P42-T5 fixture identity and authority.
- Verified linked sandbox contract, sandbox preflight, and sandbox runner
  validation digests.
- Verified operator approval binding to one adapter, repository revision,
  sandbox policy, runner validation report, and output root.
- Verified synthetic output candidate safe paths, byte sizes, SHA-256 digests,
  adapter identity, and source input digest references.
- Verified audit record path/digest/reference requirements.
- Preserved no-real-execution, no-dependency-install, no-package-manager,
  no-network, no-registry-authority, and no-output-acceptance boundaries.
- Added GitHub docs, DocC docs, roadmap/capabilities links, and regression
  tests.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_trusted_local_adapter_synthetic_sandbox_run_verifier.py -q
```

Result: `10 passed`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_synthetic_trusted_local_adapter_sandbox_run_verifier_is_documented -q
```

Result: `1 passed`.

```bash
PYTHONPATH=src pytest tests/test_trusted_local_adapter_synthetic_sandbox_run_verifier.py tests/test_docs_contracts.py::test_synthetic_trusted_local_adapter_sandbox_run_verifier_is_documented -q
```

Result: `11 passed`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `133 passed`.

```bash
PYTHONPATH=src pytest -q
```

Result: `831 passed, 1 skipped`.

```bash
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed; `129 files already formatted`.

```bash
PYTHONPATH=src python -m spec_harvester.cli \
  synthetic-trusted-local-adapter-sandbox-run-verifier \
  --fixture tests/fixtures/repository_plugins/synthetic-trusted-local-adapter-sandbox-run.example.json \
  --output /tmp/spec-harvester-p42-t6-verifier-report.json
```

Result: `status: passed`, `linkedArtifactCount: 3`,
`syntheticOutputCandidateCount: 3`, `executedAdapterCount: 0`.

```bash
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
```

Result: `831 passed, 1 skipped`; total coverage `90.53%`.

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
- Verification remains producer-side review evidence only and does not grant
  real adapter execution permission or registry authority.
