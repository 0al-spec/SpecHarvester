# P55-T10G5 Validation Report

## Verdict

PASS

## Scope Validated

- Candidate YAML capability IDs outside the candidate namespace are detected
  from digest-bound `specpm.yaml` and `*.spec.yaml` evidence.
- Provider requests carry exact prohibited IDs and candidate-scoped replacement
  requirements only when a namespace defect exists.
- A valid, complete, unique proposal-only replacement record passes transport
  validation without changing static candidate YAML.
- Missing, malformed, repeated, duplicate, incomplete, or out-of-scope repair
  records yield the stable `capability_namespace_violation` semantic error.
- The second identical semantic violation stops after the existing single JSON
  repair attempt; no third provider request is issued.
- Simulated Codex 5.3 Spark CLI and LM Studio OpenAI-compatible transports
  preserve the original system prompt, request, evidence, roles, and repair
  budget.
- Independent quality reporting turns a valid repair proposal into
  `review_required` and calibration-ineligible evidence; it does not accept or
  materialize a static change.

## Quality Gates

| Gate | Result |
| --- | --- |
| Focused semantic repair, provider, schema, portable-record, and quality suites | PASS: 135 passed |
| `PYTHONPATH=src .venv/bin/python -m pytest` | PASS: 1437 passed |
| `.venv/bin/ruff check src tests` | PASS |
| `.venv/bin/ruff format --check src tests` | PASS |
| `PYTHONPATH=src .venv/bin/python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS: threshold met |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `git diff --check` | PASS |

## Execution Boundary

- No Codex, LM Studio, or other provider was invoked.
- No raw prompt, response, hidden reasoning, credential, or machine-local path
  was persisted.
- No proposal was accepted, materialized, canonicalized, published, or used to
  mutate SpecPM or registry truth.
