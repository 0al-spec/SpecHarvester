# P35-T1 Validation Report

## Summary

P35-T1 added the corpus selection policy for Phase 35. The policy records how
SpecHarvester should choose important multi-ecosystem repository/package-family
targets without becoming an open-ended registry crawler.

## Changed Artifacts

- `docs/CORPUS_SELECTION_POLICY.md`
- `Sources/SpecHarvester/Documentation.docc/CorpusSelectionPolicy.md`
- `docs/README.md`
- `docs/CAPABILITIES.md`
- `Sources/SpecHarvester/Documentation.docc/SpecHarvester.md`
- `Sources/SpecHarvester/Documentation.docc/Capabilities.md`
- `docs/ROADMAP.md`
- `Sources/SpecHarvester/Documentation.docc/Roadmap.md`
- `tests/test_docs_contracts.py`

## Policy Coverage

The policy covers:

- bounded curated corpus scope;
- repository/package-family selection units;
- importance signals;
- ecosystem quotas;
- exclusion and deferral rules;
- pinned local checkout requirements;
- local-only harvesting boundary;
- non-authority review boundary;
- Phase 35 follow-up tasks from `P35-T2` through `P35-T6`.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_curated_multi_ecosystem_corpus_selection_phase_is_planned -q
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift package dump-package >/dev/null
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester
```

## Results

- Focused corpus selection policy test: passed.
- Full docs contract suite: `93 passed`.
- Full pytest suite: `718 passed, 1 skipped`.
- Ruff check: passed.
- Ruff format check: `116 files already formatted`.
- Diff whitespace check: passed.
- Swift docs target build: passed.
- Coverage gate: passed, `90.96%` total coverage with required `90%`.
- Swift package manifest dump: passed.
- DocC static generation: passed and generated `.docc-build`.

## Verdict

Passed. P35-T1 is ready for Flow archive and review.
