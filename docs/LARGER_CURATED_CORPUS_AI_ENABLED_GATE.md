# Larger Curated Corpus AI-Enabled Gate

Status: P51-T5 real local AI-enabled proposal-only gate.

P51-T5 runs the 12-source P51 larger curated corpus manifest through the local
LM Studio/OpenAI-compatible provider after the P51-T4 static-only gate passed.
The run records proposal-only AI draft and enrichment evidence. It does not
change registry truth.

The source manifest is:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The durable fixture is:

```text
tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-ai-enabled-gate/v0
kind: SpecHarvesterLargerCuratedCorpusAIEnabledGate
authority: producer_ai_enabled_proposal_evidence_only
```

## What Was Run

Run root:

```text
/tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z
```

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p51-larger-curated-corpus \
  --out /tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z/output \
  --repository-profile-selection auto \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
```

The source manifest digest was:

```text
sha256:7676d9d5069f223c33c3e3650c76a60897ada6bed05034dfb5f94dba1d4be79a
```

The batch report digest was:

```text
sha256:3072ee644db22cad1cdafdf39f5de23a336c848a3aa1709c129bcd6c2cad1c29
```

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | failed |
| Processed repositories | 12 |
| Failed repositories | 1 |
| Passed preflights | 12 |
| Candidate packages | 15 |
| Relation proposals | 3 |
| AI draft artifacts | 12 |
| AI draft proposals | 11 |
| AI draft completed repositories | 5 |
| AI draft warning repositories | 6 |
| AI draft failed repositories | 1 |
| AI enrichment proposals | 12 |
| AI enrichment completed repositories | 8 |
| AI enrichment warning repositories | 4 |
| AI enrichment provider total tokens | 190,282 |
| AI-enriched preview applied packages | 8 |
| AI-enriched preview skipped packages | 7 |
| Trusted local adapter sidecars | 0 |

In prose: the larger curated corpus AI-enabled path processed all 12 selected
repositories and all preflights passed. The evidence capture is complete, but
the AI-enabled gate status is `failed` because `hyperprompt.aiDraft` exhausted
one JSON repair attempt and emitted `package_set_subject_metadata_missing`.

## Repository Results

| Repository | Batch status | AI draft | AI enrichment | AI-enriched preview | Main diagnostics |
| --- | --- | --- | --- | --- | --- |
| Flask | passed | warning | warning | skipped 1 | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | passed | warning | completed | applied 1 | `selected_member_role_unknown` |
| xyflow | passed | completed | warning | skipped 4 | `refined_summary_missing`; interface partial, 29 diagnostics |
| Cupertino | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| NavigationSplitView | passed | warning | warning | skipped 1 | `selected_member_role_unknown`, `ai_json_repair_needed` |
| docc2context | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| FastAPI | passed | completed | completed | applied 1 | none |
| FastMCP | passed | completed | completed | applied 1 | none |
| SpecPM | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| Hypercode | passed | completed | completed | applied 1 | none |
| SpecNode | passed | completed | warning | skipped 1 | `model_evidence_path_unsupported` |
| Hyperprompt | failed | failed | completed | applied 1 | `ai_json_repair_exhausted`, `ai_json_repair_needed`, `package_set_subject_metadata_missing` |

## Carry-Forward Triage

Four caveats remain visible for P51-T7 triage:

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`
- `hyperprompt.ai_draft_failed_after_json_repair`

The `hyperprompt.aiDraft` sidecar is the only hard blocker in P51-T5. P51-T6
is the targeted repair task for that blocker; P51-T7 output triage must use the
repair result rather than treating the failed P51-T5 sidecar as accepted
evidence.

## Gate Decision

P51-T5 is complete as an evidence-capture task. The AI-enabled gate did not
pass cleanly.

P51-T6 targeted repair is allowed and required before P51-T7 can triage corpus
outputs. P51-T7 must triage the static candidates, relation proposals, AI draft
sidecars, AI enrichment sidecars, warning evidence, repaired Hyperprompt
fallback evidence, and carried-forward checkout/interface caveats without
accepting packages or relations.

## Boundary

P51-T5 ran AI through the operator-provided local LM Studio endpoint and used
`--apply-ai-enrichment` to prepare copied preview candidates where enrichment
was clean. All AI output remains proposal-only review evidence.

P51-T5 did not enable trusted local adapter execution, run adapter code, clone
or fetch repositories, install dependencies, invoke package managers, execute
harvested code, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, persist raw prompts, persist raw provider
responses, persist secrets, or persist chain-of-thought.

The run does not treat static output as registry truth, AI output as registry
truth, enriched preview output as registry truth, or adapter output as registry
truth. All generated candidates, relation proposals, AI sidecars, and
AI-enriched preview copies remain review evidence requiring SpecPM maintainer
review.
