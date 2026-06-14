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

When a pre-provisioned executable is intentionally available, operators may add:

```bash
  --executable /path/to/codegraph
```

The executable probe runs only the fixture-declared version command with
`CODEGRAPH_NO_DOWNLOAD=1`; it does not index a repository.

## Report Identity

```json
{
  "schemaVersion": 1,
  "kind": "SpecHarvesterCodeGraphCompatibilityReport"
}
```

The report verifies:

- pinned package name, version, license, integrity, and shasum metadata;
- binary availability contract: `optional_preprovisioned`;
- download-disabled environment: `CODEGRAPH_NO_DOWNLOAD=1`;
- required JSON CLI commands: `status`, `query`, `files`, `callers`,
  `callees`, `impact`, and `affected`;
- fixture sample mapping into `schemaVersion:
  spec-harvester-codegraph-v1` and `kind: source_graph_index`;
- optional local executable version output when an executable path is provided.

## Failure Policy

The CLI returns:

- `0` when the report status is `passed`;
- `1` when fixture compatibility checks fail;
- `2` for invalid inputs or unreadable fixture files.

The absence of a CodeGraph executable is a skipped check, not a failure. This
keeps ordinary CI offline and reproducible.

## Boundary

This guard checks interface compatibility, not CodeGraph quality on real
repositories. Live indexing remains an explicit operator action outside normal
CI.
