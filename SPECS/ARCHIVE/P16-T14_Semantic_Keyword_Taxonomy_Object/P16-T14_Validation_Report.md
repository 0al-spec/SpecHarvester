# P16-T14 Validation Report

Task: `P16-T14 — Semantic Keyword Taxonomy Object`
Branch: `feature/P16-T14-semantic-keyword-taxonomy`
Date: 2026-05-26
Verdict: PASS

## Summary

- Added `SemanticKeywordTaxonomy` as the shared source for markdown semantic
  hint terms and drafter semantic domain rules.
- Refactored `collector.py` and `drafter.py` to consume the shared taxonomy
  instead of maintaining separate keyword lists.
- Added regression coverage for stable markdown hint ordering and semantic
  domain rule IDs.
- Preserved semantic hint order, including `cookie` and `cookies`, and preserved
  existing cluster IDs, intent IDs, labels, contexts, and minimum scores.

## Duplicate-Code Metrics

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t14-dup-pylint.json`
  - PASS: `duplicateBlockCount=0`, `duplicateOccurrenceCount=0`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t14-dup-builtin.json`
  - ATTENTION: `duplicateBlockCount=10`, `duplicateOccurrenceCount=21`
  - Remaining advisory clusters are outside the semantic taxonomy area:
    analyzer option shapes, upstream report checks, and real repository quality
    rating helpers.

## Architecture-Lint Metrics

- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t14-architecture-lint.json`
  - ATTENTION: `issueCount=1`
  - Existing advisory: `manifest_parser_pattern` in
    `src/spec_harvester/license_provenance_reports.py`.
  - This issue is unrelated to the semantic taxonomy refactor.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_semantic_keyword_taxonomy.py tests/test_collector.py tests/test_popular_repository_smoke.py -q`
  - PASS: `77 passed`
- `PYTHONPATH=src python -m pytest`
  - PASS: `400 passed, 1 skipped`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: `400 passed, 1 skipped`
  - Coverage: `91.51%`
- `ruff check src tests`
  - PASS
- `ruff format --check src tests`
  - PASS: `63 files already formatted`
- `swift package dump-package >/dev/null`
  - PASS
- `swift build --target SpecHarvesterDocs`
  - PASS

## Follow-Up Candidates

- Refactor remaining builtin advisory duplication in analyzer option dataclasses
  only if a shared analyzer options object does not obscure language-specific
  behavior.
- Refactor upstream report check duplication through a shared behavior-rich
  upstream verification object.
- Refactor `real_repo_quality_report.py` rating helpers if duplicate windows
  remain materially noisy after the current stack lands.
