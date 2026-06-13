# P33-T8 Validation Report

Task: P33-T8 Next-Corpus Intake Readiness Decision
Date: 2026-06-14
Verdict: PASS

## Summary

P33-T8 records the final Phase 33 next-corpus intake readiness decision as
machine-readable producer preview evidence.

The decision fixture records:

- status: `ready_for_author_maintainer_review_with_explicit_deferral`;
- selected candidates: `serena.core`, `transmission.core`, `specpm.core`;
- deferred candidates: `mcpm.system`, `specgraph.system`;
- SpecPM selected handoff preflight status: `passed`;
- selectedCandidateCount: 3;
- deferredCandidateCount: 2;
- requiredEvidenceRoleCount: 4;
- digestVerifiedCount: 1;
- warningCount: 0;
- errorCount: 0.

The task did not run a new scrape, rerun LM Studio, clone/fetch repositories,
install dependencies, execute harvested code, mutate generated candidates,
accept packages, accept relations, seed baselines, remove `preview_only`,
publish registry metadata, or create a SpecPM pull request.

## Artifacts

- `tests/fixtures/next_corpus_intake_readiness_decision/p33-t8-next-corpus-intake-readiness-decision.example.json`
- `docs/NEXT_CORPUS_INTAKE_READINESS_DECISION.md`
- `Sources/SpecHarvester/Documentation.docc/NextCorpusIntakeReadinessDecision.md`
- Updated Phase 33 references in docs, DocC, roadmap, workplan, and
  docs-contract tests.

## SpecPM Preflight Evidence

Command:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle \
  preflight-selected-candidate-handoff \
  --body /Users/egor/Development/GitHub/0AL/SpecHarvester/tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json \
  --root /Users/egor/Development/GitHub/0AL/SpecHarvester \
  --json
```

Result:

```json
{
  "status": "passed",
  "summary": {
    "selectedCandidateCount": 3,
    "deferredCandidateCount": 2,
    "requiredEvidenceRoleCount": 4,
    "digestVerifiedCount": 1,
    "errorCount": 0,
    "warningCount": 0
  }
}
```

SpecPM revision:

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
```

## Validation Commands

```bash
python3 -m json.tool tests/fixtures/next_corpus_intake_readiness_decision/p33-t8-next-corpus-intake-readiness-decision.example.json >/tmp/p33-t8-json-check.json
PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'intake_readiness_decision or durable_selected_handoff or current_next_task'
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src python -m spec_harvester source-manifests inputs/p33-next-corpus
PYTHONPATH=src python -m pytest -q
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --disable-indexing --transform-for-static-hosting --hosting-base-path SpecHarvester --output-path ./.docc-build
```

## Validation Results

- JSON fixture parse: passed.
- Targeted docs-contract tests: `5 passed, 83 deselected`.
- Ruff check: passed.
- Ruff format check: `107 files already formatted`.
- Git diff whitespace check: passed.
- Source manifest CLI check: `status: ok`, `repositoryCount: 5`.
- Full pytest: `664 passed, 1 skipped`.
- Swift package dump: passed.
- Swift docs target build: passed.
- Coverage: `664 passed, 1 skipped`, total coverage `90.56%`, coverage gate
  passed with required threshold `90%`.
- Static DocC generation: passed with pre-existing unrelated warnings for
  `AcceptedPackageUpdateProposals` and inline command references.

## Acceptance Criteria

- Decision status is
  `ready_for_author_maintainer_review_with_explicit_deferral`: satisfied.
- Selected candidate count is 3: satisfied.
- Deferred candidate count is 2: satisfied.
- SpecPM preflight status is `passed`: satisfied.
- Warning count is 0 and error count is 0: satisfied.
- The decision is review evidence only and does not perform registry
  acceptance, relation acceptance, baseline seeding, `preview_only` removal,
  registry publication, or SpecPM PR creation: satisfied.
- Documentation and tests link the decision from Phase 33 docs, roadmap, docs
  index, and DocC: satisfied.
