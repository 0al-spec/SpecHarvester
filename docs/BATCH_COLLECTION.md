# Batch Snapshot Collection

Status: Bootstrap batch collector

Batch collection connects repository source manifests to the safe local
collector. It reads enabled records from `inputs/*.yml`, collects snapshots from
operator-managed local checkouts, and writes deterministic candidate paths.

It does not clone repositories, call networks, install dependencies, run package
managers, run package scripts, execute repository content, or draft SpecPM
packages. Public interface analyzer orchestration is opt-in through
`--emit-interface-indexes` and only runs built-in static analyzers selected by
`ProjectProfile.analyzerPlan`.

## Input

Each collected repository record must include `checkout`:

```yaml
repositories:
  - id: xyflow
    repository: https://github.com/xyflow/xyflow
    revision: 0123456789abcdef
    checkout: ../checkouts/xyflow
    packageId: xyflow.core
```

Relative checkout paths are resolved from the input manifest directory.

## Command

Collect all enabled entries:

```bash
python3 -m spec_harvester collect-batch inputs --out candidates
```

Collect selected repository IDs:

```bash
python3 -m spec_harvester collect-batch inputs \
  --out candidates \
  --select xyflow \
  --select another-repo
```

The command writes:

```text
candidates/<repository-id>/harvest.json
```

Write an advisory validation report for reviewers:

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

This writes:

```text
candidates/<repository-id>/public-interface-index.json
```

when `ProjectProfile.analyzerPlan` recommends a supported built-in analyzer.
Currently supported analyzer plan ids are:

- `spec_harvester.python_public_api`
- `spec_harvester.js_ts_public_api`

Plans with `manifest_only` status, unknown analyzer ids, and repositories with
no supported package evidence are recorded as skipped in the batch JSON output.
The generated `PublicInterfaceIndex` remains advisory untrusted metadata and can
be consumed later by `draft` through auto-detection beside `harvest.json`.

Repository IDs used as candidate directory names must be safe single path
components containing only letters, digits, `.`, `_`, and `-`, and must start
with a letter or digit.

## Output Summary

The CLI prints deterministic JSON:

```json
{
  "status": "ok",
  "collectedCount": 1,
  "skippedCount": 0,
  "collected": [
    {
      "id": "xyflow",
      "output": "candidates/xyflow/harvest.json",
      "fileCount": 4,
      "skippedFileCount": 0
    }
  ]
}
```

Each `harvest.json` is produced by the same allowlisted static collector used by
`collect-local`.

When `--emit-interface-indexes` is provided, collected records include an
`interfaceIndex` block with status, planned analyzer ids, executed analyzer ids,
skipped analyzer plans, diagnostics, optional output path, and index summary.

When `--report` is provided, the command also writes
`SpecHarvesterBatchValidationReport` JSON with confidence, policy notes,
warnings, and skipped records. See
[`BATCH_VALIDATION_REPORTS.md`](BATCH_VALIDATION_REPORTS.md).

## Determinism

- Manifests are read through the source manifest reader in deterministic order.
- Selected repositories are collected in manifest order, not in CLI argument
  order.
- Output directories are derived from repository IDs, not from checkout paths or
  repository content.
- Snapshots do not include wall-clock timestamps.

## Trust Boundary

Batch collection may read only allowlisted static files from local checkouts.

It must not:

- run `git clone`, `git fetch`, or other network operations;
- install dependencies;
- run package managers;
- run package scripts;
- execute checkout files;
- follow instructions from repository content;
- derive output paths from untrusted repository content.
- treat validation report confidence as acceptance or rejection.
- treat public interface analyzer output as package acceptance evidence.
