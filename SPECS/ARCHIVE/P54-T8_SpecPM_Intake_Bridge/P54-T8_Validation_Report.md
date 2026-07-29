# P54-T8 Validation Report

**Task:** SpecPM Intake Bridge
**Date:** 2026-07-29
**Verdict:** PASS

## Delivered

- A bounded `build-local-specpm-intake-proposal` CLI command.
- Archive, catalog, packet, immutable decision-history, and current-decision
  digest revalidation before SpecPM execution.
- Temporary reconstruction of declared candidate files only.
- Read-only `specpm validate --json` execution for current
  `accept_for_intake` decisions carrying `evidence_verified`.
- Deterministic proposal evidence with normalized validation reports,
  `preview_only` enforcement, explicit non-authority, and
  `registryMutationCount: 0`.
- Failure coverage for unsafe paths, missing files, malformed reports,
  oversized output, process startup errors, timeouts, invalid packages, and
  stale bindings.

## Quality Gates

| Gate | Result |
| --- | --- |
| Python tests | PASS: 1151 passed, 1 skipped |
| Coverage | PASS: 90.03% total; 92% intake bridge |
| Intake bridge focused tests | PASS: 25 passed |
| Ruff lint | PASS |
| Ruff format check | PASS |
| Swift package manifest | PASS |
| Swift documentation target | PASS |
| Real local SpecPM preflight | PASS: 1 package, warning-only |
| SpecPM worktree mutation check | PASS: clean before and after |

## Commands

```bash
uv run pytest tests/test_local_specpm_intake_bridge.py \
  --cov=spec_harvester.local_specpm_intake_bridge \
  --cov-report=term-missing
uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
uv run ruff check src tests
uv run ruff format --check src tests
swift package dump-package >/dev/null
swift build --target SpecHarvesterDocs
```

The real evidence run used the installed `specpm` command against a temporary
reconstruction of the approved `rtk-ai-rtk` candidate. SpecPM returned
`warning_only` solely because the package remains `preview_only`.

## Evidence

`SPECS/EVIDENCE/P54-T8/P54-T8_Local_SpecPM_Intake_Proposal.example.json`
records:

- source bundle:
  `db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63`;
- approved candidate: `rtk-ai-rtk`;
- packet:
  `e1aed867b62f5374dbec871d1938d3c4b94516f980b8f50801004ee89a56e06b`;
- immutable decision:
  `861d05af7cfdd8ea40156b3e0ffcdc2228433775d3726a3a14cb4acc0cc49ef3`;
- one reconstructed package, one passed preflight, zero failed preflights;
- normalized SpecPM report:
  `f3b9dd0e56da08d94c6c7a8a81b6459b9b505220963e0a8ba722070bfe9b7e28`;
- zero registry mutations.

## Type Check Note

The new intake bridge passes isolated mypy validation with imports skipped.
Following all project imports exposes 60 pre-existing type errors outside this
task's scope; no new local bridge error remains.

## Boundary Checks

- Only operator-provided `specpm validate` executes.
- Candidate package managers, builds, tests, adapters, and source code do not
  execute.
- Candidate files are reconstructed beneath a temporary root from verified,
  declared regular archive members.
- Machine-local paths and raw process diagnostics are omitted from portable
  output.
- The bridge cannot accept packages or relations, remove `preview_only`,
  mutate accepted sources or public-index metadata, or create a SpecPM pull
  request.
