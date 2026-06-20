# Operational MVP Warning Triage

Status: P44-T1 quality-hardening warning triage.

P44-T1 turns the P43-T7 `needs_quality_hardening` exit decision into the first
bounded hardening artifact. It triages the P43-T5 `package_set_id_missing` AI
draft warnings for xyflow, FastAPI, and Gin without rerunning AI, applying AI
output, or changing registry truth.

The durable fixture is:

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

The triage references:

```text
tests/fixtures/operational_mvp_validation/p43-t5-operational-mvp-ai-enabled-comparison.example.json
sha256:cd03f8486a7cb9bd1dcf6efde1c7660ce6f63457a082207b1e81ee62ff5e327a

tests/fixtures/operational_mvp_validation/p43-t7-operational-mvp-exit-report.example.json
sha256:28d1dc5d3d8ad24d1050e4a7fbb170a00ffa20043c80fbe2bb8a33c375bf78d7
```

P43-T5 used local LM Studio with `openai/gpt-oss-20b`. The provider was
available, the batch passed, and all AI output remained proposal-only. Raw
prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Triage Result

The shared warning is:

```text
package_set_id_missing
```

The triage classifies all three repository warnings with primary cause
`ai_proposal_shape`:

| Repository | Expected shape | Draft warning | Enrichment | Primary cause |
| --- | --- | --- | --- | --- |
| `xyflow` | package-set monorepo | `package_set_id_missing` | completed, 4 proposals | `ai_proposal_shape` |
| `fastapi` | framework library package | `package_set_id_missing` | completed, 1 proposal | `ai_proposal_shape` |
| `gin` | single package framework | `package_set_id_missing` | completed, 1 proposal | `ai_proposal_shape` |

This does not prove package-set identity drift in the source checkouts. The
static-only baseline preserved the expected candidate topology, while the AI
draft proposal layer failed to provide the package-set identity expected by the
proposal schema. AI enrichment completed cleanly, so enrichment sidecars remain
reviewable author evidence.

## Follow-Up Guidance

P44-T1 does not fix the warning. It narrows the next work:

- `P44-T2`: review the proposal-only AI enrichment artifacts for usefulness,
  noise, unsupported claims, and do-not-promote output;
- `P44-T3`: resolve or explicitly accept xyflow's partial public-interface and
  fork-origin manual-correction caveats;
- `P44-T4`: rerun the bounded corpus after targeted warning and caveat
  hardening;
- `P44-T5`: record the post-hardening readiness decision before bounded
  popular-library scraping.

## Boundary

P44-T1 does not:

- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- call hosted AI services;
- run AI;
- run LM Studio or any other AI provider;
- persist raw prompts;
- persist raw provider responses;
- persist chain-of-thought;
- enable trusted local adapter execution;
- run adapter code;
- accept packages or relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- treat AI output as registry truth;
- treat adapter output as registry truth;
- treat warning triage output as registry truth.

## References

- [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md)
- [`OPERATIONAL_MVP_EXIT_REPORT.md`](OPERATIONAL_MVP_EXIT_REPORT.md)
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md)
- [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md)
