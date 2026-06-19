# Repository Plugin Real Run: FastMCP

Status: Phase 38 real-repository plugin evidence.

P38-T6 ran a pinned local FastMCP checkout through the repository plugin
evidence path and compared it with the current Phase 37 repository profile
selection behavior. The run validates
`SpecHarvesterRepositoryPluginApplicabilityReport` as static sidecar evidence,
not runtime plugin execution.

## Source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/jlowin/fastmcp` |
| Local checkout | `/Users/egor/Development/GitHub/fastmcp` |
| Revision | `3b8538e2422a1c43fdb69661c610de7985b785f2` |
| Run root | `/tmp/specharvester-p38-t6-fastmcp-20260619T005454Z` |
| AI mode | disabled through `--skip-ai` |
| Network | not required |

The durable summary fixture lives at:

```text
tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json
```

It declares `apiVersion: spec-harvester.repository-plugin-real-run/v0`,
`kind: SpecHarvesterRepositoryPluginRealRunComparison`, and `schemaVersion: 1`.

## Commands

Profile evidence run:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

Plugin sidecar run:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/sidecar-inputs" \
  --out "$RUN_ROOT/sidecar-output" \
  --skip-ai \
  --repository-profile-selection auto \
  --repository-plugin-applicability "$RUN_ROOT/repository-plugin-applicability-report.json"
```

Both batch reports completed with `status: passed`.

## Result

P37-T7 previously recorded a FastMCP fallback to `generic.repository.v0`. The
current run selects `generic.single_package.v0` with `confidence: high` because
the harvested manifest fallback exposes `root_manifest_present` evidence.

The run records:

- public interface entrypoints: `772`;
- public interface symbols: `9199`;
- candidate preflight status: `passed`;
- author-ready status: `author_ready_draft`;
- `repositoryPluginApplicability` sidecar status: `recorded`;
- sidecar selected count: `3`;
- sidecar rejected count: `1`;
- sidecar blocked count: `1`;
- `appliedToDrafting: false`;
- `registryAuthority: false`.

## Verdict

```text
real_plugin_evidence_path_validated
```

Current repository profile selection handles this FastMCP root as a generic
single package, while repository plugin applicability remains review evidence.
The sidecar does not change drafting, parser behavior, profile scoring, or
registry authority.

## Boundary

This real run is producer-side evidence only. It does not load third-party
plugin code, execute plugins, run plugin code, clone or fetch repositories,
install dependencies, execute harvested code, invoke package managers, run AI,
change parser profile behavior, change repository profile scoring, accept
packages, accept relations, publish registry metadata, remove `preview_only`,
treat plugin decisions as registry truth, or treat AI output as registry truth.
