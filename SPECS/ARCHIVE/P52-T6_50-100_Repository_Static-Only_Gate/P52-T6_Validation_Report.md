# P52-T6 Validation Report

**Task:** `P52-T6` 50-100 Repository Static-Only Gate  
**Date:** 2026-07-23  
**Verdict:** PASS

## Summary

The digest-bound P52-T6 gate processed all 50 approved P52-T5 sources exactly
once through the existing deterministic autonomous candidate batch with AI
disabled. Forty-eight sources passed strict collection validation and candidate
preflight, producing a 96% static completion rate against the required 95%
minimum. P52-T7 is unlocked.

`actix-web` and `uv` are retained as explicit failures. Both checkouts contain
root `LICENSE-APACHE` and `LICENSE-MIT` files, but those filenames are not
recognized by the current strict collector allowlist, resulting in
`missing_license_file`. Their deterministic drafts and preflights completed;
neither failure was omitted from the gate metric.

## Live Gate Evidence

- Source outcomes: `50/50`, with no missing or unexpected ids.
- Strict static completion: `48/50` (`0.96`), minimum `0.95`.
- Candidate preflights: `50` passed.
- Failed source ids: `actix-web`, `uv`.
- AI mode: `disabled`; provider and model: `null`.
- AI proposal artifacts: `0`.
- Repository and trusted adapter execution: `not_run`.
- Package manager and harvested-code execution: `false`.
- Gate decision: `unlock_p52_t7`.
- Authority: `producer_static_gate_evidence_only`.

The underlying autonomous batch status remains `failed` because its strict
collection report contains the two license findings. P52-T6 passes because the
approved policy permits explicit failures while the completion rate remains at
or above 95% and all source, report, and execution-boundary checks pass.

## Artifact Digests

| Artifact | SHA-256 |
| --- | --- |
| P52-T5 readiness fixture | `49b31573ea40eeb1396b0dea67164264d4e7effa1fbc5fc0996b5d0210d5c9af` |
| P52-T6 durable gate fixture | `64a142093fec3587437702fa4845c1bcddfeaab0c578f7f8c0d9ce3caec805cf` |
| Disposable autonomous batch report | `e660723a9006088cbce979100df9a63ec3a9d6aa4f6106f6d0e6c772f6ad5cb3` |
| Disposable collection validation report | `29ee43d6eb7d98982fda3f52b7fa65ddf8d56491437f4b188532c7a742b16f73` |

Only the sanitized P52-T6 gate fixture is retained in the repository. The full
147 MB live output remains disposable and is not committed.

## Validation Commands

```text
.venv/bin/pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
957 passed, 1 skipped; total coverage 90.02%

.venv/bin/ruff check src tests
All checks passed!

.venv/bin/ruff format --check src tests
139 files already formatted

swift package dump-package
PASS

swift build --target SpecHarvesterDocs
Build complete (with the existing unhandled Documentation.docc resource warning)

.venv/bin/python -m json.tool tests/fixtures/final_corpus_static_only_gate/p52-t6-final-corpus-static-only-gate.example.json
PASS

git diff --check
PASS
```

## Boundary Verification

The gate did not invoke LM Studio, Codex Spark, another model provider,
adapters, package managers, builds, tests, or harvested code. Generated output
remains preview-only producer evidence. It does not accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`, or
change registry truth.
