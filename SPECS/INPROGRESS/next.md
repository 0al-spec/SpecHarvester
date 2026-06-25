# Next Task: P51-T8 Larger Curated Corpus Exit Decision

**Status:** Selected
**Phase:** Phase 51. Larger Curated Corpus Planning After Restored Rerun
**Task:** `P51-T8`
**Last Archived:** `P51-T7` Larger Curated Corpus Output Triage
**Depends On:** `P51-T7` Larger Curated Corpus Output Triage

## Goal

Record the larger curated corpus exit decision using P51-T7 triage evidence.
Decide whether to proceed, run another targeted pass, or stop on a documented
blocker before any further expansion.

## Context

P51-T7 produced the machine-readable
`SpecHarvesterLargerCuratedCorpusOutputTriage` fixture:

```text
tests/fixtures/larger_curated_corpus_output_triage/p51-t7-larger-curated-corpus-output-triage.example.json
```

The triage classified 15 static packages, three relation proposals, 12 AI
draft sidecars, 12 AI enrichment sidecars, AI-enriched preview outcomes,
warning evidence, and carried-forward caveats into:

```text
selected_for_author_review
deferred
do_not_promote
```

The previous `hyperprompt.aiDraft` hard blocker is superseded by P51-T6
fallback evidence, but the repaired sidecar remains proposal-only and carries
`hyperprompt.single_package_deterministic_fallback_applied`.

P51-T7 carries these caveats into the P51-T8 exit decision:

```text
xyflow.partial_public_interface_index
xyflow.operator_checkout_origin_fork_mismatch
docc2context.source_checkout_had_untracked_doccarchive
hyperprompt.single_package_deterministic_fallback_applied
```

## Scope

- Decide whether Phase 51 can proceed, needs another targeted pass, or must
  stop on a documented blocker.
- Preserve the distinction between author-review evidence and registry truth.
- Carry selected, deferred, and do_not_promote outcomes forward explicitly.
- Record whether any further larger curated corpus expansion is approved.

## Boundaries

- Do not rerun the larger corpus in P51-T8.
- Do not run AI in P51-T8.
- Do not accept packages or relations.
- Do not publish registry metadata.
- Do not seed baselines.
- Do not remove `preview_only`.
- Do not treat static output, readiness output, AI output, AI-enriched preview
  output, repair output, rerun output, planning output, triage output, or
  adapter output as registry truth.
- Do not persist raw prompts.
- Do not persist raw provider responses.
- Do not persist secrets.
- Do not persist chain-of-thought.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
