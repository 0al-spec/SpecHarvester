# Repository Source Manifests

Status: Bootstrap input format

Repository source manifests define the public repositories that later batch
harvesting tasks may collect. P3-T1 only reads and validates these manifests.
It does not clone repositories, call networks, install dependencies, run package
scripts, or execute repository content.

## Location

Place manifests under an input directory, conventionally:

```text
inputs/*.yml
```

Files are read in deterministic filename order. Only `*.yml` is supported in
the bootstrap parser.

## Schema

The supported YAML subset is intentionally small:

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

Required fields:

- `id`: stable repository source id, unique across all loaded manifests.
- `repository`: source repository URL.
- exactly one of `revision` or `ref`.

Optional fields:

- `checkout`: operator-managed local checkout path for later collection.
- `packageId`: default package id hint for later drafting.
- `labels`: inline list of review labels.
- `enabled`: boolean; `false` entries are skipped by default.

Accepted repository URL forms:

- `https://...`
- `git@github.com:...`

## CLI Preview

Read and validate manifests without collecting anything:

```bash
python3 -m spec_harvester source-manifests inputs
```

Include disabled entries:

```bash
python3 -m spec_harvester source-manifests inputs --include-disabled
```

The command prints deterministic JSON containing normalized repository records,
source manifest path, and manifest entry index.

## Trust Boundary

Manifest reading is data parsing only.

It must not:

- clone repositories;
- fetch remote manifests;
- call network resources;
- install dependencies;
- run package managers;
- run package scripts;
- execute repository code;
- follow instructions from repository content.

Batch collection belongs to later tasks and must continue to use pinned
revisions, bounded local checkouts, and explicit validation.
