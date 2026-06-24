# P49-T3 Validation Report

Task: P49-T3 Run Same-Scope Bounded Rerun Gate
Date: 2026-06-25
Branch: `feature/P49-T3-run-same-scope-bounded-rerun-gate`

## Scope

P49-T3 attempted the same six-repository bounded rerun gate after P49-T2. The
gate stopped at operator-local checkout preflight because all six P46 checkout
paths were absent. The task did not clone, fetch, install dependencies, invoke
package managers, execute harvested code, run the static-only gate, run the
AI-enabled gate, run adapters, accept packages, accept relations, publish
registry metadata, seed baselines, remove `preview_only`, or approve larger
curated corpus planning.

## Preflight Evidence

The P46 source manifest resolved these missing checkout paths:

| Repository | Resolved checkout | Exists |
| --- | --- | --- |
| `flask` | `/Users/egor/Development/GitHub/0AL/flask` | false |
| `gin` | `/Users/egor/Development/GitHub/0AL/gin` | false |
| `xyflow` | `/Users/egor/Development/GitHub/0AL/xyflow` | false |
| `cupertino` | `/Users/egor/Development/GitHub/0AL/cupertino` | false |
| `navigation-split-view` | `/Users/egor/Development/GitHub/0AL/NavigationSplitView` | false |
| `docc2context` | `/Users/egor/Development/GitHub/0AL/docc2context` | false |

LM Studio availability was checked:

```bash
curl -sS --max-time 5 http://127.0.0.1:1234/v1/models
```

Result: passed; `openai/gpt-oss-20b` was listed.

## Validation Commands

```bash
python3 -m json.tool tests/fixtures/docc2context_ai_draft_same_scope_bounded_rerun_gate/p49-t3-docc2context-ai-draft-same-scope-bounded-rerun-gate.example.json >/dev/null
```

Result: passed.

```bash
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "docc2context_ai_draft_same_scope_bounded_rerun_gate or docc2context_ai_draft_targeted_follow_up_pass"
```

Result: passed, `2 passed, 176 deselected`.

```bash
python3 -m ruff format --check src tests
```

Result: passed, `131 files already formatted`.

```bash
PYTHONPATH=src python3 -m pytest
```

Result: passed, `909 passed, 1 skipped`.

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

PASS for bounded evidence recording. The P49-T3 gate result is:

```text
same_scope_bounded_rerun_gate_blocked_operator_local_checkouts_missing
```

P49-T4 is the next decision point. Larger curated corpus planning remains
blocked.
