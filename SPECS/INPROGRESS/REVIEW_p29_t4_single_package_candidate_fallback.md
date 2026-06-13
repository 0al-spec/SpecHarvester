## REVIEW REPORT — P29-T4 Single-Package Candidate Fallback

**Scope:** `codex/p29-t3-corpus-baseline-gap-report..HEAD`
**Files:** 21

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

- The fallback is intentionally narrow: it activates only when there are no
  selected package records and no inventory package records at all. This avoids
  converting example/tooling-only monorepos into fake core packages.
- Source manifest `packageId` is preserved in workspace inventory source
  metadata and used as the fallback package identity when available.
- The candidate is generated from the repository-level `harvest.json` and
  colocated `public-interface-index.json`, so it reuses deterministic evidence
  instead of inventing package metadata.
- Relation output remains explicit but empty: `package-relation-proposals.json`
  is written with `relationCount: 0`.
- The real Flask/Gin/xyflow deterministic smoke confirms the original P29-T3
  blocker is removed for Flask and Gin while xyflow package-set behavior stays
  intact.

### Tests

- `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py -q`
  - PASS: `24 passed`
- `PYTHONPATH=src python -m pytest tests/test_autonomous_candidate_batch.py -q`
  - PASS: `6 passed`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: `54 passed`
- `PYTHONPATH=src python -m pytest tests/test_autonomous_candidate_batch.py tests/test_package_set_drafter.py tests/test_docs_contracts.py tests/test_batch_collection.py::test_collect_batch_snapshots_emits_deterministic_workspace_inventory -q`
  - PASS: `85 passed`
- `PYTHONPATH=src python -m pytest -q`
  - PASS: `618 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `618 passed, 1 skipped`, coverage `90.07%`
- `PYTHONPATH=src ruff check src tests`
  - PASS
- `PYTHONPATH=src ruff format --check src tests`
  - PASS
- `git diff --check`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- Real deterministic corpus smoke:
  - Flask: `1` candidate, `0` relations, preflight `passed`.
  - Gin: `1` candidate, `0` relations, preflight `passed`.
  - xyflow: `4` candidates, `3` relations, preflight `passed`.

### Next Steps

- FOLLOW-UP skipped: no new actionable findings were found during review.
- Continue with the already selected `P29-T5 LM Studio JSON Repair and Retry`.
