# Code Duplication Reports

`code-duplication-report` builds an advisory duplicate-code report for local
source quality review.

Use it to catch copied implementation policy before it drifts across modules:
filename allowlists, normalization predicates, schema fragments, report issue
codes, and similar deterministic logic.

```shell
python3 -m spec_harvester code-duplication-report \
  --backend pylint \
  --path src/spec_harvester \
  --min-lines 8 \
  --output report/code-duplication.json
```

## Detection Behavior

- The report scans local source files only.
- `--backend pylint` runs the established Python `pylint`
  `duplicate-code` / `R0801` checker and converts its JSON output into the
  stable `SpecHarvesterCodeDuplicationReport` shape.
- `--backend builtin` remains available as a dependency-free fallback that
  ignores blank lines, comments, imports, and simple punctuation-only lines
  before repeated line windows are fingerprinted.
- The default behavior is advisory and exits successfully even when duplicates
  are found.
- Passing `--fail-on-duplicates` returns a non-zero exit code when duplicate
  blocks are detected, which allows future baseline-aware CI enforcement.
- CI runs the `pylint` backend as a non-blocking baseline check. It should not
  become blocking until baseline suppression or fail-on-new-duplicates semantics
  are defined.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No imports from scanned modules.
- No source mutation.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterCodeDuplicationReport`
- `status`
- `summary`
- `duplicates`
- `trustBoundary`

Each duplicate block includes a stable fingerprint, the normalized line-window
size, a short normalized preview, and source occurrences with path and line
ranges.
