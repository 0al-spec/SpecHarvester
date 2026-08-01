# P55-T10G Validation Report

**Task:** P55-T10G Ten-Repository Semantic Root-Cause Calibration

**Date:** 2026-08-01

**Verdict:** PARTIAL

## Execution Result

- The frozen plan bound exactly ten P55-T10C targets before provider execution;
  plan SHA-256: `376001a3ea1053afb5908bf1b7cb8125b95da4eebf2d76a6422e733f06844a11`.
- Codex 5.3 Spark produced 8 completed and 2 failed terminal records through 15
  provider attempts. Five completed records used bounded JSON repair.
- All 7 baseline generic-intent references were removed. Eight completed records
  proposed one evidence-bound experimental intent each.
- False novelty, duplicate experimental IDs, and duplicate experimental semantic
  stems were all zero.
- Bitcoin failed twice at the generic-only contradiction gate. Excalidraw failed
  twice because its experimental ID leaked the candidate namespace.

## Frozen Gates

| Gate | Result | Required | Status |
| --- | ---: | ---: | --- |
| Purpose accuracy | 0.60 | >= 0.85 | FAIL |
| Evidence-supported claims | 0.80 | >= 0.95 | FAIL |
| Schema-valid proposals | 0.80 | 1.00 | FAIL |
| Reviewer edit burden | 0.40 | <= 0.25 | FAIL |
| Generic intent reduction | 7 | > 0 | PASS |
| Repaired generic-case improvement | 5 cases | >= 1 | PASS |
| False novelty | 0 | 0 | PASS |
| Duplicate IDs / semantic stems | 0 / 0 | 0 / 0 | PASS |

The digest-bound supervisor assessment marked Axios, n8n agents, Firecrawl,
Codex, claude-mem, and freeCodeCamp API purpose claims accurate. Angular `adev`
and Electron `dialog-helper` remained structurally valid but described package
identity or consumption rather than the selected package's concrete outcome.

## Decision and Boundary

P55-T10H remains blocked. The result proves that relevant routing and the
contradiction gate remove silent generic reuse, but purpose specificity and
repair convergence require bounded follow-up. Thresholds were not changed and
no recovery model was used.

No repository code or package manager ran. No proposal was accepted,
materialized, canonicalized, written to SpecPM or registry truth, or published.
No raw prompt, raw response, hidden reasoning, credential, or machine-local path
was persisted in durable evidence.

## Validation

- Frozen plan construction and exact ten-target binding: passed.
- Real Codex 5.3 Spark run and deterministic finalization: passed with PARTIAL
  calibration verdict.
- Focused calibration and routing tests: passed.
- `uv run pytest --cov=spec_harvester --cov-report=term-missing
  --cov-fail-under=90`: 1390 passed, 1 skipped; total coverage 90.00%.
- `uv run ruff check src tests
  scripts/run_p55_t10g_semantic_root_cause_calibration.py`: passed.
- `uv run ruff format --check src tests
  scripts/run_p55_t10g_semantic_root_cause_calibration.py`: passed; 200 files
  formatted.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing unhandled
  DocC catalog warning.
- `jq empty SPECS/EVIDENCE/P55-T10G/*.json` and `git diff --check`: passed.

## Review Follow-Up

- Frozen-plan validation now checks the complete contract and independently pins
  the expected plan digest, so fully rehashed binding substitutions fail closed.
- Unknown quality-gate operators now raise instead of falling through to
  equality.
- Purpose assessment and report construction complete before the durable archive
  is replaced during finalization.
- Failed repaired cases count as improvements only for an explicit generic-only
  contradiction; unrelated input, transport, quota, or namespace failures do
  not qualify. The corrected result contains five improved repaired cases.
- Focused review regression suite: `17 passed`.
