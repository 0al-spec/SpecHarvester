# P16-T13 — Public API Payload Records

Branch: `feature/P16-T13-public-api-payload-records`
Review subject: `p16_t13_public_api_payload_records`

## Context

After P16-T12, `pylint` duplicate-code baseline still reports two major
clusters. One cluster is duplicated public API analyzer cache payload validation
between `go_public_api.py` and `python_public_api.py`:

- entrypoint belongs to path
- every symbol belongs to path through evidence
- diagnostic belongs to path through evidence

This is a small behavior that should be owned by a shared object rather than
repeated as analyzer-local helper functions.

## Scope

- Add a shared public API payload record object for cached analyzer payload
  validation.
- Refactor Python and Go public API analyzers to use the shared object.
- Preserve analyzer cache schema, public interface index output, diagnostics,
  and evidence shape.
- Add direct regression coverage for entrypoint, symbol, diagnostic, and invalid
  payload shapes.
- Re-run duplicate-code and architecture-lint baselines.

## Non-Goals

- Do not change analyzer output schema.
- Do not change public API extraction logic.
- Do not add new language analyzers.
- Do not execute harvested repository code.
- Do not refactor semantic keyword lists in `collector.py`/`drafter.py`; that is
  the remaining duplicate cluster after this task.

## Acceptance Criteria

- Python and Go analyzers delegate cached payload path validation to the shared
  object.
- Existing public API analyzer tests pass.
- `pylint` duplicate-code baseline improves by removing the Python/Go payload
  validation cluster.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_python_public_api.py tests/test_go_public_api.py tests/test_public_api_payload_records.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t13-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t13-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t13-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

