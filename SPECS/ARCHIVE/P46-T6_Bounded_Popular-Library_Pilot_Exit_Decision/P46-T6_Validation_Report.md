# P46-T6 Validation Report

## Task

P46-T6 Bounded Popular-Library Pilot Exit Decision

## Verdict

PASS

## Summary

P46-T6 records the Phase 46 exit decision as
`run_targeted_quality_pass_before_larger_curated_corpus`. The static pilot
produced reviewable evidence for all six repositories, but larger curated
corpus expansion remains blocked until targeted AI sidecar and xyflow caveat
quality work is complete.

## Durable Artifacts

- `tests/fixtures/bounded_popular_library_pilot_exit_decision/p46-t6-bounded-popular-library-pilot-exit-decision.example.json`
- `docs/BOUNDED_POPULAR_LIBRARY_PILOT_EXIT_DECISION.md`
- `Sources/SpecHarvester/Documentation.docc/BoundedPopularLibraryPilotExitDecision.md`

## Decision Summary

| Field | Result |
| --- | --- |
| Selected decision | `run_targeted_quality_pass_before_larger_curated_corpus` |
| Larger curated corpus approved now | no |
| Targeted quality pass required | yes |
| Stop on documented blocker | no |
| Reviewable static members | 9 |
| Reviewable repositories | 6 |
| Do-not-promote AI sidecars | 2 |
| Unsupported AI sidecars | 1 |
| Evidence-gap repositories | 1 |

## Key Outcomes

- Static output remains reviewable for Flask, Gin, xyflow, Cupertino,
  NavigationSplitView, and docc2context.
- `gin.aiDraft` and `docc2context.aiDraft` remain do-not-promote sidecars and
  block larger curated corpus expansion until targeted repair.
- xyflow still requires explicit caveat disposition for
  `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, and
  `model_evidence_path_unsupported`.
- `proceed_to_larger_curated_corpus` is rejected for now.
- `stop_on_documented_blocker` is rejected because the remaining blockers are
  targeted and repairable.

## Boundary Verification

P46-T6 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

The exit decision is not registry truth. Handoff output, static output, AI
output, and adapter output remain non-authoritative review evidence.

## Commands

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/bounded_popular_library_pilot_exit_decision/p46-t6-bounded-popular-library-pilot-exit-decision.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'bounded_popular_library_pilot_exit_decision'` | PASS, `1 passed, 166 deselected` |
| `ruff format tests/test_docs_contracts.py` | PASS |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` | PASS, `167 passed` |
| `git diff --check` | PASS |

## Remaining Gap

Phase 46 is complete. The recommended follow-up is Phase 47 Targeted Pilot
Quality Follow-Up Planning before any larger curated corpus expansion.
