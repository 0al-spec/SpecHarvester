# P49-T3 Run Same-Scope Bounded Rerun Gate

## Goal

Run the same six-repository bounded rerun gate after P49-T2 cleared or
explicitly disposed the previous `docc2context.aiDraft` blockers for the gate.

P49-T3 must preserve static-only-before-AI ordering, use the same P46 bounded
pilot manifest, and keep all AI output proposal-only.

## Context

P49-T2 selected:

```text
docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3
```

The previous `docc2context.aiDraft` blockers are cleared or explicitly disposed
for P49-T3:

- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

P49-T2 carries the warning `excluded_package_also_selected` as non-blocking for
this gate.

## Execution Plan

1. Verify P49-T2 evidence and the P46 source manifest.
2. Resolve the six operator-local checkout paths from:

   ```text
   inputs/p46-bounded-popular-library-pilot/repositories.yml
   ```

3. If all six checkouts are present, run the static-only gate first:

   ```bash
   PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch \
     <p49-t3-inputs> \
     --out <p49-t3-output-static> \
     --skip-ai \
     --repository-profile-selection auto
   ```

4. If the static-only gate passes and LM Studio is available, run the
   AI-enabled gate:

   ```bash
   PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch \
     <p49-t3-inputs> \
     --out <p49-t3-output-ai> \
     --repository-profile-selection auto \
     --lm-studio-base-url http://127.0.0.1:1234 \
     --lm-studio-model openai/gpt-oss-20b \
     --json-repair-max-attempts 1
   ```

5. Record durable P49-T3 gate evidence under
   `tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/`.
6. Document the result in GitHub docs and DocC.
7. Advance `SPECS/INPROGRESS/next.md` to P49-T4 only if P49-T3 records a
   completed gate result or a bounded blocker that P49-T4 can decide on.

## Stop Conditions

P49-T3 must not substitute a smaller run for the six-repository bounded rerun.
If one or more operator-local checkouts are absent, record a gate-blocked
evidence artifact instead of cloning, fetching, expanding the corpus, or using
synthetic replacements.

## Deliverables

- Durable P49-T3 bounded rerun gate evidence fixture.
- GitHub and DocC documentation for the P49-T3 result.
- Contract tests covering:
  - source linkage to P49-T2;
  - same six repository IDs and manifest path;
  - static-only-before-AI ordering;
  - all missing-checkout stop conditions, if any;
  - no clone/fetch/package manager/harvested-code execution boundaries;
  - proposal-only and no raw prompt/response/chain-of-thought boundaries;
  - carried-forward warning IDs and xyflow caveats;
  - next-state handoff to P49-T4 when the gate result is recorded.
- Validation report.
- Flow archive and review artifacts.

## Acceptance Criteria

- Same-scope gate evidence exists for the six P46 repositories, or a bounded
  gate-blocked artifact records exactly why the gate could not run.
- The task does not approve larger curated corpus planning.
- The task does not expand beyond the P46 six-repository scope.
- Static-only-before-AI ordering is preserved when execution reaches AI.
- AI output, static output, rerun output, targeted follow-up output, and
  adapter output are not accepted as registry truth.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.

## Boundaries

- Do not approve a larger curated corpus.
- Do not expand beyond the same six-repository bounded pilot scope.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.

## Validation

Run at minimum:

```bash
python3 -m json.tool tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/p49-t3-docc2context-ai-draft-same-scope-bounded-rerun-gate.example.json >/dev/null
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "docc2context_ai_draft_same_scope_bounded_rerun_gate or docc2context_ai_draft_targeted_follow_up_pass"
PYTHONPATH=src python3 -m pytest
python3 -m ruff format --check src tests
python3 -m ruff check src tests
swift package describe >/dev/null
swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs
git diff --check
```
