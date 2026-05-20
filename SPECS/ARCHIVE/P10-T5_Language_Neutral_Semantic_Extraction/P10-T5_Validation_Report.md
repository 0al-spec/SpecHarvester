# P10-T5 Validation Report

Status: PASS
Date: 2026-05-20
Task: P10-T5 Language-Neutral Semantic Extraction

## Scope Validated

- Collector records bounded `semanticHints` for allowlisted Markdown.
- Drafter consumes `semanticHints` when building deterministic semantic
  evidence clusters.
- Manifest-poor documentation repositories can use semantic evidence instead of
  the generic public metadata fallback.
- Existing manifest-derived package intents remain compatible when only
  language-neutral documentation clusters are present.
- GitHub documentation and DocC mirror document the evidence contract.

## Commands

```bash
ruff check src tests
```

Result: PASS

```bash
ruff format --check src tests
```

Result: PASS

```bash
PYTHONPATH=src python -m pytest tests/test_collector.py tests/test_docs_contracts.py -q
```

Result: PASS, `75 passed`

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: PASS, `203 passed`, total coverage `90.68%`

```bash
swift package dump-package >/dev/null
```

Result: PASS

```bash
swift build --target SpecHarvesterDocs
```

Result: PASS

## Notes

- `semanticHints` are compact deterministic terms, not raw documentation bodies.
- Language-neutral clusters are used as manifest-poor fallback capability
  intents. For repositories with supported package manifests, they remain
  review evidence and do not replace manifest-derived package intents unless a
  stronger Swift/iOS semantic profile is present.
- Generated semantic claims remain advisory review evidence, not accepted
  SpecPM registry truth.
