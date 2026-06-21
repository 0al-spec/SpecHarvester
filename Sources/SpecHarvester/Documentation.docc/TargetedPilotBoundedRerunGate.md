# Targeted Pilot Bounded Rerun Gate

Status: P47-T3 bounded rerun gate evidence.

P47-T3 runs the same six-repository P46 bounded pilot after the P47-T2
dispositions. The gate preserves static-only-before-AI ordering and keeps all
AI output proposal-only. The result is not larger curated corpus approval.

The durable fixture is:

```text
tests/fixtures/targeted_pilot_bounded_rerun_gate/p47-t3-targeted-pilot-bounded-rerun-gate.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.targeted-pilot-bounded-rerun-gate/v0
kind: SpecHarvesterTargetedPilotBoundedRerunGate
authority: producer_bounded_rerun_gate_evidence_only
```

## Source Scope

The source manifest remains:

```text
inputs/p46-bounded-popular-library-pilot/repositories.yml
```

Source manifest digest:

```text
sha256:b00a59837c64477819e01d5f97845ab8379cbe909ae464d2f1faee37e65c2f61
```

The run used the same six repository ids: Flask, Gin, xyflow, Cupertino,
NavigationSplitView, and docc2context. No repository was added or removed.

The operator-local manifest-relative checkout paths were unavailable in the
current workspace, so P47-T3 used a temporary input mirror with clean
`git archive` snapshots from already-existing local checkouts at the pinned
manifest revisions. This did not clone or fetch repositories.

## Static-Only Gate

Command:

```bash
PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch \
  /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs \
  --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-static \
  --skip-ai \
  --repository-profile-selection auto
```

Static result:

| Metric | Result |
| --- | ---: |
| Batch status | passed |
| Processed repositories | 6 |
| Failed repositories | 0 |
| Passed preflights | 6 |
| Candidate packages | 9 |
| Relation proposals | 3 |
| AI draft proposals | 0 |
| AI enrichment proposals | 0 |
| Trusted local adapter sidecars | 0 |

xyflow still has a `partial_public_interface_index` with 29 diagnostics. That
caveat remains visible for P47-T4.

## AI-Enabled Gate

Command:

```bash
PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch \
  /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/inputs \
  --out /tmp/specharvester-p47-t3-bounded-rerun-gate-20260621T130000Z/output-ai \
  --repository-profile-selection auto \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Provider:

```text
provider: lm_studio
model: openai/gpt-oss-20b
mode: local_lm_studio
```

AI-enabled result:

| Metric | Result |
| --- | ---: |
| Batch status | failed |
| Processed repositories | 6 |
| Failed repositories | 2 |
| Passed preflights | 6 |
| AI draft proposals | 4 |
| AI enrichment proposals | 6 |
| AI draft completed repositories | 1 |
| AI draft warning repositories | 3 |
| AI draft failed repositories | 2 |
| AI enrichment completed repositories | 3 |
| AI enrichment warning repositories | 3 |
| AI enrichment provider total tokens | 110,953 |

## Repository Results

| Repository | Static | AI draft | AI enrichment | Main signal |
| --- | --- | --- | --- | --- |
| Flask | passed | warning | warning | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | passed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |
| xyflow | passed with partial interface index | completed | warning | `ai_json_repair_needed`; `model_evidence_path_unsupported` did not repeat |
| Cupertino | passed | warning | warning | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| NavigationSplitView | passed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |
| docc2context | passed | warning | completed | `ai_json_repair_needed`, repaired to non-blocking warning |

## Gate Outcome

Selected outcome:

```text
bounded_rerun_executed_static_passed_ai_failed
```

The static gate passed. The AI-enabled gate did not pass because Gin and
NavigationSplitView AI drafts failed after one JSON repair attempt. The
current P47-T2 excluded sidecars were not reused as registry truth.

Important changes from P46:

- `docc2context.aiDraft` improved from do-not-promote failure to non-blocking
  warning.
- `gin.aiDraft` remains a blocking AI draft failure.
- `navigation-split-view.aiDraft` is a new blocking AI draft failure.
- `xyflow.aiEnrichment` no longer repeats `model_evidence_path_unsupported`,
  but it still carries an `ai_json_repair_needed` warning.
- xyflow `partial_public_interface_index` remains visible.
- xyflow operator checkout origin caveat remains visible because the local
  source checkout origin differs from the canonical manifest repository.

## Boundary

P47-T3 did not approve a larger curated corpus, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, clone or
fetch repositories, install dependencies, invoke package managers inside
harvested repositories, execute harvested code, run adapters, or enable trusted
local adapter execution.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted. Static output, AI output, and adapter output are not registry truth.

## Follow-Up

P47-T4 must record the targeted quality follow-up exit decision. The larger
curated corpus remains blocked until P47-T4 explicitly decides whether to run
another targeted pass, stop on documented blockers, or allow broader planning.
