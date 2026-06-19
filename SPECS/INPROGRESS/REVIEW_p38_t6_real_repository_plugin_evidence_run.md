## REVIEW REPORT — P38-T6 Real Repository Plugin Evidence Run

**Scope:** `origin/main..HEAD`
**Files:** 21

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None found.

### Secondary Issues

None found.

### Architectural Notes

- The real FastMCP fixture is correctly framed as producer-side review
  evidence. It records plugin applicability as a sidecar and keeps
  `appliedToDrafting: false` and `registryAuthority: false`.
- The task does not introduce runtime plugin loading, plugin execution,
  language-specific rules, package acceptance, relation acceptance, or
  registry publication.
- The comparison usefully records that current repository profile selection
  now chooses `generic.single_package.v0` for the pinned FastMCP checkout,
  while the P37-T7 baseline fell back to `generic.repository.v0`.
- Regression coverage checks selected plugin input consistency against the
  registry fixture, which guards against selecting plugins whose declared
  `inputEvidenceKinds[]` are missing from static evidence.

### Tests

- `python3 -m json.tool tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json >/tmp/p38-t6-plugin-real-run.pretty.json`
  passed.
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_plugin_real_run or current_next_task'`
  passed with `1 passed, 111 deselected` after archive.
- `PYTHONPATH=src pytest -q` passed with `766 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  passed with total coverage `91.16%`.
- `PYTHONPATH=src ruff check .`, `PYTHONPATH=src ruff format --check src tests`,
  `git diff --check`, and `swift build --target SpecHarvesterDocs` passed.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Before merge, verify the PR body follows the repository template and GitHub
  checks are green.
