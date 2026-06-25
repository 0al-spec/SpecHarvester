# Next Task: P51-T1 Larger Curated Corpus Planning Phase

**Status:** Selected
**Branch:** `feature/P51-T1-larger-curated-corpus-planning-phase`
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T1`
**Last Archived:** `P50-T1` Record Restored-Checkout Rerun Evidence
**Depends On:** `P50-T1` Record Restored-Checkout Rerun Evidence

## Goal

Plan the larger curated corpus phase from the P50 restored-checkout rerun
evidence.

## Context

P50-T1 selected:

```text
larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun
```

That decision means the previous operator-local checkout blocker is resolved:
the same six P46 repositories passed both the static-only and AI-enabled gates
after the manifest-expected checkout paths were restored through symlinks.

Planning readiness is not execution approval. The next phase must define the
curated source-selection rules, checkout requirements, gate order, warning
policy, triage criteria, and exit decision before any larger corpus run.

## Scope

- Add a durable Phase 51 planning artifact backed by P50 evidence.
- Define follow-up tasks for source manifest authoring, readiness, static-only
  gate, AI-enabled gate, triage, and exit decision.
- Preserve remaining warning/caveat evidence from P50.
- Keep no-authority and no-execution boundaries explicit.

## Expected Deliverables

- Workplan Phase 51 roadmap.
- Larger curated corpus planning fixture.
- GitHub and DocC documentation.
- Focused docs-contract tests.
- Validation report and archive artifacts for P51-T1.

## Boundaries

- Do not run a larger corpus batch in P51-T1.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, static output, rerun output, planning output, or
  adapter output as registry truth.

## Validation Expectations

- Validate the durable JSON fixture with `python3 -m json.tool`.
- Run focused docs-contract tests for P51-T1 and current next task.
- Run formatting, lint, coverage, Swift manifest, Swift docs build, and
  whitespace checks as required by Flow.
