# P31-T5 Validation Report: Deferred Selected Candidate Regeneration Requirements

**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P31-T5 records requirements for the six P30 deferred candidates before they can
enter a future selected handoff proposal. The task is a contract/documentation
change with a machine-readable fixture; it does not regenerate candidates or
modify accepted registry state.

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
  - Result: PASS, `70 passed`
- `PYTHONPATH=src pytest -q`
  - Result: PASS, `646 passed, 1 skipped`
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`
  - Result: PASS, `646 passed, 1 skipped`, total coverage `90.56%`
- `PYTHONPATH=src ruff check .`
  - Result: PASS
- `PYTHONPATH=src ruff format --check src tests`
  - Result: PASS, `107 files already formatted`
- `git diff --check`
  - Result: PASS
- `swift package dump-package >/tmp/specharvester-p31-t5-package.json && swift build --target SpecHarvesterDocs`
  - Result: PASS
- `swift package --allow-writing-to-directory /tmp/specharvester-p31-t5-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p31-t5-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester`
  - Result: PASS
  - Notes: emitted pre-existing unrelated DocC warnings for
    `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Acceptance Criteria

- PASS: GitHub docs and DocC mirror define the P31-T5 regeneration requirement
  contract.
- PASS: Fixture identity is versioned as
  `SpecHarvesterDeferredSelectedCandidateRegenerationRequirements`.
- PASS: Fixture includes all six P30 deferred candidates.
- PASS: Fixture covers package-set identity regeneration, warning-bearing
  enrichment regeneration, and identity-drift resolution.
- PASS: Docs and fixture preserve the non-authority boundary: no package
  acceptance, relation acceptance, baseline seeding, `preview_only` removal,
  registry publication, or SpecPM pull request creation.
