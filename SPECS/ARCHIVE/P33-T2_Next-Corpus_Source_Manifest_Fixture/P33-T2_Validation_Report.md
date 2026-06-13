# P33-T2 Validation Report

**Task:** P33-T2 Next-Corpus Source Manifest Fixture
**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P33-T2 adds the next bounded corpus source manifest fixture before any new
scrape runs. The change commits the existing source manifest YAML shape,
records a companion `SpecHarvesterNextCorpusSourceManifestFixture`, links
operator docs and DocC, and adds docs-contract coverage.

## Commands

```bash
PYTHONPATH=src python3 -m spec_harvester source-manifests inputs/p33-next-corpus
```

Result: `status: ok`, `repositoryCount: 5`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'bounded_corpus_expansion_plan or next_corpus_source_manifest' -x --tb=short
```

Result: `2 passed, 76 deselected`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `78 passed`.

```bash
PYTHONPATH=src ruff check .
```

Result: `All checks passed!`.

```bash
PYTHONPATH=src ruff format tests/test_docs_contracts.py
PYTHONPATH=src ruff format --check src tests
```

Result: `1 file reformatted`, then `107 files already formatted`.

## Notes

- No collection run was executed.
- No deterministic draft run was executed.
- No live local-model run was executed.
- No repository was cloned or fetched.
- No dependencies were installed.
- No harvested code or package script was executed.
- No SpecPM registry metadata was published.
- No packages or relations were accepted.
- No `preview_only` flag was removed.
