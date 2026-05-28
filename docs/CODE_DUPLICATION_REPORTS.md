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

For an optional multi-language scan, provide a local `jscpd` command:

```shell
python3 -m spec_harvester code-duplication-report \
  --backend jscpd \
  --jscpd-command "jscpd" \
  --path src \
  --min-lines 8 \
  --output report/code-duplication-jscpd.json
```

## Detection Behavior

- The report scans local source files only.
- `--backend pylint` runs the established Python `pylint`
  `duplicate-code` / `R0801` checker and converts its JSON output into the
  stable `SpecHarvesterCodeDuplicationReport` shape.
- `--backend jscpd` runs an operator-provided `jscpd` command and converts the
  generated `jscpd-report.json` into the same stable report shape. `jscpd`
  4.2.4 is MIT-licensed and supports many source formats, but it is npm-supplied
  and optional.
- `--backend builtin` remains available as a dependency-free fallback that
  ignores blank lines, comments, imports, and simple punctuation-only lines
  before repeated line windows are fingerprinted.
- The default behavior is advisory and exits successfully even when duplicates
  are found.
- Passing `--fail-on-duplicates` returns a non-zero exit code when duplicate
  blocks are detected, which allows future baseline-aware CI enforcement.
- CI runs the `pylint` backend as a non-blocking baseline check. The `jscpd`
  backend is not installed or executed by default CI because npm registry access
  is a supply-chain and reliability boundary. It should stay opt-in until the
  project pins installation, caching, and baseline semantics.

## Backend Evaluation

The `jscpd` backend was added as an optional adapter rather than a dependency:

- npm registry metadata observed for `jscpd@4.2.4` reports `license: MIT`;
- direct dependencies include `@jscpd/core`, `@jscpd/finder`,
  `@jscpd/tokenizer`, reporter packages, `commander`, `colors`, and
  `fs-extra`;
- the JSON reporter writes `jscpd-report.json` with `duplicates` entries that
  include `fragment`, `firstFile`, `secondFile`, line ranges, and aggregate
  `statistic` data;
- SpecHarvester treats invalid JSON, missing report files, malformed duplicate
  entries, missing commands, and non-zero tool exits as errors;
- ordinary CI does not run `npx` or install npm packages for this backend.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No imports from scanned modules.
- No source mutation.

The trust boundary above applies to SpecHarvester report conversion. Operators
who choose `--backend jscpd` must provide a trusted local `jscpd` executable;
SpecHarvester does not fetch it, install it, or audit its transitive npm
dependencies at runtime. If `--jscpd-command` points at a wrapper such as
`npx`, any registry access or package installation is outside SpecHarvester's
trust boundary and should not be used in default CI.

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
