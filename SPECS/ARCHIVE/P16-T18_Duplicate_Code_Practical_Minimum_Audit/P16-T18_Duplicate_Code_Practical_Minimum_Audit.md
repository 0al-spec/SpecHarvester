# P16-T18 — Duplicate-Code Practical-Minimum Audit

Branch: `feature/P16-T18-duplicate-code-practical-minimum-audit`
Review subject: `p16_t18_duplicate_code_practical_minimum_audit`

## Context

P16-T14 through P16-T17 reduced duplicated implementation blocks across the
SpecHarvester Python codebase. After P16-T17, both duplicate-code detector
backends report zero duplicate blocks for `src/spec_harvester`.

This task records the practical-minimum baseline and decides whether more
duplicate-code refactoring is warranted before the project moves back to other
signal-quality tasks.

## Scope

- Capture duplicate-code reports for both builtin and `pylint` backends.
- Capture the architecture lint advisory state so duplicate-code success is not
  confused with unrelated structural advisories.
- Document the practical-minimum conclusion in a reviewable audit artifact.
- Mark P16-T18 complete and advance `next.md` to the next non-duplicate-code
  workplan item.

## Non-Goals

- Do not refactor code unless the audit finds non-zero duplicate-code blocks.
- Do not change detector thresholds or make advisory checks blocking.
- Do not add generated `.smoke/` artifacts.
- Do not change CI configuration.

## Acceptance Criteria

- Builtin duplicate-code report is recorded with zero duplicate blocks, or any
  non-zero windows are explicitly classified.
- `pylint` duplicate-code report is recorded with zero duplicate blocks, or any
  non-zero windows are explicitly classified.
- The audit states whether the duplicate-reduction goal has reached a practical
  and reasonable minimum.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t18-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t18-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t18-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
