# P37-T7 Real Repository Profile Auto-Selection Run

## Motivation

P37-T6 proves repository profile selection with static fixtures. The next
question is whether the generic profile selection layer is useful on a real
checkout, especially for the FastMCP-style problem that motivated Phase 37:
manual targeting can improve output quality, but operators should not have to
hand-author targets for every repository shape.

## Goal

Run a real repository through repository profile auto-selection and compare the
result against manual targeting evidence.

The report must evaluate the generic subsystem:

- detection evidence;
- selected profile;
- confidence;
- overrides;
- public-interface precision;
- topology hints;
- author-ready output quality.

## Deliverables

- Run a local real-repository validation on FastMCP or another available
  checkout.
- Capture deterministic run artifacts outside the repository and record their
  paths/digests in docs.
- Add a durable fixture summarizing the real-repository comparison.
- Document the result in GitHub docs and DocC.
- Link the result from roadmap, capabilities, repository profile selection
  docs, and documentation indexes.
- Add docs-contract and fixture regression tests.
- Archive the task through Flow.

## Acceptance Criteria

- The comparison fixture records:
  - source repository id, URL, local path, and revision;
  - auto-selection command summary;
  - manual-targeting command summary;
  - selected profile and confidence;
  - profile detection evidence paths;
  - advisory hints;
  - public-interface precision summary;
  - author-ready quality summary;
  - verdict.
- The auto-selection run uses
  `--repository-profile-selection auto`.
- The manual targeting comparison uses explicit operator targeting rather than
  hidden profile selection.
- The result states whether auto-selection improves output, merely explains the
  output, or still needs another bounded follow-up.
- Documentation explicitly states that the run is producer-side evidence only
  and does not accept packages, accept relations, publish registry metadata,
  remove `preview_only`, or treat profile decisions, hints, manual targeting,
  or AI output as registry truth.

## Non-Goals

- Do not implement an ecosystem-specific FastMCP profile.
- Do not change repository profile scoring semantics.
- Do not change package-set drafting semantics.
- Do not require network access or clone repositories.
- Do not require live AI; use `--skip-ai` unless a future task explicitly asks
  for live model comparison.
- Do not promote generated candidates into SpecPM.

## Dependencies

- P37-T1 repository profile selection contract.
- P37-T2 detection fixture format.
- P37-T3 detection CLI/report surface.
- P37-T4 autonomous batch sidecar evidence integration.
- P37-T5 generic profile discovery hints.
- P37-T6 cross-ecosystem profile fixtures.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_repository_profile_detection.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'repository_profile'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
