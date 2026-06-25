# Larger Curated Corpus Planning Phase

Status: P51-T1 plan.

P51-T1 turns the P50 restored-checkout rerun result into the next bounded
planning phase. It does not run a larger corpus batch. It defines the order and
constraints for the tasks that must happen before a larger corpus can be
treated as ready to execute.

The durable fixture is:

```text
tests/fixtures/larger_curated_corpus_planning_phase/p51-t1-larger-curated-corpus-planning-phase.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.larger-curated-corpus-planning-phase/v0
kind: SpecHarvesterLargerCuratedCorpusPlanningPhase
authority: producer_larger_curated_corpus_planning_phase_only
```

## Source Evidence

P51-T1 is based on:

```text
tests/fixtures/restored_checkout_rerun_evidence/p50-t1-restored-checkout-rerun-evidence.example.json
```

P50-T1 selected:

```text
larger_corpus_planning_reconsideration_ready_after_restored_checkout_rerun
```

That means the previous operator-local checkout blocker is resolved and the
same six-repository static-only and AI-enabled gates passed. It means planning
can continue. It does not mean a larger corpus run is approved yet.

## Phase 51 Task Order

Phase 51 is intentionally split so the project cannot jump straight from P50
into unbounded harvesting.

| Task | Purpose | Runs batch |
| --- | --- | --- |
| `P51-T1` | Plan the larger curated corpus phase from P50 evidence. | no |
| `P51-T2` | Author the larger curated corpus source plan and manifest criteria. | no |
| `P51-T3` | Run the checkout readiness gate for the selected local checkouts. | no |
| `P51-T4` | Run the static-only gate. | yes |
| `P51-T5` | Run the AI-enabled proposal-only gate. | yes |
| `P51-T6` | Triage selected, deferred, and do-not-promote output. | no |
| `P51-T7` | Record the exit decision before any further expansion. | no |

The gate order is:

```text
source plan -> readiness -> static-only -> AI-enabled -> triage -> exit decision
```

Static-only evidence must come before AI-enabled evidence.

## Curated Corpus Constraints

The larger corpus remains curated and bounded:

- operator-selected sources only;
- pinned local checkouts required;
- no registry search crawl;
- ecosystem diversity across Python, Go, Swift, JavaScript/TypeScript, and
  documentation-heavy repositories;
- repository-shape diversity across single-package, workspace/monorepo,
  documentation-heavy, framework/runtime library, and tooling/adapter-like
  projects;
- explicit importance signals, repository shape, expected package subject,
  pinned revision, local checkout path, and deferral reason when applicable.

P51-T1 does not choose the final larger corpus. P51-T2 must author the source
plan and manifest criteria before readiness can be checked.

## Carried-Forward Caveats

P51 keeps the P50 warnings and caveats visible:

- Flask: `excluded_package_also_selected`,
  `selected_member_role_unknown`, `refined_summary_missing`.
- Gin: `selected_member_role_unknown`.
- xyflow: `partial_public_interface_index`,
  `operator_checkout_origin_fork_mismatch`, `refined_summary_missing`.
- Cupertino: `excluded_package_also_selected`,
  `selected_member_role_unknown`.
- NavigationSplitView: `selected_member_role_unknown`,
  `ai_json_repair_needed`.
- docc2context: `excluded_package_also_selected`,
  `selected_member_role_unknown`.

These caveats must be triaged before a P51 exit decision can approve further
expansion.

## Current Decision

P51-T1 starts the planning phase and selects `P51-T2` as the next task:

```text
Author the larger curated corpus source plan and manifest criteria
```

The larger curated corpus is not execution-ready after P51-T1.

## Boundary

P51-T1 does not run a larger corpus batch, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, run adapters,
enable trusted local adapter execution, run AI, persist raw prompts, persist
raw provider responses, persist secrets, or persist chain-of-thought.

P51-T1 does not accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, or treat AI output, static output, rerun
output, planning output, or adapter output as registry truth.
