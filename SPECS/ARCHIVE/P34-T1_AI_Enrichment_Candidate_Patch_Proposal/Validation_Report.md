# P34-T1 Validation Report

Status: PASS

## Local Checks

- `PYTHONPATH=src pytest tests/test_ai_enrichment_candidate_patch.py -q`
  - `6 passed`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
  - `92 passed`
- `PYTHONPATH=src pytest tests/test_ai_enrichment_candidate_patch.py tests/test_docs_contracts.py -q`
  - `98 passed`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `PYTHONPATH=src pytest -q`
  - `710 passed, 1 skipped`
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed
- `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester`
  - passed
  - emitted existing unrelated DocC warnings for `AcceptedPackageUpdateProposals`
    and literal command references in `RealRepositoryQualityReport`

## Practical FastAPI AI Smoke

Source artifacts:

- Proposal:
  `/tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/package-sets/fastapi/ai/package-set-ai-enrichment-proposal.json`
- Source candidate:
  `/tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/package-sets/fastapi/fastapi.core`
- Enriched preview candidate:
  `/tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/enriched/fastapi.core`

Command:

```bash
PYTHONPATH=src python3 -m spec_harvester apply-ai-enrichment-proposal \
  --proposal /tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/package-sets/fastapi/ai/package-set-ai-enrichment-proposal.json \
  --candidate /tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/package-sets/fastapi/fastapi.core \
  --package-id fastapi.core \
  --output /tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/enriched/fastapi.core
```

Result:

- patch report `status`: `prepared`
- applied changes: `8`
- skipped changes: `0`
- package id: `fastapi.core`
- `previewOnly`: `true`
- `sourceMutated`: `false`

Follow-up checks:

```bash
PYTHONPATH=src python3 -m spec_harvester preflight-candidate-bundle \
  /tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/enriched/fastapi.core
```

- status: `passed`
- diagnostics: `0`
- errors: `0`
- warnings: `0`

```bash
/Users/egor/Development/GitHub/0AL/SpecPM/.venv/bin/python -m specpm.cli validate \
  /tmp/spec-harvester-fastapi-llm-20260614T103407Z/live-llm/enriched/fastapi.core
```

- result: `warning_only: fastapi.core`
- errors: `0`
- warnings: `1`
- warning: `preview_only_package`, expected for a producer-side preview copy

Observed enriched content:

- summary:
  `FastAPI Core is a statically evidenced Python web framework that provides HTTP routing, middleware, request/response handling, and automatic OpenAPI documentation.`
- capabilities:
  - `fastapi.core`
  - `fastapi.core.http_routing`
  - `fastapi.core.middleware_support`
  - `fastapi.core.request_response_context`
  - `fastapi.core.openapi_generation`

## Verdict

P34-T1 meets the task goal. A clean local-model
`SpecHarvesterPackageSetAIEnrichmentProposal` can now become a copied enriched
preview candidate with a machine-readable patch report, refreshed receipt
digests, producer preflight compatibility, and preserved non-authority
boundaries.

## Review Fix Validation

PR review identified two P2 safety gaps:

- `specs[].path` could be absolute or `..`-escaping and point outside the
  copied candidate.
- a non-preview source candidate could be enriched when `preview_only` was
  missing or false.

Added guards and regression coverage:

- source candidate `specpm.yaml` must declare `preview_only: true`;
- `specs[].path` must be bundle-relative and contained by the candidate root
  before copying/applying;
- candidate digest reads use the same safe bundle path resolver;
- producer receipt output digest refresh uses safe bundle paths.

Validation:

- `PYTHONPATH=src pytest tests/test_ai_enrichment_candidate_patch.py -q`
  - `10 passed`
- `PYTHONPATH=src ruff check src/spec_harvester/ai_enrichment_candidate_patch.py tests/test_ai_enrichment_candidate_patch.py`
  - passed
- `PYTHONPATH=src ruff format --check src/spec_harvester/ai_enrichment_candidate_patch.py tests/test_ai_enrichment_candidate_patch.py`
  - passed
- `PYTHONPATH=src pytest -q`
  - `714 passed, 1 skipped`
- `PYTHONPATH=src ruff check .`
  - passed
- `PYTHONPATH=src ruff format --check src tests`
  - passed
- `git diff --check`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed

Practical FastAPI re-smoke after safety fixes:

- patch report `status`: `prepared`
- applied changes: `8`
- skipped changes: `0`
- `previewOnly`: `true`
- `sourceMutated`: `false`
- producer preflight status: `passed`
- producer preflight diagnostics/errors/warnings: `0/0/0`
