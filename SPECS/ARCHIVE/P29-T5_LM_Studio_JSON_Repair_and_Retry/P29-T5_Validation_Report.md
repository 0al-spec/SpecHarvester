# P29-T5 Validation Report

## Summary

Verdict: Passed.

`P29-T5` adds bounded JSON repair/retry for live
LM Studio/OpenAI-compatible package-set AI draft and enrichment proposal
generation. Malformed local model output now becomes structured proposal
diagnostics and safe repair metadata instead of an uncaught provider failure or
silent success.

## Implementation Checks

- Shared `model_json_repair` helper added for JSON object parsing, bounded
  repair prompt orchestration, and provider usage aggregation.
- `package-set-ai-draft-proposal` live provider path records:
  - `jsonRepairNeeded`;
  - `jsonRepairAttemptCount`;
  - `jsonRepairStatus`;
  - `ai_json_repair_needed`;
  - `ai_json_repair_exhausted` on exhausted repair.
- `package-set-ai-enrichment-proposal` applies the same behavior per package
  member.
- `autonomous-candidate-batch` forwards `--json-repair-max-attempts`, records
  `jsonRepairMaxAttempts`, and surfaces AI proposal `diagnosticCodes` plus
  `jsonRepair` summaries.
- Successful repair persists only the accepted parsed response digest.
  Exhausted repair does not persist raw provider response text or an accepted
  `responseDigest`.
- External `--model-output` wrapping behavior remains unchanged.

## Commands Run

```bash
PYTHONPATH=src pytest tests/test_package_set_ai_draft_proposal.py tests/test_package_set_ai_enrichment.py tests/test_autonomous_candidate_batch.py tests/test_docs_contracts.py -q
```

Result: `83 passed`.

```bash
PYTHONPATH=src python -m pytest -q
```

Result: `622 passed, 1 skipped`.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q
```

Result: `622 passed, 1 skipped`; total coverage `90.58%`.

```bash
PYTHONPATH=src ruff check .
```

Result: passed.

```bash
PYTHONPATH=src ruff format --check src tests
```

Result: `105 files already formatted`.

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Notes

- Tests use monkeypatched OpenAI-compatible responses; no CI test calls LM
  Studio or any live provider.
- Repair prompts are transient provider requests. Request/proposal artifacts
  still record compact evidence and safe metadata only.
- `P29-T6` remains the follow-up task for the mixed Flask/Gin/xyflow corpus
  quality gate after deterministic fallback and bounded JSON repair support.
