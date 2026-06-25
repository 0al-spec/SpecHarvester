# P51-T6 Validation Report

**Task:** P51-T6 Hyperprompt AI Draft Single-Package Fallback
**Date:** 2026-06-25
**Verdict:** PASS

## Summary

P51-T6 repairs the reproducible `hyperprompt.aiDraft` hard blocker by adding a
deterministic producer-side fallback for exhausted JSON repair when the request
contains exactly one recoverable package subject.

The fallback keeps the sidecar proposal-only, preserves JSON repair diagnostics
as warning-level evidence, and leaves malformed multi-package AI draft output
blocking.

## Targeted Live Rerun

Command:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/p51-larger-curated-corpus \
  --select hyperprompt \
  --out /tmp/specharvester-p51-t6-hyperprompt-fallback-rerun-20260625T131341Z/output \
  --repository-profile-selection auto \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1 \
  --apply-ai-enrichment
```

Result:

```text
exit code: 0
batch status: passed
processed repositories: 1
failed repositories: 0
repository: hyperprompt
repository status: passed
aiDraft status: warning
aiDraft selected members: 1
aiDraft errors: 0
aiDraft stop policy: stop_for_author_review
aiEnrichment status: completed
aiEnrichedPreview status: prepared
```

Artifacts:

```text
run root: /tmp/specharvester-p51-t6-hyperprompt-fallback-rerun-20260625T131341Z
batch report digest: sha256:14bcf72675c758a68f59531799b804ccc803282b47d44b2986d2f2a43ac6090f
AI draft proposal digest: sha256:7f2e9c3c6433d2952d0cf8686b0fd56722275a9f776e164c747b1d74beac34e7
validation report digest: sha256:092fc097577e45e2094fe22f3dc0a8aa32cd177561201a5afc0acb6fd1733365
```

The repaired sidecar records:

```text
ai_json_repair_needed
ai_json_repair_exhausted
package_set_subject_metadata_missing
single_package_deterministic_fallback_applied
```

`ai_json_repair_exhausted` is warning-level with
`nonBlockingReason: deterministic_single_package_fallback`.

## Quality Gates

```bash
PYTHONPATH=src python3 -m pytest tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py -k "package_set_ai_draft or larger_curated_corpus_ai_enabled_gate or hyperprompt_ai_draft_single_package_fallback"
```

Result: `32 passed, 184 deselected`.

```bash
PYTHONPATH=src python3 -m pytest
```

Result: `918 passed, 1 skipped`.

```bash
python3 -m ruff format --check src tests && python3 -m ruff check src tests && git diff --check
```

Result: `131 files already formatted`; `All checks passed!`; no whitespace
errors.

```bash
PYTHONPATH=src python3 -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `918 passed, 1 skipped`; total coverage `90.49%`.

```bash
swift package dump-package >/dev/null && swift build --target SpecHarvesterDocs
```

Result: `Build of target: 'SpecHarvesterDocs' complete!`

## Boundary Checks

- Proposal-only authority preserved.
- No package or relation acceptance.
- No registry publication.
- No baseline seeding.
- No `preview_only` removal.
- No raw prompts, raw provider responses, secrets, or chain-of-thought
  persisted.
- No clone/fetch, dependency installation, package manager invocation, adapter
  execution, or harvested-code execution.

## Next State

P51-T7 should triage larger curated corpus output with Hyperprompt classified
as author-reviewable fallback evidence carrying a non-blocking single-package
fallback warning.
