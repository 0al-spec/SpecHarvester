# P35-T2 Validation Report

## Summary

P35-T2 defined the machine-readable `SpecHarvesterCorpusPlan` contract for
curated multi-ecosystem source batches.

## Changed Artifacts

- `docs/SPECHARVESTER_CORPUS_PLAN.md`
- `Sources/SpecHarvester/Documentation.docc/SpecHarvesterCorpusPlan.md`
- `tests/fixtures/corpus_plan/p35-t2-corpus-plan.example.json`
- `docs/CORPUS_SELECTION_POLICY.md`
- `Sources/SpecHarvester/Documentation.docc/CorpusSelectionPolicy.md`
- `docs/README.md`
- `docs/CAPABILITIES.md`
- `Sources/SpecHarvester/Documentation.docc/Capabilities.md`
- `Sources/SpecHarvester/Documentation.docc/SpecHarvester.md`
- `docs/ROADMAP.md`
- `Sources/SpecHarvester/Documentation.docc/Roadmap.md`
- `tests/test_docs_contracts.py`

## Contract Coverage

The contract defines:

- `apiVersion: spec-harvester.corpus-plan/v0`;
- `kind: SpecHarvesterCorpusPlan`;
- `schemaVersion: 1`;
- `authority: producer_corpus_plan_only`;
- corpus metadata and per-ecosystem quotas;
- selected/deferred/rejected source entries;
- selected, deferred, rejected, and excluded-subpackage reason codes;
- pinned local checkout expectations;
- expected analyzer coverage;
- stop conditions;
- downstream autonomous-batch command plan;
- required non-authority statements.

## Fixture Coverage

The fixture covers:

- selected sources for JavaScript/TypeScript, Python, Rust, Go, and Swift;
- deferred `types.react` source using `types_only_package`;
- rejected React internal test utility using `test_fixture` and
  `registry_search_noise`;
- required non-authority statements.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_curated_multi_ecosystem_corpus_selection_phase_is_planned tests/test_docs_contracts.py::test_spec_harvester_corpus_plan_contract_is_documented -q
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift build --target SpecHarvesterDocs
swift package dump-package >/dev/null
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester
```

## Results

- Focused P35-T1/P35-T2 docs-contract tests: `2 passed`.
- Full docs contract suite: `94 passed`.
- Full pytest suite: `719 passed, 1 skipped`.
- Ruff check: passed.
- Ruff format check: passed after formatting `tests/test_docs_contracts.py`.
- Diff whitespace check: passed.
- Swift docs target build: passed.
- Swift package manifest dump: passed.
- Coverage gate: passed, `90.96%` total coverage with required `90%`.
- DocC static generation: passed and generated `.docc-build`.

## Verdict

Passed. P35-T2 is ready for Flow archive and review.
