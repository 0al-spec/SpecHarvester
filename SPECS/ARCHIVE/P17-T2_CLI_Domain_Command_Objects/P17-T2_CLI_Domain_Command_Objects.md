# P17-T2 CLI Domain Command Objects

Status: Planned
Phase: Phase 17. Elegant Objects Refactoring Strategy
Owner: SpecHarvester CLI and EO refactoring track

## Objective

Split a narrow slice of CLI command execution behavior out of
`src/spec_harvester/cli.py` into small command objects while keeping `argparse`
as the shell. The first slice covers:

- `code-duplication-report`;
- `architecture-lint`;
- `procedural-style-report`.

The goal is behavior movement, not a parser rewrite. Public CLI names, flags,
defaults, JSON output, report schemas, and exit codes must remain unchanged.

## Motivation

`P17-T1` established procedural-style metrics and identified `cli.py` as a
large procedural hotspot. `P17-T2` starts reducing that concentration by moving
mature command execution bodies behind behavior-rich command objects. These
commands are good first candidates because they already have stable JSON
contracts and focused tests.

## Deliverables

- Add CLI command objects for the three selected report flows.
- Keep parser construction and `set_defaults(func=...)` compatibility intact.
- Add characterization tests that prove the new objects preserve success,
  failure, output-file, JSON error, and fail-on-* exit-code behavior.
- Update EO refactoring docs or docs-contract tests only if necessary to name
  the completed slice.
- Add validation report and Flow archive/review artifacts.

## Acceptance Criteria

- `spec-harvester code-duplication-report` preserves:
  - `--path`, `--min-lines`, `--output`, `--backend`,
    `--pylint-command`, `--jscpd-command`, and
    `--fail-on-duplicates`;
  - JSON error output with exit code `2` for invalid inputs;
  - exit code `1` for `--fail-on-duplicates` when duplicate blocks exist.
- `spec-harvester architecture-lint` preserves:
  - `--path`, `--output`, and `--fail-on-issues`;
  - JSON error output with exit code `2` for invalid inputs;
  - exit code `1` for `--fail-on-issues` when issues exist.
- `spec-harvester procedural-style-report` preserves:
  - `--path`, `--output`, `--hotspot-min-top-level-count`,
    `--hotspot-min-top-level-span`, and `--fail-on-hotspots`;
  - JSON error output using `procedural_style_error`;
  - exit code `1` for `--fail-on-hotspots` when hotspots exist.
- No report schema, issue code, trust-boundary text, CLI flag, or default value
  changes.
- Coverage remains at or above 90%.

## Test-First Plan

1. Add direct command-object tests that instantiate the new objects with
   `argparse.Namespace` values and assert the same reports and exit codes as
   the CLI tests.
2. Keep existing CLI tests unchanged as end-to-end characterization.
3. Run focused tests for code duplication, architecture lint, procedural style,
   and docs contracts before full gates.

## Implementation Plan

### Phase 1: Command Object Seam

Inputs:

- current `run_code_duplication_report`;
- current `run_architecture_lint`;
- current `run_procedural_style_report`.

Outputs:

- a small module that owns command objects and wrappers used by `cli.py`;
- no parser changes beyond importing and delegating to wrappers.

Verification:

- direct command-object tests pass;
- existing CLI tests pass without fixture changes.

### Phase 2: Behavior Preservation

Inputs:

- existing report builders and writer functions;
- existing fail-on flags and JSON error behavior.

Outputs:

- command objects own argument normalization, result building, output writing,
  stdout serialization, and exit-code policy for their command.

Verification:

- output file content equals stdout JSON for success paths;
- invalid input returns JSON `{"status": "error", "message": ...}` and exit
  code `2`;
- fail-on flags return exit code `1` only when the report summary requires it.

### Phase 3: Flow Validation

Inputs:

- `.flow/params.yaml` quality gates;
- EO refactoring strategy acceptance criteria.

Outputs:

- validation report;
- archived task artifacts;
- review report.

Verification:

- full pytest;
- ruff check and format check;
- coverage gate;
- Swift manifest and docs build when docs are touched;
- procedural-style report smoke for `cli.py` if practical.

## Non-Goals

- Do not rewrite parser construction.
- Do not move all CLI commands.
- Do not change public command names, flags, defaults, or help text.
- Do not change report schemas, issue codes, trust-boundary text, or markdown
  output.
- Do not change SpecPM or SpecNode contracts.
- Do not make architecture lint, duplicate-code, or procedural-style reports
  blocking by default.
