# Procedural Style Report

`procedural-style-report` builds an advisory procedural-style metrics report for
local Python source review.

Use it to measure whether EO refactoring work is actually moving behavior out of
large procedural modules and into behavior-rich objects.

```shell
python3 -m spec_harvester procedural-style-report \
  --path src/spec_harvester \
  --output report/procedural-style.json
```

Optional hotspot failure mode:

```shell
python3 -m spec_harvester procedural-style-report \
  --path src/spec_harvester \
  --hotspot-min-top-level-count 15 \
  --hotspot-min-top-level-span 300 \
  --fail-on-hotspots
```

## Detection Behavior

- The report scans local Python source files only.
- Repeated or overlapping `--path` values are deduplicated before analysis.
- Files that cannot be read or parsed are reported as explicit skipped files.
- The report measures top-level function count and span, method count and span,
  class count, behavior-rich class count, DTO-only class count, exception-like
  class count, module hotspots, and largest top-level functions.
- Behavior-rich classes are counted conservatively: a class must own at least
  two non-dunder methods and not be classified as exception-like.
- DTO-only classes are counted conservatively: a class must be dataclass-like,
  have no non-dunder methods, and not be exception-like.
- The default behavior is advisory and exits successfully even when hotspots are
  found.
- Passing `--fail-on-hotspots` returns a non-zero exit code when hotspot files
  are detected under the configured thresholds.
- CI should treat this report as a baseline and review aid until the project
  explicitly decides on a blocking policy.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No imports from scanned modules.
- No source mutation.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterProceduralStyleReport`
- `status`
- `summary`
- `skippedFiles`
- `fileMetrics`
- `hotspots`
- `largestTopLevelFunctions`
- `trustBoundary`

The summary includes repository-wide counts and shares for:

- `topLevelFunctionCount`
- `topLevelFunctionSpan`
- `methodCount`
- `methodSpan`
- `classCount`
- `behaviorRichClassCount`
- `dtoOnlyClassCount`
- `exceptionLikeClassCount`
- `hotspotCount`

Each `fileMetrics` entry is deterministically sorted by path and records the
same per-file metrics plus top-level and method span share. `hotspots` contains
files whose top-level function count or top-level span meets the configured
policy threshold. `largestTopLevelFunctions` is sorted by descending span, then
path, line, and function name.
