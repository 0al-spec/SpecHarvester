# P51-T6 Hyperprompt AI Draft Single-Package Fallback

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Depends On:** P51-T5 Larger Curated Corpus AI-Enabled Proposal-Only Gate

## Problem

P51-T5 exposed a reproducible `hyperprompt.aiDraft` hard blocker. The full
12-repository AI-enabled run failed, and a targeted rerun of only Hyperprompt
confirmed the same failure:

```text
ai_json_repair_needed
ai_json_repair_exhausted
package_set_subject_metadata_missing
```

The failure is narrower than a repository, checkout, static harvest, interface
index, or AI enrichment failure. Hyperprompt has one deterministic inventory
package (`hyperprompt.core`) and a recoverable package-set identity
(`hyperprompt.workspace`), but malformed model output prevents the package-set
AI draft sidecar from becoming author-reviewable evidence.

## Goal

Make failed AI draft JSON output non-blocking for deterministic single-package
workspaces when the producer can recover the package-set identity and the only
inventory package from deterministic inputs.

## Deliverables

- Add a deterministic fallback that builds a proposal-only package-set draft
  from the request when:
  - provider JSON repair is exhausted;
  - the request has exactly one inventory package;
  - package-set identity is recoverable;
  - the model output did not select, exclude, or relate unsupported subjects.
- Preserve the original repair diagnostics as warnings so the evidence remains
  transparent.
- Keep exhausted JSON repair as a hard failure for multi-package workspaces.
- Add unit tests for:
  - single-package exhausted repair becoming author-reviewable fallback evidence;
  - multi-package exhausted repair remaining failed.
- Run a targeted Hyperprompt AI-enabled rerun through LM Studio to verify the
  repair against the reproduced blocker.
- Record validation evidence and update docs/fixtures as needed.

## Acceptance Criteria

- `hyperprompt.aiDraft` no longer fails solely because malformed model output
  exhausted repair when deterministic single-package fallback conditions are
  satisfied.
- The resulting sidecar remains `proposal_only_not_registry_acceptance`.
- The sidecar records that JSON repair was exhausted and that fallback evidence
  was produced from deterministic request context.
- Multi-package malformed AI draft output still fails with
  `ai_json_repair_exhausted`.
- The targeted Hyperprompt rerun exits `0` or otherwise records a clear
  non-blocking disposition for the previous hard blocker.
- Raw prompts, raw provider responses, secrets, and chain-of-thought remain
  unpersisted.

## Boundaries

- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat repair output, AI output, or rerun output as registry truth.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.

## Follow-Up

If the repair verifies, P51-T7 should triage larger curated corpus output using
the repaired Hyperprompt evidence as author-reviewable producer evidence rather
than preserving the previous `hyperprompt.aiDraft` hard blocker.
