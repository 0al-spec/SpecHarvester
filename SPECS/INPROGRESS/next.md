# Next Task: P51-T6 Hyperprompt AI Draft Single-Package Fallback

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T6`
**Last Archived:** `P51-T5` Larger Curated Corpus AI-Enabled Proposal-Only Gate
**Depends On:** `P51-T5` Larger Curated Corpus AI-Enabled Proposal-Only Gate

## Goal

Repair the reproducible `hyperprompt.aiDraft` failure exposed by P51-T5 and
confirmed by the targeted Hyperprompt rerun. The repair must keep AI output
proposal-only while allowing a single-package workspace to produce
author-reviewable package-set evidence when deterministic inventory already
contains exactly one package subject.

## Context

P51-T5 processed all 12 larger curated corpus repositories. The batch evidence
capture completed, but the AI-enabled gate failed because `hyperprompt.aiDraft`
exhausted one JSON repair attempt and emitted:

```text
ai_json_repair_exhausted
ai_json_repair_needed
package_set_subject_metadata_missing
```

A targeted rerun of only `hyperprompt` reproduced the same failure:

```text
run root: /tmp/specharvester-p51-t5-hyperprompt-rerun-20260625T130432Z
exit code: 1
repository status: failed
aiDraft: failed
aiEnrichment: completed
aiEnrichedPreview: prepared
```

The targeted rerun showed that the static path, preflight, interface index,
AI enrichment, and AI-enriched preview are not the blocker. The blocker is the
package-set AI draft JSON contract for a single-package workspace when the
local model response remains malformed after bounded repair.

## Scope

- Add a deterministic producer-side fallback for failed AI draft JSON output
  when the workspace inventory has exactly one package subject and the request
  package-set identity is recoverable.
- Keep the fallback explicitly proposal-only and author-review evidence only.
- Preserve diagnostics that explain the AI draft JSON repair failure.
- Ensure the fallback does not hide malformed AI output for multi-package
  workspaces.
- Add focused tests for the single-package exhausted-repair fallback and the
  multi-package failure boundary.
- Run a targeted `hyperprompt` AI-enabled rerun with LM Studio to verify the
  fix against the reproduced blocker.

## Boundaries

- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, AI output, AI-enriched preview output, repair
  output, rerun output, planning output, or adapter output as registry truth.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets.
- Do not persist chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.

## Expected Follow-Up

If P51-T6 verifies the repair, P51-T7 should triage the larger curated corpus
outputs with Hyperprompt classified from repaired targeted evidence rather than
from the previous hard blocker.
