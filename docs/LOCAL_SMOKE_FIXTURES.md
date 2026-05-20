# Local Smoke Fixtures

Status: Local operator workflow

Local smoke fixtures are reproducible, low-cost checks against real adjacent
repository checkouts. They are intended to exercise SpecHarvester on real input
shape without cloning repositories, installing harvested dependencies, running
package managers, running package scripts, or promoting generated candidates.

## Directory Convention

Use one ignored local workspace:

```text
.smoke/
  inputs/
    repositories.yml
  output/
    candidates/
    batch-validation.json
    governance-claims.json
    namespace-upstream.json
    license-provenance.json
    smoke-triage.json
```

The `.smoke/` directory is ignored by Git. Legacy local scratch directories
`smoke-inputs/` and `smoke-output*/` are also ignored so old smoke runs do not
pollute repository status.

## Fixture Manifest

From the SpecHarvester repository root, generate the input manifest for the
adjacent repository layout used during local validation:

```bash
mkdir -p .smoke/inputs .smoke/output
checkout_root="$(cd ../.. && pwd)"

cat > .smoke/inputs/repositories.yml <<YAML
repositories:
  - id: cupertino
    repository: git@github.com:mihaelamj/cupertino.git
    revision: 65dcae238d30cfbd0d9d15ae10f7b8c67575c19b
    checkout: "${checkout_root}/cupertino"
    packageId: cupertino.core
    labels: [swift, local-smoke]

  - id: xyflow
    repository: git@github.com:SoundBlaster/xyflow.git
    revision: a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd
    checkout: "${checkout_root}/xyflow"
    packageId: xyflow.core
    labels: [typescript, local-smoke]

  - id: docc2context
    repository: git@github.com:SoundBlaster/docc2context.git
    revision: a2babcc4910c87bbd1b65f9a4221097f5ae4b753
    checkout: "${checkout_root}/docc2context"
    packageId: docc2context.core
    labels: [swift, local-smoke]

  - id: puzzle
    repository: https://github.com/SoundBlaster/Puzzle
    revision: fd7daf17b60ba562c4aa41eff1332b0e97477005
    checkout: "${checkout_root}/Puzzle"
    packageId: puzzle.core
    labels: [swift, local-smoke]
YAML
```

If a checkout has moved, update only its `checkout` value. If the local `Puzzle`
checkout later receives an `origin` remote, keep `repository` aligned with that
public URL. The collector records the URL as provenance metadata and does not
fetch it.

## Multi-Language Synthetic Matrix

The committed test suite also carries a synthetic multi-language smoke matrix.
It creates tiny local checkouts under `tmp_path`, runs `collect-batch`, and
verifies `ProjectProfile` output without cloning repositories or writing
generated candidates into the repository.

The matrix covers:

- npm JavaScript/TypeScript package evidence;
- SPM Swift package evidence;
- Gradle/Maven Java/Kotlin project evidence;
- Go modules evidence;
- Composer PHP package evidence;
- CMake C/C++ project evidence;
- Xcode/CocoaPods Objective-C/iOS project evidence;
- RubyGems/Bundler package evidence;
- Python packaging evidence;
- a documentation-first manifest-poor README fixture with `semanticHints` and
  language-neutral `semantic_intent_static_evidence`.

The matrix verifies languages, ecosystems, analyzer plan ids/statuses,
diagnostics, strict public license evidence, and documentation semantic fallback
behavior. It is a regression guard for the deterministic collector and drafter;
it is not a registry acceptance decision.

Generated smoke outputs remain ignored local artifacts. Do not commit
`.smoke/output/`, `smoke-output*/`, synthetic batch output, or generated
candidate directories.

Do not commit generated smoke outputs.

## Collection

Validate the manifest without reading checkout files:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/inputs
```

Collect all enabled fixture snapshots:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/candidates \
  --report .smoke/output/batch-validation.json
```

This default is strict for public SpecPM.dev intake:

- staged git changes in any checkout fail preflight;
- missing allowlisted `LICENSE`/`COPYING` evidence produces
  `missing_license_file` and `status: error` in `batch-validation.json`.
- a generated batch report with `status: error` makes `collect-batch` exit
  non-zero.

For private-code spec coverage, add `--relaxed-private` explicitly.

Collect one repository when iterating on a targeted bug:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/candidates \
  --report .smoke/output/batch-validation.json \
  --select xyflow
```

## Drafting Candidates

Draft each collected candidate explicitly so package ids are stable:

```bash
PYTHONPATH=src python -m spec_harvester draft .smoke/output/candidates/cupertino \
  --package-id cupertino.core \
  --out .smoke/output/candidates/cupertino

PYTHONPATH=src python -m spec_harvester draft .smoke/output/candidates/xyflow \
  --package-id xyflow.core \
  --out .smoke/output/candidates/xyflow

PYTHONPATH=src python -m spec_harvester draft .smoke/output/candidates/docc2context \
  --package-id docc2context.core \
  --out .smoke/output/candidates/docc2context

PYTHONPATH=src python -m spec_harvester draft .smoke/output/candidates/puzzle \
  --package-id puzzle.core \
  --out .smoke/output/candidates/puzzle
```

The output remains preview-only. Do not copy `.smoke/output/candidates/*` into
`accepted/` unless a separate review and promotion task explicitly requires it.

## Review Reports

Generate advisory reports from the smoke candidates:

```bash
PYTHONPATH=src python -m spec_harvester governance-report \
  --candidates-root .smoke/output/candidates \
  --output .smoke/output/governance-claims.json

PYTHONPATH=src python -m spec_harvester governance-upstream-report \
  --candidates-root .smoke/output/candidates \
  --output .smoke/output/namespace-upstream.json

PYTHONPATH=src python -m spec_harvester governance-license-provenance-report \
  --candidates-root .smoke/output/candidates \
  --output .smoke/output/license-provenance.json
```

Reports are review signals only. They do not accept, reject, publish, install,
or execute package content.

## Triage Summary

Build a compact summary that points back to the detailed reports:

```bash
PYTHONPATH=src python -m spec_harvester smoke-triage-summary \
  --batch-validation .smoke/output/batch-validation.json \
  --governance-claims .smoke/output/governance-claims.json \
  --namespace-upstream .smoke/output/namespace-upstream.json \
  --license-provenance .smoke/output/license-provenance.json \
  --output .smoke/output/smoke-triage.json
```

The summary reports:

- batch error count;
- batch warning count;
- duplicate intent/capability claim count;
- namespace/upstream issue count;
- license/provenance issue count;
- detailed report paths for drill-down review.

## Reproducibility Checklist

- Pin `revision` to each checkout's `git rev-parse HEAD`.
- Keep `checkout` paths operator-owned and local.
- Keep generated files under `.smoke/output/`.
- Recreate `.smoke/inputs/repositories.yml` when fixture revisions change.
- Keep checkout staging areas empty before strict public smoke runs.
- Ensure public candidates include allowlisted `LICENSE`/`COPYING` evidence.
- Do not run package managers inside harvested checkouts.
- Do not run harvested package scripts, tests, or build commands from harvested
  repositories.
- Do not install harvested dependencies.
- Do not grant smoke runs access to secrets or private credentials.
- Commit only source, docs, tests, and Flow artifacts.

## Trust Boundary

The smoke workflow reuses `source-manifests`, `collect-batch`, `draft`, and
governance report commands. It reads allowlisted static files from local
checkouts and writes derived candidate evidence to an ignored output root.

It must not:

- Do not clone or fetch repositories.
- Do not install harvested dependencies.
- Do not run harvested package managers.
- Do not run harvested package scripts.
- Do not execute harvested repository code.
- Do not promote generated candidates into accepted source.
