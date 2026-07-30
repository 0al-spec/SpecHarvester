# P55-T4 Validation Report

**Task:** Provider-Neutral Semantic Author Pass
**Date:** 2026-07-30
**Verdict:** PASS

## Result

P55-T4 adds a provider-neutral semantic-author pass that accepts only a
validated P55-T3 bounded input pack. Codex 5.3 Spark is implemented through a
bounded read-only `codex exec` adapter; LM Studio is implemented through a
credential-free loopback OpenAI-compatible adapter with a P55-T2 JSON Schema
response constraint.

The pass normalizes provider output into one P55-T2 proposal contract, computes
the receipt and proposal digests locally, validates candidate/source-bundle
identity, evidence allowlists, and observed-intent reuse, and fails closed on
provider, JSON, schema, binding, or budget errors.

## Safety Boundary

No live provider was called by validation. Tests use deterministic transports.
Codex output is held in a temporary file removed immediately after reading;
LM Studio raw response is parsed in memory. Portable results retain only a
normalized proposal and non-sensitive receipt metadata, with explicit raw
prompt, raw response, and chain-of-thought non-persistence assertions.

The pass cannot create reviewer decisions, materialize candidates, mutate
SpecPM or a registry, canonicalize intents, or publish output.

## Quality Gates

```text
uv run pytest tests/test_semantic_author_pass.py tests/test_semantic_author_input_pack.py tests/test_p55_semantic_author_schemas.py -q
39 passed

uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90 -q
1203 passed, 1 skipped
Total coverage: 90.02%

uv run ruff check src tests
All checks passed

uv run ruff format --check src tests
176 files already formatted

git diff --check
passed

swift package dump-package >/dev/null
passed

swift build --target SpecHarvesterDocs
Build complete
```

SwiftPM emitted the existing non-blocking warning that the DocC directory is
not declared as a target resource.

## Review Correction

The archive review found that the initial Codex prompt named the proposal schema
without including it. The pass now embeds the exact P55-T2 proposal schema in
the temporary Codex request, and the adapter test asserts that binding.
Targeted regression validation passed: `210 passed` across the semantic-author
pass and documentation-contract suites, with lint, formatting, diff, and DocC
checks also passing.

## PR Review Corrections

PR review then identified six provider-boundary gaps. The pass now supplies the
bounded evidence content and observed intents to both providers, rebuilds
portable receipts from a fixed metadata allowlist, enforces output limits while
reading Codex and LM Studio responses, rejects stale pack/request digests and
dangling intent-decision claim IDs, and performs finite JSON repair for both
adapters. Dedicated regressions cover every correction.

The post-review full gate passed with `1214 passed, 1 skipped` and `90.03%`
total coverage. The focused P55 semantic-author, input-pack, schema, and docs
contract gate passed with `250 passed` before the final receipt branch tests
were added; the semantic-author pass suite then passed with `19 passed`.
