# P30-T2 Deterministic Limited Corpus Batch

## Objective

Run the deterministic `--skip-ai` autonomous candidate batch over the P30
limited popular-library corpus and record actual collection, candidate,
relation, preflight, and stop-policy outcomes.

The task validates the P30-T1 corpus plan before any live LM Studio or SpecPM
handoff work. It must preserve the producer-preview boundary.

## Background

P30-T1 defined the limited seed corpus in:

```text
inputs/limited-popular-libraries/repositories.yml
```

The seed corpus includes:

- `flask -> flask.core`
- `gin -> gin.core`
- `xyflow -> xyflow.workspace`
- `cupertino -> cupertino.core`
- `navigation-split-view -> navigation-split-view.core`
- `docc2context -> docc2context.core`

P30-T2 executes only the deterministic path. Live model execution remains
P30-T3.

## Deliverables

- Run:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out <run-root>/deterministic \
  --skip-ai
```

- Record source manifest preview and deterministic batch summary.
- Add a machine-readable fixture for the deterministic corpus outcome.
- Add GitHub docs and DocC coverage for the deterministic run.
- Update roadmap/workplan/next/archive/review artifacts.
- Add regression tests covering:
  - fixture identity and non-authority boundary;
  - expected repository ids and package ids;
  - candidate/relation/preflight/stop-policy summaries;
  - docs and Flow pointer alignment.

## Acceptance Criteria

- The manifest parser sees exactly the six P30 seed repositories.
- Deterministic batch output is recorded even if one repository is blocked.
- Every repository outcome includes collection status, candidate count,
  relation count, preflight status, and author-ready stop-policy decision.
- The fixture explicitly states:
  - `producer_preview_evidence_only`;
  - no AI execution;
  - no package acceptance;
  - no relation acceptance;
  - no baseline seeding;
  - no registry publication;
  - no `preview_only` removal.
- The product verdict says whether the limited corpus is ready for P30-T3 live
  LM Studio processing.

## Non-Goals

- No LM Studio or other provider call.
- No repository clone/fetch.
- No dependency installation, package manager execution, build, test, or
  package script execution inside harvested repositories.
- No SpecPM registry update or accepted-source proposal.
- No curation of generated package semantics.
