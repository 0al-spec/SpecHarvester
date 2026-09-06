# P56-T5 Side-by-Side Package Review

Status: Complete (comparison preparation only)
Date: 2026-09-06
Dependencies: P56-T4, P56-T3A

## Objective

Prepare a local offline comparison of all five preserved v2 originals against
pinned README, complete retained candidate sets and separate semantic proposals.
Reuse the existing static spec renderer; no new review application or AI run.

## Deliverables

- Bounded build command verifies T4 report/archive/file digests and frozen
  baseline selection before rendering. Refuse unsafe paths or output overwrite.
- Small static comparison index, new rendered package on the left and reference
  navigation on the right; responsive layout, no remote resources or source
  execution. Retained monorepo members all remain reachable, not just one chosen
  principal member. Original YAML/evidence downloads remain byte-identical.
- Clearly label producer/model, pin, scope, rejected proposal, baseline
  mismatches, warning counts and original evidence-fidelity defects.
- Human review remains pending; supply separate per-surface questions/lookup
  fields for T6 without generated answers or cross-surface score transfer.
- Tests for complete accounting, bytes and digest/path failures; desktop/mobile
  browser checks with screenshots; full FLOW validation and PR.

## Non-Goals

No original correction, new authoring, registry writes, acceptance, publication,
quality ranking, fair cost/model comparison, or human-review impersonation.
The deferred T3 and historical v1 protocol remain untouched. Preserve uv.lock.
