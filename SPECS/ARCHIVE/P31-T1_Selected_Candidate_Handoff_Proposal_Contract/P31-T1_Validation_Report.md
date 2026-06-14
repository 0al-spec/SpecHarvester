# P31-T1 Validation Report

Task: P31-T1 Selected Candidate Handoff Proposal Contract
Date: 2026-06-13
Verdict: PASS

## Scope

P31-T1 added the producer-side
`SpecHarvesterSelectedCandidateHandoffProposal` contract for selected
candidate SpecPM review evidence.

Implemented artifacts:

- `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`;
- `Sources/SpecHarvester/Documentation.docc/SelectedCandidateHandoffProposal.md`;
- `tests/fixtures/selected_candidate_handoff_proposal/p31-t1-selected-candidate-handoff.example.json`;
- docs links from the SpecPM handoff guide, P30 selected handoff dry-run docs,
  roadmap, docs index, and DocC root;
- regression tests for fixture shape, selected/deferred candidates, required
  evidence roles, and non-authority boundaries.

## Validation Commands

```bash
python -m json.tool tests/fixtures/selected_candidate_handoff_proposal/p31-t1-selected-candidate-handoff.example.json >/tmp/p31-t1-fixture.json
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
PYTHONPATH=src pytest -q
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
swift package dump-package >/tmp/specharvester-p31-t1-package.json
swift build --target SpecHarvesterDocs
rm -rf /tmp/specharvester-p31-t1-docc-build-spec && swift package --allow-writing-to-directory /tmp/specharvester-p31-t1-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p31-t1-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester
```

## Results

- JSON fixture parse: passed.
- Docs contract tests: `67 passed`.
- Full tests: `635 passed, 1 skipped`.
- Coverage gate: `635 passed, 1 skipped`, total coverage `90.58%`.
- Ruff check: passed.
- Ruff format check: passed after formatting `tests/test_docs_contracts.py`.
- Diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- Static DocC generation: passed.

DocC emitted pre-existing warnings for
`AcceptedPackageUpdateProposals` references and inline command references in
`RealRepositoryQualityReport`. No P31-T1 documentation warnings were observed.

## Boundary Confirmation

The contract remains producer preview evidence only. It does not implement a
CLI helper, mutate candidate bundles, create a SpecPM pull request, accept
packages, accept relations, seed baselines, remove `preview_only`, or publish
registry metadata.
