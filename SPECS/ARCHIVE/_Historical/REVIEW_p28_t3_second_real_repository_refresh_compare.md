## REVIEW REPORT — P28-T3 Second Real Repository Refresh Compare Run

**Scope:** `origin/main..HEAD`
**Files:** Flow artifacts, docs, DocC mirror, docs-contract tests

### Summary Verdict

- [x] Approve with comments
- [ ] Request changes
- [ ] Block

P28-T3 meets its objective: a second real package-set-capable repository was
run through SpecHarvester and local SpecPM, proving the fresh refresh compare
handoff is not calibrated only against `xyflow`.

### Critical Issues

- None.

### Secondary Issues

- [Medium] Generic monorepo package-set role selection is still too operator
  dependent. The default TanStack/query draft produced only
  `tanstack_query.workspace`; the useful package-set required explicit
  `--role workspace --role member_package`. Follow-up should add a named role
  selection profile or preset so common monorepos do not require ad hoc CLI
  knowledge.
- [Medium] Refresh comparison currently assumes a current SpecPM generated
  baseline. TanStack/query correctly produced a structured
  `refresh_decision_prepare_current_contract_files_missing` result, but that
  means first-time repositories need a separate first-submission or
  seeded-baseline workflow before refresh comparison can emit a decision file.

### Architectural Notes

- The missing-baseline result is the right trust boundary. SpecHarvester should
  not invent SpecPM registry truth for a repository that has not been seeded or
  accepted.
- The 39-candidate / 38-relation TanStack/query output shows that the existing
  package-set model can describe a larger workspace once the intended role set
  is selected.
- P28-T3 should remain a recorded dry run, not a registry update or proposal to
  publish TanStack/query packages.

### Tests

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester`

Coverage was already re-run during EXECUTE with `90%` total coverage, above the
project threshold.

### Next Steps

- Add a follow-up task for package-set role selection profiles/presets.
- Add a follow-up task for first-submission or seeded-baseline refresh workflow.
