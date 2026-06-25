# P51-T8 Larger Curated Corpus Exit Decision

**Status:** Planned
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T8`
**Depends On:** `P51-T7` Larger Curated Corpus Output Triage

## Goal

Record the larger curated corpus exit decision using the P51-T7 triage
artifact. The decision must state whether Phase 51 proceeds, needs another
targeted pass, or stops on a documented blocker before any further expansion.

## Source Evidence

P51-T8 uses this P51-T7 fixture as its only evidence source:

```text
tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json
```

Source digest:

```text
sha256:6c757fe4c65546404076a5b4b4d45d09b8f815859495fa467dc6a1e9cd9b8b11
```

P51-T7 reported:

- 12 repositories triaged.
- 15 static candidate packages.
- 11 static packages selected for author review.
- 4 static packages deferred.
- 3 relation proposals deferred.
- 12 AI draft sidecars classified.
- 12 AI enrichment sidecars classified.
- 8 AI-enriched previews prepared and kept deferred.
- 7 AI-enriched previews skipped or do-not-promote.
- 4 carried-forward caveats.
- 5 registry-promotion blockers.
- No larger corpus rerun required for the exit decision.

## Decision To Record

The expected P51-T8 decision is:

```text
complete_phase_51_with_author_review_evidence_no_further_expansion
```

This means Phase 51 produced enough classified evidence for maintainer or
author review. It does not mean package acceptance, relation acceptance,
registry publication, baseline seeding, or larger corpus expansion approval.

## Deliverables

- Add a machine-readable
  `SpecHarvesterLargerCuratedCorpusExitDecision` fixture.
- Add GitHub Markdown documentation for the decision.
- Add matching DocC documentation.
- Link the decision from docs index, capabilities, roadmap, and DocC root docs.
- Add contract tests for source digest, selected decision, rejected
  alternatives, boundaries, carried-forward caveats, and no-next-task state.
- Add a validation report with the commands actually run.
- Archive the task PRD and validation report after validation.
- Mark `P51-T8` complete in the workplan.
- Update `SPECS/INPROGRESS/next.md` to show that Phase 51 is complete and no
  next task is selected.

## Acceptance Criteria

- The fixture references the P51-T7 triage artifact by path, digest,
  `apiVersion`, `kind`, and `authority`.
- The selected decision is
  `complete_phase_51_with_author_review_evidence_no_further_expansion`.
- The decision records:
  - `phase51Complete: true`
  - `largerCuratedCorpusRerunRequired: false`
  - `needsAnotherTargetedPass: false`
  - `stoppedOnDocumentedBlocker: false`
  - `furtherExpansionApproved: false`
  - `registryPromotionAllowed: false`
  - `authorReviewEvidenceReady: true`
- The decision rejects:
  - another targeted pass before exit
  - stopping on a hard documented blocker
  - approving further larger corpus expansion
- The four P51-T7 caveats are carried forward:
  - `xyflow.partial_public_interface_index`
  - `xyflow.operator_checkout_origin_fork_mismatch`
  - `docc2context.source_checkout_had_untracked_doccarchive`
  - `hyperprompt.single_package_deterministic_fallback_applied`
- The decision preserves the distinction between author-review evidence and
  registry truth.
- Tests prove no raw prompt, raw provider response, secret, or chain-of-thought
  persistence is introduced.
- Tests prove P51-T8 does not rerun the corpus, run AI, clone/fetch, install
  dependencies, invoke package managers, execute harvested code, run adapters,
  accept packages or relations, publish registry metadata, seed baselines, or
  remove `preview_only`.

## Out Of Scope

- Rerunning the larger curated corpus.
- Running AI.
- Running adapters or enabling trusted local adapter execution.
- Accepting packages or relations.
- Publishing registry metadata.
- Seeding baselines.
- Removing `preview_only`.
- Treating static output, readiness output, AI output, AI-enriched preview
  output, repair output, rerun output, planning output, triage output, or
  adapter output as registry truth.
- Persisting raw prompts, raw provider responses, secrets, or chain-of-thought.
- Cloning or fetching repositories.
- Installing dependencies.
- Invoking package managers.
- Executing harvested code.

## Validation Plan

Run focused documentation contract tests:

```bash
pytest tests/test_docs_contracts.py -k larger_curated_corpus_exit_decision
```

Run the full documentation contract suite if the focused test passes:

```bash
pytest tests/test_docs_contracts.py
```
