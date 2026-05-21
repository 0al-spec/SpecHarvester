# P12-T5 Validation Report

Task: `P12-T5` Evidence Support Target Contract Alignment
Date: 2026-05-21
Verdict: PASS

## Summary

SpecHarvester no longer emits the unsupported nested evidence support target
`provides.capabilities.intentIds`. Semantic intent evidence now targets only
declared SpecPM support targets: `intent.summary`, `provides.capabilities`, and
`provides.capabilities.<capability_id>`.

Local SpecPM `0.2.0` validation confirms that generated candidates with
`semantic_intent_static_evidence` no longer warn with
`evidence_support_target_unknown`.

## Quality Gates

| Gate | Result |
|------|--------|
| `PYTHONPATH=src python -m pytest tests/test_collector.py::test_draft_spec_package_uses_documentation_semantics_without_package_manifests tests/test_collector.py::test_draft_spec_package_uses_web_framework_intents_from_flask_like_index tests/test_docs_contracts.py -q` | PASS, 10 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 223 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 43 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 223 passed, total coverage 90.47% |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## SpecPM Validation Smoke

Candidate:
`.smoke/output/p12-t3-popular-candidates/gin`

Command:

```bash
PYTHONPATH=src python -m spec_harvester draft \
  .smoke/output/p12-t3-popular-candidates/gin \
  --package-id gin.core \
  --name Gin \
  --out .smoke/output/p12-t3-popular-candidates/gin

specpm validate .smoke/output/p12-t3-popular-candidates/gin --json
```

Result:

- status: `warning_only`
- errors: `0`
- warnings: `preview_only_package`
- `evidence_support_target_unknown`: absent
- `unknown_evidence_kind`: absent

## CI Integration Smoke

A local reproduction of the updated CI `specpm-integration` fixture produced a
candidate containing both `semantic_intent_static_evidence` and
`public-interface-index.json`, then validated it with SpecPM `0.2.0`.

Assertions:

- `id: semantic_intent_static_evidence` is present.
- `provides.capabilities.<capability_id>` support targets are present.
- `provides.capabilities.intentIds` is absent.
- `evidence_support_target_unknown` is absent.
- `unknown_evidence_kind` is absent.

Result:

- status: `warning_only`
- errors: `0`
- warnings: `preview_only_package`
