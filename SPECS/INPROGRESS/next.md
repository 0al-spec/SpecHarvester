# Next Task: P51-T2 Larger Curated Corpus Source Plan and Manifest Criteria

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T2`
**Last Archived:** `P51-T1` Larger Curated Corpus Planning Phase
**Depends On:** `P51-T1` Larger Curated Corpus Planning Phase

## Goal

Author the larger curated corpus source plan and manifest criteria before any
readiness check or corpus run.

## Context

P51-T1 created the planning phase from P50 restored-checkout rerun evidence.
P50 showed that the previous operator-local checkout blocker is resolved and
that the same six-repository static-only and AI-enabled gates passed.

P51-T1 did not run a larger corpus batch and did not approve execution. It
defined the required sequence:

```text
source plan -> readiness -> static-only -> AI-enabled -> triage -> exit decision
```

## Scope

- Define the target larger corpus count bounds.
- Define required ecosystem and repository-shape coverage.
- Define source importance signals and exclusion rules.
- Define pinned revision and operator-local checkout path requirements.
- Define the manifest criteria that P51-T3 must check before any batch run.
- Carry P50 warnings and xyflow caveats forward as review evidence.

## Boundaries

- Do not run a larger corpus batch in P51-T2.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not treat AI output, static output, rerun output, planning output, or
  adapter output as registry truth.
