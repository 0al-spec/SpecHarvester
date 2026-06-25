# P51-T7 Larger Curated Corpus Output Triage

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T7`
**Depends On:** `P51-T5`, `P51-T6`

## Goal

Classify the larger curated corpus output into selected, deferred, and
do-not-promote outcomes using only existing P51 evidence. The triage must carry
warning and caveat evidence forward for P51-T8 without accepting packages,
relations, AI output, enriched preview output, or adapter output as registry
truth.

## Inputs

- `tests/fixtures/larger_curated_corpus_static_only_gate/p51-t4-larger-curated-corpus-static-only-gate.example.json`
- `tests/fixtures/larger_curated_corpus_ai_enabled_gate/p51-t5-larger-curated-corpus-ai-enabled-gate.example.json`
- `tests/fixtures/hyperprompt_ai_draft_single_package_fallback/p51-t6-hyperprompt-ai-draft-single-package-fallback.example.json`
- `SPECS/ARCHIVE/P51-T5_Larger_Curated_Corpus_AI-Enabled_Proposal-Only_Gate/P51-T5_Validation_Report.md`
- `SPECS/ARCHIVE/P51-T6_Hyperprompt_AI_Draft_Single-Package_Fallback/P51-T6_Validation_Report.md`

## Deliverables

- Add a durable machine-readable triage fixture:
  `tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json`.
- Add GitHub and DocC documentation for the triage:
  `docs/LARGER_CURATED_CORPUS_OUTPUT_TRIAGE.md` and
  `Sources/SpecHarvester/Documentation.docc/LargerCuratedCorpusOutputTriage.md`.
- Add docs contract coverage proving the triage fixture, documentation,
  cross-document links, and next task pointer.
- Update documentation indexes, capabilities, and roadmap references.
- Create a validation report for P51-T7.

## Classification Rules

- **Selected:** static package evidence with passed preflight and no blocking
  static caveat. Selected means selected for author review only.
- **Deferred:** evidence that remains reviewable but should not be promoted
  before P51-T8 records an explicit disposition or before a later targeted task
  resolves a visible caveat.
- **Do not promote:** AI sidecars, enriched preview copies, relation proposals,
  or caveat-bearing outputs that must not be used as registry promotion input
  in their current form.

## Expected Triage Shape

- Classify all 15 static candidate packages from P51-T4.
- Classify all 3 relation proposals from P51-T4.
- Classify all 12 AI draft sidecars from P51-T5, using the repaired P51-T6
  Hyperprompt sidecar instead of the failed P51-T5 `hyperprompt.aiDraft`.
- Classify all 12 AI enrichment sidecars and all AI-enriched preview copies
  from P51-T5.
- Carry forward these caveats:
  - `xyflow.partial_public_interface_index`
  - `xyflow.operator_checkout_origin_fork_mismatch`
  - `docc2context.source_checkout_had_untracked_doccarchive`
  - `hyperprompt.single_package_deterministic_fallback_applied`
- Decide whether P51-T8 exit decision can proceed.

## Acceptance Criteria

- The fixture records source artifact digests for P51-T4, P51-T5, and P51-T6.
- The fixture records `candidatePackageCount: 15`, `relationProposalCount: 3`,
  `repositoriesTriaged: 12`, and `p51T8ExitDecisionAllowed: true`.
- The triage keeps all output non-authoritative:
  packages not accepted, relations not accepted, registry metadata not
  published, baselines not seeded, and `preview_only` not removed.
- The triage states that raw prompts, raw provider responses, secrets, and
  chain-of-thought were not persisted.
- The triage states that no repositories were cloned/fetched, no dependencies
  were installed, no package managers were invoked, no adapters were run, and
  no harvested code was executed.
- Docs and DocC pages link to the new triage artifact.
- `SPECS/INPROGRESS/next.md` advances to `P51-T8`.
- Required quality gates pass.

## Boundaries

- Do not rerun the larger corpus.
- Do not run AI.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, AI output, enriched preview output, repair output,
  rerun output, planning output, triage output, or adapter output as registry
  truth.
- Do not persist raw prompts, raw provider responses, secrets, or
  chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
