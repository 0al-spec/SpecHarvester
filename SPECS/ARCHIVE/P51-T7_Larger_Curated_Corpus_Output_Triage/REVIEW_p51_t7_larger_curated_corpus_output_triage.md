## REVIEW REPORT — P51-T7 Larger Curated Corpus Output Triage

**Scope:** `main..HEAD`
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

- The triage fixture preserves the authority boundary: `selected_for_author_review`
  is explicitly not registry acceptance, and static, AI, enriched preview,
  triage, and adapter output remain non-authoritative review evidence.
- Hyperprompt is classified from P51-T6 repaired fallback evidence while the
  failed P51-T5 `hyperprompt.aiDraft` sidecar is explicitly superseded and
  `do_not_promote`.
- `xyflow`, `docc2context`, `hyperprompt`, and `specnode` caveats remain visible
  as registry-promotion blockers, but they do not block P51-T8 exit decision.

### Tests

- `python3 -m json.tool tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json >/dev/null`
- `python3 -m ruff format tests/test_docs_contracts.py && PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_output_triage" -q`
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python3 -m pytest`
- `python3 -m ruff format --check src tests && python3 -m ruff check src tests && git diff --check`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `swift package dump-package >/dev/null && swift build --target SpecHarvesterDocs`

Coverage remains above the required threshold at `90.49%`.

### Next Steps

FOLLOW-UP skipped: no actionable review findings were identified.
