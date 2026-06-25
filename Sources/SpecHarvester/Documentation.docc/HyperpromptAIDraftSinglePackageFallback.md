# Hyperprompt AI Draft Single-Package Fallback

Status: P51-T6 targeted repair evidence.

P51-T6 repairs the reproducible `hyperprompt.aiDraft` blocker found by the
P51-T5 larger curated corpus AI-enabled gate. The local model response still
exhausts bounded JSON repair, but deterministic single-package request context
now allows SpecHarvester to produce proposal-only fallback evidence for
`hyperprompt.core`.

The repair is narrow: it applies only when the workspace inventory has exactly
one package subject and the package-set identity is recoverable.
multi-package malformed AI draft output remains a hard failure.

## Fixture

```text
tests/fixtures/hyperprompt_ai_draft_single_package_fallback/p51-t6-hyperprompt-ai-draft-single-package-fallback.example.json
```

## Result

| Field | Value |
| --- | --- |
| Exit code | `0` |
| Batch status | `passed` |
| Repository | `hyperprompt` |
| Repository status | `passed` |
| AI draft status | `warning` |
| Selected members | `1` |
| AI draft errors | `0` |
| Stop policy | `stop_for_author_review` |

The sidecar preserves these warning diagnostics:

```text
ai_json_repair_needed
ai_json_repair_exhausted
package_set_subject_metadata_missing
single_package_deterministic_fallback_applied
```

The non-blocking reason is `deterministic_single_package_fallback`.

No registry truth changes, package acceptance, relation acceptance, raw prompt
persistence, raw provider response persistence, secrets, or chain-of-thought
persistence are introduced.
No package acceptance or relation acceptance happens in this task.

P51-T7 can now triage the larger curated corpus with Hyperprompt treated as
author-reviewable producer evidence carrying a non-blocking fallback warning.
