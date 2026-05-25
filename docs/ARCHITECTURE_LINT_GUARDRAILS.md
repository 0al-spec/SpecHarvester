# Architecture Lint Guardrails

`architecture-lint` builds an advisory architecture lint report for local source
review before larger structural refactors.

The command is intentionally narrow. It does not try to enforce all Elegant
Objects rules. It catches project-specific relapse risks that matter for the
planned report-layer refactor:

- broad `Helper`, `Manager`, `Processor`, `Service`, and `Utils` names;
- I/O or heavy work inside constructors;
- static/class helper methods in domain objects;
- repeated `specpm.yaml` manifest parser markers.

```shell
python3 -m spec_harvester architecture-lint \
  --path src/spec_harvester \
  --output report/architecture-lint.json
```

## Detection Behavior

- The report scans local Python source files only.
- The default behavior is advisory and exits successfully even when issues are
  found.
- Passing `--fail-on-issues` returns a non-zero exit code when architecture lint
  issues are detected.
- CI runs this command as a non-blocking baseline check. It should not become
  blocking until current baseline findings are either resolved or explicitly
  allowlisted.

## Trust Boundary

- No repository code execution.
- No package installation.
- No network calls.
- No imports from scanned modules.
- No source mutation.

## Report Format

The report is a deterministic JSON object with:

- `schemaVersion`
- `kind: SpecHarvesterArchitectureLintReport`
- `status`
- `summary`
- `issues`
- `trustBoundary`

Each issue includes a rule code, source path, line, advisory severity, name, and
message.
