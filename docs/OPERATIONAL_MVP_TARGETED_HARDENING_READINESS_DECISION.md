# Operational MVP Targeted-Hardening Readiness Decision

Status: P45-T8 Phase 46 readiness decision.

P45-T8 records the final targeted-hardening readiness decision after the P45-T7
rerun. It does not rerun AI and does not broaden the corpus. It uses the
P45-T7 evidence to decide whether the next bounded popular-library pilot may
start.

The durable fixture is:

```text
tests/fixtures/operational_mvp_quality_hardening/p45-t8-targeted-hardening-readiness-decision.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.targeted-hardening-readiness-decision/v0
kind: SpecHarvesterTargetedHardeningReadinessDecision
authority: producer_targeted_hardening_readiness_decision_only
```

## Decision

Selected state:

```text
ready_for_phase46_bounded_popular_library_pilot
```

Rejected states:

- `needs_another_targeted_ai_draft_hardening_pass`
- `blocked_until_adapter_execution`
- `approve_unbounded_popular_library_scraping`
- `start_phase46_without_warning_carry_forward`

Phase 46 can start as a bounded popular-library pilot. This is not approval for
unbounded scraping, package acceptance, relation acceptance, or registry
publication.

The readiness basis is narrow:

- xyflow no longer reports `selected_member_role_unknown`;
- FastAPI keeps only a successful `ai_json_repair_needed` warning under the
  single-package `no_proposal_subjects` non-blocking policy;
- Gin no longer has an AI draft `no_proposal_subjects` blocker;
- all AI output remains proposal-only;
- raw prompts, raw provider responses, secrets, and chain-of-thought were not
  persisted.

## Remaining Warning

Gin still carries AI enrichment warning-level `model_evidence_path_unsupported`
diagnostics. P45-T8 treats this as non-blocking for starting the Phase 46
bounded pilot because it is not an AI draft selection blocker.

The warning is still a registry-promotion blocker until triaged. Phase 46 must
carry it into:

- P46-T4 pilot candidate-layer and AI sidecar triage;
- P46-T5 author-facing handoff summaries.

## Phase 46 Start Conditions

P46-T1 may define the first bounded popular-library pilot manifest. The manifest
must define pinned local checkout requirements, multi-ecosystem coverage,
exclusion rules, stop conditions, and the static-only gate before any AI-enabled
pilot run.

The pilot must preserve proposal-only AI output, no raw prompt, raw provider
response, or chain-of-thought persistence, and no registry truth mutation.

## Boundary

P45-T8 does not run AI, rerun the corpus, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, enable trusted
local adapter execution, accept packages or relations, publish registry
metadata, seed baselines, remove `preview_only`, approve unbounded
popular-library scraping, treat AI output as registry truth, treat adapter
output as registry truth, or treat readiness output as registry truth.

P45-T8 also does not persist raw prompts, persist raw provider responses,
persist secrets, or persist chain-of-thought.
