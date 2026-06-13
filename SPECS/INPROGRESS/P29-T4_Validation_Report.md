# P29-T4 Validation Report

Task: `P29-T4 Single-Package Candidate Fallback`
Verdict: PASS
Date: 2026-06-13

## Scope

Implemented the deterministic single-package fallback for repositories that
collect useful public evidence but have no workspace package records.

Changes include:

- preserving source manifest `packageId` in `workspace-inventory.json` source
  metadata;
- generating one `single_package` preview candidate when package-set drafting
  has no selected package records and no inventory package records;
- drafting the candidate from colocated repository-level `harvest.json`;
- including colocated `public-interface-index.json` when available;
- writing normal candidate bundle artifacts:
  `producer-receipt.json`, `validation-report.json`, `diagnostics.json`, and
  `author-ready-draft-quality-report.json`;
- recording `selectionReason: single_package_source_manifest_fallback`;
- preserving empty relation proposals with `relationCount: 0`;
- documenting the fallback in GitHub docs and DocC.

## Acceptance Coverage

- Flask-style Python fixture produces one `flask.core` preview candidate.
- Gin-style Go fixture produces one `gin.core` preview candidate through
  `autonomous-candidate-batch`.
- Fallback candidates include `public-interface-index.json` when available.
- Bundle-set preflight passes with one candidate and zero relations.
- `package-relation-proposals.json` remains present but has an empty
  `relations[]` list.
- The fallback preserves `preview_only`, `producer_preview_evidence_only`, and
  no registry mutation boundaries.

## Gates

- `PYTHONPATH=src python -m pytest tests/test_package_set_drafter.py -q`
  - PASS: `24 passed`
- `PYTHONPATH=src python -m pytest tests/test_autonomous_candidate_batch.py -q`
  - PASS: `6 passed`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: `54 passed`
- `PYTHONPATH=src python -m pytest tests/test_autonomous_candidate_batch.py tests/test_package_set_drafter.py tests/test_docs_contracts.py tests/test_batch_collection.py::test_collect_batch_snapshots_emits_deterministic_workspace_inventory -q`
  - PASS: `85 passed`
- `PYTHONPATH=src python -m pytest -q`
  - PASS: `618 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `618 passed, 1 skipped`
  - Coverage: `90.07%`
- `PYTHONPATH=src ruff check src tests`
  - PASS
- `PYTHONPATH=src ruff format --check src tests`
  - PASS after applying `ruff format` to touched tests
- `git diff --check`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Boundary

The fallback is producer-side preview evidence only.

It does not:

- implement LM Studio JSON repair/retry;
- re-run the final mixed corpus quality gate;
- accept packages;
- accept relations;
- seed baselines;
- publish registry metadata;
- remove `preview_only`;
- replace SpecPM validation or maintainer review.
