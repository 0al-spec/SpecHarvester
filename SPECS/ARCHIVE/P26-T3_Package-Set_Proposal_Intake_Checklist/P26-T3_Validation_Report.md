# P26-T3 Validation Report: Package-Set Proposal Intake Checklist

**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P26-T3 documents the SpecPM-facing intake checklist for
`SpecHarvesterPackageSetHandoffProposal` package-set evidence. The task adds
GitHub docs, a DocC mirror, cross-links from handoff and automation docs, and
regression coverage for the package member / relation acceptance boundary.

## Validation

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
  - Result: PASS, `71 passed`
- `PYTHONPATH=src pytest -q`
  - Result: PASS, `647 passed, 1 skipped`
- `PYTHONPATH=src ruff check .`
  - Result: PASS
- `PYTHONPATH=src ruff format --check src tests`
  - Result: PASS, `107 files already formatted`
- `git diff --check`
  - Result: PASS
- `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`
  - Result: PASS, `647 passed, 1 skipped`, total coverage `90.56%`
- `swift package dump-package >/tmp/specharvester-p26-t3-package.json && swift build --target SpecHarvesterDocs`
  - Result: PASS
- `swift package --allow-writing-to-directory /tmp/specharvester-p26-t3-docc-build-spec generate-documentation --target SpecHarvester --output-path /tmp/specharvester-p26-t3-docc-build-spec --transform-for-static-hosting --hosting-base-path SpecHarvester`
  - Result: PASS
  - Notes: emitted pre-existing unrelated DocC warnings for
    `AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Acceptance Criteria

- PASS: GitHub docs and DocC mirror define the package-set proposal intake
  checklist.
- PASS: The checklist names
  `SpecHarvesterPackageSetHandoffProposal` and
  `spec-harvester.package-set-handoff-proposal/v0`.
- PASS: Required evidence roles are covered, including member package evidence,
  relation proposal evidence, quality reports, and package relation summaries.
- PASS: The docs preserve the boundary that package member acceptance is
  separate from relation acceptance.
- PASS: `registryAcceptanceDecision.status: external_required` and
  `producerAuthority: evidence_only` remain explicit.
- PASS: The suggested future SpecPM report is consumer preflight evidence only,
  not package acceptance, relation acceptance, registry publication, or PR
  creation.
