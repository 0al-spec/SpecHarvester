# Accepted Manifest Entries

Status: Bootstrap integration command

After a candidate is reviewed, operators can prepare a PR-ready accepted manifest
entry without mutating accepted package directories yet. This keeps proposal
preparation deterministic and review-friendly.

## Command

Prepare a manifest entry for a reviewed candidate:

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest /Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml
```

The command:

- reads `<candidate>/specpm.yaml` metadata;
- derives `packageId` and `packageVersion`;
- writes `<manifest>` entry as `public-index/generated/<packageId>/<packageVersion>`;
- uses deterministic insertion for `packages` list location in the manifest; and
- returns machine-readable JSON with manifest update status.

## Options

- `--manifest` (required)
  path to `accepted-packages.yml`.

- `--manifest-entry-path`
  explicit `path` to write; overrides prefix and subdir.

- `--manifest-entry-prefix`
  prefix used when path is inferred; default `public-index/generated`.

- `--package-subdir`
  explicit package subdir instead of `<packageId>/<packageVersion>`.

## Output

Successful output resembles:

```json
{
  "status": "ok",
  "candidate": "candidates/github.com/example/project",
  "packageId": "example.core",
  "packageVersion": "0.1.0",
  "packageSubdir": "example.core/0.1.0",
  "manifest": {
    "path": "/Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml",
    "entry": "public-index/generated/example.core/0.1.0",
    "updated": true
  }
}
```

`updated: false` indicates the same entry was already present.

## Trust Boundary

The command reads only the candidate directory and manifest file.
It does not:

- run `specpm` validation;
- copy candidate directories;
- fetch remotes;
- install dependencies;
- run repository code.

It is a deterministic preparation step for later review and proposal workflows.
