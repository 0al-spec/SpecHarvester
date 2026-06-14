# P35-T3 Validation Report

## Summary

P35-T3 documented the candidate source classifier plan for Phase 35. The plan
defines how package-like source units should be classified before drafting so
examples, tooling, generated artifacts, internal utilities, type-only packages,
deprecated sources, and evidence-only units do not become primary candidates
accidentally.

## Changed Artifacts

- `docs/CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`
- `Sources/SpecHarvester/Documentation.docc/CandidateSourceClassifierPlan.md`
- `tests/fixtures/source_classifier_plan/p35-t3-source-classifier-plan.example.json`
- `docs/SPECHARVESTER_CORPUS_PLAN.md`
- `Sources/SpecHarvester/Documentation.docc/SpecHarvesterCorpusPlan.md`
- `docs/README.md`
- `docs/CAPABILITIES.md`
- `Sources/SpecHarvester/Documentation.docc/Capabilities.md`
- `Sources/SpecHarvester/Documentation.docc/SpecHarvester.md`
- `docs/ROADMAP.md`
- `Sources/SpecHarvester/Documentation.docc/Roadmap.md`
- `tests/test_docs_contracts.py`

## Contract Coverage

The classifier plan defines:

- `apiVersion: spec-harvester.source-classification-plan/v0`;
- `kind: SpecHarvesterCandidateSourceClassificationPlan`;
- `schemaVersion: 1`;
- `authority: producer_classification_plan_only`;
- source classes;
- allowed actions;
- local reviewable inputs;
- classification output shape;
- reason codes;
- operator override expectations;
- stop conditions;
- non-authority statements.

## Fixture Coverage

The fixture covers:

- `package_set_root`;
- `primary_package`;
- `plugin_package`;
- `example_package`;
- `tooling_package`;
- `types_only_package`;
- `generated_artifact`;
- `internal_utility`;
- `deprecated_source`;
- `evidence_only`;
- all allowed actions: `select_primary`, `select_member`, `defer`,
  `exclude`, and `include_as_evidence_only`.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_candidate_source_classifier_plan_contract_is_documented -q
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

- Focused classifier plan test: passed.
- Full docs contract suite: `95 passed`.
- Full pytest suite: `720 passed, 1 skipped`.
- Ruff check: passed.
- Ruff format check: passed after formatting `tests/test_docs_contracts.py`.
- Diff whitespace check: passed.
- Swift docs target build: passed.
- Swift package manifest dump: passed.
- Coverage gate: passed, `90.96%` total coverage with required `90%`.
- DocC static generation: passed and generated `.docc-build`.

## Verdict

Passed. P35-T3 is ready for Flow archive and review.
