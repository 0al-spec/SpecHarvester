# P29-T1 Validation Report

## Summary

Implemented the autonomous candidate batch runner MVP.

The runner consumes existing repository source manifests and local checkouts,
collects deterministic evidence, emits workspace inventory and public interface
indexes, drafts package-set preview bundles, runs bundle-set preflight, and can
call a local LM Studio/OpenAI-compatible provider for schema-bound AI draft and
enrichment proposals.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_autonomous_candidate_batch.py tests/test_package_set_drafter.py tests/test_docs_contracts.py -q` | PASS, `75 passed` |
| `PYTHONPATH=src python -m pytest -q` | PASS, `609 passed, 1 skipped` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `609 passed, 1 skipped`, coverage `90.02%` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS with pre-existing DocC warnings |

## Practical Smoke

### Local LM Studio Fixture

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  <fixture-inputs> \
  --out <run-root>/out \
  --lm-studio-model openai/gpt-oss-20b
```

Observed:

- run root: `/tmp/specharvester-autonomous-live-eKi4B1`
- report status: `passed`
- role profile: `autonomous_popular_mvp`
- AI mode: `local_lm_studio`
- candidate count: `3`
- relation count: `2`
- preflight: `passed`
- AI draft: `completed`
- AI enrichment: `completed`

### Real `xyflow` Checkout

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  <xyflow-inputs> \
  --out <run-root>/out \
  --skip-ai
```

Observed:

- checkout: `/Users/egor/Development/GitHub/xyflow`
- revision: `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`
- run root: `/tmp/specharvester-autonomous-xyflow-n057cz`
- report status: `passed`
- role profile: `autonomous_popular_mvp`
- AI mode: `disabled`
- candidate count: `4`
- relation count: `3`
- preflight: `passed`
- author-ready decision: `stop_for_author_review`

## Boundary Check

- No repository cloning was added.
- No harvested package code execution was added.
- No dependency installation, package manager execution, build, or test run was
  added.
- AI execution is local operator opt-in through LM Studio/OpenAI-compatible
  endpoint.
- Generated output remains producer preview evidence and does not imply SpecPM
  acceptance or registry publication.
