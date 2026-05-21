# P12-T4 Validation Report

Task: `P12-T4` PublicInterfaceIndex Evidence Contract Alignment
Date: 2026-05-21
Verdict: PASS

## Summary

SpecHarvester now keeps `kind: public_interface_index` for generated
`PublicInterfaceIndex` evidence and records explicit artifact metadata:
`artifactKind`, `mediaType`, `schemaVersion`, and `summary`.

Local SpecPM `0.2.0` validation confirms that the evidence kind is accepted.
The only remaining public smoke warning is the known `P12-T5`
`provides.capabilities.intentIds` support-target warning.

## Quality Gates

| Gate | Result |
|------|--------|
| `PYTHONPATH=src python -m pytest tests/test_collector.py::test_draft_spec_package_enriches_interfaces_from_public_interface_index tests/test_docs_contracts.py -q` | PASS, 9 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 223 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, 43 files already formatted |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 223 passed, total coverage 90.46% |
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
- warnings: `preview_only_package`,
  `evidence_support_target_unknown`
- `unknown_evidence_kind`: absent

The remaining `evidence_support_target_unknown` warning references
`provides.capabilities.intentIds` and is tracked by `P12-T5`.

## CI Integration Smoke

A local reproduction of the updated CI `specpm-integration` fixture produced a
candidate with `public-interface-index.json`, validated it with SpecPM `0.2.0`,
and asserted these BoundarySpec evidence fields:

- `kind: public_interface_index`
- `artifactKind: SpecHarvesterPublicInterfaceIndex`
- `mediaType: application/vnd.spec-harvester.public-interface-index+json`
- `schemaVersion: 2`

Result:

- status: `warning_only`
- errors: `0`
- warnings: `preview_only_package`
- `unknown_evidence_kind`: absent
