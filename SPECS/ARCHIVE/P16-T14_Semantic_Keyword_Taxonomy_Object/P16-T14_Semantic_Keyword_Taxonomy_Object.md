# P16-T14 — Semantic Keyword Taxonomy Object

Branch: `feature/P16-T14-semantic-keyword-taxonomy`
Review subject: `p16_t14_semantic_keyword_taxonomy_object`

## Context

After P16-T13, `pylint` duplicate-code baseline reports one remaining major
cluster: duplicated semantic keyword lists between `collector.py` and
`drafter.py`. These terms are part of one conceptual taxonomy:

- collected `semanticHints` in markdown evidence
- draft semantic domain rules and intent clusters

The taxonomy should be represented once and reused by both phases.

## Scope

- Add a shared semantic keyword taxonomy object.
- Refactor collector semantic hints to use taxonomy-provided hint terms.
- Refactor drafter semantic domain rules to use taxonomy term groups.
- Preserve semantic hint order, semantic cluster IDs, intent IDs, labels,
  minimum scores, and output schema.
- Re-run duplicate-code and architecture-lint baselines.

## Non-Goals

- Do not change semantic intent thresholds.
- Do not add or remove semantic intents.
- Do not change generated candidate package schemas.
- Do not refactor Swift-specific semantic rules unless needed to keep the
  taxonomy cohesive.
- Do not execute harvested repository code.

## Acceptance Criteria

- `pylint` duplicate-code baseline reaches zero duplicate blocks or any
  remaining block is justified as below practical minimum.
- Existing collector and drafter semantic tests pass.
- Full Flow validation passes.
- Workplan advances to the next non-duplication task only if duplication is at a
  practical minimum.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_popular_repository_smoke.py -q`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t14-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t14-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t14-architecture-lint.json`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`

