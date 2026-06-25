# Hyperprompt AI Draft Single-Package Fallback

Status: P51-T6 targeted repair evidence.

P51-T6 repairs the reproducible `hyperprompt.aiDraft` blocker found by the
P51-T5 larger curated corpus AI-enabled gate. The blocker was reproduced in a
targeted Hyperprompt rerun: the local model response remained malformed after
one bounded JSON repair attempt and omitted the top-level `packageSet` subject.

The repair is intentionally narrow. It applies only when deterministic request
context contains exactly one package subject and the package-set identity is
recoverable. In that case, SpecHarvester emits proposal-only fallback evidence
from the deterministic inventory, preserves the JSON repair diagnostics as
warnings, and marks the sidecar ready for author review without treating AI or
fallback output as registry truth.

## Fixture

```text
tests/fixtures/hyperprompt_ai_draft_single_package_fallback/p51-t6-hyperprompt-ai-draft-single-package-fallback.example.json
```

The fixture records:

- the previous reproduced hard blocker;
- the targeted rerun command and exit code;
- the repaired `hyperprompt.aiDraft` warning sidecar;
- the selected fallback member `hyperprompt.core`;
- the non-blocking diagnostics;
- raw prompt, raw provider response, secret, and chain-of-thought
  non-persistence;
- proposal-only and no-registry-truth boundaries.

## Targeted Rerun Result

| Field | Value |
| --- | --- |
| Run root | `/tmp/specharvester-p51-t6-hyperprompt-fallback-rerun-20260625T131341Z` |
| Exit code | `0` |
| Batch status | `passed` |
| Processed repositories | `1` |
| Failed repositories | `0` |
| Repository | `hyperprompt` |
| Repository status | `passed` |
| AI draft status | `warning` |
| AI draft selected members | `1` |
| AI draft errors | `0` |
| AI enrichment status | `completed` |
| AI-enriched preview status | `prepared` |

The AI draft sidecar still records the original repair path:

```text
ai_json_repair_needed
ai_json_repair_exhausted
package_set_subject_metadata_missing
single_package_deterministic_fallback_applied
```

`ai_json_repair_exhausted` remains visible, but it is warning-level with
`nonBlockingReason: deterministic_single_package_fallback`.

## Boundary

This repair does not make malformed AI output acceptable in general:
multi-package malformed AI draft output remains a hard failure, as do cases
where the producer cannot recover exactly one deterministic package subject.

P51-T6 does not accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, persist raw prompts, raw provider responses,
secrets, or chain-of-thought, or treat fallback output as registry truth.
No package acceptance or relation acceptance happens in this task.
No registry truth changes are made by this repair.

## Next State

P51-T7 can triage larger curated corpus outputs with Hyperprompt classified as
author-reviewable producer evidence carrying a non-blocking single-package
fallback warning, instead of carrying the previous `hyperprompt.aiDraft` hard
blocker forward.
