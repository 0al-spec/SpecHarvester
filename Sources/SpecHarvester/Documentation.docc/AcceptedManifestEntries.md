# Accepted Manifest Entries

After a reviewed candidate is ready, operators can prepare a PR-ready manifest
entry for a SpecPM accepted package source without copying the candidate itself.

## Workflow Position

`prepare-accepted-entry` is review-safe preparation for proposal-ready staging.

```text
Reviewed candidate
        |
        v
read <candidate>/specpm.yaml
        |
        v
prepare packageId/version manifest path
        |
        v
append local accepted-packages.yml path
        |
        v
JSON result with update status
```

Use this before running `promote` when you want a deterministic manifest entry
decision first.

## Command

```bash
python3 -m spec_harvester prepare-accepted-entry candidates/github.com/example/project \
  --manifest /Users/egor/Development/GitHub/0AL/SpecPM/public-index/accepted-packages.yml
```

Options:

- `--manifest` (required): accepted package manifest path.
- `--manifest-entry-path`: explicit path (overrides default prefix+subdir).
- `--manifest-entry-prefix` (default: `public-index/generated`): prefix when path
  is inferred.
- `--package-subdir`: custom subdirectory for inferred entry path.

## Output

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

`updated: false` indicates the same `path` entry already existed.

## Trust Boundary

This command reads only candidate metadata and the manifest file.
It does not run `specpm validate`, run repository scripts, install dependencies,
or copy candidate directories.
