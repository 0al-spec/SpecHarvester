# P32-T3 Validation Report: Xyflow Package-Set Identity Regeneration Dry Run

**Date:** 2026-06-13
**Verdict:** PASS

## Scope

P32-T3 ran the P32-T2 deferred candidate regeneration runbook for `xyflow`
only and recorded the package-set identity dry-run evidence.

The dry run produced:

- `xyflow.workspace`
- `xyflow.react`
- `xyflow.svelte`
- `xyflow.system`

The recorded candidate-layer decision is
`candidate_layer_review_required` with `selectedHandoffEligible: true`.

## Run Evidence

```bash
PYTHONPATH=src python -m spec_harvester source-manifests \
  inputs/limited-popular-libraries \
  > .smoke/p32-deferred-regeneration/20260613T181500Z/source-manifest-validation.json
```

Result: passed. The local xyflow checkout existed, was a git worktree, was
clean, and matched revision `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd`.

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --select xyflow \
  --out .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

Result: passed. The batch processed `xyflow`, skipped the other five limited
corpus repositories, produced 4 candidates and 3 relations, and bundle-set
preflight passed with warning count `0` and error count `0`.

```bash
PYTHONPATH=src python -m spec_harvester render-package-set-site \
  --bundle-set .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/package-sets/xyflow \
  --output .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/viewer
```

Result: passed. The viewer reported `status: ok`, `candidateCount: 4`, and
`relationCount: 3`.

```bash
PYTHONPATH=src python -m spec_harvester preflight-bundle-set \
  .smoke/p32-deferred-regeneration/20260613T181500Z/xyflow/package-sets/xyflow
```

Result: passed.

## Fixture

Recorded fixture:

```text
tests/fixtures/xyflow_package_set_identity_regeneration/p32-t3-xyflow-package-set-identity-regeneration.example.json
```

The fixture records package-set identity `xyflow.workspace`, member package
ids, relation topology, key artifact digests, preflight/viewer summaries,
author-ready status, and the non-authority boundary.

## Validation

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py -q
```

Result: `73 passed`

```bash
PYTHONPATH=src pytest -q
```

Result: `649 passed, 1 skipped`

```bash
PYTHONPATH=src ruff check .
```

Result: passed

```bash
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90
```

Result: `649 passed, 1 skipped`; coverage `90.56%`

```bash
swift package dump-package >/tmp/specharvester-p32-t3-package.json
swift build --target SpecHarvesterDocs
```

Result: passed

```bash
rm -rf /tmp/specharvester-p32-t3-docc-build-spec
swift package --allow-writing-to-directory /tmp/specharvester-p32-t3-docc-build-spec \
  generate-documentation \
  --target SpecHarvester \
  --output-path /tmp/specharvester-p32-t3-docc-build-spec \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester
```

Result: passed. The command emitted pre-existing unrelated DocC warnings for
`AcceptedPackageUpdateProposals` and `RealRepositoryQualityReport`.

## Boundary

- No broad limited-corpus rerun was performed.
- No Cupertino or NavigationSplitView regeneration was performed.
- No accepted-source files were changed.
- No SpecPM repository files were changed.
- No package or relation was accepted.
- No baseline was seeded.
- No `preview_only` marker was removed.
- No registry metadata was published.
