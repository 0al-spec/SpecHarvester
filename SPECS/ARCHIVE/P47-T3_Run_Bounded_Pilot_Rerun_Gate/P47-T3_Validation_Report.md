# P47-T3 Validation Report

Task: P47-T3 Run Bounded Pilot Rerun Gate
Date: 2026-06-21
Verdict: PASS

## Summary

P47-T3 ran the bounded pilot rerun gate over the same six P46 repositories.
The static-only gate passed. The AI-enabled gate executed against LM Studio
with `openai/gpt-oss-20b` and produced proposal-only evidence, but the batch
status was `failed` because `gin.aiDraft` and
`navigation-split-view.aiDraft` failed after one JSON repair attempt.

This is a successful P47-T3 evidence task because the gate result was captured
durably and honestly. It is not larger curated corpus approval. P47-T4 must
record the exit decision.

## Run Setup

The source manifest stayed:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

Run root:

```text
/tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z
```

The manifest-relative checkout paths were unavailable under
`/Users/egor/Development/GitHub/0AL`, but the same pinned local checkouts were
available under `/Users/egor/Development/GitHub`. All six revisions matched
the manifest. P47-T3 used clean `git archive` snapshots from those local
checkouts to avoid untracked working-tree drift; no clone or fetch was run.

## Run Results

| Gate | Result |
| --- | --- |
| Source manifest preflight | PASS, `repositoryCount: 6` |
| Static-only batch | PASS, `processedCount: 6`, `failedRepositoryCount: 0`, `passedPreflightCount: 6` |
| AI-enabled batch | EXPECTED NONZERO EXIT, report status `failed`, `processedCount: 6`, `failedRepositoryCount: 2`, `passedPreflightCount: 6` |

AI-enabled summary:

- `aiDraftProposalCount`: 4
- `aiDraftCompletedRepositoryCount`: 1
- `aiDraftWarningRepositoryCount`: 3
- `aiDraftFailedRepositoryCount`: 2
- `aiEnrichmentProposalCount`: 6
- `aiEnrichmentCompletedRepositoryCount`: 3
- `aiEnrichmentWarningRepositoryCount`: 3
- `aiEnrichmentProviderTotalTokens`: 110,953

Repository highlights:

- `docc2context.aiDraft` improved from P46 do-not-promote failure to warning
  with `ai_json_repair_needed` repaired.
- `gin.aiDraft` remains a failed AI draft with
  `ai_json_repair_exhausted` and `package_set_subject_metadata_missing`.
- `navigation-split-view.aiDraft` is a new failed AI draft with
  `ai_json_repair_exhausted` and `package_set_subject_metadata_missing`.
- `xyflow.aiEnrichment` did not repeat `model_evidence_path_unsupported`, but
  it carries `ai_json_repair_needed`.
- xyflow static interface evidence remains partial with 29 diagnostics.

## Artifacts

| Artifact | Result |
| --- | --- |
| `tests/fixtures/targeted_pilot_bounded_rerun_gate/p47-t3-targeted-pilot-bounded-rerun-gate.example.json` | Added durable P47-T3 gate fixture. |
| `docs/TARGETED_PILOT_BOUNDED_RERUN_GATE.md` | Added GitHub documentation. |
| `Sources/SpecHarvester/Documentation.docc/TargetedPilotBoundedRerunGate.md` | Added DocC mirror. |
| `tests/test_docs_contracts.py` | Added contract coverage for fixture identity, source digests, static-before-AI ordering, run outcomes, sidecar/caveat results, boundaries, links, and next-task readiness. |

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python3 -m spec_harvester source-manifests /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs` | PASS, `repositoryCount: 6` |
| `PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-static --skip-ai --repository-profile-selection auto` | PASS, batch status `passed` |
| `PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1` | EXPECTED NONZERO EXIT, report status `failed`, evidence captured |
| `python3 -m json.tool tests/fixtures/targeted_pilot_bounded_rerun_gate/p47-t3-targeted-pilot-bounded-rerun-gate.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -q -k 'targeted_pilot_bounded_rerun_gate'` | PASS, `1 passed, 169 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
| `PYTHONPATH=src python3 -m pytest` | PASS, `901 passed, 1 skipped` |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS, `131 files already formatted` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |
| `PYTHONPATH=src uv run --extra dev pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `901 passed, 1 skipped`, total coverage `90.51%` |

## Boundary

P47-T3 did not approve a larger curated corpus, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, clone or
fetch repositories, install dependencies, invoke package managers inside
harvested repositories, execute harvested code, run adapters, or enable trusted
local adapter execution.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted. Static output, AI output, and adapter output were not treated as
registry truth.
