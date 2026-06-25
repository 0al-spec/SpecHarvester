# P51-T1 Larger Curated Corpus Planning Phase

## Summary

Create the Phase 51 planning layer that turns P50-T1 restored-checkout rerun
evidence into a bounded, curated, gated roadmap for the next larger corpus
expansion.

This task does not run the larger corpus. It defines what must exist before
that run can be considered ready.

## Source Evidence

- P50-T1 restored the operator-local checkout paths expected by the P46
  manifest through symlinks.
- The same six-repository static-only rerun passed.
- The same six-repository AI-enabled rerun passed.
- P50-T1 selected
  `larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun`.
- Remaining warnings and xyflow caveats stayed visible as review evidence.

## Deliverables

- Add a durable `SpecHarvesterLargerCuratedCorpusPlanningPhase` fixture.
- Add GitHub and DocC documentation for the Phase 51 planning contract.
- Expand Workplan Phase 51 with follow-up tasks for:
  - curated source plan and manifest criteria;
  - local checkout readiness;
  - static-only gate;
  - AI-enabled proposal-only gate;
  - output triage;
  - exit decision.
- Update documentation indexes, roadmap, and capability map.
- Update `SPECS/INPROGRESS/next.md` so the next task after P51-T1 is the first
  executable follow-up task, not an immediate corpus run.
- Add focused docs-contract tests.
- Create a validation report and archive/review artifacts through Flow.

## Acceptance Criteria

- The plan fixture links back to P50-T1 evidence and records the P50 decision.
- The fixture defines a curated, bounded, pinned local-checkout corpus planning
  contract.
- The plan requires static-only-before-AI ordering for future gates.
- AI output remains proposal-only, with no raw prompt/response/CoT persistence.
- The follow-up tasks are explicit enough to prevent jumping from P50 directly
  into unbounded harvesting.
- Remaining P50 warnings and xyflow caveats stay visible as carried-forward
  review evidence.
- Documentation and DocC pages explain that this is planning readiness only.
- Tests cover fixture identity, source linkage, task ordering, gate ordering,
  boundaries, docs links, and current next-state.

## Non-Goals

- Do not run a larger corpus batch.
- Do not author the final larger corpus source manifest in P51-T1.
- Do not clone or fetch repositories.
- Do not install dependencies or invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, static output, rerun output, planning output, or
  adapter output as registry truth.

## Validation Plan

- Validate the JSON fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P51-T1 and current next task.
- Run repository Flow gates from `.flow/params.yaml`:
  - `PYTHONPATH=src python3 -m pytest`
  - `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - `python3 -m ruff format --check src tests`
  - `python3 -m ruff check src tests`
  - Swift manifest/docs checks
  - `git diff --check`
