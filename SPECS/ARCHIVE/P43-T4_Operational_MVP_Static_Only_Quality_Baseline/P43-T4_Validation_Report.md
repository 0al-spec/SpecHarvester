# P43-T4 Validation Report

## Task

P43-T4 Operational MVP Static-Only Quality Baseline.

## Result

PASS.

## Static-Only Run Evidence

Run root:

```text
/tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z
```

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/inputs \
  --out /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/output \
  --skip-ai \
  --repository-profile-selection auto
```

Observed result:

- `status`: `passed`
- `processedCount`: `3`
- `passedPreflightCount`: `3`
- `failedRepositoryCount`: `0`
- `aiDraftProposalCount`: `0`
- `aiEnrichmentProposalCount`: `0`
- `repositoryPluginAdapterEvidenceSidecarCount`: `0`
- `trustedLocalAdapterRunEvidenceSidecarCount`: `0`

Input manifest digest:

```text
sha256:f83b92e94bf766f7b308f77633c4980a60a7dfffa0bd400d7e8faacdf10663de
```

Autonomous batch report digest:

```text
sha256:735cc878bc3dc19325c269adf2f2e5e12798373527b37979a92ce6f950062499
```

## Corpus

| Repository | Ecosystem | Revision | Checkout state | Result |
| --- | --- | --- | --- | --- |
| `xyflow` | JavaScript/TypeScript | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | clean | passed, 4 candidates, 3 relations |
| `fastapi` | Python | `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263` | clean | passed, 1 candidate |
| `gin` | Go | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | clean | passed, 1 candidate |

The `xyflow` checkout origin is `git@github.com:SoundBlaster/xyflow.git`; the
baseline fixture records this explicitly rather than rewriting it to the
canonical example upstream.

## Boundary Validation

The static-only run used operator-provided pinned local checkouts and recorded:

- `ai.mode`: `disabled`
- `adapterExecution`: `not_run`
- `repositoryPluginAdapterEvidence.status`: `not_provided`
- `trustedLocalAdapterRunEvidence.status`: `not_provided`
- `registryAuthority`: `false`
- no package acceptance, relation acceptance, baseline seeding, preview removal,
  or registry publishing.

## Quality Notes

- FastAPI and Gin produced complete public-interface indexes.
- xyflow produced a partial public-interface index with 29 diagnostics; this is
  recorded as `partial_public_interface_index` caveat, not as a blocking stop
  condition.
- All three repository-level results are `author_ready_draft` and
  `specpmHandoffReadiness.ready: true`, with explicit `requiresAuthorReview:
  true` and `registryAuthority: false`.

## Validation Commands

- `PYTHONPATH=src python -m spec_harvester source-manifests /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/inputs` — PASS.
- `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/inputs --out /tmp/specharvester-p43-t4-operational-mvp-static-only-20260620T000000Z/output --skip-ai --repository-profile-selection auto` — PASS.
- `python3 -m json.tool tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json >/dev/null` — PASS.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_static_only_baseline or current_next_task'` — PASS, `1 passed, 148 deselected`.
- `ruff check src tests` — PASS.
- `ruff format --check src tests` — initially reported `tests/test_docs_contracts.py`; after `ruff format tests/test_docs_contracts.py`, PASS with `131 files already formatted`.
- `swift package dump-package >/dev/null` — PASS.
- `git diff --check` — PASS.
- `PYTHONPATH=src python -m pytest` — PASS, `862 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` — PASS, `862 passed, 1 skipped`, coverage `90.49%`.
- `swift build --target SpecHarvesterDocs` — PASS.
