# P34-T2 Autonomous Batch AI Enriched Preview Output

## Summary

Add an explicit opt-in autonomous batch mode that applies clean AI enrichment
proposals into copied enriched preview candidates.

P34-T1 added `apply-ai-enrichment-proposal` for one candidate bundle. P34-T2
connects that helper to `autonomous-candidate-batch` so a live AI-enabled run
can emit reviewable enriched preview candidates beside the existing
proposal-only AI artifacts.

## Motivation

- AI-enabled usage is the preferred practical path for improving generated
  starter specs before author review.
- Autonomous runs currently write `package-set-ai-enrichment-proposal.json`,
  but operators must manually apply each clean proposal afterward.
- Batch output should make the clean path obvious while preserving
  `preview_only`, non-authority boundaries, and deterministic review evidence.

## Deliverables

1. Add an explicit `autonomous-candidate-batch` opt-in option for enriched
   preview output.
2. Apply clean AI enrichment proposals by reusing the P34-T1 apply helper.
3. Write enriched preview candidates under a separate batch output subtree, not
   over the generated source candidates.
4. Emit `ai-enrichment-candidate-patch.json` reports for each applied
   candidate.
5. Record per-repository and summary counts in
   `autonomous-candidate-batch-report.json`.
6. Leave default autonomous batch behavior proposal-only.
7. Update docs, DocC, tests, and Flow validation evidence.

## Output Shape

When enabled, each successful package-set run may write:

```text
package-sets/<repository-id>/enriched/<package-id>/
  specpm.yaml
  specs/*.spec.yaml
  producer-receipt.json
  validation-report.json
  diagnostics.json
  ai-enrichment-candidate-patch.json
```

The existing generated candidate bundle remains under the existing candidate
output path and must not be mutated.

## Acceptance Criteria

- The CLI exposes an explicit opt-in flag; existing invocations remain
  proposal-only and preserve current report shape except for extension-safe
  summary defaults.
- Enriched output is attempted only when AI is enabled and an enrichment
  proposal exists.
- A proposal is applied only when the P34-T1 helper accepts it as clean,
  completed, package-aligned, preview-only, and diagnostic-free.
- Failed, warning-bearing, missing, or unsupported proposals remain sidecar-only
  and are counted as skipped rather than treated as batch failures.
- Patch reports include before/after digests and preserve the non-authority
  boundary.
- Batch reports include enough summary data for review tooling to distinguish
  `applied`, `skipped`, and `failed` enriched preview attempts.
- Tests prove default behavior remains unchanged, opt-in output writes an
  enriched candidate copy, and warning-bearing proposals do not emit enriched
  output.

## Non-Goals

- No SpecPM package acceptance.
- No relation acceptance.
- No baseline seeding.
- No `preview_only` removal.
- No source candidate mutation.
- No registry publication.
- No SpecPM pull request creation.
- No raw prompt or raw model response persistence.
- No automatic application when proposal diagnostics are warnings or failures.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_ai_enrichment_candidate_patch.py tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- DocC static generation command from `.github/workflows/docs.yml`
