# P49-T2 Execute docc2context AI Draft Targeted Follow-Up Pass

## Goal

Execute the targeted follow-up pass selected by P49-T1 for the remaining
`docc2context.aiDraft` blocker before the same-scope P49-T3 bounded rerun gate.

The pass must target only `docc2context.aiDraft`, constrain subject/member
metadata around `docc2context.core`, and clear or explicitly dispose the
previous `ai_json_repair_exhausted`, `ai_json_repair_needed`, and
`package_set_subject_metadata_missing` diagnostics.

## Context

P49-T1 selected:

```text
docc2context_ai_draft_targeted_follow_up_before_larger_curated_corpus
```

P48-T3 showed that the static-only same-scope bounded gate passed, but the
AI-enabled gate failed on `docc2context.aiDraft` with:

- `ai_json_repair_exhausted`
- `ai_json_repair_needed`
- `package_set_subject_metadata_missing`

P49-T2 must keep all AI output proposal-only. It is not registry authority and
does not approve larger curated corpus planning.

## Execution Plan

1. Verify P49-T1 plan evidence and the P46 six-repository source manifest.
2. Confirm the operator-local `docc2context` checkout required by
   `inputs/p46-bounded-popular-library-pilot/repositories.yml` is already
   available. Do not clone or fetch if it is absent.
3. Generate a deterministic workspace inventory for the existing local
   `docc2context` checkout, preserving `docc2context.core` as the subject.
4. Run only the package-set AI draft proposal path for `docc2context` with the
   local LM Studio provider:

   ```bash
   PYTHONPATH=src python3 -m spec_harvester package-set-ai-draft-proposal \
     <docc2context-workspace-inventory.json> \
     --source-checkout <docc2context-checkout> \
     --provider-base-url http://127.0.0.1:1234 \
     --provider-name lm_studio \
     --model openai/gpt-oss-20b \
     --json-repair-max-attempts 1 \
     --request-output <request.json> \
     --output <proposal.json>
   ```

5. Record durable P49-T2 execution evidence under
   `tests/fixtures/docc2context_ai_draft_targeted_follow_up_pass/`.
6. Document the result in GitHub docs and DocC.
7. Advance `SPECS/INPROGRESS/next.md` to P49-T3 only if P49-T2 records either
   `docc2context.aiDraft_completed` or
   `docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3`.

## Deliverables

- Durable P49-T2 execution evidence fixture.
- GitHub and DocC documentation for the targeted follow-up pass result.
- Contract tests covering:
  - P49-T2 source linkage to P49-T1;
  - target sidecar is exactly `docc2context.aiDraft`;
  - `docc2context.core` is present in subject/member metadata;
  - JSON repair exhaustion is absent or explicitly non-blocking;
  - `package_set_subject_metadata_missing` is absent or explicitly non-blocking;
  - proposal-only and no raw prompt/response/chain-of-thought boundaries;
  - P48 warning IDs and xyflow caveats remain visible.
- Validation report.
- Flow archive and review artifacts.

## Acceptance Criteria

- `docc2context.aiDraft` is recorded as `completed` or as an explicitly
  non-blocking `warning` for the P49-T3 rerun gate.
- `ai_json_repair_exhausted` is absent or explicitly disposed as non-blocking
  for P49-T3.
- `package_set_subject_metadata_missing` is absent or explicitly disposed as
  non-blocking for P49-T3.
- `docc2context.core` remains the selected subject/member identity.
- AI output remains proposal-only and is not accepted as registry truth.
- Raw prompts, raw provider responses, secrets, and chain-of-thought are not
  persisted.
- Larger curated corpus planning remains blocked until P49-T3 and P49-T4.

## Boundaries

- Do not approve a larger curated corpus.
- Do not run the same-scope bounded rerun in P49-T2.
- Do not expand beyond `docc2context.aiDraft`.
- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not run adapters or enable trusted local adapter execution.
- Do not clone or fetch repositories.
- Do not execute harvested code.
- Do not treat AI output, static output, targeted follow-up output,
  exit-decision output, plan output, or adapter output as registry truth.

## Validation

Run at minimum:

```bash
python3 -m json.tool tests/fixtures/docc2context_ai_draft_targeted_follow_up_pass/p49-t2-docc2context-ai-draft-targeted-follow-up-pass.example.json >/dev/null
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "docc2context_ai_draft_targeted_follow_up"
PYTHONPATH=src python3 -m pytest
python3 -m ruff format --check src tests
python3 -m ruff check src tests
swift package describe >/dev/null
swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs
git diff --check
```
