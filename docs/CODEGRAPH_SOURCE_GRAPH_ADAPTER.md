# CodeGraph Source Graph Adapter

Status: Optional adapter boundary

`codegraph-source-graph-index` normalizes pre-existing CodeGraph evidence into
a SpecHarvester-owned `source_graph_index` payload.

The command is an adapter boundary. It does not install CodeGraph, run `npx`,
download platform bundles, or index repositories. Operators must provide an
already-produced JSON output or SQLite database.

## Command

```bash
python3 -m spec_harvester codegraph-source-graph-index \
  --input codegraph.json \
  --input-format json \
  --source-target-kind folder \
  --source-target-path Sources \
  --analyzer-version 0.9.7 \
  --output source-graph-index.json
```

SQLite input is also supported when an existing CodeGraph database is provided:

```bash
python3 -m spec_harvester codegraph-source-graph-index \
  --input .codegraph/codegraph.db \
  --input-format sqlite \
  --output source-graph-index.json
```

## JSON Identity

```json
{
  "schemaVersion": "spec-harvester-codegraph-v1",
  "kind": "source_graph_index"
}
```

The normalized payload records:

- trust policy for the third-party local binary;
- source repository, revision, target kind, and target path;
- input artifact path and SHA-256 digest;
- optional executable path and SHA-256 digest;
- source file digests when CodeGraph evidence includes them;
- bounded file, node, edge, and diagnostic records.

## Trust Boundary

Every payload declares:

```json
{
  "trustLevel": "untrusted_optional_tool",
  "classification": "third_party_local_binary",
  "executedRepositoryCode": false,
  "allowedNetwork": false,
  "installation": "out_of_band_required"
}
```

`source_graph_index` is assistive producer evidence. It is not SpecPM registry
authority and cannot accept a package, relation, or capability claim by itself.

## Safety Rules

- CodeGraph must be installed or run out of band by the operator.
- The command reads only the provided JSON or SQLite artifact and optional
  executable file for digesting.
- Unsafe absolute paths, parent traversal, empty paths, and backslash paths are
  rejected before output is produced.
- Node and edge output is bounded by `--max-nodes` and `--max-edges`.
- Truncation is represented as diagnostics, not silent data loss.

## P20-T7 Boundary

This adapter does not verify the live CodeGraph executable, npm package
integrity, CLI flags, or upstream compatibility. That pinned interface guard is
owned by `P20-T7`.
