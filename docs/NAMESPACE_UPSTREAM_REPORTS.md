# Namespace and Upstream Relationship Reports

Status: Governance review

Namespace and upstream relationship reports summarize `specpm.yaml` metadata for
candidate and accepted package review.

These checks are advisory and designed to help maintainers review package
ownership signals before acceptance.

## Report Command

Build the report from one or more metadata roots:

```bash
python3 -m spec_harvester governance-upstream-report \
  --accepted-root accepted \
  --candidates-root candidates \
  --output report/namespace-upstream.json
```

The command:

- scans every `specpm.yaml` under `--accepted-root` and `--candidates-root`;
- extracts package `metadata.id`, `metadata.version`, package `namespace`, and
  `foreignArtifacts`;
- identifies duplicated namespaces;
- validates upstream relationship presence and origin consistency for
  `foreignArtifacts` entries with `id: upstream_repository`;
- returns deterministic JSON on stdout.

If `--output` is provided, the report is written as stable JSON to that path.

At least one of `--accepted-root` or `--candidates-root` must be provided.

## Report Structure

The report contains:

- `schemaVersion`
- `kind: SpecHarvesterNamespaceUpstreamReviewReport`
- `status`: `ok` or `partial` when issues were found;
- `summary` with counts (records, duplicate namespaces, missing upstream,
  mismatch/invalid upstream, issue count);
- `records` for all parsed packages with namespace and upstream artifacts;
- `duplicates.namespace` for overlapping namespaces;
- `issues` for malformed or suspicious upstream metadata; and
- `trustBoundary` advisory notes.

## Current Warnings / Checks

- `missing_upstream_repository`: no `id: upstream_repository` found.
- `duplicate_upstream_repository_entries`: more than one upstream repository
  artifact per package.
- `invalid_upstream_repository_uri`: malformed or unparseable upstream URI.
- `upstream_namespace_mismatch`: package namespace does not match inferred
  upstream owner.

## Trust Boundary

The report command reads local `specpm.yaml` files only.

It does not:

- execute repository scripts;
- install dependencies;
- run analyzers;
- clone repositories;
- write candidate or accepted package content.
