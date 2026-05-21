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
    smoke-triage.json
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

## Multi-Language Synthetic Matrix

The test suite includes a synthetic multi-language smoke matrix that creates
tiny local checkouts under `tmp_path`, runs `collect-batch`, and verifies
`ProjectProfile` output without cloning repositories or committing generated
candidates.

The matrix covers:

- npm JavaScript/TypeScript package evidence
- SPM Swift package evidence
- Gradle/Maven Java/Kotlin project evidence
- Go modules evidence
- Composer PHP package evidence
- CMake C/C++ project evidence
- Xcode/CocoaPods Objective-C/iOS project evidence
- RubyGems/Bundler package evidence
- Python packaging evidence
- a documentation-first manifest-poor README fixture with `semanticHints` and
  language-neutral `semantic_intent_static_evidence`

The matrix verifies languages, ecosystems, analyzer plan ids/statuses,
diagnostics, strict public license evidence, and documentation semantic fallback
behavior. Generated smoke outputs remain ignored local artifacts and should not
be committed.

Do not commit generated smoke outputs.

## Popular Flask/Gin Smoke

Use this scenario for popular web-framework repository shapes. The committed
pytest coverage uses synthetic Flask/Gin fixtures; this recipe describes the
real local checkout run with generated smoke outputs kept under `.smoke/output/`.

Create a dedicated manifest:

```bash
mkdir -p .smoke/inputs .smoke/output
checkout_root="$(cd ../.. && pwd)"
flask_revision="$(git -C "${checkout_root}/flask" rev-parse HEAD)"
gin_revision="$(git -C "${checkout_root}/gin" rev-parse HEAD)"

cat > .smoke/inputs/popular.yml <<YAML
repositories:
  - id: flask
    repository: https://github.com/pallets/flask
    revision: ${flask_revision}
    checkout: "${checkout_root}/flask"
    packageId: flask.core
    labels: [python, flask, popular-smoke, license-txt]

  - id: gin
    repository: https://github.com/gin-gonic/gin
    revision: ${gin_revision}
    checkout: "${checkout_root}/gin"
    packageId: gin.core
    labels: [go, gin, popular-smoke]
YAML
```

Keep strict public preflight enabled:

```bash
git -C "${checkout_root}/flask" diff --cached --quiet
git -C "${checkout_root}/gin" diff --cached --quiet
```

Collect with deterministic public interface indexes:

```bash
PYTHONPATH=src python -m spec_harvester collect-batch .smoke/inputs \
  --out .smoke/output/popular-candidates \
  --report .smoke/output/popular-batch-validation.json \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/analyzer-cache \
  --select flask \
  --select gin
```

Expected collection checks:

- Flask accepts `LICENSE.txt` as strict public license evidence.
- Gin reads `go.mod` and emits `public-interface-index.json` through
  `spec_harvester.go_public_api`.
- Analyzers keep `execution: none`, `networkAccess: none`, and
  `packageScripts: not_run`.

Draft preview-only candidates:

```bash
PYTHONPATH=src python -m spec_harvester draft .smoke/output/popular-candidates/flask \
  --package-id flask.core \
  --name Flask \
  --out .smoke/output/popular-candidates/flask

PYTHONPATH=src python -m spec_harvester draft .smoke/output/popular-candidates/gin \
  --package-id gin.core \
  --name Gin \
  --out .smoke/output/popular-candidates/gin
```

Expected draft checks:

- Both candidates include `preview_only: true`.
- Both candidates include `intent.web.framework_surface`,
  `intent.web.http_routing`, `intent.web.middleware_pipeline`, and
  `intent.web.request_response_context`.
- Both candidates keep `kind: public_interface_index` evidence with
  `artifactKind: SpecHarvesterPublicInterfaceIndex`.
- SpecPM validation may still report `preview_only_package`, but should not
  report `unknown_evidence_kind` or `evidence_support_target_unknown`.

Validate with SpecPM when available:

```bash
specpm validate .smoke/output/popular-candidates/flask --json
specpm validate .smoke/output/popular-candidates/gin --json
```

Generate governance reports and a smoke triage summary:

```bash
PYTHONPATH=src python -m spec_harvester governance-report \
  --candidates-root .smoke/output/popular-candidates \
  --output .smoke/output/popular-governance-claims.json

PYTHONPATH=src python -m spec_harvester governance-upstream-report \
  --candidates-root .smoke/output/popular-candidates \
  --output .smoke/output/popular-namespace-upstream.json

PYTHONPATH=src python -m spec_harvester governance-license-provenance-report \
  --candidates-root .smoke/output/popular-candidates \
  --output .smoke/output/popular-license-provenance.json

PYTHONPATH=src python -m spec_harvester smoke-triage-summary \
  --batch-validation .smoke/output/popular-batch-validation.json \
  --governance-claims .smoke/output/popular-governance-claims.json \
  --namespace-upstream .smoke/output/popular-namespace-upstream.json \
  --license-provenance .smoke/output/popular-license-provenance.json \
  --output .smoke/output/popular-smoke-triage.json
```

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

The default mode is strict for public SpecPM.dev intake. staged git changes fail
preflight, and missing allowlisted `LICENSE`/`COPYING` evidence is reported as
`missing_license_file` with `status: error`. Use `--relaxed-private` only for
private-code spec coverage. A generated batch report with `status: error` makes
`collect-batch` exit non-zero.

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

## Triage Summary

Build a compact review summary from the detailed smoke reports:

```bash
PYTHONPATH=src python -m spec_harvester smoke-triage-summary \
  --batch-validation .smoke/output/batch-validation.json \
  --governance-claims .smoke/output/governance-claims.json \
  --namespace-upstream .smoke/output/namespace-upstream.json \
  --license-provenance .smoke/output/license-provenance.json \
  --output .smoke/output/smoke-triage.json
```

The summary keeps the detailed report paths and groups batch, duplicate,
namespace/upstream, and license/provenance signals into one reviewable JSON
object.

## Reproducibility Checklist

- Pin `revision` to each checkout's `git rev-parse HEAD`.
- Keep `checkout` paths local and operator-owned.
- Keep generated files under `.smoke/output/`.
- Recreate `.smoke/inputs/repositories.yml` when fixture revisions change.
- Keep checkout staging areas empty before strict public smoke runs.
- Ensure public candidates include allowlisted `LICENSE`/`COPYING` evidence.
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
