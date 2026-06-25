# P51-T8 Validation Report

**Task:** `P51-T8` Larger Curated Corpus Exit Decision
**Status:** Passed
**Date:** 2026-06-25

## Scope

Validation covers the P51-T8 exit-decision fixture, GitHub Markdown docs, DocC
docs, documentation indexes, roadmap entries, workplan linkage, and
`SPECS/INPROGRESS/next.md` contract handling.

P51-T8 did not rerun the larger corpus, run AI, run adapters, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, accept packages or relations, publish registry metadata, seed baselines,
or remove `preview_only`.

## Commands

Initial collection attempts:

```bash
pytest tests/test_docs_contracts.py -k larger_curated_corpus_exit_decision
```

Result: failed during collection because the local package was not on
`PYTHONPATH`.

```bash
PYTHONPATH=Sources pytest tests/test_docs_contracts.py -k larger_curated_corpus_exit_decision
```

Result: failed during collection because the Python package lives under
`src/spec_harvester`, not `Sources`.

Focused corrected validation:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -k larger_curated_corpus_exit_decision
```

Result:

```text
1 passed, 187 deselected
```

Full corrected validation:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py
```

Result:

```text
188 passed
```

Post-archive focused validation:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -k larger_curated_corpus_exit_decision
```

Initial post-archive result: failed because `next.md` used `Further expansion`
with uppercase `F` while the no-next-state contract expected the literal
lowercase phrase `further expansion is not approved`. The text was corrected
without changing the decision semantics.

Final post-archive result:

```text
1 passed, 187 deselected
```

Post-archive full validation:

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py
```

Result:

```text
188 passed
```

## Verified

- `SpecHarvesterLargerCuratedCorpusExitDecision` fixture identity.
- P51-T7 source artifact path, digest, `apiVersion`, `kind`, and `authority`.
- Selected decision:
  `complete_phase_51_with_author_review_evidence_no_further_expansion`.
- Rejected alternatives:
  - another targeted pass before exit
  - stopping on a hard documented blocker
  - approving further larger corpus expansion
- Phase 51 completion state.
- No next task selected after archive state.
- Four carried-forward caveats:
  - `xyflow.partial_public_interface_index`
  - `xyflow.operator_checkout_origin_fork_mismatch`
  - `docc2context.source_checkout_had_untracked_doccarchive`
  - `hyperprompt.single_package_deterministic_fallback_applied`
- Five registry-promotion blockers, including
  `specnode.model_evidence_path_unsupported`.
- No registry authority, package acceptance, relation acceptance, registry
  publication, baseline seeding, or `preview_only` removal.
- No raw prompt, raw provider response, secret, or chain-of-thought
  persistence.

## Verdict

P51-T8 passes validation as an evidence-only exit decision. Phase 51 can be
archived as complete after moving the PRD and validation report into the task
archive and updating `next.md` to the no-next-task state.
