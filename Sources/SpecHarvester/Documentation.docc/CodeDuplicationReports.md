# CodeDuplicationReports

`code-duplication-report` builds an advisory duplicate-code report for local
source quality review.

Use it to catch copied implementation policy before it drifts across modules:
filename allowlists, normalization predicates, schema fragments, report issue
codes, and similar deterministic logic.

```shell
python3 -m spec_harvester code-duplication-report \
  --path src/spec_harvester \
  --min-lines 8 \
  --output report/code-duplication.json
```

## Detection Behavior

- The report scans local source files only.
- The current built-in detector is dependency-free and Python-oriented.
- Blank lines, comments, imports, and simple punctuation-only lines are ignored
  before repeated line windows are fingerprinted.
- The default behavior is advisory and exits successfully even when duplicates
  are found.
- Passing `--fail-on-duplicates` returns a non-zero exit code when duplicate
  blocks are detected, which allows future baseline-aware CI enforcement.

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
