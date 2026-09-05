# P56-T3 Bounded Investigative Authoring Runner

Status: In Progress
Priority: P0
Dependencies: P56-T1, P56-T2
Review subject: p56_t3_bounded_investigative_authoring_runner

## Objective

Execute the repository skill through caller-owned bounded source and output
operations, with independent SpecPM validation and fail-closed experimental
admission. Preserve the frozen T1 protocol and all original attempt results.

## Implementation Sequence

1. Implement and test the shared read/evidence budget, portable operation
   ledger, UTF-8 byte-range accounting, pinned input checks, and candidate sink.
2. Integrate an isolated worker transport with no direct source filesystem,
   evaluator, sibling, personal configuration, network, or shell access.
   Model transport is a separate trusted boundary; ordinary read-only Codex
   execution is not accepted as an isolation proof.
3. Enforce model-call deadlines, shared attempt/repair budgets, independent
   trusted validation, and normalized receipts without raw transport retention.
4. Demonstrate denial probes on the actual worker runtime and bounded current-arm
   execution; freeze the execution lock before any scored generation.

## Acceptance

- Read budgets match T1: 100 calls, 96 KiB unique source plus generated evidence,
  24 KiB per source file. Overlapping reads charge the union of actual returned
  byte ranges; every request, including denied requests, is observable.
- Source bytes are pinned and read-only. Traversal, links, special files,
  unlisted paths, and source drift fail closed before content is returned.
- All final candidate files together fit 256 KiB; output is separate, portable,
  newly created, and never overwrites original attempt output.
- One initial attempt, at most one eligible retry and one repair per attempt;
  300 seconds per call, 600 per attempt, 1,200 model seconds per unit. Missing
  usage is unknown, not zero.
- Runtime denial receipts and path-level input hashes are bound into the
  execution lock. Test doubles cannot authorize a scored run.
- Current-arm wrapping must preserve frozen semantics. Any required protocol
  amendment is explicit and precedes both arms, not an unreported adjustment.
- All required FLOW gates pass; preparation cannot imply empirical quality,
  human acceptance, publication authority, or P56-T4 readiness.

## Scope Boundary

No scored repository generation, benchmark answer changes, model substitution,
source execution, package installation, registry changes, or publication.
The independent Luna-medium Logrus smoke is not experimental evidence.

## Branch

Started atop unmerged P56-T2 (#371) to retain the skill dependency. Until that
PR is merged, the incremental PR base is its feature branch. User-owned
untracked uv.lock is excluded. No merge is inferred from task execution.
