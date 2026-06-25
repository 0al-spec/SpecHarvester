# Next Task: P51-T6 Larger Curated Corpus Output Triage

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T6`
**Last Archived:** `P51-T5` Larger Curated Corpus AI-Enabled Proposal-Only Gate
**Depends On:** `P51-T5` Larger Curated Corpus AI-Enabled Proposal-Only Gate

## Goal

Triage the larger curated corpus static, AI draft, AI enrichment, AI-enriched
preview, relation, warning, failed-sidecar, and caveat evidence into selected,
deferred, and do-not-promote outcomes without rerunning the corpus or changing
registry truth. This larger curated corpus output triage is an evidence
classification task, not an acceptance task.

## Context

P51-T5 ran the same 12 selected sources from the P51 manifest through local
LM Studio `openai/gpt-oss-20b`:

```text
inputs/p51-larger-curated-corpus/repositories.yml
```

The AI-enabled gate fixture is:

```text
tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json
```

AI-enabled batch ended `failed`, but evidence capture completed:

```text
processed repositories: `12`
failed repositories: `1`
AI draft proposals: `11`
AI enrichment proposals: `12`
AI-enriched preview applied packages: `8`
```

The hard blocker is `hyperprompt.aiDraft`, which exhausted one JSON repair
attempt and emitted:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

All AI output remains proposal-only. Raw prompt, raw provider response,
secret, and chain-of-thought non-persistence remains part of the evidence.

## Scope

- Classify all 15 static candidate packages and 3 relation proposals.
- Classify AI draft sidecars, including the failed `hyperprompt.aiDraft`
  sidecar.
- Classify AI enrichment sidecars and AI-enriched preview copies.
- Classify warning-only proposal evidence as selected, deferred, or
  do-not-promote.
- Carry `xyflow.partial_public_interface_index`,
  `xyflow.operator_checkout_origin_fork_mismatch`,
  `docc2context.source_checkout_had_untracked_doccarchive`, and
  `hyperprompt.ai_draft_failed_after_json_repair` forward as triage evidence.
- Decide whether P51-T7 exit decision can proceed.

## Boundaries

- Do not rerun the larger corpus in P51-T6.
- Do not run AI in P51-T6.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, readiness output, AI output, AI-enriched preview
  output, rerun output, planning output, triage output, or adapter output as
  registry truth.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets.
- Do not persist chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
