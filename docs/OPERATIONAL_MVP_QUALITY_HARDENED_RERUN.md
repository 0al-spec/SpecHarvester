# Operational MVP Quality-Hardened Rerun

Status: P44-T4 quality-hardening rerun evidence.

P44-T4 reruns the bounded operational MVP corpus after P44-T1 through P44-T3:
xyflow, FastAPI, and Gin. The rerun keeps the same pinned corpus lineage as P43,
compares static-only and AI-enabled proposal output, and records whether the
quality-hardening work made the output cleaner.

The durable fixture is:

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

Both reruns passed:

| Mode | Repositories | Failed | Candidates | Relations | AI proposals |
| --- | --- | --- | --- | --- | --- |
| static-only | 3 | 0 | 6 | 3 | 0 |
| AI-enabled | 3 | 0 | 6 | 3 | 6 |

The static-only rerun matches the P43-T4 baseline. The AI-enabled rerun again
produces proposal-only AI sidecars and does not apply AI enrichment into preview
candidates.

## Comparison

P44-T4 keeps the output reviewable but does not fully resolve warning ambiguity:

| Repository | AI draft warning | Comparison |
| --- | --- | --- |
| `xyflow` | `package_set_id_missing` | unchanged from P43 |
| `fastapi` | `package_set_id_missing` | unchanged from P43 |
| `gin` | `excluded_package_unknown` | changed warning code, not clean |

The LM Studio run used `openai/gpt-oss-20b` and `81,003` total provider tokens.
Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Decision Input

P44-T4 is ready for P44-T5 readiness evaluation. The evidence points to
`rerun_passed_but_warning_ambiguity_not_fully_resolved`: the operational MVP
still produces valid, reviewable proposal output, but the AI draft layer is not
clean enough to treat as a broad autonomous scraping gate.

## Boundary

P44-T4 does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, enable trusted local adapter
execution, apply AI enrichment, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, persist raw prompts, persist raw
responses, persist chain-of-thought, treat AI output as registry truth, treat
adapter output as registry truth, or treat quality-hardened rerun output as
registry truth.
