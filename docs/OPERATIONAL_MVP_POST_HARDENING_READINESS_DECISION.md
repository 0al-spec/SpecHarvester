# Operational MVP Post-Hardening Readiness Decision

Status: P44-T5 Phase 44 exit decision.

P44-T5 records the post-hardening readiness decision after P44-T1 through
P44-T4. The decision is conservative: SpecHarvester should not yet proceed to
bounded popular-library scraping.

The durable fixture is:

```text
tests/fixtures/operational_mvp_quality_hardening/p44-t5-operational-mvp-post-hardening-readiness-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-post-hardening-readiness-decision/v0
kind: SpecHarvesterOperationalMVPPostHardeningReadinessDecision
authority: producer_operational_mvp_post_hardening_readiness_decision_only
```

## Decision

Selected state: `needs_another_quality_pass`.

Rejected states:

- `ready_for_bounded_popular_library_scraping`
- `blocked_until_adapter_execution`

P44-T4 passed, but it resolved zero AI draft warnings. xyflow and FastAPI still
report `package_set_id_missing`, while Gin changed to `excluded_package_unknown`.
That is not clean enough for broader autonomous scraping.

## Next Phase

Recommended next phase: P45 Operational MVP AI Draft Shape Hardening.

The first recommended task is P45-T1: fix AI draft proposal subject identity so
the bounded corpus can rerun without `package_set_id_missing` or
`excluded_package_unknown` warnings.

## Boundary

P44-T5 does not run AI, clone or fetch repositories, install dependencies,
invoke package managers, execute harvested code, enable trusted local adapter
execution, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, approve bounded popular-library scraping,
treat AI output as registry truth, treat adapter output as registry truth, or
treat readiness output as registry truth.
