## REVIEW REPORT — p19_t1_static_spec_renderer

**Scope:** `origin/feature/P18-T1-swift-public-api-analyzer..HEAD`
**Files:** 17

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

- The renderer keeps SpecPM as validation and registry authority. It reads local
  candidate YAML only to produce a browser-oriented `SpecHarvesterStaticSpecPackage`
  JSON payload.
- The browser side has no YAML parser, no npm build step, and no runtime network
  dependency. `index.html` embeds escaped JSON for `file://` preview while
  preserving `spec-package.json` for static hosting and tooling.
- During review, two trust-boundary hardening gaps were fixed before this report:
  referenced spec symlinks are rejected before path resolution hides the symlink,
  and non-finite YAML floats such as `.nan` are rejected as non-JSON values.
- `PyYAML>=6.0` is a new direct runtime dependency. This is justified because the
  renderer consumes real SpecPM YAML rather than the limited source-manifest
  subset parsed elsewhere in SpecHarvester.
- The PR is stacked on `feature/P18-T1-swift-public-api-analyzer`; after PR #95
  lands, this branch should be rebased or retargeted to `main`.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py -q`:
  PASS, `7 passed`.
- `PYTHONPATH=src python -m pytest tests/test_static_spec_renderer.py tests/test_docs_contracts.py -q`:
  PASS, `33 passed`.
- `ruff check src tests`: PASS.
- `ruff format --check src tests`: PASS.
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/spec-harvester-architecture-lint-p19.json`:
  PASS command exit; existing advisory `manifest_parser_pattern` remains limited
  to `src/spec_harvester/license_provenance_reports.py`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --backend pylint --path src/spec_harvester --min-lines 8 --output /tmp/spec-harvester-pylint-duplicates-p19.json`:
  PASS, `duplicateBlockCount: 0`.
- `swift package dump-package >/dev/null`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS.
- `PYTHONPATH=src python -m pytest`: PASS, `446 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  PASS, total coverage `91.76%`.
- Local collect/draft/render smoke: PASS, renderer returned `status: ok` and
  wrote `index.html`, `assets/spec-renderer.js`, `assets/spec-renderer.css`, and
  `spec-package.json`.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings remain.
- Before merge, the PR body should match `.github/PULL_REQUEST_TEMPLATE.md` and
  explicitly state that this is a stacked PR on top of PR #95.
