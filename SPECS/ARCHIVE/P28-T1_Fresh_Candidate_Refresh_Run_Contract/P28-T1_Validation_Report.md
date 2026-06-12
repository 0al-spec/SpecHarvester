# P28-T1 Validation Report

Verdict: PASS
Date: 2026-06-12

## Scope

P28-T1 added the fresh candidate refresh run bridge between SpecHarvester and
SpecPM:

- `SpecHarvesterFreshCandidateRefreshRun`
- `fresh-candidate-refresh-run` CLI command
- SpecPM-compatible fresh generated root layout:
  `<package_id>/<version>/specpm.yaml` and `specs/*.spec.yaml`
- contract-file SHA-256 digests for manifests and boundary specs
- SpecPM consumer metadata for
  `specpm producer-bundle prepare-refresh-decision`
- GitHub docs, DocC, roadmap, workplan, and docs-contract coverage

The command prepares review evidence and filesystem layout only. It does not
run SpecPM, mutate SpecPM sources, publish registry metadata, or accept
packages.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_fresh_candidate_refresh_run.py tests/test_docs_contracts.py -q
```

Result: passed, `50 passed`.

```bash
PYTHONPATH=src pytest -q
```

Result: passed, `592 passed, 1 skipped`.

```bash
PYTHONPATH=src pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: passed, `592 passed, 1 skipped`; total coverage `90.12%`.

```bash
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: passed.

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
rm -rf .docc-build && \
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvester \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester; \
rc=$?; rm -rf .docc-build; exit $rc
```

Result: passed. Existing unrelated DocC warnings remain for
`AcceptedPackageUpdateProposals` references and inline command references in
`RealRepositoryQualityReport`.

## CLI Smoke

```bash
rm -rf /tmp/specharvester-p28-t1 && mkdir -p /tmp/specharvester-p28-t1

PYTHONPATH=src python3 -m spec_harvester xyflow-package-set-smoke \
  --output /tmp/specharvester-p28-t1/xyflow-smoke \
  >/tmp/specharvester-p28-t1/xyflow-smoke-report.json

PYTHONPATH=src python3 -m spec_harvester fresh-candidate-refresh-run \
  --bundle-set /tmp/specharvester-p28-t1/xyflow-smoke/package-set \
  --fresh-generated-root /tmp/specharvester-p28-t1/fresh-generated \
  --output /tmp/specharvester-p28-t1/fresh-candidate-refresh-run.json \
  >/tmp/specharvester-p28-t1/fresh-candidate-refresh-run.stdout.json
```

Observed result:

- status: `prepared`
- runId: `fresh-candidate-refresh-3bae061342f36b9e`
- packages:
  - `xyflow.workspace`
  - `xyflow.react`
  - `xyflow.svelte`
  - `xyflow.system`
- fresh root: `/private/tmp/specharvester-p28-t1/fresh-generated`
- each package has `0.1.0/specpm.yaml` and `0.1.0/specs/*.spec.yaml`
- `specpmConsumer.command` is
  `specpm producer-bundle prepare-refresh-decision`

## Boundary Checks

- The command reads local package-set JSON/YAML artifacts only.
- It copies generated candidates into a normalized root.
- It records digests for contract-bearing files only.
- It records `producerEvidenceAuthority: evidence_only`.
- It records `noRegistryMutation: true`.
- It does not execute harvested repository code.
- It does not run package managers.
- It does not mutate SpecPM curated artifacts.
- It does not publish registry metadata.
- It does not replace SpecPM maintainer review.
