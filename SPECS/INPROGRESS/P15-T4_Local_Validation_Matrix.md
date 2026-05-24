# P15-T4 Local Validation Matrix

Status: Planned
Task: `P15-T4`
Phase: Phase 15. Real Repository Refinement Validation
Priority: P1
Effort: 4-8 hours
Dependencies: `P15-T1`, `P15-T2`, `P15-T3`, `P15-T6`

## Problem

The real-repository validation plan, local runner, and structured quality
report now exist, but they have not been exercised as a representative matrix
against different local repository shapes.  Operators need a compact, committed
summary of what happens when the flow is run on real checkout directories
without committing generated candidates or raw harvested outputs.

## Goals

- Run the local real-repository validation flow against a small representative
  set of operator-supplied public checkout paths under `~/Development/GitHub`.
- Cover several repository shapes, targeting Swift/SPM, JavaScript/TypeScript,
  Python, documentation-first, and mixed-language where available locally.
- Produce only compact triage summaries and failure classes in committed docs.
- Keep `.smoke/inputs`, `.smoke/output`, generated candidates, raw prompts,
  provider transcripts, and model outputs uncommitted.
- Convert repeated or structural failures into follow-up Workplan items only
  when they are actionable and not already covered by existing tasks.

## Non-Goals

- Do not clone new repositories or contact package registries as part of the
  validation run.
- Do not run harvested repository tests, package scripts, builds, dependency
  installers, or package managers.
- Do not implement SpecNode runtime or invoke a live model provider.
- Do not treat generated candidates as accepted SpecPM registry truth.
- Do not commit generated `.smoke/` artifacts or local machine-specific input
  manifests.

## Deliverables

1. A committed GitHub documentation page with the local validation matrix
   summary, selected repository shapes, command pattern, compact outcomes, and
   failure classes.
2. A DocC mirror page linked from the DocC root/workflow topics.
3. Docs contract coverage that prevents the matrix summary from disappearing
   from the GitHub docs and DocC navigation.
4. `SPECS/INPROGRESS/P15-T4_Validation_Report.md` recording validation commands
   and local matrix run outcomes.

## Execution Approach

1. Inspect local checkout candidates under `~/Development/GitHub`.
2. Build an untracked `.smoke/inputs/p15-t4-local-validation.yml` manifest with
   public repository URLs, local checkout paths, pinned local `HEAD` revisions,
   and package IDs.
3. Run `scripts/run_real_repository_validation.py` with:
   - `--inputs .smoke/inputs`
   - `--out .smoke/output/p15-t4-local-validation`
   - `--emit-interface-indexes`
   - `--analyzer-cache-dir .smoke/output/p15-t4-analyzer-cache`
   - `--skip-specpm-validation` when local SpecPM CLI availability would
     otherwise dominate matrix results
4. Run `python -m spec_harvester quality-report` against the generated
   `run-report.json`.
5. Summarize only compact counts, status, failure classes, and review notes in
   committed docs.

## Acceptance Criteria

- At least four local checkout entries are attempted, or the validation report
  explains why fewer were available.
- Matrix coverage includes at least three distinct repository shapes.
- The committed summary records selected repository IDs, ecosystem/shape,
  runner status, quality verdict, and failure class.
- Generated `.smoke/` inputs and outputs remain uncommitted.
- Quality gates from `.flow/params.yaml` are run or explicitly scoped with
  rationale in the validation report.
