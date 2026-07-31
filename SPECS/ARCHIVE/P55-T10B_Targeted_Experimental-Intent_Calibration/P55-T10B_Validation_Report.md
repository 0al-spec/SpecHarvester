# P55-T10B Validation Report

**Task:** P55-T10B Targeted Experimental-Intent Calibration

**Date:** 2026-07-31

**Verdict:** PASS

## Scope and Bindings

- Codex 5.3 Spark ran against exactly four pinned, clean targets: RTK, OpenAI
  Codex, ripgrep, and claude-mem.
- The run is bound to the P55-T10A decision policy, P55-T5 frozen quality
  policy, unchanged P55-T9 target rubric, source manifest, and exact source
  revisions by SHA-256.
- The reusable runner verifies exact provider and model identity, full target
  accounting, candidate packets, source revisions, attempt budgets, and policy
  bindings before finalizing evidence.

## Observed Result

| Measure | Result |
| --- | ---: |
| Completed / failed | 4 / 0 |
| Provider attempts | 5 |
| Evidence-supported experimental intents | 2 |
| Experimental proposal rate | 0.50 |
| Purpose accuracy | 1.00 |
| Evidence-supported claim rate | 1.00 |
| Schema-valid proposal rate | 1.00 |
| Reviewer edit-burden estimate | 0.125 |
| Nearby-intent differentiation rate | 0.50 |
| False novelty | 0 |
| Duplicate experimental IDs / semantic stems | 0 / 0 |

All unchanged P55-T5 numerical gates passed. OpenAI Codex and claude-mem
received evidence-supported experimental intents. RTK and ripgrep retained
overly broad observed intents; neither is counted as justified reuse and both
carry an experimental-intent edit requirement.

Claude-mem's first provider attempt failed closed because its experimental ID
was not collision-bound. Its second and final allowed attempt completed without
JSON repair. The failure remains recorded in the durable target record.

## Decision and Authority

- `p55T10CUnblocked` is `true` because all targets completed, all frozen gates
  passed, two useful experimental intents were produced, and false novelty,
  duplicate IDs, and duplicate semantic stems remained zero.
- `thresholdsRedefined` is `false`.
- `maintainerDecisionRecorded` is `false`: calibration success is not intent
  acceptance, materialization, canonicalization, or publication.
- Two static candidates retain pre-existing `capability_namespace_violation`
  diagnostics and remain ineligible for materialization without correction.

## Privacy and Execution Boundary

- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths were not persisted.
- No harvested repository code or package manager was executed.
- No candidate was accepted or materialized; SpecPM, registry truth, and public
  output were unchanged.

## Validation Commands

- Real run with
  `scripts/run_p55_t10b_experimental_intent_calibration.py`: completed `4/4`,
  emitted evidence SHA-256
  `7e7739374bfe78c3e72179e5521ee941cd9eefa94fba147a8e1f7e74397e361f`,
  and returned `p55T10CUnblocked: true`.
- `uv run pytest tests/test_experimental_intent_calibration.py
  --cov=spec_harvester.experimental_intent_calibration --cov-report=term-missing
  -q`: `16 passed`; module coverage `90%`.
- `uv run pytest --cov=spec_harvester --cov-report=term-missing
  --cov-fail-under=90`: `1326 passed, 1 skipped`; total coverage `90.03%`.
- `uv run ruff check src tests
  scripts/run_p55_t10b_experimental_intent_calibration.py`: passed.
- `uv run ruff format --check src tests
  scripts/run_p55_t10b_experimental_intent_calibration.py`: passed.
- `jq empty` on durable T10B evidence: passed.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing warning
  that the DocC catalog is unhandled by the executable target.
- `git diff --check`: passed.
