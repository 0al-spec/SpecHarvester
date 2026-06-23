# P48-T3 Validation Report

Task: P48-T3 Run Bounded Pilot Rerun Gate After AI Draft Blocker Follow-Up
Date: 2026-06-23

## Run Evidence

Static-only rerun:

```text
PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/inputs --out /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/output-static --skip-ai --repository-profile-selection auto
```

Result:

```text
exit code: 0
status: passed
processed: 6
failed repositories: 0
passed preflight: 6
```

AI-enabled rerun:

```text
PYTHONPATH=src python3 -m spec_harvester autonomous-candidate-batch /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/inputs --out /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/output-ai --repository-profile-selection auto --lm-studio-base-url http://127.0.0.1:1234 --lm-studio-model openai/gpt-oss-20b --json-repair-max-attempts 1
```

Result:

```text
exit code: 1
status: failed
processed: 6
failed repositories: 1
passed preflight: 6
AI draft proposals: 5
AI enrichment proposals: 6
```

## Digest Evidence

```text
058be58216a5a9e21a7a34040cb6f8dba4c5a8d05ec5875a628ca26d9897ab53  /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/inputs/repositories.yml
ed91f040ac028aae33622802407c820ac430da106d63237ce4890d7e52f72cd2  /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/output-static/autonomous-candidate-batch-report.json
b15d6a29e1c0de693e6bf0737c39a52d20d36ea8d67ffe81f11de1fc906054de  /tmp/specharvester-p48-t3-bounded-rerun-gate-20260623T000000Z/output-ai/autonomous-candidate-batch-report.json
60d863511a1b1de59be344fc9a1e4354ad323a6798d953ad19c438ed7f8dd6b8  tests/fixtures/ai_draft_blocker_follow_up_pass/p48-t2-ai-draft-blocker-follow-up-pass.example.json
```

## Repository Summary

| Repository | Batch status | Interface index | AI draft | AI enrichment |
| --- | --- | --- | --- | --- |
| `flask` | passed | complete | warning | warning |
| `gin` | passed | complete | warning | completed |
| `xyflow` | passed | partial | completed | completed |
| `cupertino` | passed | complete | warning | completed |
| `navigation-split-view` | passed | complete | warning | completed |
| `docc2context` | failed | complete | failed | completed |

P48-T2's explicit dispositions were enough to move `gin.aiDraft` and
`navigation-split-view.aiDraft` from hard failures to warning-level results.
The remaining hard blocker is `docc2context.aiDraft`, which exhausted one JSON
repair attempt and emitted `package_set_subject_metadata_missing`.

## Validation Commands

```text
python3 -m json.tool tests/fixtures/ai_draft_blocker_bounded_rerun_gate/p48-t3-ai-draft-blocker-bounded-rerun-gate.example.json >/dev/null
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "ai_draft_blocker_bounded_rerun_gate or ai_draft_blocker_follow_up_pass"
PYTHONPATH=src python3 -m pytest
python3 -m ruff check .
swift package describe >/dev/null
swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs
```

Result:

```text
json fixture validation passed
focused docs-contract tests: 2 passed, 172 deselected
full pytest: 905 passed, 1 skipped
ruff: All checks passed
swift package describe: passed
DocC generate-documentation: passed
```

## Decision

P48-T3 is complete as a bounded rerun gate. The next selected task is P48-T4
Record Post-Blocker Follow-Up Exit Decision.

Larger curated corpus planning remains blocked until P48-T4 records whether
the remaining `docc2context.aiDraft` blocker requires another targeted pass,
can be accepted as a non-blocking pilot caveat, or stops expansion.
