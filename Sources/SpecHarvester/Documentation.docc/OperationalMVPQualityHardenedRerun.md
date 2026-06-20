# Operational MVP Quality-Hardened Rerun

P44-T4 reruns xyflow, FastAPI, and Gin after P44-T1 through P44-T3 and records
the quality-hardening comparison against the P43 baseline.

```text
tests/fixtures/operational_mvp_quality_hardening/p44-t4-operational-mvp-quality-hardened-rerun.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-quality-hardened-rerun/v0
kind: SpecHarvesterOperationalMVPQualityHardenedRerun
authority: producer_operational_mvp_quality_hardened_rerun_only
```

## Result

The static-only rerun passed for all three repositories and matches the P43-T4
baseline. The AI-enabled rerun also passed and produced six proposal-only AI
artifacts with `openai/gpt-oss-20b`.

P44-T4 records `rerun_passed_but_warning_ambiguity_not_fully_resolved`:
`xyflow` and `fastapi` still report `package_set_id_missing`, while `gin`
reports `excluded_package_unknown`.

## Boundary

P44-T4 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, enable trusted local adapter
execution, apply AI enrichment, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, persist raw prompts, persist raw
responses, persist chain-of-thought, treat AI output as registry truth, treat
adapter output as registry truth, or treat quality-hardened rerun output as
registry truth.
