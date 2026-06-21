## REVIEW REPORT - P47-T3 Run Bounded Pilot Rerun Gate

**Scope:** `origin/main..HEAD`
**Files:** 15

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

- P47-T3 correctly keeps the bounded rerun gate as evidence-only authority:
  the static result, AI-enabled result, and sidecars remain proposal-only and
  are not promoted to registry truth.
- The failed AI-enabled batch is recorded as the intended gate evidence, not
  masked as a successful quality outcome. This preserves the Phase 47 boundary
  that larger curated corpus planning remains blocked until P47-T4 records an
  explicit exit decision.
- The temporary input mirror documents why clean `git archive` snapshots were
  used from already-pinned local checkouts, while preserving the original P46
  source manifest digest and same six-repository scope.

### Tests

- `PYTHONPATH=src python3 -m spec_harvester source-manifests /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs` - PASS.
- `PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-static --skip-ai --repository-profile-selection auto` - PASS.
- `PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1` - expected nonzero exit, evidence captured.
- `python3 -m json.tool tests/fixtures/targeted_pilot_bounded_rerun_gate/p47-t3-targeted-pilot-bounded-rerun-gate.example.json >/dev/null` - PASS.
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q -k 'targeted_pilot_bounded_rerun_gate'` - PASS, `1 passed, 169 deselected`.
- `ruff check tests/test_docs_contracts.py` - PASS.
- `ruff format --check tests/test_docs_contracts.py` - PASS.
- `git diff --check` - PASS.
- `PYTHONPATH=src python3 -m pytest` - PASS, `901 passed, 1 skipped`.
- `ruff check src tests` - PASS.
- `ruff format --check src tests` - PASS, `131 files already formatted`.
- `swift package dump-package >/dev/null` - PASS.
- `swift build --target SpecHarvesterDocs` - PASS.
- `PYTHONPATH=src uv run --extra dev pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` - PASS, `901 passed, 1 skipped`, total coverage `90.51%`.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings were identified.
- P47-T4 should record the targeted quality follow-up exit decision using the
  P47-T3 evidence: static-only gate passed, AI-enabled gate failed, and larger
  curated corpus remains blocked unless the exit decision explicitly chooses
  readiness from evidence.
