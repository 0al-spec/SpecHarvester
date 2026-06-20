# P46-T3 Validation Report

## Task

P46-T3 Bounded Popular-Library Pilot AI-Enabled Run

## Verdict

PASS as evidence capture; AI proposal layer is blocked for P46-T4 triage.

## Summary

P46-T3 ran the same six-repository bounded pilot manifest through local LM
Studio with `openai/gpt-oss-20b`. The batch completed as a controlled
AI-enabled run but returned status `failed` because Gin and docc2context AI
draft proposals exhausted one JSON repair attempt and still had
`package_set_subject_metadata_missing`.

The result is intentionally recorded as pilot evidence. The static-only P46-T2
candidate/relation baseline remains valid; AI sidecars remain proposal-only.

## Run Root

```text
/tmp/specharvester-p46-t3-bounded-popular-library-ai-enabled-20260620T202117Z
```

## Runtime Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/p46-bounded-popular-library-pilot

PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p46-bounded-popular-library-pilot \
  --out /tmp/specharvester-p46-t3-bounded-popular-library-ai-enabled-20260620T202117Z/output \
  --repository-profile-selection auto \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

## Durable Artifacts

- `tests/fixtures/bounded_popular_library_pilot_ai_enabled_run/p46-t3-bounded-popular-library-pilot-ai-enabled-run.example.json`
- `docs/BOUNDED_POPULAR_LIBRARY_PILOT_AI_ENABLED_RUN.md`
- `Sources/SpecHarvester/Documentation.docc/BoundedPopularLibraryPilotAIEnabledRun.md`

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | failed |
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

Batch report digest:

```text
sha256:fddb8c06ee36c6df005beb6a9c790038ef61ec0b27d939929a27ecb6c45b4f51
```

## Repository Results

| Repository | Batch status | AI draft | AI enrichment | Main diagnostic |
| --- | --- | --- | --- | --- |
| Flask | passed | warning | warning | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | failed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |
| xyflow | passed | completed | warning | `model_evidence_path_unsupported` |
| Cupertino | passed | warning | completed | `selected_member_role_unknown` |
| NavigationSplitView | passed | warning | completed | `selected_member_role_unknown` |
| docc2context | failed | failed | completed | `ai_json_repair_exhausted`, `package_set_subject_metadata_missing` |

## Boundary Verification

P46-T3 did not change the source manifest, clone or fetch repositories, install
dependencies, invoke package managers, execute harvested code, enable trusted
local adapter execution, run adapter code, accept packages or relations,
publish registry metadata, seed baselines, or remove `preview_only`.

Raw prompts, raw provider responses, secrets, and chain-of-thought were not
persisted. AI output remained proposal-only and was not treated as registry
truth.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p46-bounded-popular-library-pilot` | PASS, `repositoryCount: 6` |
| `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p46-bounded-popular-library-pilot --out /tmp/specharvester-p46-t3-bounded-popular-library-ai-enabled-20260620T202117Z/output --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1` | Completed, batch status `failed` |
| `python3 -m json.tool tests/fixtures/bounded_popular_library_pilot_ai_enabled_run/p46-t3-bounded-popular-library-pilot-ai-enabled-run.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'bounded_popular_library_pilot_ai_enabled_run'` | PASS, `1 passed, 163 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Remaining Gap

P46-T4 must triage the candidate layer and AI sidecars, especially the failed
Gin and docc2context AI draft outputs, before any author-facing handoff or
larger-corpus decision.
