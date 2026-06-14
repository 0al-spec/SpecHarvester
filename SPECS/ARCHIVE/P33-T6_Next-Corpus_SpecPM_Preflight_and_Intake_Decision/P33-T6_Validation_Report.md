# P33-T6 Validation Report: Next-Corpus SpecPM Preflight and Intake Decision

Task: P33-T6 Next-Corpus SpecPM Preflight and Intake Decision

## Scope

P33-T6 records the SpecPM consumer preflight outcome for the P33 next bounded
corpus after P33-T5 selected `serena.core`, `transmission.core`, and
`specpm.core` for the next handoff boundary.

This task did not run a new scrape, did not rerun LM Studio, did not clone or
fetch repositories, did not install dependencies, did not execute harvested
code, and did not mutate SpecPM registry state.

## SpecPM Revision

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
Merge pull request #140 from 0al-spec/codex/selected-candidate-handoff-preflight
```

## SpecPM Consumer Gate

Command:

```bash
PYTHONPATH=src python3 -m specpm.cli producer-bundle \
  preflight-selected-candidate-handoff \
  --body /Users/egor/Development/GitHub/0AL/SpecHarvester/tests/fixtures/next_corpus_candidate_layer_triage/p33-t5-next-corpus-candidate-layer-triage.example.json \
  --root /Users/egor/Development/GitHub/0AL/SpecHarvester \
  --json
```

Result:

```json
{
  "status": "failed",
  "summary": {
    "selectedCandidateCount": 0,
    "deferredCandidateCount": 0,
    "requiredEvidenceRoleCount": 0,
    "digestVerifiedCount": 0,
    "errorCount": 1,
    "warningCount": 0
  },
  "errors": [
    {
      "code": "selected_handoff_payload_missing",
      "field": "body"
    }
  ]
}
```

Interpretation: the current P33-T5 candidate-layer triage fixture is not a
supported SpecHarvester selected handoff payload. SpecPM correctly refuses to
treat candidate-layer triage as intake handoff evidence.

## Decision Fixture

Added:

- `tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json`
- `docs/NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`
- `Sources/SpecHarvester/Documentation.docc/NextCorpusSpecPMPreflightIntakeDecision.md`

Decision:

```text
not_ready_requires_durable_selected_handoff_artifact
```

Selected candidates that need a durable handoff artifact:

- `serena.core`
- `transmission.core`
- `specpm.core`

Deferred candidates that remain outside selected handoff:

- `mcpm.system`
- `specgraph.system`

## Quality Gates

```bash
python3 -m json.tool tests/fixtures/next_corpus_specpm_preflight_intake_decision/p33-t6-next-corpus-specpm-preflight-intake-decision.example.json
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'next_corpus_specpm_preflight_intake_decision or current_next_task or next_corpus_candidate_layer_triage'
PYTHONPATH=src pytest -q
PYTHONPATH=src ruff format tests/test_docs_contracts.py
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q
swift build --target SpecHarvesterDocs
swift package dump-package >/dev/null
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvester \
  --disable-indexing \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester \
  --output-path ./.docc-build
PYTHONPATH=src python -m spec_harvester source-manifests inputs/p33-next-corpus
```

Results:

- JSON syntax check: PASS.
- Targeted docs contracts: `4 passed, 80 deselected`.
- Full pytest: `660 passed, 1 skipped`.
- Ruff format applied to `tests/test_docs_contracts.py`, then format check PASS.
- Ruff check: PASS.
- `git diff --check`: PASS.
- Coverage: `91%`.
- Swift docs target build: PASS.
- DocC static generation: PASS with existing unrelated DocC warnings about
  unresolved historical references.
- Source manifest validation: `status: ok`, `repositoryCount: 5`.

## Boundary Check

P33-T6 preserves the non-authority boundary:

- no package acceptance;
- no relation acceptance;
- no baseline seeding;
- no `preview_only` removal;
- no public registry publication;
- no SpecPM pull request creation;
- no AI output treated as registry truth;
- no fabricated per-file evidence digests from summary-only fixtures.

## Verdict

PASS. P33-T6 records that the selected P33 scope is not ready for SpecPM
maintainer intake review until a durable selected handoff artifact exists or
the SpecPM consumer gate is explicitly extended.

