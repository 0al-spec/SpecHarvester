# P49-T2 Validation Report

Task: P49-T2 Execute docc2context AI Draft Targeted Follow-Up Pass
Date: 2026-06-24
Branch: `feature/P49-T2-execute-docc2context-ai-draft-targeted-follow-up-pass`

## Scope

P49-T2 executed the targeted package-set AI draft proposal path for
`docc2context.aiDraft` only. It did not run the same-scope bounded rerun gate,
expand the corpus, run adapters, accept packages, accept relations, publish
registry metadata, seed baselines, remove `preview_only`, clone or fetch
repositories, install dependencies, invoke package managers, execute harvested
code, or persist raw prompts, raw provider responses, secrets, or
chain-of-thought.

## Live Targeted Run

LM Studio availability was confirmed through:

```bash
curl -sS --max-time 5 http://127.0.0.1:1234/v1/models
```

Result: passed; `openai/gpt-oss-20b` was listed.

The operator-local checkout from the P46 manifest resolved to:

```text
/Users/egor/Development/GitHub/0AL/docc2context
```

Result: absent. P49-T2 did not clone or fetch. The targeted run used a
source-manifest-backed minimal workspace inventory for `docc2context.core`.

The targeted AI draft command was:

```bash
PYTHONPATH=src python3 -m spec_harvester package-set-ai-draft-proposal /tmp/specharvester-p49-t2-docc2context-ai-draft-20260624T204500Z/input/workspace-inventory.json --provider-base-url http://127.0.0.1:1234 --provider-name lm_studio --model openai/gpt-oss-20b --json-repair-max-attempts 1 --request-output /tmp/specharvester-p49-t2-docc2context-ai-draft-20260624T204500Z/output/request.json --output /tmp/specharvester-p49-t2-docc2context-ai-draft-20260624T204500Z/output/proposal.json
```

Result: passed with exit code `0`.

Observed result:

- status: `warning`
- selected outcome: `docc2context.aiDraft_warning_explicitly_non_blocking_for_p49_t3`
- current warning: `excluded_package_also_selected`
- JSON repair: `not_needed`
- total tokens: `1198`
- selected member: `docc2context.core`
- raw prompt persisted: `false`
- raw provider response persisted: `false`
- chain-of-thought persisted: `false`

## Validation Commands

```bash
python3 -m json.tool tests/fixtures/docc2context_ai_draft_targeted_follow_up_pass/p49-t2-docc2context-ai-draft-targeted-follow-up-pass.example.json >/dev/null
```

Result: passed.

```bash
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "docc2context_ai_draft_targeted_follow_up"
```

Result: passed, `2 passed, 175 deselected`.

```bash
python3 -m ruff format --check src tests
```

Result: passed, `131 files already formatted`.

```bash
PYTHONPATH=src python3 -m pytest
```

Result: passed, `908 passed, 1 skipped`.

```bash
python3 -m ruff check src tests
```

Result: passed, `All checks passed!`.

```bash
swift package describe >/dev/null
```

Result: passed.

```bash
swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs
```

Result: passed; documentation archive generated at `.build/docs`.

```bash
git diff --check
```

Result: passed.

## Result

PASS for P49-T2. The previous `docc2context.aiDraft` blockers
`ai_json_repair_exhausted`, `ai_json_repair_needed`, and
`package_set_subject_metadata_missing` are cleared or explicitly disposed for
the P49-T3 bounded rerun gate.

Larger curated corpus planning remains blocked until P49-T3 runs the same-scope
bounded rerun gate and P49-T4 records the exit decision.
