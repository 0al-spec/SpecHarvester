# Next Task: P29-T2 SpecPM Candidate-Layer Intake Policy

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P29-T2 SpecPM Candidate-Layer Intake Policy
**Phase:** Phase 29. Autonomous Candidate Harvest MVP
**Last Archived:** P29-T1 Autonomous Candidate Batch Runner

## Recently Archived

- Prior completed boundary: `P28-T5 First-Submission or Seeded-Baseline
  Workflow`.
- Prior role-profile boundary: `P28-T4 Package-Set Role Selection Profiles`.
- Prior refresh context: `P28-T2` ran real `xyflow`, and the later
  TanStack/query refresh at `feb1efd804c1262106f72c8adc1d82a8ce9cfbb0`
  established `no_contract_delta` handling before seeded-baseline intake.
- `P29-T1` added `autonomous-candidate-batch`, an MVP runner over repository
  source manifests and local public checkouts. It orchestrates deterministic
  collection, workspace inventory, public interface indexes, package-set draft,
  bundle-set preflight, optional local LM Studio AI draft/enrichment proposals,
  and `SpecHarvesterAutonomousCandidateBatchReport`.
- The default autonomous role profile is `autonomous_popular_mvp`, selecting
  workspace, `core_runtime`, React/Svelte binding, and generic member package
  roles while excluding examples, tests, fixtures, and private tooling from
  primary candidate output.
- Live LM Studio smoke with `openai/gpt-oss-20b` passed on a local fixture:
  `3` candidates, `2` relations, preflight `passed`, AI draft `completed`, and
  AI enrichment `completed`.
- Real `xyflow` smoke at `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` passed
  with 4 candidates, 3 relations, preflight `passed`, and
  `authorReadyDraftSummary.decision: stop_for_author_review`.
- Follow-up corpus check over local Flask, Gin, and xyflow found two concrete
  technical-debt items now captured in
  `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`: Flask and Gin collect public
  evidence but produce `0` package candidates without a single-package
  fallback, and live LM Studio output can still need bounded JSON repair/retry
  when the model returns malformed JSON.

## Outcome

SpecHarvester now has an operator-facing MVP for autonomous popular-library
scraping into reviewable SpecPM preview artifacts. The runner does not clone
repositories, execute harvested code, install dependencies, publish registry
metadata, accept packages, or remove `preview_only`.

## Next Step

Implement `P29-T2`: define the SpecPM-facing candidate-layer intake policy for
autonomous batch output.

The policy should explain how `SpecHarvesterAutonomousCandidateBatchReport`,
package-set preview bundles, AI draft/enrichment proposals, and author-ready
summaries can be reviewed by SpecPM maintainers without turning producer output
into registry authority.

After that policy boundary, the planned autonomous-runner technical-debt stack
is:

1. `P29-T3` corpus baseline and gap report.
2. `P29-T4` single-package candidate fallback.
3. `P29-T5` LM Studio JSON repair/retry.
4. `P29-T6` corpus quality gate after fallback and retry support.
