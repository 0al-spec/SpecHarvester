# P16-T17 — Real Repository Quality Rating Policy Objects

Branch: `feature/P16-T17-real-repo-quality-rating-policy`
Review subject: `p16_t17_real_repo_quality_rating_policy_objects`

## Context

After P16-T16, the trusted `pylint` duplicate-code backend reports zero
duplicate blocks. The builtin advisory backend reports seven remaining duplicate
windows, all inside `src/spec_harvester/real_repo_quality_report.py`.

Those windows are the shared guard sequence used by intent and capability rating
derivation:

- dry-run scoring should be unscored.
- the `draft` step must exist and have status `ok`.
- the draft summary artifact must exist.
- the candidate payload must be an object.
- then each rating dimension applies its own domain-specific scoring rule.

## Scope

- Add behavior-rich rating policy objects for real-repository quality scoring.
- Represent the shared draft preflight once and let intent/capability policies
  consume the validated candidate payload.
- Preserve existing private helper functions used by tests and callers.
- Preserve quality report JSON fields, rating literals, notes, and overall
  verdict behavior.
- Re-run duplicate-code, architecture-lint, quality-report tests, and full Flow
  gates.

## Non-Goals

- Do not change quality report schemas.
- Do not change analyzer coverage, SpecPM status, retry, token usage, or summary
  behavior.
- Do not add generated `.smoke/` artifacts.
- Do not make advisory duplicate-code or architecture-lint findings blocking.
- Do not execute harvested repository code.

## Acceptance Criteria

- `tests/test_real_repo_quality_report.py` passes without behavior changes.
- Builtin duplicate-code report no longer reports duplicate windows in
  `real_repo_quality_report.py`, or any remaining window is explicitly justified
  as practical-minimum detector noise.
- `pylint` duplicate-code remains at zero duplicate blocks.
- Coverage remains at or above the configured 90% threshold.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_real_repo_quality_report.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t17-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t17-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t17-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
