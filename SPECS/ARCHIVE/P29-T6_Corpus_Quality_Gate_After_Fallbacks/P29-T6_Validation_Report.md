# P29-T6 Validation Report

Task: `P29-T6 Corpus Quality Gate After Fallbacks`

Verdict: `PASS`

## Corpus Inputs

Run root:

```text
/tmp/spec-harvester-p29-t6.edfHiE
```

Pinned local checkouts:

| Repository | Checkout | Revision |
| --- | --- | --- |
| Flask | `/Users/egor/Development/GitHub/flask` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | `/Users/egor/Development/GitHub/gin` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | `/Users/egor/Development/GitHub/xyflow` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |

## Deterministic Gate

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/spec-harvester-p29-t6.edfHiE/inputs \
  --out /tmp/spec-harvester-p29-t6.edfHiE/deterministic \
  --skip-ai
```

Result:

- status: `passed`
- collected repositories: `3`
- processed repositories: `3`
- passed preflight repositories: `3`
- failed repositories: `0`
- report digest: `sha256:ea20d3fe25eb4c1c9094c6db194636a2d71edd64dc75b4883c7c401851846640`

Repository summary:

| Repository | Candidates | Candidate ids | Relations | Preflight | Author decision |
| --- | ---: | --- | ---: | --- | --- |
| Flask | `1` | `flask.core` | `0` | `passed` | `stop_for_author_review` |
| Gin | `1` | `gin.core` | `0` | `passed` | `stop_for_author_review` |
| xyflow | `4` | `xyflow.workspace`, `xyflow.react`, `xyflow.svelte`, `xyflow.system` | `3` | `passed` | `stop_for_author_review` |

## Live LM Studio Gate

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/spec-harvester-p29-t6.edfHiE/inputs \
  --out /tmp/spec-harvester-p29-t6.edfHiE/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Result:

- status: `passed`
- collected repositories: `3`
- processed repositories: `3`
- passed preflight repositories: `3`
- failed repositories: `0`
- AI draft proposals: `3`
- AI enrichment proposals: `3`
- JSON repair needed: `0`
- JSON repair exhausted: `0`
- report digest: `sha256:ea2f5c3553b5827be9d440060b6f857aa59999ce7d7b835a800644b021420a9e`

Repository summary:

| Repository | AI draft | Draft diagnostics | AI enrichment | JSON repair | Status |
| --- | --- | --- | --- | --- | --- |
| Flask | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| Gin | `warning` | `excluded_package_unknown` | `completed` | `not_needed` | `passed` |
| xyflow | `warning` | `package_set_id_missing` | `completed` | `not_needed` | `passed` |

The AI draft warnings are candidate-layer review evidence. They do not promote
packages, accept relations, seed baselines, or block deterministic artifacts.

## Quality Gates

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_docs_contracts.py -q` | `56 passed` |
| `PYTHONPATH=src pytest -q` | `624 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | `624 passed, 1 skipped`; coverage `90.58%` |
| `PYTHONPATH=src ruff check .` | passed |
| `PYTHONPATH=src ruff format --check src tests` | passed |
| `git diff --check` | passed |
| `swift build --target SpecHarvesterDocs` | passed |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | passed with pre-existing unrelated DocC warnings for `AcceptedPackageUpdateProposals` |

## Product Verdict

The post-mitigation corpus satisfies the P29-T6 quality gate:

- Flask and Gin now produce reviewable single-package preview candidates.
- xyflow retains the expected package-set candidate shape and `contains`
  relation proposals.
- deterministic preflight passes for every repository;
- live LM Studio completes bounded proposal generation for every repository;
- JSON repair support was available but not needed in this run;
- results remain `producer_preview_evidence_only`.

Status: `ready_for_limited_popular_library_scraping`.

This is readiness for limited candidate-layer scraping, not automatic SpecPM
registry acceptance and not a claim that generated specs are final.
