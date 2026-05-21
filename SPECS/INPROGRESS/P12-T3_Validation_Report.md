# P12-T3 Validation Report

Task: `P12-T3 Domain Intent Inference`
Date: 2026-05-21
Verdict: PASS

## Scope

Implemented deterministic web-framework domain intent inference from static
documentation hints and `PublicInterfaceIndex` metadata.

The drafter now normalizes public interface package ids, paths, symbol names,
kinds, and signatures into compact semantic tokens. This lets static API names
such as `RouterGroup`, `HandlerFunc`, `RequestContext`, and `Blueprint` support
domain intent clusters without reading raw source bodies or executing harvested
repository code.

## Implemented Behavior

- Added web domain clusters:
  - `web.framework_surface` -> `intent.web.framework_surface`
  - `web.http_routing` -> `intent.web.http_routing`
  - `web.middleware_pipeline` -> `intent.web.middleware_pipeline`
  - `web.request_response_context` -> `intent.web.request_response_context`
- Added per-rule score thresholds so broad terms do not promote weak evidence.
- Allowed strong web semantic profiles to replace generic manifest capability
  intents, while broad API/tooling clusters remain advisory evidence unless no
  manifest capability exists.
- Added web framework semantic hint terms for allowlisted Markdown.
- Updated GitHub docs and DocC mirrors for web domain semantic extraction.

## Regression Coverage

- Flask-like `PublicInterfaceIndex` fixture produces web framework, routing,
  middleware, and request/response context intents.
- Gin-like Go `PublicInterfaceIndex` fixture produces the same web domain
  intents from router, handler, middleware, and context symbols.
- A manifest-backed package with strong web documentation replaces generic
  JavaScript manifest intents with web domain intents.
- Existing language-neutral API-contract documentation remains advisory for
  manifest-backed packages and does not override package manifest intents.
- Documentation contract tests cover the new web semantic extraction contract.

## Quality Gates

| Gate | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest` | PASS, `222 passed in 3.53s` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `43 files already formatted` |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `222 passed`, total coverage `90.48%` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Local Flask/Gin Smoke

Command:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/p12-t3-popular-candidates \
  --report .smoke/output/p12-t3-popular-batch-validation.json \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/analyzer-cache \
  --select flask \
  --select gin
```

Result: PASS, batch `status: ok`.

Draft commands:

```bash
PYTHONPATH=src python -m spec_harvester draft \
  .smoke/output/p12-t3-popular-candidates/flask \
  --package-id flask.core \
  --out .smoke/output/p12-t3-popular-candidates/flask

PYTHONPATH=src python -m spec_harvester draft \
  .smoke/output/p12-t3-popular-candidates/gin \
  --package-id gin.core \
  --out .smoke/output/p12-t3-popular-candidates/gin
```

Flask result:

- Interface index: `status: complete`, `packageCount: 1`,
  `entrypointCount: 83`, `symbolCount: 941`, `diagnosticCount: 0`
- Executed analyzers: `["spec_harvester.python_public_api"]`
- Generated web intents:
  - `intent.web.framework_surface`
  - `intent.web.http_routing`
  - `intent.web.middleware_pipeline`
  - `intent.web.request_response_context`

Gin result:

- Interface index: `status: complete`, `packageCount: 5`,
  `entrypointCount: 56`, `symbolCount: 456`, `diagnosticCount: 0`
- Executed analyzers: `["spec_harvester.go_public_api"]`
- Generated web intents:
  - `intent.web.framework_surface`
  - `intent.web.http_routing`
  - `intent.web.middleware_pipeline`
  - `intent.web.request_response_context`

Repository revisions:

- `pallets/flask` at `954f5684e4841aad84a8eec7ace7b81a0d3f6831`
- `gin-gonic/gin` at `5f4f9643258dc2a65e684b63f12c8d543c936c67`

## Notes

- Generic language-neutral clusters such as API contract or developer tooling
  may still appear as additional advisory evidence when static terms support
  them. They no longer remain the only inferred intent family for Flask/Gin.
- The change does not alter SpecPM evidence-kind vocabulary or support-target
  grammar; those warnings remain tracked by `P12-T4` and `P12-T5`.
- Generated candidates remain preview-only and require SpecPM review before
  acceptance.
