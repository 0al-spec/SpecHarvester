# Limited Popular-Library Corpus Plan

Status: P30 operator plan for bounded corpus expansion.

This page defines the first limited popular-library scraping batch after the
P29 quality gate. It turns the
`ready_for_limited_popular_library_scraping` verdict into an operator-reviewed
source manifest and runbook before any larger scrape is executed.

The companion example manifest directory is:

```text
inputs/limited-popular-libraries/repositories.yml
```

## Scope

P30 is a limited corpus expansion, not broad autonomous harvesting.

The batch must:

- read only operator-provided local public checkouts;
- use pinned revisions or explicit refs from `inputs/*.yml`;
- include a small mix of single-package and package-set repositories;
- produce preview candidate artifacts for candidate-layer review;
- keep all generated output as `producer_preview_evidence_only`;
- leave SpecPM as validation, acceptance, relation, and registry authority.

The batch must not:

- clone repositories;
- fetch updates;
- install dependencies;
- run package managers, builds, tests, or package scripts;
- browse arbitrary network resources;
- publish registry metadata;
- accept packages or relations;
- seed baselines;
- remove `preview_only`;
- treat AI output as accepted SpecPM truth.

## Selection Criteria

The initial corpus should stay small enough that an operator can inspect every
candidate bundle. A repository belongs in the limited corpus only when it has:

- a local public checkout controlled by the operator;
- a pinned revision recorded in the manifest;
- a clear package id hint;
- a useful ecosystem shape for calibration;
- no requirement to execute repository-owned code during harvest.

Use shape diversity instead of collecting every framework in one ecosystem.
The first batch should include:

- Python single-package framework;
- Go single-package framework;
- JavaScript/TypeScript package-set workspace;
- Swift/SPM package;
- Swift/Xcode project-shaped package;
- documentation-first CLI package.

## Seed Corpus

The seed corpus is intentionally limited:

| Repository | Shape | Package id hint | Revision |
| --- | --- | --- | --- |
| Flask | Python single-package framework | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | Go single-package framework | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | JavaScript/TypeScript package-set workspace | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |
| Cupertino | Swift/SPM package-shaped checkout | `cupertino.core` | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` |
| NavigationSplitView | Swift/SPM + Xcode project-shaped checkout | `navigation_split_view.core` | `2c88df50b8f587560b91f6027e9ea275aee17060` |
| docc2context | Swift/SPM documentation-first CLI | `docc2context.core` | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` |

This seed corpus is an operator calibration set. It is not a registry allowlist
and does not imply that any generated candidate should enter SpecPM.
P32-T4 updates the current NavigationSplitView package id hint to
`navigation_split_view.core`; older P30/P31 reports still preserve the previous
`navigation-split-view.core` hint as historical identity-drift evidence.

## Manifest Shape

The P30 manifest uses the existing repository source manifest contract:

```yaml
repositories:
  - id: flask
    repository: https://github.com/pallets/flask
    revision: 954f5684e4841aad84a8eec7ace7b81a0d3f6831
    checkout: ../../../../flask
    packageId: flask.core
    labels: [python, web_framework, single_package, seed_corpus]
```

Operator checkout paths are machine-local examples. P30-T2 must verify that the
paths exist, are git worktrees, are clean enough for the run policy, and match
the pinned revisions before executing the batch.

Preview the manifest without collecting snapshots:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries
```

## P30 Runbook

P30-T2 deterministic gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out .smoke/limited-popular-libraries-deterministic \
  --skip-ai
```

P30-T3 live LM Studio gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out .smoke/limited-popular-libraries-live \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

P30-T4 triage:

- `candidate_layer_review_required`: valid starter package needs author or
  maintainer review.
- `needs_regeneration`: deterministic or AI diagnostics suggest another
  producer pass.
- `blocked`: required local evidence is missing or a hard gate failed.
- `not_for_intake`: output is useful for generator calibration but should not
  be handed to SpecPM.

P30-T5 handoff:

- prepare SpecPM handoff dry-run evidence only for selected candidates;
- keep `preview_only` until explicit SpecPM maintainer acceptance;
- do not treat producer receipt, AI proposal, or triage status as registry
  authority.

The selected handoff dry-run result is recorded in
[`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md)
with verdict `selected_handoff_dry_run_ready`.

## Stop Conditions

Stop the run, or mark the affected repository as blocked, when:

- a checkout path is missing;
- a checkout is not a git worktree;
- a checkout revision does not match the manifest;
- a checkout is dirty and the run policy requires clean input;
- deterministic collection or bundle-set preflight fails;
- live provider is unavailable for a live run;
- JSON repair is exhausted;
- AI proposal diagnostics indicate package id drift, unsupported evidence, or
  ungrounded claims that require regeneration.

## Expected Outputs

Later P30 tasks should produce:

- deterministic corpus report;
- live LM Studio corpus report;
- candidate-layer triage report;
- selected-candidate handoff dry-run evidence;
- docs and fixtures that preserve non-authority boundaries.

The expected product outcome is a bounded queue of reviewable valid starter
packages, not a larger automatic registry import.

P30-T2 records the deterministic corpus report in
[`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md)
with verdict `ready_for_live_lm_studio_limited_corpus`.

P30-T3 records the live LM Studio corpus report in
[`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md)
with verdict `ready_for_candidate_layer_triage`.

P30-T4 records the candidate-layer triage report in
[`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
with verdict `ready_for_selected_handoff_dry_run`.

## Related Contracts

- [`REPOSITORY_SOURCE_MANIFESTS.md`](REPOSITORY_SOURCE_MANIFESTS.md)
- [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md)
- [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md)
- [`AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`](AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md)
