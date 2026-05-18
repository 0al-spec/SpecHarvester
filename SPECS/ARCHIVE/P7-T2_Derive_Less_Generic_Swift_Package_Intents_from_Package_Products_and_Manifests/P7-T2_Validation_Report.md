# P7-T2 Validation Report

## Validation Run

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_collector.py -q` | PASS, 53 passed |
| `PYTHONPATH=src python -m pytest` | PASS, 130 passed |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 90.09% total coverage |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Smoke Verification

Using the ignored `.smoke/output/candidates` workspace from the documented local
smoke fixture flow:

| Report | Result |
|--------|--------|
| `governance-report --candidates-root .smoke/output/candidates` | PASS, `duplicateIntentCount=0`, `duplicateCapabilityCount=0`, `issueCount=0` |

## Result

Status: PASS

## Notes

- Swift `Package.swift` files now provide bounded static package metadata:
  package name, ecosystem/language, and product names/types.
- Swift draft intents now use deterministic product-specific IDs such as
  `intent.swift.product.puzzlecore`.
- Draft capability intent derivation uses the root Swift package manifest when
  present, avoiding dependency checkout products as package intent evidence.
- JavaScript/TypeScript intent derivation remains unchanged.
