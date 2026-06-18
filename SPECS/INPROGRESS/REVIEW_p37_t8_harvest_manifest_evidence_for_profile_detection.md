## REVIEW REPORT — P37-T8 Harvest Manifest Evidence for Profile Detection

**Scope:** `feature/P37-T7-real-repository-profile-auto-selection..HEAD`  
**Files:** 18

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

- The implementation keeps workspace inventory as the primary source of profile
  evidence and only uses harvested manifest evidence when inventory has no
  profile evidence paths.
- The change stays language- and framework-agnostic: it consumes file `kind`
  metadata from `harvest.json` rather than naming FastMCP or Python.
- The root-manifest regression covers the P37-T7 failure mode without turning
  FastMCP into a normative fixture.

### Tests

Scoped validation run during EXECUTE:

```bash
PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q
PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile or autonomous_candidate_batch'
PYTHONPATH=src ruff check src/spec_harvester/autonomous_candidate_batch.py tests/test_autonomous_candidate_batch.py tests/test_docs_contracts.py
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Observed results:

```text
14 passed in 0.57s
15 passed in 0.08s
7 passed, 100 deselected in 0.03s
All checks passed!
120 files already formatted
```

Additional final Flow gates are expected before opening the pull request.

### Next Steps

FOLLOW-UP is skipped for this review because there are no new actionable
findings.
