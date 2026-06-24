# P49-T1 Plan docc2context AI Draft Targeted Follow-Up Pass

## Objective

Plan the targeted follow-up pass selected by P48-T4 for the remaining
`docc2context.aiDraft` blocker before any larger curated corpus planning.

P49-T1 is planning-only. It must not run AI, run another bounded rerun, mutate
registry truth, or accept generated package output.

## Inputs

- `SPECS/INPROGRESS/next.md`
- `SPECS/Workplan.md`
- `tests/fixtures/post_blocker_follow_up_exit_decision/p48-t4-post-blocker-follow-up-exit-decision.example.json`
- `docs/POST_BLOCKER_FOLLOW_UP_EXIT_DECISION.md`
- `Sources/SpecHarvester/Documentation.docc/PostBlockerFollowUpExitDecision.md`

## Problem Statement

P48-T3 showed that the same six-repository static-only gate passed, but the
AI-enabled gate failed on `docc2context.aiDraft` with:

- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

P48-T4 selected:

```text
run_docc2context_ai_draft_targeted_pass_before_larger_curated_corpus
```

The P49-T1 plan must translate that exit decision into concrete requirements
for P49-T2 and P49-T3.

## Deliverables

- Machine-readable P49-T1 targeted follow-up plan fixture.
- GitHub documentation page for the plan.
- DocC documentation page for the plan.
- Cross-links from docs indexes, capabilities, roadmap, and DocC topics.
- Current `next.md` advanced to P49-T2.
- Workplan updated to mark P49-T1 complete.
- Focused docs-contract test coverage for the new fixture, docs, current
  `next.md`, and authority boundaries.
- Validation report and archived Flow artifacts.

## Plan Requirements

The P49-T1 plan must require P49-T2 to:

- target only `docc2context.aiDraft`;
- preserve the same six-repository bounded pilot scope for the later P49-T3
  rerun;
- constrain AI draft subject/member metadata so the proposal cannot omit
  `docc2context.core`;
- record a disposition for `ai_json_repair_exhausted`;
- preserve proposal-only AI output;
- preserve no raw prompt, raw provider response, secrets, or chain-of-thought
  persistence;
- keep P48-T3/P48-T4 warning and caveat IDs visible unchanged.

The P49-T1 plan must require P49-T3 to rerun the same six-repository bounded
gate with static-only evidence before AI-enabled evidence.

## Acceptance Criteria

- The fixture references the P48-T4 fixture by path, digest, `apiVersion`,
  `kind`, and `authority`.
- The fixture records P48-T4's selected outcome and blocker evidence.
- The fixture defines explicit P49-T2 success criteria for clearing or
  explicitly disposing `docc2context.aiDraft`.
- The fixture defines explicit P49-T3 rerun preconditions.
- Larger curated corpus approval remains blocked.
- All non-authority boundaries remain explicit: no package acceptance, no
  relation acceptance, no registry publication, no baseline seeding, no raw
  prompt/response/chain-of-thought persistence, and no AI output as registry
  truth.
- Focused tests and project gates pass.

## Non-Goals

- Do not execute the targeted pass in P49-T1.
- Do not run another static or AI-enabled bounded rerun in P49-T1.
- Do not approve a larger curated corpus.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone/fetch repositories, install dependencies, invoke package
  managers, or execute harvested code.
