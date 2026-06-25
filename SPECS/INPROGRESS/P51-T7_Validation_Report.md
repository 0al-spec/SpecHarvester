# P51-T7 Validation Report

**Task:** P51-T7 Larger Curated Corpus Output Triage
**Date:** 2026-06-25
**Verdict:** PASS

## Summary

P51-T7 classifies the larger curated corpus output from P51-T4, P51-T5, and
P51-T6 into selected-for-author-review, deferred, and do-not-promote evidence.
The task does not rerun the corpus, run AI, accept packages or relations, or
change registry truth.

The durable triage fixture is:

```text
tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json
```

## Triage Result

```text
repositories triaged: 12
static candidate packages: 15
selected static packages: 11
deferred static packages: 4
relation proposals: 3
deferred relation proposals: 3
AI draft sidecars: 12
AI draft selected for author review: 6
AI draft deferred: 6
AI draft superseded do-not-promote sidecars: 1
AI enrichment sidecars: 12
AI enrichment selected for author review: 8
AI enrichment deferred: 3
AI enrichment do-not-promote: 1
AI-enriched preview prepared packages: 8
AI-enriched preview skipped packages: 7
carried-forward caveats: 4
P51-T8 exit decision allowed: true
```

## Carried-Forward Caveats

```text
xyflow.partial_public_interface_index
xyflow.operator_checkout_origin_fork_mismatch
docc2context.source_checkout_had_untracked_doccarchive
hyperprompt.single_package_deterministic_fallback_applied
```

The caveats do not block P51-T8 exit decision. They remain registry-promotion
blockers until a maintainer explicitly disposes them.

## Quality Gates

```bash
python3 -m json.tool tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json >/dev/null
```

Result: PASS.

```bash
python3 -m ruff format tests/test_docs_contracts.py && PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_output_triage" -q
```

Result: `1 file reformatted`; `1 passed, 186 deselected`.

```bash
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q
```

Result: `187 passed`.

```bash
PYTHONPATH=src python3 -m pytest
```

Result: `919 passed, 1 skipped`.

```bash
python3 -m ruff format --check src tests && python3 -m ruff check src tests && git diff --check
```

Result: `131 files already formatted`; `All checks passed!`; no whitespace
errors.

```bash
PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `919 passed, 1 skipped`; total coverage `90.49%`.

```bash
swift package dump-package >/dev/null && swift build --target SpecHarvesterDocs
```

Result: `Build of target: 'SpecHarvesterDocs' complete!`

## Boundary Checks

- No larger corpus rerun.
- No AI execution.
- No package or relation acceptance.
- No registry metadata publication.
- No baseline seeding.
- No `preview_only` removal.
- No raw prompts, raw provider responses, secrets, or chain-of-thought
  persisted.
- No clone/fetch, dependency installation, package manager invocation, adapter
  execution, or harvested-code execution.
- Static output, AI output, AI-enriched preview output, triage output, and
  adapter output remain non-authoritative review evidence.

## Type Checking

No mypy or equivalent typecheck command is configured in `pyproject.toml`,
`.github`, or `.flow`; the repository also has no `Makefile`.

## Next State

P51-T8 can record the larger curated corpus exit decision using P51-T7 triage
evidence.
