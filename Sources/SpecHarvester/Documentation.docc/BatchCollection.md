# Batch Collection

Batch collection reads repository source manifests, collects snapshots from
operator-managed local checkouts, and writes deterministic candidate paths.

It is a thin orchestration layer over the safe static collector. It does not
clone repositories, contact networks, install dependencies, run package
managers, run package scripts, execute checkout files, draft SpecPM packages, or
run public interface analyzers.

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

## Output Layout

Each collected repository writes:

```text
candidates/<repository-id>/harvest.json
```

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
derive output paths from repository content.

## References

- `docs/BATCH_COLLECTION.md`
- <doc:RepositorySourceManifests>
- <doc:Workflow>
- <doc:TrustBoundary>
