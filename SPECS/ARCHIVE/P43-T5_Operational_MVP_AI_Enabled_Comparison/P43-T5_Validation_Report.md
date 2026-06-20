# P43-T5 Validation Report

## Task

P43-T5 Operational MVP AI-Enabled Comparison.

## Result

PASS.

## Provider Probe

Command:

```bash
curl --silent --show-error --max-time 5 http://127.0.0.1:1234/v1/models
```

Observed result:

```text
exitCode: 0
status: provider_available
provider: lm_studio
model: openai/gpt-oss-20b
```

The local OpenAI-compatible provider was available. P43-T5 ran
`autonomous-candidate-batch` without `--skip-ai` over the same pinned corpus as
P43-T4, with local LM Studio `openai/gpt-oss-20b` and
`--json-repair-max-attempts 1`.

## Comparison Artifact

Fixture:

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
```

Fixture digest:

```text
sha256:1ad9d2b59bd17dfd50d0abd9fc481883d03dacaf3ebe8f717a064b91be58052d
```

Static-only baseline reference:

```text
tests/fixtures/operational_mvp_validation/p43-t4-operational-mvp-static-only-baseline.example.json
sha256:39e623bb3eb835ef1e57286bd6d06394c4fe62fd594e3f756e18f96a4c9ea3ab
```

Live batch report:

```text
/tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/output/autonomous-candidate-batch-report.json
sha256:3a677f471c18bdbabd7c80d6edcbb5af4ec80ec36ff7d325a483c87f672a8016
```

## Summary

- `samePinnedCorpusAsStaticBaseline`: `true`
- `providerAvailable`: `true`
- `aiEnabledRunPerformed`: `true`
- `aiDraftProposalArtifactCount`: `3`
- `aiEnrichmentProposalArtifactCount`: `3`
- `aiProposalArtifactCount`: `6`
- `aiEnrichmentProposalMemberCount`: `6`
- `aiComparisonProviderUnavailableCount`: `0`
- `aiEnrichedPreviewAppliedCount`: `0`
- `providerTotalTokens`: `81003`
- `specpmHandoffChangedByAI`: `false`
- `aiOutputAcceptedAsRegistryTruth`: `false`

## Per-Repository Outcome

| Repository | Static-only baseline | AI-enabled comparison | Delta |
| --- | --- | --- | --- |
| `xyflow` | passed, 4 candidates, 3 relations | draft warning, 4 enrichment proposals | proposal available for author review |
| `fastapi` | passed, 1 candidate | draft warning, 1 enrichment proposal | proposal available for author review |
| `gin` | passed, 1 candidate | draft warning, 1 enrichment proposal | proposal available for author review |

Each repository preserves the P43-T4 static-only handoff-ready preview state.
The live AI layer adds proposal-only sidecars. The AI draft layer records
`package_set_id_missing` warnings; the enrichment layer completes cleanly and
stops for author review.

## Boundary Validation

The comparison records:

- local LM Studio provider available;
- `aiInvocationPerformed: true`;
- `aiEnrichedPreviewApplied: false`;
- `rawPromptPersisted: false`;
- `rawResponsePersisted: false`;
- `chainOfThoughtPersisted: false`;
- `trustedLocalAdapterExecutionEnabled: false`;
- `acceptsPackages: false`;
- `acceptsRelations: false`;
- `publishesRegistryMetadata: false`;
- `seedsBaselines: false`;
- `removesPreviewOnly: false`;
- `aiOutputAcceptedAsRegistryTruth: false`.

## Validation Commands

- `curl --silent --show-error --max-time 5 http://127.0.0.1:1234/v1/models` - PASS, provider available.
- `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/inputs --out /tmp/specharvester-p43-t5-operational-mvp-ai-enabled-live-20260620T071412Z/output --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1` - PASS, batch status `passed`.
- `python3 -m json.tool tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json >/dev/null` - PASS.
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'operational_mvp_ai_enabled_comparison or current_next_task'` - PASS, `1 passed, 149 deselected`.
- `ruff check src tests` - PASS.
- `ruff format --check src tests` - PASS, `131 files already formatted`.
- `swift package dump-package >/dev/null` - PASS.
- `git diff --check` - PASS.
- `PYTHONPATH=src python -m pytest` - PASS, `863 passed, 1 skipped`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` - PASS, `863 passed, 1 skipped`, coverage `90.49%`.
- `swift build --target SpecHarvesterDocs` - PASS.
