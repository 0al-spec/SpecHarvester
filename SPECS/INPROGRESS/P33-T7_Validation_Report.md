# P33-T7 Validation Report: Durable Next-Corpus Selected Handoff Artifact

Task: P33-T7 Durable Next-Corpus Selected Handoff Artifact

## Scope

P33-T7 creates a durable selected handoff artifact for the P33 next bounded
corpus selected scope:

- `serena.core`;
- `transmission.core`;
- `specpm.core`.

It keeps `mcpm.system` and `specgraph.system` deferred. The task does not run a
new scrape, rerun LM Studio, clone repositories, fetch remote state, install
dependencies, execute harvested code, mutate generated bundles, accept
packages, accept relations, seed baselines, remove `preview_only`, publish
registry metadata, or create a SpecPM pull request.

## Durable Artifact

Added:

- `tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json`
- `docs/NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`
- `Sources/SpecHarvester/Documentation.docc/NextCorpusDurableSelectedHandoff.md`

The durable artifact uses supported SpecPM selected handoff identity:

```json
{
  "apiVersion": "spec-harvester.selected-candidate-handoff-proposal/v0",
  "kind": "SpecHarvesterSelectedCandidateHandoffProposal",
  "schemaVersion": 1,
  "authority": "producer_preview_evidence_only"
}
```

It references only committed, digest-backed P33 evidence:

- P33-T5 candidate-layer triage fixture;
- P33-T4 live local-model fixture;
- P33-T3 deterministic fixture;
- P33-T2 source manifest.

It intentionally does not fabricate per-file generated candidate digests.

## SpecPM Consumer Gate

SpecPM revision:

```text
8a5ce3dece3d18bf8f601a5a599520bd520c7839
Merge pull request #140 from 0al-spec/codex/selected-candidate-handoff-preflight
```

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

## Quality Gates

```bash
python3 -m json.tool tests/fixtures/next_corpus_durable_selected_handoff/p33-t7-next-corpus-selected-handoff.example.json
PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'durable_selected_handoff or current_next_task or next_corpus_specpm_preflight_intake_decision'
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
- SpecPM selected handoff preflight: PASS.
- Targeted docs contracts: `4 passed, 82 deselected`.
- Full pytest: `662 passed, 1 skipped`.
- Ruff format applied to `tests/test_docs_contracts.py`, then format check PASS.
- Ruff check: PASS.
- `git diff --check`: PASS.
- Coverage: `91%`.
- Swift docs target build: PASS.
- DocC static generation: PASS with existing unrelated DocC warnings about
  unresolved historical references.
- Source manifest validation: `status: ok`, `repositoryCount: 5`.

## Boundary Check

P33-T7 preserves the non-authority boundary:

- no package acceptance;
- no relation acceptance;
- no baseline seeding;
- no `preview_only` removal;
- no public registry publication;
- no SpecPM pull request creation;
- no AI output treated as registry truth;
- no fabricated per-file evidence digests from summary-only fixtures.

## Verdict

PASS. The selected P33 scope is now machine-preflightable by SpecPM as review
evidence before maintainer intake review.

