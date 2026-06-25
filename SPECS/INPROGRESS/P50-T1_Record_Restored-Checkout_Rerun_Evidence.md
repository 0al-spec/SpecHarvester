# P50-T1 Record Restored-Checkout Rerun Evidence

## Objective

Record the restored-checkout same-scope bounded rerun evidence after the
operator-local paths expected by the P46 manifest were restored through local
symlinks.

P50-T1 must preserve the history of P49-T4: P49-T4 was correct for the evidence
available at the time. P50-T1 adds new evidence after the environment was
restored and updates the current planning decision from checkout-blocked to
reconsideration-ready.

## Inputs

- `SPECS/INPROGRESS/next.md`
- `SPECS/Workplan.md`
- `tests/fixtures/docc2context_follow_up_exit_decision/p49-t4-docc2context-follow-up-exit-decision.example.json`
- `inputs/p46-bounded-popular-library-pilot/repositories.yml`
- Local rerun output:
  `/tmp/specharvester-p49-t3-rerun-after-checkout-restore-20260625T004309`

## Execution Evidence

The restored local paths are symlinks under `/Users/egor/Development/GitHub/0AL/`
to pinned checkouts under `/Users/egor/Development/GitHub/`:

- `flask`
- `gin`
- `xyflow`
- `cupertino`
- `NavigationSplitView`
- `docc2context`

The repeated gate already ran in the correct order:

1. static-only `autonomous-candidate-batch --skip-ai`;
2. AI-enabled `autonomous-candidate-batch` through LM Studio
   `openai/gpt-oss-20b`.

## Deliverables

- Machine-readable P50-T1 restored-checkout rerun evidence fixture.
- GitHub Markdown and DocC documentation explaining:
  - restored checkout provenance;
  - static-only gate result;
  - AI-enabled gate result;
  - remaining warning/caveat evidence;
  - current larger-corpus planning state;
  - no-authority boundaries.
- Cross-links from docs indexes, capabilities, roadmap, and DocC topics.
- Current `next.md` updated to the post-rerun state.
- Workplan updated to mark P50-T1 complete.
- Focused docs-contract test coverage.
- Validation report and archived Flow artifacts.

## Acceptance Criteria

- The fixture references P49-T4 by path, digest, `apiVersion`, `kind`, and
  `authority`.
- The fixture references the P46 manifest by path and digest.
- The fixture records all six restored checkout symlinks and pinned revisions.
- The fixture records the static-only gate as passed: processed `6`, failed
  `0`, passed preflight `6`.
- The fixture records the AI-enabled gate as passed: exit code `0`, processed
  `6`, failed `0`, passed preflight `6`, AI draft proposals `6`, AI enrichment
  proposals `6`.
- The fixture records remaining warnings:
  - AI draft warnings on Flask, Gin, Cupertino, NavigationSplitView, and
    docc2context;
  - AI enrichment warnings on Flask, xyflow, and NavigationSplitView;
  - xyflow partial interface index.
- The fixture records raw prompts, raw provider responses, secrets, and
  chain-of-thought as not persisted.
- The decision is explicit: larger curated corpus planning is
  reconsideration-ready, not registry-approved.
- All non-authority boundaries remain explicit.

## Non-Goals

- Do not accept packages or relations.
- Do not publish registry metadata, seed baselines, or remove `preview_only`.
- Do not clone or fetch repositories.
- Do not install dependencies.
- Do not invoke package managers.
- Do not execute harvested code.
- Do not run adapters or enable trusted local adapter execution.
- Do not treat static, AI, rerun, targeted follow-up, exit-decision, or adapter
  output as registry truth.

## Validation

Run at minimum:

```bash
python3 -m json.tool tests/fixtures/restored_checkout_rerun_evidence/p50-t1-restored-checkout-rerun-evidence.example.json >/dev/null
PYTHONPATH=src python3 -m pytest tests/test_docs_contracts.py -k "restored_checkout_rerun_evidence or docc2context_follow_up_exit_decision"
python3 -m ruff format --check src tests
PYTHONPATH=src python3 -m pytest
python3 -m ruff check src tests
swift package describe >/dev/null
swift package --allow-writing-to-directory .build/docs generate-documentation --target SpecHarvester --output-path .build/docs
git diff --check
```
