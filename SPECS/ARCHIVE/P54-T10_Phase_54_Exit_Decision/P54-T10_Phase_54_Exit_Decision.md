# P54-T10 Phase 54 Exit Decision

## Objective

Record a deterministic, digest-bound Phase 54 exit decision from the completed
Local Candidate Review Workbench implementation and P54-T9 end-to-end evidence.
Choose exactly one outcome and state what it authorizes without granting
publication or registry authority.

## Decision Options

1. Stop Phase 54 without authorizing Workbench use.
2. Run a bounded Workbench follow-up before maintainer use.
3. Authorize maintainer use of the local Workbench.
4. Plan a separate publication phase.

## Planned Decision

Select `authorize_local_maintainer_workbench_use`. P54-T9 accounts for all 100
portable candidates and four exact 25-candidate waves, validates review
decisions and restart-safe exchange, contains hostile content, rejects bounded
integrity failures, and passes one read-only SpecPM preflight with zero registry
mutations.

The same decision authorizes the separately planned Phase 55 bounded
evidence-grounded semantic-authoring follow-up. It does not turn model output,
reviewer decisions, or SpecPM preflight into accepted registry truth.

## Deliverables

- A machine-readable exit-decision fixture bound by path and SHA-256 to the
  P54-T9 E2E report and the P53-T14 portable source archive.
- Contract tests for decision identity, evidence digests, corpus metrics,
  Workbench authorization, Phase 55 authorization, privacy, and non-authority
  boundaries.
- A maintainer-facing decision document and validation report.
- Updated Workplan and next-task state completing Phase 54 and selecting P55-T1
  only after P54-T10 is archived.

## Acceptance Criteria

- The decision records `authorize_local_maintainer_workbench_use`.
- All 100 candidates, 100 archive packets, 100 detail records, 100 comparisons,
  and the `25/25/25/25` wave distribution remain represented.
- Restart hydration, portable exchange, hostile-content containment,
  Origin/CSRF checks, binding checks, interrupted-write rollback, and read-only
  SpecPM preflight remain passing evidence.
- Maintainers may inspect candidates, record or replace bounded dispositions,
  exchange decision evidence, and invoke read-only SpecPM preflight for an
  explicitly approved candidate.
- Phase 55 may begin as a proposal-only semantic-authoring follow-up with Codex
  5.3 Spark as primary worker and LM Studio as comparison provider.
- Automatic acceptance, registry mutation, publication, remote multi-user
  service, broader corpus execution, and canonical intent creation remain
  unauthorized.
- Raw prompts, raw responses, hidden reasoning, credentials, and private
  machine paths remain unpersisted.

## Execution Boundary

This task consumes existing repository evidence only. It does not clone or
fetch repositories, rerun collection, invoke Codex or LM Studio, install
dependencies, execute harvested code, run adapters, mutate SpecPM, accept
packages or relations, or publish registry metadata.

## Validation

- Focused decision and documentation contracts.
- Full Python test and coverage gates at 90% or higher.
- Ruff lint and format checks.
- `git diff --check`.
- Swift package manifest and documentation target build.
