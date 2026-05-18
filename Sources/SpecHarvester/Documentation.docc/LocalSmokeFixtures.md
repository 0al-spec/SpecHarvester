# Local Smoke Fixtures

Use local smoke fixtures to rerun SpecHarvester against real adjacent
repository checkouts without committing generated candidates.

## Directory Convention

Use one ignored workspace:

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
```

The `.smoke/` directory is ignored by Git. Legacy local scratch directories
`smoke-inputs/` and `smoke-output*/` are also ignored.

## Fixture Manifest

From the SpecHarvester repository root, create a manifest for the adjacent
repository layout:

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

If a checkout moves, update only its `checkout` value. If the local `Puzzle`
checkout later gets an `origin` remote, keep `repository` aligned with that
public URL. The URL is provenance metadata and is not fetched.

## Collection

Validate the manifest:

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/inputs
```

Collect all enabled snapshots:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/candidates \
  --report .smoke/output/batch-validation.json
```

Collect one target while iterating:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/candidates \
  --report .smoke/output/batch-validation.json \
  --select xyflow
```

## Drafting

Draft candidates explicitly:

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

Generated candidates stay preview-only until a separate review and promotion
task accepts them.

## Review Reports

Generate advisory reports:

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

## Reproducibility Checklist

- Pin `revision` to each checkout's `git rev-parse HEAD`.
- Keep `checkout` paths local and operator-owned.
- Keep generated files under `.smoke/output/`.
- Recreate `.smoke/inputs/repositories.yml` when fixture revisions change.
- Do not install harvested dependencies.
- Do not run harvested package managers.
- Do not run harvested package scripts.
- Do not execute harvested repository code.
- Do not grant smoke runs secret access.

## Trust Boundary

The smoke workflow reads allowlisted static files and writes derived evidence to
an ignored output root.

- Do not clone or fetch repositories.
- Do not install harvested dependencies.
- Do not run harvested package managers.
- Do not run harvested package scripts.
- Do not execute harvested repository code.
- Do not promote generated candidates into accepted source.
- Do not publish harvested content.

## References

- `docs/LOCAL_SMOKE_FIXTURES.md`
- <doc:RepositorySourceManifests>
- <doc:BatchCollection>
- <doc:BatchValidationReports>
- <doc:GovernanceReports>
- <doc:NamespaceUpstreamReports>
- <doc:LicenseProvenanceRiskReports>
