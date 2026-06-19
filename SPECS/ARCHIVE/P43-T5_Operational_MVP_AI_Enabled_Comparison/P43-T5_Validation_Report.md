# P43-T5 Validation Report

## Task

P43-T5 Operational MVP AI-Enabled Comparison.

## Result

PASS.

## Provider Probe

Command:

```bash
curl --silent --show-error --max-time 2 http://127.0.0.1:1234/v1/models
```

Observed result:

```text
exitCode: 7
status: provider_unavailable
```

The local OpenAI-compatible provider was unavailable. P43-T5 therefore records
a provider-unavailable comparison artifact and does not run AI-enabled
`autonomous-candidate-batch`, select a model, persist raw prompts or raw
responses, or create AI proposal artifacts.

## Comparison Artifact

Fixture:

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
```

Fixture digest:

```text
sha256:c9934bae637aff8d748e431476d297dc58f81583ab7fdb8fc00db1141889e049
```

Static-only baseline reference:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:39e623bb3eb835ef1e57286bd6d06394c4fe62fd594e3f756e18f96a4c9ea3ab
```

## Summary

- `samePinnedCorpusAsStaticBaseline`: `true`
- `providerAvailable`: `false`
- `aiEnabledRunPerformed`: `false`
- `aiProposalArtifactCount`: `0`
- `aiComparisonProviderUnavailableCount`: `3`
- `specpmHandoffChangedByAI`: `false`
- `aiOutputAcceptedAsRegistryTruth`: `false`

## Per-Repository Outcome

| Repository | Static-only baseline | AI-enabled comparison | Delta |
| --- | --- | --- | --- |
| `xyflow` | passed, 4 candidates, 3 relations | `provider_unavailable` | not evaluated |
| `fastapi` | passed, 1 candidate | `provider_unavailable` | not evaluated |
| `gin` | passed, 1 candidate | `provider_unavailable` | not evaluated |

Each repository preserves the P43-T4 static-only handoff-ready preview state.
No AI-generated improvement was available in this environment.

## Boundary Validation

The comparison records:

- local provider unavailable;
- `aiInvocationPerformed: false`;
- `rawPromptPersisted: false`;
- `rawResponsePersisted: false`;
- `trustedLocalAdapterExecutionEnabled: false`;
- `acceptsPackages: false`;
- `acceptsRelations: false`;
- `publishesRegistryMetadata: false`;
- `seedsBaselines: false`;
- `removesPreviewOnly: false`;
- `aiOutputAcceptedAsRegistryTruth: false`.

## Validation Commands

- `curl --silent --show-error --max-time 2 http://127.0.0.1:1234/v1/models` — expected provider-unavailable result, exit code `7`.
- `python3 -m json.tool tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json >/dev/null` — PASS.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_ai_enabled_comparison or current_next_task'` — PASS, `1 passed, 149 deselected`.
- `ruff check src tests` — PASS.
- `ruff format --check src tests` — PASS, `131 files already formatted`.
- `swift package dump-package >/dev/null` — PASS.
- `git diff --check` — PASS.
- `PYTHONPATH=src python -m pytest` — PASS, `863 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` — PASS, `863 passed, 1 skipped`, coverage `90.49%`.
- `swift build --target SpecHarvesterDocs` — PASS.
