# P55-T10G2 Validation Report

## Verdict

PASS

## Scope Validated

- Typed semantic violation construction and validation.
- Structured repair guidance with preserved original context and message roles.
- Generic-only contradiction and experimental namespace replacement constraints.
- Outcome-anchor repair constraints inherited from P55-T10G1.
- Deterministic unchanged-violation early termination.
- Backward-compatible parse, schema, Codex, LM Studio, and campaign paths.

## Quality Gates

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest` | PASS: 1410 passed, 1 skipped |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS: 201 files formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90` | PASS: 90.01% |
| `swift package dump-package` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

The Swift target emitted the pre-existing unhandled DocC resource warning and
built successfully.

## Budget and Authority Check

- Retained campaign budget remains two provider attempts.
- Semantic author default remains one JSON repair per provider attempt.
- No raw prompt, raw response, hidden reasoning, credential, or machine-local
  path persistence was added.
- No acceptance, materialization, canonicalization, SpecPM mutation, registry
  mutation, or publication path was added.
