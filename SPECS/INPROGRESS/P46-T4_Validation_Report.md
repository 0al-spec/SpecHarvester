# P46-T4 Validation Report

## Task

P46-T4 Bounded Popular-Library Pilot Output Triage

## Verdict

PASS

## Summary

P46-T4 records triage for the P46 bounded pilot outputs without rerunning the
pilot. The triage separates reviewable static evidence from noisy AI sidecars,
unsupported enrichment, evidence gaps, and do-not-promote AI draft outputs.

## Durable Artifacts

- `tests/fixtures/bounded_popular_library_pilot_output_triage/p46-t4-bounded-popular-library-pilot-output-triage.example.json`
- `docs/BOUNDED_POPULAR_LIBRARY_PILOT_OUTPUT_TRIAGE.md`
- `Sources/SpecHarvester/Documentation.docc/BoundedPopularLibraryPilotOutputTriage.md`

## Triage Summary

| Classification | Result |
| --- | ---: |
| Repositories triaged | 6 |
| Reviewable static repositories | 6 |
| Static candidates | 9 |
| Static relations | 3 |
| AI draft completed repositories | 1 |
| AI draft warning repositories | 3 |
| AI draft do-not-promote repositories | 2 |
| AI enrichment completed repositories | 4 |
| AI enrichment warning repositories | 2 |
| Registry-promotion blockers | 4 |

## Key Outcomes

- `gin.aiDraft` and `docc2context.aiDraft` are do-not-promote sidecars because
  they hit `ai_json_repair_exhausted` and
  `package_set_subject_metadata_missing`.
- xyflow static output remains reviewable but carries evidence gaps:
  `partial_public_interface_index` and
  `operator_checkout_origin_fork_mismatch`.
- xyflow AI enrichment is unsupported for registry promotion because it
  carries `model_evidence_path_unsupported`.
- Flask, Cupertino, and NavigationSplitView AI draft sidecars are noisy and
  require author review before any AI use.

## Boundary Verification

P46-T4 did not rerun the pilot, run AI, run adapters, enable trusted local
adapter execution, clone or fetch repositories, install dependencies, invoke
package managers, execute harvested code, accept packages or relations,
publish registry metadata, seed baselines, remove `preview_only`, persist raw
prompts, persist raw provider responses, persist secrets, or persist
chain-of-thought.

Triage output is not registry truth. Static output, AI output, and adapter
output remain non-authoritative review evidence.

## Commands

| Command | Result |
| --- | --- |
| `python3 -m json.tool tests/fixtures/bounded_popular_library_pilot_output_triage/p46-t4-bounded-popular-library-pilot-output-triage.example.json >/dev/null` | PASS |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q -k 'bounded_popular_library_pilot_output_triage'` | PASS, `1 passed, 164 deselected` |
| `ruff check tests/test_docs_contracts.py` | PASS |
| `ruff format --check tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Remaining Gap

P46-T5 must convert this triage into author-facing handoff summaries that keep
reviewable static evidence separate from noisy, unsupported, evidence-gap, and
do-not-promote AI sidecars.
