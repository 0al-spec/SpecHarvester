# Batch Collection

Batch collection reads repository source manifests, collects snapshots from
operator-managed local checkouts, and writes deterministic candidate paths.

It is a thin orchestration layer over the safe static collector. It does not
clone repositories, contact networks, install dependencies, run package
managers, run package scripts, execute checkout files, or draft SpecPM packages.
Public interface analyzer orchestration is opt-in through
`--emit-interface-indexes` and only runs built-in static analyzers selected by
`ProjectProfile.analyzerPlan`.

## Command

Collect all enabled repositories:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

Collect selected repository IDs:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow
```

Write an advisory validation report:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --report candidates/batch-validation.json
```

Opt in to built-in static public interface analyzer orchestration:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --emit-interface-indexes \
  --analyzer-cache-dir candidates/.analyzer-cache
```

This writes `candidates/<repository-id>/public-interface-index.json` when
`ProjectProfile.analyzerPlan` recommends a supported built-in analyzer:

- `spec_harvester.python_public_api`
- `spec_harvester.js_ts_public_api`
- `spec_harvester.go_public_api`

Plans with `manifest_only` status, unknown analyzer ids, and repositories with
no supported package evidence are recorded as skipped in the batch JSON output.
The generated `PublicInterfaceIndex` remains advisory untrusted metadata and can
be consumed later by `draft` through auto-detection beside `harvest.json`.

## Output Layout

Each collected repository writes:

```text
candidates/<repository-id>/harvest.json
candidates/<repository-id>/public-interface-index.json
```

`public-interface-index.json` is written only when `--emit-interface-indexes` is
enabled and at least one supported analyzer plan runs.

Repository IDs used as candidate directory names must be safe single path
components containing only letters, digits, `.`, `_`, and `-`, and must start
with a letter or digit.

## Determinism

- Source manifests are read in deterministic order.
- Selected repositories are collected in manifest order.
- Output paths are derived from repository IDs.
- Snapshots do not contain wall-clock timestamps.

## Trust Boundary

Batch collection reads only allowlisted static files from local checkouts.

It must not clone, fetch, install dependencies, run package managers, run
package scripts, execute checkout files, follow repository instructions, or
derive output paths from repository content. Public interface analyzer output is
advisory evidence, not package acceptance evidence.

## References

- `docs/BATCH_COLLECTION.md`
- <doc:BatchValidationReports>
- <doc:RepositorySourceManifests>
- <doc:Workflow>
- <doc:TrustBoundary>
