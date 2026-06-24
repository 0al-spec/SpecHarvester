# P49-T4 Record docc2context Follow-Up Exit Decision

## Objective

Record the Phase 49 exit decision after P49-T3 documented that the same-scope
bounded rerun gate is blocked by missing operator-local checkouts.

The decision must preserve the P49 no-clone/no-fetch boundary and must not
infer larger curated corpus readiness from a gate that did not reach static-only
or AI-enabled execution.

## Inputs

- `SPECS/INPROGRESS/next.md`
- `SPECS/Workplan.md`
- `tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/p49-t3-docc2context-ai-draft-same-scope-bounded-rerun-gate.example.json`
- `docs/DOCC2CONTEXT_AI_DRAFT_SAME_SCOPE_BOUNDED_RERUN_GATE.md`
- `Sources/SpecHarvester/Documentation.docc/Docc2contextAIDraftSameScopeBoundedRerunGate.md`

## Decision Scope

P49-T4 must choose one explicit outcome:

- stop Phase 49 on the operator-local checkout blocker;
- request a P49-T3 rerun after the six operator-local checkouts are restored;
- record no larger curated corpus readiness.

Because P49-T3 did not run the static-only gate or the AI-enabled gate, P49-T4
must not approve larger curated corpus planning. The safe selected outcome is
to record no larger corpus readiness and require a same-scope P49-T3 rerun if
the operator wants to reconsider readiness later.

## Deliverables

- Machine-readable P49-T4 exit decision fixture.
- GitHub documentation page for the decision.
- DocC documentation page for the decision.
- Cross-links from docs indexes, capabilities, roadmap, and DocC topics.
- Current `next.md` advanced to the selected follow-up state.
- Workplan updated to mark P49-T4 complete.
- Focused docs-contract test coverage for the new fixture, docs, current
  `next.md`, and authority boundaries.
- Validation report and archived Flow artifacts.

## Acceptance Criteria

- The decision fixture references the P49-T3 fixture by path, digest,
  `apiVersion`, `kind`, and `authority`.
- The decision records P49-T3 facts: six repository IDs, all six checkouts
  missing, static-only gate not run, AI-enabled gate not run, LM Studio
  available but not reached, and proposal-only boundaries preserved.
- The selected outcome explicitly records no larger curated corpus readiness.
- The decision requires restoring the same six operator-local checkouts before
  any P49-T3 rerun can reconsider readiness.
- P49-T2 warning IDs and P49-T3 xyflow caveats remain visible unchanged.
- All non-authority boundaries remain explicit: no package acceptance, no
  relation acceptance, no registry publication, no baseline seeding, no raw
  prompt/response/chain-of-thought persistence, and no exit-decision output as
  registry truth.
- Focused tests and project gates pass.

## Non-Goals

- Do not run another bounded rerun in P49-T4.
- Do not run AI.
- Do not approve or execute a larger curated corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone/fetch repositories, install dependencies, invoke package
  managers, or execute harvested code.
