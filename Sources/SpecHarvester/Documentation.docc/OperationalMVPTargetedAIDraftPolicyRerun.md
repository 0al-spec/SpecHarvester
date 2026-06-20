# Operational MVP Targeted AI Draft Policy Rerun

Status: P45-T7 targeted rerun evidence.

P45-T7 reruns the bounded operational MVP corpus after the targeted P45-T5 and
P45-T6 AI draft policy fixes:

- P45-T5 normalizes selected-member role aliases so xyflow no longer reports
  `selected_member_role_unknown` for known package-set roles.
- P45-T6 accepts stable single-package zero-subject drafts as non-blocking and
  hardens relation endpoint normalization.

The durable fixture is:

```text
tests/fixtures/operational_mvp_quality_hardening/p45-t7-operational-mvp-targeted-ai-draft-policy-rerun.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.operational-mvp-targeted-ai-draft-policy-rerun/v0
kind: SpecHarvesterOperationalMVPTargetedAIDraftPolicyRerun
authority: producer_operational_mvp_targeted_ai_draft_policy_rerun_only
```

## Run Summary

The rerun uses the same pinned local checkouts as P45-T3: xyflow, FastAPI, and
Gin.

| Mode | Processed | Failed | Preflight passed | Candidates | Relations | AI draft proposals | AI enrichment proposals |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| static-only | 3 | 0 | 3 | 6 | 3 | 0 | 0 |
| AI-enabled | 3 | 0 | 3 | 6 | 3 | 3 | 3 |

AI-enabled output produced 6 proposal artifacts and 6 enrichment proposal
members. AI enrichment stayed proposal-only and was not applied into preview
candidate copies.

## Comparison Against P45-T3

| Repository | P45-T3 AI draft signal | P45-T7 AI draft signal | Result |
| --- | --- | --- | --- |
| xyflow | `selected_member_role_unknown`, continue generation | completed, stop for author review | role and relation target blockers resolved |
| FastAPI | `no_proposal_subjects`, continue generation | `ai_json_repair_needed`, stop for author review | zero-subject policy accepted repaired JSON as non-blocking |
| Gin | `no_proposal_subjects`, continue generation | completed, stop for author review | zero-subject blocker resolved |

P45-T7 resolves the AI draft blockers that P45-T4 identified. The remaining
warning is not in AI draft selection: Gin AI enrichment still reports
warning-level `model_evidence_path_unsupported` diagnostics. P45-T7 records
that warning for P45-T8; it does not decide Phase 46 readiness.

Token summary:

- AI draft provider total tokens: 19,179.
- AI enrichment provider total tokens: 81,140.

## Provider and Privacy

The live local provider was LM Studio with `openai/gpt-oss-20b` at
`http://127.0.0.1:1234`. Bounded JSON repair was used for FastAPI and succeeded.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

## Authority Boundary

P45-T7 is producer-side review evidence only. It does not:

- broaden the corpus;
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
- make the Phase 46 readiness decision.

P45-T8 owns the final targeted-hardening readiness decision.
