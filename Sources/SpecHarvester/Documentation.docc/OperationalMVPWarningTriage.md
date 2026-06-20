# Operational MVP Warning Triage

P44-T1 records producer-side warning triage for the P43-T5
`package_set_id_missing` AI draft diagnostics.

The machine-readable fixture is:

```text
tests/fixtures/operational_mvp_quality_hardening/p44-t1-operational-mvp-warning-triage.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-warning-triage/v0
kind: SpecHarvesterOperationalMVPWarningTriage
authority: producer_operational_mvp_warning_triage_only
```

## Source Evidence

The triage references P43-T5
`SpecHarvesterOperationalMVPAIEnabledComparison` and P43-T7
`SpecHarvesterOperationalMVPExitReport` by path, digest, API version, kind, and
authority.

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
sha256:cd03f8486a7cb9bd1dcf6efde1c7660ce6f63457a082207b1e81ee62ff5e327a

tests/fixtures/operational_mvp_validation/p43-t7-operational-mvp-exit-report.example.json
sha256:28d1dc5d3d8ad24d1050e4a7fbb170a00ffa20043c80fbe2bb8a33c375bf78d7
```

P43-T5 used local LM Studio with `openai/gpt-oss-20b`, completed the batch, and
kept AI draft and enrichment output proposal-only.

## Result

All three warnings for xyflow, FastAPI, and Gin are classified with primary
cause `ai_proposal_shape`:

| Repository | Expected shape | Enrichment result |
| --- | --- | --- |
| `xyflow` | package-set monorepo | completed, 4 proposals |
| `fastapi` | framework library package | completed, 1 proposal |
| `gin` | single package framework | completed, 1 proposal |

The warning does not prove package-set identity drift in the source checkouts.
It identifies a draft proposal identity-field shape issue while preserving
proposal-only AI enrichment for author review.

## Follow-Up

- `P44-T2`: review AI enrichment proposal quality.
- `P44-T3`: resolve or explicitly accept xyflow manual-correction caveats.
- `P44-T4`: rerun the bounded corpus after hardening.
- `P44-T5`: record the post-hardening readiness decision.

## Boundary

The triage does not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, run AI, enable trusted local adapter
execution, accept packages or relations, publish registry metadata, seed
baselines, remove `preview_only`, treat AI output as registry truth, treat
adapter output as registry truth, or treat warning triage output as registry
truth.
