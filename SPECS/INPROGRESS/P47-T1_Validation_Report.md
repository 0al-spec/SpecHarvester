# P47-T1 Validation Report

## Task

P47-T1 Targeted Pilot Quality Follow-Up Plan

## Verdict

PASS

## Summary

P47-T1 records a targeted quality follow-up plan after the P46 exit decision.
The plan keeps `gin.aiDraft`, `docc2context.aiDraft`, and xyflow caveats
visible, defines repair or explicit disposition workstreams, and requires a
bounded rerun gate before any larger curated corpus approval.

P47-T1 did not rerun the pilot, run AI, run adapters, clone or fetch
repositories, execute harvested code, or change registry truth.

## Durable Artifacts

- `tests/fixtures/targeted_pilot_quality_follow_up_plan/p47-t1-targeted-pilot-quality-follow-up-plan.example.json`
- `docs/TARGETED_PILOT_QUALITY_FOLLOW_UP_PLAN.md`
- `Sources/SpecHarvester/Documentation.docc/TargetedPilotQualityFollowUpPlan.md`

## Plan Summary

| Field | Result |
| --- | --- |
| Selected plan | `targeted_quality_follow_up_before_larger_curated_corpus` |
| Larger curated corpus approved now | no |
| Pilot rerun approved now | no |
| Next execution task | `P47-T2` |
| Do-not-promote AI sidecars carried forward | 2 |
| xyflow caveats carried forward | 3 |
| Workstreams planned | 4 |

## Carry-Forward Blockers

- `gin.aiDraft`: regenerate or explicitly accept as non-blocking.
- `docc2context.aiDraft`: regenerate or explicitly accept as non-blocking.
- `partial_public_interface_index`: resolve or explicitly accept.
- `operator_checkout_origin_fork_mismatch`: verify origin or explicitly accept.
- `model_evidence_path_unsupported`: resolve unsupported enrichment path or
  explicitly exclude enrichment.

## Boundary Verification

P47-T1 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The plan is not registry truth. Exit-decision output, handoff output, static
output, AI output, and adapter output remain non-authoritative review evidence.

## Commands

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/targeted_pilot_quality_follow_up_plan/p47-t1-targeted-pilot-quality-follow-up-plan.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'targeted_pilot_quality_follow_up_plan'` | PASS, `1 passed, 167 deselected` |
| `ruff format tests/test_docs_contracts.py` | PASS, `1 file reformatted` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python -m pytest` | PASS, `899 passed, 1 skipped` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS |
| `swift package dump-package >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `899 passed, 1 skipped`, coverage `90.52%` |
| `swift build --target SpecHarvesterDocs` | PASS |

## Remaining Gap

The larger curated corpus remains blocked. P47-T2 must execute the targeted
quality pass and produce repair or explicit disposition evidence before the
bounded rerun gate can run.
