# P52-T5 Validation Report

## Result

PASS

## Scope

Validated the final Phase 52 corpus manifest, companion selection metadata, and
deterministic checkout-readiness gate for 50 public repositories.

## Readiness Evidence

- Manifest repositories: 50.
- Clean checkouts at matching immutable revisions: 50.
- Resolved repository and license provenance: 50.
- Checkouts within tracked-file size budgets: 50.
- Ecosystem categories: 13.
- Repository shapes: 6.
- P52-T6 decision: unlocked.
- Durable report digest:
  `sha256:e19cb19c393fc55bf1cd09ce9214be73408dab1cc267e7cfa53239c77acfb140`.

The final live rerun and committed fixture produced the same digest.

## Quality Gates

- `PYTHONPATH=src python -m spec_harvester final-corpus-checkout-readiness inputs/p52-final-corpus --metadata inputs/p52-final-corpus/selection-metadata.json --out /tmp/p52-t5-readiness-final.json`: PASS, 50/50 ready.
- `python -m json.tool inputs/p52-final-corpus/selection-metadata.json`: PASS.
- `python -m json.tool tests/fixtures/final_corpus_checkout_readiness/p52-t5-final-corpus-checkout-readiness.example.json`: PASS.
- `.venv/bin/pytest -q tests/test_final_corpus_checkout_readiness.py tests/test_cli_report_commands.py -k 'final_corpus or final-corpus'`: PASS, 8 passed and 5 deselected.
- `.venv/bin/pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90`: PASS, 947 passed, 1 skipped, 90.02% total coverage.
- `uv run ruff check src tests`: PASS.
- `uv run ruff format --check src tests`: PASS.
- `swift package dump-package`: PASS.
- `swift build --target SpecHarvesterDocs`: PASS with the existing unhandled DocC resource warning.
- `git diff --check`: PASS.

## Trust Boundary

- The readiness command only reads operator-provided manifests and local Git
  checkout state. It does not clone, fetch, restore, or modify repositories.
- No static collection, package manager, adapter, LM Studio, Codex, or harvested
  code was executed by the gate.
- The report is readiness evidence only. It grants no package, relation,
  publication, baseline, or registry authority.
- No raw prompts, provider responses, secrets, session state, or chain-of-thought
  are persisted.
