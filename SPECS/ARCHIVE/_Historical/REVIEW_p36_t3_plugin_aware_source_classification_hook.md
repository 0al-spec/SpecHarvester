## REVIEW REPORT — P36-T3 Plugin-Aware Source Classification Hook

**Scope:** origin/main..HEAD
**Files:** 18

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None remaining.

### Secondary Issues

- [Low] Unknown parser profiles were initially validated only when the Python
  analyzer received the option. This could let unsupported parser profile ids
  be silently ignored for non-Python analyzer plans. Fixed in follow-up commit
  `e6427e7` by validating the parser profile before analyzer dispatch and
  adding regression coverage.

### Architectural Notes

- The hook remains deliberately small: it is an opt-in static path
  classifier, not a dynamic plugin runtime.
- Parser profile decisions are stored as extra package-level review metadata
  (`repositoryParsingProfile`, `pathClassification`) instead of diagnostics,
  so clean profile usage does not degrade `PublicInterfaceIndex.summary.status`.
- Only analyzers that declare `supports_parser_profile` receive the new option;
  JS/TypeScript, Go, and Swift analyzer compatibility is preserved.

### Tests

- `PYTHONPATH=src pytest -q` -> `731 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` -> `731 passed, 1 skipped`, total coverage `91.02%`
- `PYTHONPATH=src ruff check .` -> passed
- `PYTHONPATH=src ruff format --check src tests` -> passed
- `git diff --check` -> passed
- `swift build --target SpecHarvesterDocs` -> passed
- `swift package dump-package >/dev/null` -> passed
- DocC static generation -> passed

### Next Steps

- No additional P36-T3 follow-up is required.
- Continue with P36-T4: run the FastAPI AI-enabled comparison using
  `--parser-profile python.web_framework.v0`.
