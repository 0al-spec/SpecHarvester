## REVIEW REPORT — p33_t4_live_local_model_next_corpus_dry_run

**Scope:** `codex/p33-t3-deterministic-next-corpus-dry-run..HEAD`
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

- P33-T4 remains correctly scoped as producer preview evidence. The live local
  model output is documented as proposal-only and does not replace generated
  package files, accepted SpecPM metadata, package acceptance, relation
  acceptance, baseline seeding, or `preview_only` policy.
- The new fixture keeps the deterministic P33-T3 baseline explicit, records
  provider identity and privacy boundaries, and preserves the P33 gate sequence
  by selecting P33-T5 candidate-layer triage as the next step.
- The review findings are intentionally carried forward instead of silently
  normalized: `ai_draft_no_proposal_subjects`,
  `ai_draft_warning_diagnostics`, and package-id drift signals remain visible
  for P33-T5.

### Tests

- `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p33-next-corpus`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` — `80 passed`
- `PYTHONPATH=src python -m pytest -q` — `656 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` — `656 passed, 1 skipped`, coverage `90.56%`
- `PYTHONPATH=src ruff check src tests`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvesterDocs --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester`

### Next Steps

- FOLLOW-UP skipped: no actionable findings.
- Continue with P33-T5, using the archived P33-T4 fixture and docs as the
  candidate-layer triage input.
