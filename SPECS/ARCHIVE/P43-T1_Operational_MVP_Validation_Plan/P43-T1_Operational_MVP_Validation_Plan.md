# P43-T1 Operational MVP Validation Plan

## Status

Planned.

## Motivation

SpecHarvester now has profile selection, repository plugin applicability,
adapter contracts, no-execution trusted local adapter readiness, and sandbox
review boundaries. Those layers make future execution safer, but they do not
answer the product question on their own:

```text
Can an author point SpecHarvester at a real popular repository and receive a
valid, personalized starter SpecPackage/package-set that is worth reviewing?
```

Phase 43 answers that question before expanding autonomous scraping or enabling
real local adapter execution.

## Goal

Define the operational MVP validation loop for a bounded pinned real-repository
corpus. The loop must compare static-only and AI-enabled output quality, record
author-ready quality signals, and decide whether the current pipeline is ready
for bounded autonomous popular-library scraping.

## Deliverables

- GitHub documentation page:
  `docs/OPERATIONAL_MVP_VALIDATION_PLAN.md`.
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/OperationalMVPValidationPlan.md`.
- Workplan Phase 43 task stack.
- Roadmap section for Phase 43.
- Documentation index links.
- Docs-contract regression coverage proving the plan is linked and the next
  task points to P43-T2 after archive.
- Validation report for this task.

## Operational Validation Model

The validation loop is intentionally bounded:

```text
pinned local checkout
  -> static-only draft/package-set run
  -> optional AI-enabled proposal run
  -> quality report
  -> author handoff summary
  -> SpecPM handoff readiness decision
```

## Corpus Strategy

P43 should use operator-provided pinned local checkouts. It must not fetch or
clone repositories implicitly.

Target coverage:

- JS/TS monorepo or package-set repository, such as `xyflow`.
- Python library/framework, such as `FastAPI` or `FastMCP`.
- Go library/framework, such as `gin`.
- One additional ecosystem when a pinned local checkout exists.

Each corpus item should record:

- repository URL;
- local checkout path;
- exact revision;
- ecosystem/language family;
- expected package-family shape;
- run modes allowed;
- known stop conditions.

## Quality Dimensions

Operational MVP validation should measure:

- `validity`: generated artifacts validate and pass preflight.
- `repositorySpecificity`: summaries, intent, capabilities, and evidence are
  specific to the repository rather than generic package labels.
- `evidencePrecision`: public API evidence is not dominated by docs/examples,
  tests, generated files, or internal tooling.
- `packageTopology`: package-set/member structure is useful for monorepos and
  does not collapse scoped members into one broad package.
- `claimConservatism`: claims remain supported by observed evidence.
- `authorActionability`: an author can see what to keep, revise, reject, or
  enrich.
- `SpecPMHandoffReadiness`: output is ready for reviewable handoff, not
  necessarily accepted registry publication.

## Stop Policy

The phase should stop and record a blocker when:

- a required local checkout is missing or not pinned;
- required generated artifacts cannot be produced;
- validation or preflight fails;
- AI-enabled output attempts to become authority rather than proposal evidence;
- evidence over-capture makes the package unusable as a starter draft;
- the output would require real adapter execution, which remains disabled.

## Non-Authority Boundary

P43 artifacts remain producer-side operational evidence. They do not:

- accept packages;
- accept relations;
- seed baselines;
- publish registry metadata;
- remove `preview_only`;
- treat AI output as registry truth;
- treat adapter output as registry truth;
- enable trusted local adapter execution.

## Acceptance Criteria

- The plan defines the corpus strategy, run modes, quality dimensions, stop
  policy, and non-authority boundary.
- The Workplan lists P43-T1 through P43-T7.
- GitHub docs and DocC both link the plan.
- `SPECS/INPROGRESS/next.md` advances to P43-T2 during archive.
- Docs-contract tests cover the plan links and next-task state.

## Validation Commands

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'operational_mvp_validation or current_next_task'`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
