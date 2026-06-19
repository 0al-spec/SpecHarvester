# Repository Plugin Real Run: FastMCP

Status: Phase 38 real-repository plugin evidence.

P38-T6 ran a pinned local FastMCP checkout through the repository plugin
evidence path and compared it with the current Phase 37 repository profile
selection behavior. The goal was to validate the `SpecHarvesterRepositoryPluginApplicabilityReport`
sidecar path on a real repository without implementing runtime plugin loading
or a FastMCP-specific rule.

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

It uses:

```json
{
  "apiVersion": "spec-harvester.repository-plugin-real-run/v0",
  "kind": "SpecHarvesterRepositoryPluginRealRunComparison",
  "schemaVersion": 1
}
```

## Commands

The profile evidence run used repository-wide input and enabled automatic
profile selection:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/auto-inputs" \
  --out "$RUN_ROOT/auto-output" \
  --skip-ai \
  --repository-profile-selection auto
```

The sidecar run supplied a static plugin applicability report:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  "$RUN_ROOT/sidecar-inputs" \
  --out "$RUN_ROOT/sidecar-output" \
  --skip-ai \
  --repository-profile-selection auto \
  --repository-plugin-applicability "$RUN_ROOT/repository-plugin-applicability-report.json"
```

Both batch reports completed with `status: passed`.

## Profile Result

P37-T7 previously recorded a FastMCP fallback to `generic.repository.v0`. After
the P37-T8 harvested-manifest fallback, the current profile run selects a
single-package profile:

| Field | Value |
| --- | --- |
| Mode | `auto` |
| Decision | `selected` |
| Selected profile | `generic.single_package.v0` |
| Fallback profile | `generic.repository.v0` |
| Confidence | `high` |
| Reason | `root_manifest_present` |

The run still records the same real source shape:

| Metric | Value |
| --- | ---: |
| Harvested package manifests | `1` |
| Workspace inventory package manifests | `0` |
| Public interface entrypoints | `772` |
| Public interface symbols | `9199` |
| Candidate preflight errors | `0` |
| Candidate preflight warnings | `0` |

## Plugin Sidecar Result

The static `SpecHarvesterRepositoryPluginApplicabilityReport` selected three
generic plugin roles and rejected or blocked the roles that did not fit the
real single-package evidence:

| Decision | Count | Notes |
| --- | ---: | --- |
| `selectedPlugins[]` | `3` | `parser_profile`, `repository_profile`, `manifest_summary` |
| `rejectedPlugins[]` | `1` | `package_topology` rejected because no workspace members were present |
| `fallbackPlugins[]` | `0` | No fallback plugin was needed |
| `blockedPlugins[]` | `1` | `review_surface` blocked until topology hint evidence exists |
| `diagnostics[]` | `5` | `plugin_selected`, `plugin_rejected_low_confidence`, `plugin_blocked_required_evidence_missing` |

The autonomous batch copied the sidecar into:

```text
reports/repository-plugin-applicability/repository-plugin-applicability-report.json
```

and reported:

```json
{
  "repositoryPluginApplicability": {
    "status": "recorded",
    "appliedToDrafting": false,
    "registryAuthority": false
  }
}
```

In plain terms, the sidecar is `appliedToDrafting: false` and
`registryAuthority: false`.

## Verdict

```text
real_plugin_evidence_path_validated
```

The product meaning is narrow and useful:

- current repository profile selection handles this FastMCP root as
  `generic.single_package.v0`;
- repository plugin applicability evidence can be attached to the autonomous
  batch as a sidecar;
- plugin evidence remains review evidence and does not change drafting,
  parser behavior, profile scoring, or registry authority.

## Boundary

This real run is producer-side evidence only.

It does not:

- load third-party plugin code;
- execute plugins;
- run plugin code;
- clone or fetch repositories;
- install dependencies;
- execute harvested code;
- invoke package managers;
- run AI;
- change parser profile behavior;
- change repository profile scoring;
- accept packages;
- accept relations;
- publish registry metadata;
- remove `preview_only`;
- treat plugin decisions as registry truth;
- treat AI output as registry truth.
