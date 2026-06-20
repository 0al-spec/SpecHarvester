# Operational MVP Xyflow Caveat Resolution

P44-T3 accepts xyflow's partial `PublicInterfaceIndex` and SoundBlaster fork
origin caveats for bounded P44 rerun evidence while keeping both caveats as
registry-promotion blockers.

```text
tests/fixtures/operational_mvp_quality_hardening/p44-t3-operational-mvp-xyflow-caveat-resolution.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-xyflow-caveat-resolution/v0
kind: SpecHarvesterOperationalMVPXyflowCaveatResolution
authority: producer_operational_mvp_xyflow_caveat_resolution_only
```

## Decision

| Caveat | P44 rerun | Registry promotion |
| --- | --- | --- |
| `partial_public_interface_index` | accepted | blocked |
| `operator_checkout_origin_fork_mismatch` | accepted | blocked |

## Boundary

P44-T3 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, run AI, enable trusted local adapter
execution, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, treat AI output as registry truth, treat
adapter output as registry truth, or treat caveat-resolution output as registry
truth.
