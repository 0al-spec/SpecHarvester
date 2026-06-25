# Next Task: P51-T7 Larger Curated Corpus Output Triage

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T7`
**Last Archived:** `P51-T6` Hyperprompt AI Draft Single-Package Fallback
**Depends On:** `P51-T6` Hyperprompt AI Draft Single-Package Fallback

## Goal

Triage the larger curated corpus static, AI draft, AI enrichment, AI-enriched
preview, relation, warning, fallback, and caveat evidence into selected,
deferred, and do-not-promote outcomes without changing registry truth.

## Context

P51-T6 repaired the reproduced `hyperprompt.aiDraft` hard blocker with a
deterministic single-package fallback:

```text
fixture: tests/fixtures/hyperprompt_ai_draft_single_package_fallback/p51-t6-hyperprompt-ai-draft-single-package-fallback.example.json
targeted rerun exit code: 0
batch status: passed
repository status: passed
aiDraft status: warning
aiDraft selected members: 1
aiDraft stop policy: stop_for_author_review
diagnostic: single_package_deterministic_fallback_applied
```

The repaired sidecar still records `ai_json_repair_exhausted`,
`ai_json_repair_needed`, and `package_set_subject_metadata_missing`, but these
are non-blocking fallback warnings for the deterministic single-package
Hyperprompt inventory.

P51-T5 remains the full-corpus evidence source, and P51-T6 is the targeted
repair evidence source for Hyperprompt.

## Scope

- Classify all 15 static candidate packages and 3 relation proposals.
- Classify AI draft sidecars, including repaired `hyperprompt.aiDraft`.
- Classify AI enrichment sidecars and AI-enriched preview copies.
- Classify warning-only proposal evidence as selected, deferred, or
  do-not-promote.
- Carry `xyflow.partial_public_interface_index`,
  `xyflow.operator_checkout_origin_fork_mismatch`,
  `docc2context.source_checkout_had_untracked_doccarchive`, and
  `hyperprompt.single_package_deterministic_fallback_applied` forward as
  triage evidence.
- Decide whether P51-T8 exit decision can proceed.

## Boundaries

- Do not rerun the larger corpus in P51-T7.
- Do not run AI in P51-T7.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, readiness output, AI output, AI-enriched preview
  output, repair output, rerun output, planning output, triage output, or
  adapter output as registry truth.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets.
- Do not persist chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
