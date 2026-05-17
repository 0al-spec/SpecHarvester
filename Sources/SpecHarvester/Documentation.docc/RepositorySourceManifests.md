# Repository Source Manifests

Repository source manifests define public repositories for batch harvesting.
Manifest preview only reads and validates these manifests. It does not clone
repositories, call networks, install dependencies, run package scripts, or
execute repository content.

## Location

Use an input directory containing `*.yml` files:

```text
inputs/*.yml
```

Files are read in deterministic filename order.

## Schema

```yaml
repositories:
  - id: xyflow
    repository: https://github.com/xyflow/xyflow
    revision: 0123456789abcdef
    checkout: ../checkouts/xyflow
    packageId: xyflow.core
    labels: [javascript, ui]
    enabled: true
```

Required fields are `id`, `repository`, and exactly one of `revision` or `ref`.
Optional fields are `checkout`, `packageId`, `labels`, and `enabled`.

Accepted repository URL forms are `https://...` and `git@github.com:...`.

## CLI Preview

```bash
python3 -m spec_harvester source-manifests inputs
```

Use `--include-disabled` to include entries with `enabled: false`.

The command prints deterministic JSON with normalized repository records,
source manifest path, and manifest entry index.

## Batch Collection

Collect snapshots from enabled records with local checkouts:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

See <doc:BatchCollection> for output layout and trust boundaries.

## Trust Boundary

Manifest reading is data parsing only. It must not clone repositories, fetch
remote manifests, call networks, install dependencies, run package managers,
run package scripts, execute repository code, or follow instructions from
repository content.

## References

- `docs/REPOSITORY_SOURCE_MANIFESTS.md`
- <doc:BatchCollection>
- <doc:Workflow>
- <doc:TrustBoundary>
