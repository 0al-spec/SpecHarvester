# P55-T2 Validation Report

**Task:** AI Semantic-Author Schemas
**Date:** 2026-07-29
**Verdict:** PASS

## Result

P55-T2 adds a versioned JSON Schema Draft 2020-12 bundle for provider-neutral,
evidence-grounded semantic authoring. It defines standalone request, proposal,
intent-reuse, experimental-intent, nearby-intent analysis, reviewer-edit, and
future materialization-decision records plus an all-record fixture envelope.

The deterministic validator supplements JSON Schema with cross-record checks:
proposal, claim evidence, reviewer edit, and materialization records must share
the request source-bundle digest; reviewer/materialization records bind the
proposal digest; materialization binds the reviewer-edit digest; and duplicate
experimental intent IDs are rejected.

Experimental intent IDs must use `intent.experimental.*`. A materialization
record requires an explicit accepted or edited reviewer decision but remains
`previewOnly: true` and `isRegistryTruth: false`; P55-T2 does not perform it.

## Evidence

The valid schema fixture binds the P55-T1 product and authority contract:

| Source | SHA-256 |
| --- | --- |
| `tests/fixtures/ai_semantic_author_contract/p55-t1-ai-semantic-author-contract.example.json` | `ddde481a6f9cdb8ec051b0d1d8944d217b7f1616174a987db1bb6f1357b9dd32` |

Invalid fixtures cover malformed digest, unsupported evidence class, absolute
path, duplicate experimental intent, stale reviewer source-bundle binding, and
materialization without an accepted or edited decision.

## Execution Boundary

P55-T2 did not build semantic input packs, invoke Codex 5.3 Spark or LM Studio,
execute repository content, install dependencies, run adapters, record live
reviewer decisions, materialize candidate revisions, mutate SpecPM, create a
canonical intent, accept a package, or publish an index.

Portable schemas contain no raw prompt, raw provider response, hidden
reasoning, credential, or private machine-path fields.

## Quality Gates

```text
uv run pytest tests/test_p55_semantic_author_schemas.py tests/test_docs_contracts.py -q
212 passed

uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
1174 passed, 1 skipped
Total coverage: 90.02%

uv run ruff check src tests
All checks passed

uv run ruff format --check src tests
172 files already formatted

git diff --check
passed

swift package dump-package >/dev/null
passed

swift build --target SpecHarvesterDocs
Build complete
```

SwiftPM emitted the existing non-blocking warning that the DocC directory is
not declared as a target resource.
