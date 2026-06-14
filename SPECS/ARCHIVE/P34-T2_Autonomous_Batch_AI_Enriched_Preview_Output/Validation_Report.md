# P34-T2 Validation Report

## Summary

P34-T2 adds opt-in autonomous batch AI-enriched preview output.

The implementation keeps default autonomous batch behavior proposal-only. When
`--apply-ai-enrichment` is set, the batch runner applies clean
`SpecHarvesterPackageSetAIEnrichmentProposal` artifacts into copied preview
candidate directories under `package-sets/<repository-id>/enriched/<package-id>/`
and records `ai-enrichment-candidate-patch.json` reports plus batch summary
counts.

## Validation

| Command | Result |
| --- | --- |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py -q` | PASS, `10 passed` |
| `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_ai_enrichment_candidate_patch.py tests/test_docs_contracts.py -q` | PASS, `112 passed` |
| `PYTHONPATH=src pytest -q` | PASS, `717 passed, 1 skipped` |
| `PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90 -q` | PASS, `717 passed, 1 skipped`, total coverage `90.96%` |
| `PYTHONPATH=src ruff check .` | PASS |
| `PYTHONPATH=src ruff format --check src tests` | PASS |
| `git diff --check` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester` | PASS |

## Practical Smoke

Ran an autonomous batch smoke with a local provider stub equivalent to a clean
LM Studio/OpenAI-compatible enrichment proposal:

```text
repository source manifest
  -> autonomous-candidate-batch live-AI path
  -> --apply-ai-enrichment
  -> copied enriched preview candidate
  -> ai-enrichment-candidate-patch.json
```

Result:

```json
{
  "status": "passed",
  "applied": 1,
  "skipped": 2,
  "failed": 0,
  "patchExists": true
}
```

The smoke verified that the source generated candidates remain separate from
the copied enriched preview candidate subtree.

## Boundary

The task does not:

- accept packages;
- accept relations;
- seed baselines;
- remove `preview_only`;
- mutate source candidates;
- publish registry metadata;
- create a SpecPM pull request;
- treat AI output as maintainer approval;
- treat AI output as upstream project endorsement.
