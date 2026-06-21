# P47-T4 Validation Report

Task: P47-T4 Record Targeted Quality Follow-Up Exit Decision
Date: 2026-06-21
Verdict: PASS

## Summary

P47-T4 recorded the targeted quality follow-up exit decision from the P47-T3
bounded rerun gate evidence.

Selected decision:

```text
run_another_targeted_quality_pass_before_larger_curated_corpus
```

The decision does not approve larger curated corpus planning. P47-T3 showed a
passed static-only gate, but the AI-enabled gate failed on `gin.aiDraft` and
`navigation-split-view.aiDraft`. `docc2context.aiDraft` improved to a repaired
non-blocking warning, and xyflow caveats remain visible.

P47-T4 added Phase 48 as the next bounded follow-up path, starting with
`P48-T1` Plan AI Draft Blocker Follow-Up Pass.

## Artifacts

| Artifact | Result |
| --- | --- |
| `tests/fixtures/targeted_pilot_quality_follow_up_exit_decision/p47-t4-targeted-pilot-quality-follow-up-exit-decision.example.json` | Added durable P47-T4 exit decision fixture. |
| `docs/TARGETED_PILOT_QUALITY_FOLLOW_UP_EXIT_DECISION.md` | Added GitHub documentation. |
| `Sources/SpecHarvester/Documentation.docc/TargetedPilotQualityFollowUpExitDecision.md` | Added DocC mirror. |
| `tests/test_docs_contracts.py` | Added contract coverage for fixture identity, P47-T3 source digest, selected/rejected decision paths, blocker treatment, Phase 48 next path, authority boundaries, and docs links. |
| `SPECS/Workplan.md` | Added Phase 48 AI Draft Blocker Follow-Up Before Larger Corpus. |

## Validation Commands

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/targeted_pilot_quality_follow_up_exit_decision/p47-t4-targeted-pilot-quality-follow-up-exit-decision.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q -k 'targeted_pilot_quality_follow_up_exit_decision'` | PASS, `1 passed, 170 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python3 -m pytest` | PASS, `902 passed, 1 skipped` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `131 files already formatted` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `PYTHONPATH=src uv run --extra dev pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `902 passed, 1 skipped`, total coverage `90.51%` |

## Boundary

P47-T4 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
harvested package managers, execute harvested code, accept packages or
relations, publish registry metadata, seed baselines, remove `preview_only`, or
approve a larger curated corpus.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted. Exit-decision output, bounded rerun gate output, static output, AI
output, and adapter output were not treated as registry truth.
