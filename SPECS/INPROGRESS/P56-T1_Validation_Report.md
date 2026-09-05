# P56-T1 Validation Report

Date: 2026-09-05

Verdict: PASS for benchmark preparation, not for agent-first effectiveness.

## Delivered

- Frozen protocol and evaluator-only, digest-bound benchmark: five pinned
  repositories, 25 practical questions, 50 canonical facts and source spans.
- All referenced file hashes independently recomputed with `git show REV:PATH`
  from retained local checkouts. No source code or package manager executed.
- Same-model generation budgets, end-to-end and boundary-coverage endpoints,
  README comparator, failure accounting, human adjudication and adoption gates.
- Regression contract for artifact completeness/digests and the T2 handoff.

## Checks

- `PYTHONPATH=src .venv/bin/python -m pytest tests/test_p56_practical_utility_benchmark.py tests/test_docs_contracts.py -q`: 204 passed.
- `PYTHONPATH=src .venv/bin/python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: 1442 passed, 1 skipped; coverage 90.03%.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: 203 files already formatted.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed; existing unhandled Documentation.docc warning.
- `git diff --check`: passed.

## Orchestration and Limits

Three read-only GPT 5.6 Luna High agents supplied source research, feasibility
analysis and independent adversarial review. The main agent integrated edits,
recomputed every source hash and spot-checked source claims. Source research
needed a time-bound stop; agents did not modify Git or repository files.

Review prompted explicit product-boundary accounting, equivalent upper evidence
budgets, byte/time ledger definitions, input isolation probes, per-category
floors, scoring adjudication and protection against timing wins from failures.
Population confidence claims are intentionally excluded for five selected repos;
paired deltas and leave-one-out sensitivity are required instead.

No experimental generation, maintainer quality scoring, package acceptance or
publication occurred. Runtime isolation and budget enforcement remain T3 work;
their denial-test receipts are mandatory before T4. The experimental worker
remains Spark low; Luna High was used only for this task's research/review.
