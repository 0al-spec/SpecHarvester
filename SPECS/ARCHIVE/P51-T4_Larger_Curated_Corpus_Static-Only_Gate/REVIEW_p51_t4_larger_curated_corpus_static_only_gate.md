## REVIEW REPORT — P51-T4 Larger Curated Corpus Static-Only Gate

**Scope:** `origin/main..HEAD`
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

- The P51-T4 gate preserves the static-only-before-AI ordering from Phase 51.
  It allows P51-T5 only after a passed static-only batch over the same 12-source
  manifest.
- The durable fixture records real `/tmp` batch evidence while keeping all
  generated candidates and relations producer-side preview evidence only.
- The run produced 15 preview candidates and three relation proposals, all from
  static evidence. AI draft/enrichment proposal counts remain zero.
- No runtime harvesting behavior changed. The implementation adds evidence,
  docs, DocC mirroring, and docs-contract coverage.
- xyflow and docc2context caveats remain visible for P51-T6 triage.
- `next.md` correctly selects P51-T5 AI-enabled proposal-only gate after
  archive.

### Tests

- `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p51-larger-curated-corpus`
  - PASS: `repositoryCount: 12`
- `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p51-larger-curated-corpus --out /tmp/specharvester-p51-t4-larger-curated-corpus-static-only-20260625T103322Z/output --skip-ai --repository-profile-selection auto`
  - PASS: batch status `passed`
- `python3 -m json.tool tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_static_only_gate or larger_curated_corpus_checkout_readiness or larger_curated_corpus_source_plan or larger_curated_corpus_planning_phase"`
  - PASS: `4 passed, 180 deselected`
- `python3 -m ruff format --check src tests`
  - PASS
- `python3 -m ruff check src tests`
  - PASS
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `915 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: total coverage `90.48%`, threshold `90%`
- `swift package describe`
  - PASS
- `swift package dump-package`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS
- `swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs`
  - PASS
- `git diff --check`
  - PASS

### Next Steps

- No actionable follow-up tasks are required from this review.
- FOLLOW-UP is skipped.
- Archive this review report into the P51-T4 archive folder.
