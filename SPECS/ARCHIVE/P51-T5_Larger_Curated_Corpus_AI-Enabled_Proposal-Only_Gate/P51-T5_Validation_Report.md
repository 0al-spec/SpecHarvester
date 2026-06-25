# P51-T5 Validation Report

**Task:** `P51-T5` Larger Curated Corpus AI-Enabled Proposal-Only Gate
**Date:** 2026-06-25
**Verdict:** PASS as evidence capture; AI-enabled gate status `failed`

## Summary

P51-T5 ran the larger curated corpus AI-enabled proposal-only gate over the
same 12 selected P51 sources that passed P51-T4 static-only execution. The run
used the local LM Studio/OpenAI-compatible endpoint with
`openai/gpt-oss-20b`, bounded JSON repair, and explicit AI enrichment preview
copying.

The evidence capture completed and recorded all 12 repositories, but the
AI-enabled batch report status was `failed` because `hyperprompt.aiDraft`
exhausted one JSON repair attempt and emitted
`package_set_subject_metadata_missing`. The failed sidecar remains
proposal-only evidence for P51-T6 output triage. It is not registry truth.

## Run Root

```text
/tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z
```

## Runtime Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/p51-larger-curated-corpus

curl -sS http://127.0.0.1:1234/v1/models

PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p51-larger-curated-corpus \
  --out /tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z/output \
  --repository-profile-selection auto \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
```

The shell command returned exit code `1`; the wrapper process captured it
durably after the report was written.

## Durable Artifacts

- `tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json`
- `docs/LARGER_CURATED_CORPUS_AI_ENABLED_GATE.md`
- `Sources/SpecHarvester/Documentation.docc/LargerCuratedCorpusAIEnabledGate.md`

## Result Summary

| Metric | Result |
| --- | ---: |
| Batch status | failed |
| Processed repositories | 12 |
| Failed repositories | 1 |
| Passed preflights | 12 |
| Candidate packages | 15 |
| Relation proposals | 3 |
| AI draft artifacts | 12 |
| AI draft proposals | 11 |
| AI draft completed repositories | 5 |
| AI draft warning repositories | 6 |
| AI draft failed repositories | 1 |
| AI enrichment proposals | 12 |
| AI enrichment completed repositories | 8 |
| AI enrichment warning repositories | 4 |
| AI enrichment provider prompt tokens | 183,710 |
| AI enrichment provider completion tokens | 6,572 |
| AI enrichment provider total tokens | 190,282 |
| AI-enriched preview applied packages | 8 |
| AI-enriched preview skipped packages | 7 |
| Trusted local adapter sidecars | 0 |

Batch report digest:

```text
sha256:3072ee644db22cad1cdafdf39f5de23a336c848a3aa1709c129bcd6c2cad1c29
```

Batch validation report digest:

```text
sha256:a23b0e495b2f70ee5a122704868974135abcc214830d71e847f762547dfdeb87
```

## Repository Results

| Repository | Batch status | AI draft | AI enrichment | AI-enriched preview | Main diagnostics |
| --- | --- | --- | --- | --- | --- |
| Flask | passed | warning | warning | skipped 1 | `excluded_package_also_selected`, `selected_member_role_unknown`, `refined_summary_missing` |
| Gin | passed | warning | completed | applied 1 | `selected_member_role_unknown` |
| xyflow | passed | completed | warning | skipped 4 | `refined_summary_missing`; interface partial, 29 diagnostics |
| Cupertino | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| NavigationSplitView | passed | warning | warning | skipped 1 | `selected_member_role_unknown`, `ai_json_repair_needed` |
| docc2context | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| FastAPI | passed | completed | completed | applied 1 | none |
| FastMCP | passed | completed | completed | applied 1 | none |
| SpecPM | passed | warning | completed | applied 1 | `excluded_package_also_selected`, `selected_member_role_unknown` |
| Hypercode | passed | completed | completed | applied 1 | none |
| SpecNode | passed | completed | warning | skipped 1 | `model_evidence_path_unsupported` |
| Hyperprompt | failed | failed | completed | applied 1 | `ai_json_repair_exhausted`, `ai_json_repair_needed`, `package_set_subject_metadata_missing` |

## Caveats Carried Forward

- `xyflow.partial_public_interface_index`
- `xyflow.operator_checkout_origin_fork_mismatch`
- `docc2context.source_checkout_had_untracked_doccarchive`
- `hyperprompt.ai_draft_failed_after_json_repair`

The first three caveats were already present after P51-T4. The fourth is new
P51-T5 evidence and must be classified by P51-T6 before P51-T7 can make an
exit decision.

## Boundary Verification

P51-T5 did not clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, run adapters, enable trusted local
adapter execution, accept packages or relations, publish registry metadata,
seed baselines, remove `preview_only`, persist raw prompts, persist raw
provider responses, persist secrets, or persist chain-of-thought.

AI output, enriched preview output, static output, and adapter output were not
treated as registry truth. Compact structured model request records were
persisted as review evidence; raw provider responses were not persisted.

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m spec_harvester source-manifests inputs/p51-larger-curated-corpus` | PASS, `repositoryCount: 12` |
| `curl -sS http://127.0.0.1:1234/v1/models` | PASS, model list included `openai/gpt-oss-20b` |
| `PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch inputs/p51-larger-curated-corpus --out /tmp/specharvester-p51-t5-larger-curated-corpus-ai-enabled-20260625T115302Z/output --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1 --apply-ai-enrichment` | EXPECTED NONZERO EXIT, exit code `1`, batch status `failed`, evidence captured |
| `python3 -m json.tool tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "larger_curated_corpus_ai_enabled_gate or larger_curated_corpus_static_only_gate"` | PASS, `2 passed, 183 deselected` |
| `python3 -m ruff format tests/test_docs_contracts.py` | PASS, `1 file reformatted` |
| `git diff --check` | PASS |
| `python3 -m ruff format --check src tests` | PASS, `131 files already formatted` |
| `python3 -m ruff check src tests` | PASS, `All checks passed!` |
| `PYTHONPATH=src python3 -m pytest` | PASS, `916 passed, 1 skipped` |
| `PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, `916 passed, 1 skipped`; total coverage `90.48%` |
| `swift package dump-package >/dev/null` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

## Next Step

P51-T6 should triage the static candidates, relation proposals, AI draft
sidecars, AI enrichment sidecars, AI-enriched preview copies, warning evidence,
failed `hyperprompt.aiDraft` sidecar, and carried-forward caveats into
selected, deferred, and do-not-promote outcomes without rerunning the larger
corpus or changing registry truth.
