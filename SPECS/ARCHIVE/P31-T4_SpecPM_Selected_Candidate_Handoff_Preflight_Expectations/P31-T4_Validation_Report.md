# P31-T4 Validation Report: SpecPM Selected Candidate Handoff Preflight Expectations

**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P31-T4 documents the expected future SpecPM-side consumer preflight for
`SpecHarvesterSelectedCandidateHandoffProposal` artifacts. The change is
documentation and docs-contract test coverage only; it does not implement a
SpecPM preflight command.

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
  - Result: PASS, `69 passed`
- `PYTHONPATH=src pytest -q`
  - Result: PASS, `645 passed, 1 skipped`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`
  - Result: PASS, `645 passed, 1 skipped`, total coverage `90.56%`
- `PYTHONPATH=src ruff check .`
  - Result: PASS
- `PYTHONPATH=src ruff format --check src tests`
  - Result: PASS, `107 files already formatted`
- `git diff --check`
  - Result: PASS
- `swift package dump-package >/tmp/specharvester-p31-t4-package.json && swift build --target SpecHarvesterDocs`
  - Result: PASS
- `swift package --allow-writing-to-directory /tmp/specharvester-p31-t4-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p31-t4-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester`
  - Result: PASS
  - Notes: emitted pre-existing unrelated DocC warnings for
    `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Acceptance Criteria

- PASS: GitHub docs define the downstream preflight expectations.
- PASS: DocC mirror links the same contract.
- PASS: docs-contract regression tests cover identity, evidence roles, digest
  checks, non-authority semantics, report identity, and P31-T5 follow-up.
- PASS: Existing package generation, proposal, and handoff tests continue to pass.
