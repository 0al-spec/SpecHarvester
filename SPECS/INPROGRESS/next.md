# Next Task: P15-T1 Real-Repository Refinement Validation Plan

**Status:** Selected
**Workplan:** `SPECS/Workplan.md`

## Description

Add a reproducible real-repository refinement validation plan for running the
local `collect -> draft -> SpecNode refine -> semantic review -> retry` loop
against operator-supplied public repository checkouts without committing
generated candidate outputs or expanding the trust boundary.

## Scope

- Define repository selection rules and safe input manifest shape.
- Define exact command sequence and expected local artifacts.
- Define a quality scoring rubric for real-repository outputs.
- Define non-committed output policy for `.smoke/`, raw prompts, provider logs,
  generated candidates, and model chain-of-thought.
- Identify validation metrics that separate deterministic evidence gaps,
  SpecPM contract mismatches, and model interpretation failures.

## Next Step

Run the Flow SELECT step for `P15-T1`, then create the task PRD.
