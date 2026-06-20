# Bounded Popular-Library Pilot AI-Enabled Run

Status: P46-T3 real local AI-enabled run.

P46-T3 runs the same pinned P46 bounded popular-library pilot manifest through
the local OpenAI-compatible provider after the P46-T2 static-only gate passed.
The run records proposal-only AI evidence and does not change registry truth.

The durable fixture is:

```text
tests/fixtures/bounded_popular_library_pilot_ai_enabled_run/p46-t3-bounded-popular-library-pilot-ai-enabled-run.example.json
```

Fixture identity:

```text
apiVersion: spec-harvester.bounded-popular-library-pilot-ai-enabled-run/v0
kind: SpecHarvesterBoundedPopularLibraryPilotAIEnabledRun
authority: producer_ai_proposal_evidence_only
```

## What Was Run

Run root:

```text
/tmp/specharvester-p46-t3-bounded-popular-library-ai-enabled-20260620T202117Z
```

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p46-bounded-popular-library-pilot \
  --out /tmp/specharvester-p46-t3-bounded-popular-library-ai-enabled-20260620T202117Z/output \
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

Batch report digest:

```text
sha256:fddb8c06ee36c6df005beb6a9c790038ef61ec0b27d939929a27ecb6c45b4f51
```

## Result Summary

The AI-enabled batch status was `failed`. This is recorded as pilot evidence,
not hidden by an unplanned broader retry.

| Metric | Result |
| --- | ---: |
| Processed repositories | 6 |
| Failed repositories | 2 |
| Passed static preflights | 6 |
| AI draft proposals | 4 |
| AI enrichment proposals | 6 |
| AI draft failed repositories | 2 |
| AI draft warning repositories | 3 |
| AI draft completed repositories | 1 |
| AI enrichment warning repositories | 2 |
| AI enrichment completed repositories | 4 |
| AI enrichment provider total tokens | 110,186 |
| Trusted local adapter sidecars | 0 |

P46-T2 static-only baseline remained the comparison anchor: six repositories
processed, nine preview candidates, three relation proposals, zero preflight
warnings, zero AI proposals, zero adapter sidecars, and no registry authority.

## Repository Results

| Repository | Batch status | AI draft | AI enrichment | Main diagnostic |
| --- | --- | --- | --- | --- |
| Flask | passed | warning | warning | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | failed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |
| xyflow | passed | completed | warning | `model_evidence_path_unsupported` |
| Cupertino | passed | warning | completed | `selected_member_role_unknown` |
| NavigationSplitView | passed | warning | completed | `selected_member_role_unknown` |
| docc2context | failed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |

## Triage Outcome

The P46-T3 AI proposal layer is blocked for P46-T4 triage:

- Gin AI draft exhausted one JSON repair attempt and still produced
  `package_set_subject_metadata_missing`.
- docc2context AI draft exhausted one JSON repair attempt and still produced
  `package_set_subject_metadata_missing`.
- Flask, Cupertino, and NavigationSplitView produced reviewable AI draft
  warnings around `selected_member_role_unknown`.
- xyflow AI draft completed cleanly, while enrichment retained
  `model_evidence_path_unsupported`.

These are proposal-layer findings. They do not invalidate the P46-T2
static-only candidate layer.

## Boundary

P46-T3 did not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, enable trusted local adapter
execution, run adapter code, accept packages or relations, publish registry
metadata, seed baselines, or remove `preview_only`.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted.

The run does not treat AI output as registry truth, does not treat static
output as registry truth, and does not treat adapter output as registry truth.
All AI sidecars remain proposal-only review evidence.

## Follow-Up

P46-T4 must triage the static candidate layer and AI proposal sidecars,
including the failed Gin and docc2context AI draft outputs, before any
author-facing handoff or larger corpus decision.
