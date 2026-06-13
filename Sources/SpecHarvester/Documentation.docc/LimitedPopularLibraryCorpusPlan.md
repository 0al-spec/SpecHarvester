# Limited Popular-Library Corpus Plan

This page defines the P30 operator plan for the first bounded corpus expansion
after the P29 `ready_for_limited_popular_library_scraping` quality gate.

The companion source manifest is:

```text
inputs/limited-popular-libraries.example.yml
```

## Boundary

The limited corpus reads only operator-provided local public checkouts. It does
not clone repositories, fetch updates, install dependencies, run package
managers, execute package scripts, publish registry metadata, accept packages,
accept relations, seed baselines, remove `preview_only`, or treat AI output as
accepted SpecPM truth.

All output remains `producer_preview_evidence_only` until author review and
explicit SpecPM maintainer acceptance.

## Seed Corpus

| Repository | Shape | Package id hint | Revision |
| --- | --- | --- | --- |
| Flask | Python single-package framework | `flask.core` | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` |
| Gin | Go single-package framework | `gin.core` | `5f4f9643258dc2a65e684b63f12c8d543c936c67` |
| xyflow | JavaScript/TypeScript package-set workspace | `xyflow.workspace` | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` |
| Cupertino | Swift/SPM package-shaped checkout | `cupertino.core` | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` |
| NavigationSplitView | Swift/SPM + Xcode project-shaped checkout | `navigation-split-view.core` | `2c88df50b8f587560b91f6027e9ea275aee17060` |
| docc2context | Swift/SPM documentation-first CLI | `docc2context.core` | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` |

The seed corpus provides shape diversity. It is not a registry allowlist and
does not imply SpecPM acceptance.

## Manifest

The manifest uses the existing repository source manifest shape:

```yaml
repositories:
  - id: flask
    repository: https://github.com/pallets/flask
    revision: 954f5684e4841aad84a8eec7ace7b81a0d3f6831
    checkout: ../../../flask
    packageId: flask.core
    labels: [python, web_framework, single_package, seed_corpus]
```

Preview the manifest:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests inputs
```

## P30 Runbook

Deterministic gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs \
  --out .smoke/limited-popular-libraries-deterministic \
  --skip-ai
```

Live LM Studio gate:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs \
  --out .smoke/limited-popular-libraries-live \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Triage states are `candidate_layer_review_required`, `needs_regeneration`,
`blocked`, and `not_for_intake`.

Stop conditions include missing checkouts, non-git checkouts, revision mismatch,
dirty input when clean input is required, deterministic preflight failure,
provider unavailability, exhausted JSON repair, package id drift, unsupported
evidence, or ungrounded claims.

See also <doc:RepositorySourceManifests>, <doc:AutonomousCandidateBatch>,
<doc:AutonomousCandidateIntakePolicy>, and
<doc:AutonomousCandidateCorpusQualityGate>.
