# Operational MVP AI Draft Shape Rerun

P45-T3 reruns the bounded operational MVP corpus after the P45 AI draft shape
fixes:

- P45-T1 resolves safe package-set subject identity normalization;
- P45-T2 records the `validationGuard` boundary before proposal evidence is
  accepted.

The rerun uses the same pinned local checkouts as P44-T4: xyflow, FastAPI, and
Gin. It compares static-only output, AI draft warnings, proposal counts, and
proposal-only authority boundaries against P44-T4.

Machine-readable evidence:

```text
tests/fixtures/operational_mvp_quality_hardening/p45-t3-operational-mvp-ai-draft-shape-rerun.example.json
```

Identity:

```yaml
apiVersion: spec-harvester.operational-mvp-ai-draft-shape-rerun/v0
kind: SpecHarvesterOperationalMVPAIDraftShapeRerun
authority: producer_operational_mvp_ai_draft_shape_rerun_only
```

## Run Summary

| Mode | Processed | Failed | Preflight passed | Candidates | Relations | AI draft proposals | AI enrichment proposals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| static-only | 3 | 0 | 3 | 6 | 3 | 0 | 0 |
| AI-enabled | 3 | 0 | 3 | 6 | 3 | 3 | 3 |

AI-enabled output produced 6 proposal artifacts and 6 enrichment proposal
members. AI enrichment stayed proposal-only and was not applied into preview
candidate copies.

## Warning Comparison

| Repository | P44-T4 AI draft warning codes | P45-T3 AI draft warning codes | Result |
| --- | --- | --- | --- |
| xyflow | `package_set_id_missing` | `selected_member_role_unknown` | identity warning resolved, role taxonomy warning remains |
| FastAPI | `package_set_id_missing` | - | resolved |
| Gin | `excluded_package_unknown` | - | resolved |

P45-T3 resolves the old identity/unknown-exclusion warning class across the
bounded corpus. The AI draft layer is still not fully clean because xyflow now
has warning-level `selected_member_role_unknown` diagnostics. FastAPI and Gin
draft proposals have no diagnostics, but their draft stop-policy reason remains
`no_proposal_subjects`; their enrichment proposals still complete as
proposal-only author-review evidence.

## Provider and Privacy

The live local provider was LM Studio with `openai/gpt-oss-20b` at
`http://127.0.0.1:1234`. Bounded JSON repair was available but not needed.

Token summary:

- AI draft provider total tokens: 17,837;
- AI enrichment provider total tokens: 80,994.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Authority Boundary

P45-T3 is producer-side review evidence only. It does not:

- clone or fetch repositories;
- install dependencies;
- invoke package managers;
- execute harvested code;
- enable trusted local adapter execution;
- apply AI enrichment;
- accept packages or relations;
- publish registry metadata;
- seed baselines;
- remove `preview_only`;
- persist raw prompts;
- persist raw responses;
- persist chain-of-thought;
- treat AI output as registry truth;
- treat adapter output as registry truth;
- treat post-fix rerun output as registry truth.

P45-T3 is ready for the separate P45-T4 readiness decision. It does not itself
approve bounded popular-library scraping.
