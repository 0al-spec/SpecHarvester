# Single-Package Deferred Candidate Regeneration Dry Run

Status: P32-T4 recorded dry-run evidence.

This report records a bounded regeneration dry run for the two P30/P31
deferred single-package candidates:

- `cupertino.core`;
- `navigation_split_view.core`.

It follows the operator procedure in
[`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
and records which candidates can re-enter refreshed candidate-layer review.

## Input

The run used the limited popular-library source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

P32-T4 updates the current NavigationSplitView manifest hint to
`navigation_split_view.core`. The previous `navigation-split-view.core` hint is
retained only as historical identity-drift evidence from P30/P31 reports.

The operator verified the local checkouts before the dry run:

```text
repository id: cupertino
checkout: /Users/egor/Development/GitHub/cupertino
revision: 65dcae238d30cfbd0d9d15ae10f7b8c67575c19b
worktree: clean

repository id: navigation-split-view
checkout: /Users/egor/Development/GitHub/NavigationSplitView
revision: 2c88df50b8f587560b91f6027e9ea275aee17060
worktree: clean
```

Source manifest validation was recorded at:

```text
.smoke/p32-deferred-regeneration/20260613T184534Z/source-manifest-validation.json
```

## Command

The dry run was scoped to `cupertino` and `navigation-split-view` only:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --select cupertino \
  --select navigation-split-view \
  --out .smoke/p32-deferred-regeneration/20260613T184534Z/single-package \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Static viewers and candidate preflights were rendered separately for each
candidate:

```bash
PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/cupertino/cupertino.core \
  --output .smoke/p32-deferred-regeneration/20260613T184534Z/viewer/cupertino.core

PYTHONPATH=src python -m spec_harvester preflight-candidate-bundle \
  .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/cupertino/cupertino.core

PYTHONPATH=src python -m spec_harvester render-spec-site \
  --candidate .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/navigation-split-view/navigation_split_view.core \
  --output .smoke/p32-deferred-regeneration/20260613T184534Z/viewer/navigation_split_view.core

PYTHONPATH=src python -m spec_harvester preflight-candidate-bundle \
  .smoke/p32-deferred-regeneration/20260613T184534Z/single-package/package-sets/navigation-split-view/navigation_split_view.core
```

The machine-readable summary fixture is:

```text
tests/fixtures/single_package_deferred_candidate_regeneration/p32-t4-single-package-deferred-candidate-regeneration.example.json
```

It uses:

```json
{
  "apiVersion": "spec-harvester.single-package-deferred-regeneration-dry-run/v0",
  "kind": "SpecHarvesterSinglePackageDeferredCandidateRegenerationDryRun",
  "schemaVersion": 1
}
```

## Result

The dry run processed exactly two repositories:

```text
selected: cupertino, navigation-split-view
skipped: flask, gin, xyflow, docc2context
```

It produced two preview candidates:

```text
cupertino.core
navigation_split_view.core
```

Both candidates retained `preview_only: true`, produced valid validation
reports, clean diagnostics, static viewer output, and clean producer preflight:

```json
{
  "candidateCount": 2,
  "passedPreflightCount": 2,
  "warningCount": 0,
  "errorCount": 0
}
```

No package relation proposals were produced because both repositories are
single-package candidates.

## Candidate Decisions

### Cupertino

`cupertino.core` regenerated a valid preview candidate:

```text
bundle-set preflight: passed
candidate preflight: passed
static viewer: ok
authorReadyDraft.status: author_ready_draft
```

However, the live LM Studio AI enrichment proposal still reported:

```text
refined_summary_missing
```

The recorded candidate-layer decision remains:

```text
needs_regeneration
selectedHandoffEligible: false
```

Product verdict: `cupertino.core` should stay deferred until regenerated
enrichment supplies a refined summary or author-curated summary evidence is
attached.

### NavigationSplitView

`navigation_split_view.core` regenerated under the chosen canonical id:

```text
canonicalPackageId: navigation_split_view.core
rejectedOrAliasedPackageIds: navigation-split-view.core
bundle-set preflight: passed
candidate preflight: passed
static viewer: ok
authorReadyDraft.status: author_ready_draft
```

The generated `specpm.yaml`, validation report, candidate preflight,
bundle-set preflight, and viewer output all agree on
`navigation_split_view.core`.

The AI draft proposal retained a warning-level `excluded_package_unknown`
diagnostic. P32-T4 records that warning as proposal-only context rather than
registry truth. The deterministic source manifest, generated candidate, clean
preflight, and viewer evidence prove the actual single-package identity for
this dry run.

The recorded candidate-layer decision is:

```text
candidate_layer_review_required
selectedHandoffEligible: true
```

Product verdict: the NavigationSplitView identity blocker is resolved enough
for `navigation_split_view.core` to re-enter P32-T5 refreshed candidate-layer
triage if no later review blocks it.

## Boundary

This dry run is producer evidence only. It does not accept packages, accept
relations, seed baselines, remove `preview_only`, publish registry metadata,
create a SpecPM pull request, or treat AI output as registry truth.

SpecPM remains the validation, relation, acceptance, and registry authority.

## See Also

- [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md)
- [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md)
- [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
