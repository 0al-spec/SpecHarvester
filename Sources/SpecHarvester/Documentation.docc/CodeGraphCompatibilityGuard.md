# CodeGraph Compatibility Guard

Status: Offline compatibility report

`codegraph-compatibility-report` validates the pinned CodeGraph interface
fixture used by the optional `source_graph_index` adapter.

The command is designed for ordinary CI. It does not install CodeGraph, run
`npm` or `npx`, download platform bundles, or index third-party repositories.

## Command

```bash
python3 -m spec_harvester codegraph-compatibility-report \
  --fixture tests/fixtures/codegraph_compatibility/codegraph-0.9.7.json \
  --output codegraph-compatibility.json
```

When a pre-provisioned executable is intentionally available, operators may add
`--executable /path/to/codegraph`.

The executable probe runs only the fixture-declared version command with
`CODEGRAPH_NO_DOWNLOAD=1`; it does not index a repository.

## Report Identity

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterCodeGraphCompatibilityReport"
}
```

The report verifies pinned package metadata, the `optional_preprovisioned`
binary contract, download-disabled environment, JSON CLI command names, fixture
sample mapping into `source_graph_index`, and optional local executable version
output.

Required JSON CLI commands are `status`, `query`, `files`, `callers`,
`callees`, `impact`, and `affected`.

## Failure Policy

The CLI returns `0` when passed, `1` when compatibility checks fail, and `2` for
invalid inputs. The absence of a CodeGraph executable is a skipped check, not a
failure.

## Boundary

This guard checks interface compatibility, not CodeGraph quality on real
repositories. Live indexing remains an explicit operator action outside normal
CI.
