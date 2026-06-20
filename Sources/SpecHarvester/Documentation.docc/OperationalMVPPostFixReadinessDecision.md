# Operational MVP Post-Fix Readiness Decision

P45-T4 records the Phase 45 readiness decision after the bounded operational
MVP corpus rerun from P45-T3.

Machine-readable evidence:

```text
tests/fixtures/operational_mvp_quality_hardening/p45-t4-operational-mvp-post-fix-readiness-decision.example.json
```

Identity:

```yaml
apiVersion: spec-harvester.operational-mvp-post-fix-readiness-decision/v0
kind: SpecHarvesterOperationalMVPPostFixReadinessDecision
authority: producer_operational_mvp_post_fix_readiness_decision_only
```

## Decision

Selected state:

```text
needs_targeted_ai_draft_quality_pass_before_bounded_popular_library_scraping
```

Rejected states:

- `ready_for_bounded_popular_library_scraping`
- `blocked_until_adapter_execution`
- `proceed_after_identity_fix_only`

P45-T3 resolves the old `package_set_id_missing` and
`excluded_package_unknown` identity-warning class across xyflow, FastAPI, and
Gin. It does not make the AI draft layer fully clean: xyflow now reports
`selected_member_role_unknown`, while FastAPI and Gin have no diagnostics but
still stop with `no_proposal_subjects`.

## Evidence Comparison

| Signal | P44-T5 / P44-T4 | P45-T4 / P45-T3 |
| --- | --- | --- |
| Readiness decision | `needs_another_quality_pass` | `needs_targeted_ai_draft_quality_pass_before_bounded_popular_library_scraping` |
| Same pinned corpus | yes | yes |
| Static-only baseline | passed | still matches P44 |
| AI-enabled run | passed | passed |
| Old identity warning class | still present | resolved |
| AI draft warning repositories | 3 | 1 |
| AI draft warning diagnostics | 3 | 3 |
| Remaining warning class | `package_set_id_missing`, `excluded_package_unknown` | `selected_member_role_unknown` |
| Single-package stop policy | ambiguous | `no_proposal_subjects` remains visible |
| AI output authority | proposal-only | proposal-only |

## Required Condition Before Approval

P45-T4 does not add a new Workplan task. It records the condition that must be
true before bounded popular-library scraping can be approved:

- resolve `selected_member_role_unknown` for xyflow or document why it is
  non-blocking for bounded popular-library scraping;
- resolve `no_proposal_subjects` for FastAPI/Gin or document why it is
  non-blocking for single-package repositories;
- preserve proposal-only AI output;
- preserve no raw prompt, raw provider response, or chain-of-thought
  persistence;
- keep registry truth unchanged.

## Boundary

P45-T4 does not run AI, clone or fetch repositories, install dependencies,
invoke package managers, execute harvested code, enable trusted local adapter
execution, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, approve bounded popular-library scraping,
treat AI output as registry truth, treat adapter output as registry truth, or
treat readiness output as registry truth.

P45-T4 also does not persist raw prompts, persist raw provider responses,
persist secrets, or persist chain-of-thought, and it does not add Workplan
tasks.
