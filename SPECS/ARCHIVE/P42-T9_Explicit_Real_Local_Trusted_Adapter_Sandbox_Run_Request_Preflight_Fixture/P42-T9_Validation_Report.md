# P42-T9 Validation Report

## Task

P42-T9 Explicit Real Local Trusted Adapter Sandbox Run Request Preflight Fixture

## Verdict

PASS

## Summary

P42-T9 adds a deterministic request preflight fixture for the P42-T8 explicit
real local trusted adapter sandbox run request. The fixture validates request
identity, digest linkage, prerequisite P42-T6/P42-T7 evidence requirements,
operator approval scope, safe path policy, runtime/output/audit boundaries, and
non-authority statements without loading adapter code, spawning adapter
processes, invoking package managers, using network access, accepting packages
or relations, or granting registry authority.

## Artifact Coverage

- Added
  `tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json`.
- Added GitHub docs and DocC mirror for the preflight fixture.
- Linked the preflight fixture from the P42-T8 request docs, runtime sandbox
  plan, docs index, DocC root, capabilities, and roadmap.
- Added regression coverage in `tests/test_docs_contracts.py`.

## Validation Commands

```text
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_explicit_real_local_sandbox_run_request_preflight_fixture_is_documented -q
1 passed
```

```text
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
136 passed
```

```text
python3 -m json.tool tests/fixtures/repository_plugins/explicit-real-local-trusted-adapter-sandbox-run-request-preflight.example.json >/dev/null
passed
```

```text
PYTHONPATH=src pytest -q
844 passed, 1 skipped
```

```text
PYTHONPATH=src ruff check src tests
All checks passed
```

```text
PYTHONPATH=src ruff check .
All checks passed
```

```text
PYTHONPATH=src ruff format --check src tests
131 files already formatted
```

```text
git diff --check
passed
```

```text
swift package dump-package >/tmp/specharvester-package-dump.json
passed
```

```text
swift build --target SpecHarvesterDocs
Build of target: 'SpecHarvesterDocs' complete
```

```text
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
844 passed, 1 skipped
Required test coverage of 90% reached. Total coverage: 90.47%
```

```text
swift package --allow-writing-to-directory /tmp/specharvester-docc-workflow-p42-t9 \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-docc-workflow-p42-t9 \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
Generated documentation archive at /tmp/specharvester-docc-workflow-p42-t9
```

## Notes

- A one-off exploratory `rg` command included a nonexistent `Makefile` path and
  exited with an expected file-not-found error. It was not a validation gate.
- No runtime runner was implemented.
- No adapter code loading, process spawning, dependency installation,
  package-manager invocation, network access, harvested-code execution, AI
  execution, registry acceptance, baseline seeding, or `preview_only` removal was
  added.
