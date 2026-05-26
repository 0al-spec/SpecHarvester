# Elegant Objects Style

SpecHarvester code should be written in the local Elegant Objects style.

## Rules

- Prefer small behavior-rich objects that own one domain decision.
- Keep constructors simple: no filesystem access, subprocesses, network calls,
  imports from analyzed repositories, or other heavy work.
- Put I/O behind explicit behavior methods with clear trust boundaries.
- Avoid broad `Helper`, `Manager`, `Processor`, `Service`, and `Utils` names.
- Avoid static/class helper methods for domain behavior; prefer an object that
  carries the required data and exposes named behavior.
- Preserve observable report schemas and CLI behavior when introducing object
  seams.
- Add characterization tests before changing mature procedural code.

## Guardrails

Run architecture lint when a change affects project structure:

```shell
PYTHONPATH=src python -m spec_harvester architecture-lint \
  --path src/spec_harvester \
  --output /tmp/specharvester-architecture-lint.json
```

The lint is advisory and intentionally narrower than the full style guide. See
[Architecture Lint Guardrails](ARCHITECTURE_LINT_GUARDRAILS.md) for the exact
rules and trust boundary.
