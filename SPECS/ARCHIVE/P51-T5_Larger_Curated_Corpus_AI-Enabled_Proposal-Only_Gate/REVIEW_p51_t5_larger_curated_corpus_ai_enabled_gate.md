## REVIEW REPORT — P51-T5 Larger Curated Corpus AI-Enabled Gate

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

- P51-T5 preserves the Phase 51 static-only-before-AI ordering: the fixture
  links back to the P51-T4 static-only gate and uses the same 12-source P51
  manifest.
- The live local LM Studio run is recorded honestly as AI-enabled gate status
  `failed`, while the Flow task itself passes as evidence capture. This matches
  the prior P46/P47/P48 pattern for controlled failed AI proposal layers.
- The failed `hyperprompt.aiDraft` sidecar remains proposal-only evidence and
  is carried into P51-T6 triage as a do-not-promote/deferred classification
  candidate, not as registry truth.
- No runtime harvesting code changed. The implementation adds durable evidence,
  docs, DocC mirroring, archive state, and docs-contract coverage.
- `next.md` correctly selects P51-T6 output triage after archive, with explicit
  no-rerun/no-AI/no-acceptance boundaries.

### Tests

- `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p51-larger-curated-corpus`
  - PASS: `repositoryCount: 12`
- `curl -sS http://127.0.0.1:1234/v1/models`
  - PASS: model list included `openai/gpt-oss-20b`
- `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p51-larger-curated-corpus --out /tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z/output --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1 --apply-ai-enrichment`
  - EXPECTED NONZERO EXIT: exit code `1`, batch status `failed`, evidence captured
- `python3 -m json.tool tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json >/dev/null`
  - PASS
- `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_ai_enabled_gate or larger_curated_corpus_static_only_gate"`
  - PASS after archive: `2 passed, 183 deselected`
- `python3 -m ruff format tests/test_docs_contracts.py`
  - PASS: `1 file reformatted`
- `git diff --check`
  - PASS
- `python3 -m ruff format --check src tests`
  - PASS: `131 files already formatted`
- `python3 -m ruff check src tests`
  - PASS: `All checks passed!`
- `PYTHONPATH=src python3 -m pytest`
  - PASS: `916 passed, 1 skipped`
- `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `916 passed, 1 skipped`; total coverage `90.48%`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

### Next Steps

FOLLOW-UP is skipped because this review found no actionable issues.

P51-T6 should triage all static candidates, relation proposals, AI draft
sidecars, AI enrichment sidecars, AI-enriched preview copies, warning evidence,
the failed `hyperprompt.aiDraft` sidecar, and carried-forward caveats without
rerunning the larger corpus or changing registry truth.
