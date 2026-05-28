## REVIEW REPORT — p16_t4_reduce_broad_semantic_intent_claims

**Scope:** origin/main..HEAD
**Files:** 10

### Summary Verdict
- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues
- None.

### Secondary Issues
- None.

### Architectural Notes
- Broad language-neutral semantic intents are now record-only signals for the
  governance duplicate-claim report.
- The report schema is preserved: broad intents remain visible in `records`,
  while `duplicates.intent` omits weak cross-package duplicate signals.
- Specific intent duplicates and duplicate capability claims retain existing
  behavior.
- The change does not alter generated `specpm.yaml` manifests, SpecPM
  proposal flows, model prompting, or analyzer outputs.
- Existing architecture-lint advisory `manifest_parser_pattern` in
  `src/spec_harvester/license_provenance_reports.py` predates this task and is
  unrelated to P16-T4.

### Tests
- `PYTHONPATH=src python -m pytest tests/test_governance_reports.py tests/test_docs_contracts.py -q`
  - PASS: 31 passed.
- `PYTHONPATH=src python -m pytest`
  - PASS: 418 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 418 passed, 1 skipped, total coverage 91.87%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 68 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t4-dup-builtin.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`.
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t4-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`.
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t4-architecture-lint.json`
  - ATTENTION: existing advisory `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`.

### Next Steps
- FOLLOW-UP skipped: no actionable review findings.
- Verify the PR body matches `.github/PULL_REQUEST_TEMPLATE.md`.
- After merge, continue with P16-T5 to rerun the representative local
  validation matrix.
