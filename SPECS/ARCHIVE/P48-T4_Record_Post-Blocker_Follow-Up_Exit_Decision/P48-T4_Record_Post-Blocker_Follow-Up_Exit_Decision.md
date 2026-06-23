# P48-T4 Record Post-Blocker Follow-Up Exit Decision

## Objective

Record the Phase 48 exit decision after the P48-T3 same-scope bounded rerun
gate, deciding what to do with the remaining `docc2context.aiDraft` blocker
before any larger curated corpus planning.

## Inputs

- `SPECS/INPROGRESS/next.md`
- `SPECS/Workplan.md`
- `tests/fixtures/ai_draft_blocker_bounded_rerun_gate/p48-t3-ai-draft-blocker-bounded-rerun-gate.example.json`
- `docs/AI_DRAFT_BLOCKER_BOUNDED_RERUN_GATE.md`
- `Sources/SpecHarvester/Documentation.docc/AIDraftBlockerBoundedRerunGate.md`

## Decision Scope

P48-T4 must choose one explicit outcome:

- proceed to larger curated corpus;
- run another targeted pass;
- stop larger corpus planning.

Because P48-T3 still has a hard `docc2context.aiDraft` blocker, proceeding is
only acceptable if P48-T4 explicitly downgrades or accepts that blocker as a
non-blocking pilot caveat. Otherwise the safe outcome is another targeted pass
or stop.

## Deliverables

- Machine-readable P48-T4 exit decision fixture.
- GitHub documentation page for the decision.
- DocC documentation page for the decision.
- Cross-links from docs indexes, capabilities, roadmap, and DocC topics.
- Current `next.md` advanced to the selected follow-up.
- Workplan updated to mark P48-T4 complete and add/confirm the follow-up task.
- Focused docs-contract test coverage for the new fixture, docs, current
  `next.md`, and authority boundaries.
- Validation report and archived Flow artifacts.

## Acceptance Criteria

- The decision fixture references the P48-T3 fixture by path, digest,
  `apiVersion`, `kind`, and `authority`.
- The decision records P48-T3 facts: static gate passed, AI gate failed,
  `docc2context.aiDraft` remains blocking, `gin.aiDraft` and
  `navigation-split-view.aiDraft` are warning-level, and xyflow caveats remain
  visible.
- The selected outcome is explicit and defensible from the evidence.
- Larger curated corpus approval is not implied by a failed AI-enabled gate.
- All non-authority boundaries remain explicit: no package acceptance, no
  relation acceptance, no registry publication, no baseline seeding, no raw
  prompt/response/chain-of-thought persistence, and no AI output as registry
  truth.
- Focused tests and project gates pass.

## Non-Goals

- Do not run another AI-enabled bounded rerun in P48-T4.
- Do not repair `docc2context.aiDraft` in P48-T4.
- Do not approve or execute a larger curated corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone/fetch repositories, install dependencies, invoke package
  managers, or execute harvested code.
