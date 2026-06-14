## REVIEW REPORT — P20-T7 CodeGraph Compatibility Guard

**Scope:** `codex/p20-t6-codegraph-adapter-boundary..HEAD`
**Files:** 14

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None.

### Secondary Issues

None.

### Architectural Notes

- The guard is correctly fixture-first and bounded to local metadata. It does
  not install CodeGraph, run npm/npx, access the network, or index third-party
  repositories in ordinary CI.
- The optional executable probe remains opt-in through an explicit local path
  and forces `CODEGRAPH_NO_DOWNLOAD=1` into the probe environment.
- Required CLI surface expectations now validate both command names and
  `--json` args, which matches the P20-T7 contract more closely than
  name-only assertions.
- The normalized mapping check reuses the P20-T6 `SourceGraphIndexPayload`
  path, so compatibility drift is tested through the actual adapter boundary
  rather than a duplicated schema assertion.

### Tests

- `PYTHONPATH=src pytest tests/test_codegraph_compatibility.py -q`
  - `7 passed`
- `PYTHONPATH=src pytest tests/test_codegraph_compatibility.py tests/test_docs_contracts.py -q`
  - `97 passed`
- `PYTHONPATH=src python -m pytest`
  - `695 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `695 passed, 1 skipped`
  - Coverage: `90.75%`
- `PYTHONPATH=src ruff check src tests`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift package dump-package >/dev/null`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/specharvester-p20-t7-architecture-lint.json`
  - command passed with the existing advisory
    `manifest_parser_pattern` in `src/spec_harvester/license_provenance_reports.py`

### Next Steps

- FOLLOW-UP skipped: no actionable P20-T7 defects were found.
- Open the stacked PR with base `codex/p20-t6-codegraph-adapter-boundary`.
