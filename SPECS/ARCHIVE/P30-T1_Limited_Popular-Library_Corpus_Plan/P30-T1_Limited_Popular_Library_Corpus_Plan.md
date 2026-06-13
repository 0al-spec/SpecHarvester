# P30-T1 Limited Popular-Library Corpus Plan

## Objective

Define the first limited popular-library scraping batch after P29 without
running a broad scrape yet.

The task should turn the P29 verdict
`ready_for_limited_popular_library_scraping` into an operator-reviewed corpus
plan, source-manifest example, runbook, and non-authority policy that later
tasks can execute.

## Background

P29 proved the autonomous candidate MVP on Flask, Gin, and xyflow:

- single-package repositories can now produce preview candidates through the
  deterministic fallback;
- package-set repositories can retain workspace/member topology;
- live LM Studio/OpenAI-compatible generation has bounded JSON repair/retry;
- all generated output remains `producer_preview_evidence_only`.

The next risk is unbounded scope. A larger scrape must not turn SpecHarvester
into a framework encyclopedia, a crawler, or a registry acceptance authority.
P30-T1 is therefore a planning and contract task before P30-T2 runs the
deterministic batch.

## Deliverables

- Add a GitHub docs page describing:
  - limited corpus selection criteria;
  - seed repository set;
  - source-manifest example;
  - deterministic and live run commands;
  - cost/time/concurrency limits;
  - triage states and stop policy;
  - non-authority boundaries.
- Add a DocC mirror for the same operator contract.
- Add a committed example source manifest for the limited corpus.
- Update docs index, DocC root, roadmap, Workplan, and `next.md`.
- Add regression tests proving the docs, manifest, and Flow pointers stay
  aligned.

## Candidate Seed Corpus

The initial limited batch should be small and mixed:

| Repository | Shape | Package id hint |
| --- | --- | --- |
| Flask | Python single-package framework | `flask.core` |
| Gin | Go single-package framework | `gin.core` |
| xyflow | JavaScript/TypeScript package-set workspace | `xyflow.workspace` |
| Cupertino | Swift/SPM app/library-style checkout | `cupertino.core` |
| NavigationSplitView | Swift/SPM + Xcode project checkout | `navigation_split_view.core` |
| docc2context | Swift/SPM documentation-first CLI | `docc2context.core` |

P30-T1 may include this as an example manifest. P30-T2 must verify which local
checkouts are present and at expected revisions before running.

## Acceptance Criteria

- The plan explicitly says the limited batch reads only operator-provided local
  public checkouts.
- The source manifest example uses existing `inputs/*.yml` shape and includes
  repository id, repository URL, pinned revision or ref, checkout path, and
  package id hint.
- The plan distinguishes seed corpus membership from registry acceptance.
- The plan defines stop conditions for:
  - missing checkout;
  - dirty checkout;
  - revision mismatch;
  - deterministic preflight failure;
  - live provider unavailable;
  - AI proposal diagnostics that require regeneration.
- The plan names expected outputs for P30-T2/P30-T3/P30-T4/P30-T5.
- Docs contract tests cover the new page, manifest, roadmap, Workplan, and
  `next.md`.

## Non-Goals

- No broad scrape in this task.
- No cloning, fetching, dependency installation, package script execution, or
  arbitrary network browsing.
- No live LM Studio call in this task.
- No SpecPM registry update, package acceptance, relation acceptance, baseline
  seeding, or `preview_only` removal.
- No claim that generated specs are final.
