# P55-T8 Validation Report

## Result

PASS

## Delivered

- Deterministic reviewer-controlled materialization into a separate preview
  candidate revision.
- Exact proposal, source, packet, reviewer-edit, reviewer identity, claim, and
  decision revalidation.
- Bounded mappings for purpose, capability, interface, non-goal, nearby-intent,
  observed-intent reuse, and experimental-intent proposal fields.
- Source-candidate immutability checks and before/after digest provenance.
- SpecHarvester manifest validation and bounded read-only SpecPM validation.
- Portable schema-valid materialization report with zero registry mutations.
- CLI, GitHub Markdown, DocC, capability inventory, and focused regression
  coverage.

## Validation

- `uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90 -q`
  - `1263 passed, 1 skipped`
  - total coverage: `90.00%`
  - `semantic_materialization.py`: `86%`
- Focused semantic, SpecPM intake, schema, and docs tests:
  - `273 passed`
- `uv run ruff check src tests`
  - passed
- `uv run ruff format --check src tests`
  - `182 files already formatted`
- `git diff --check`
  - passed
- `python -m json.tool schemas/semantic-materialization-v0.schema.json`
  - passed
- `swift package dump-package`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed with the repository's existing unhandled DocC resource warning

## Authority Boundary

Materialization creates only a new `preview_only` candidate revision. It does
not invoke an AI provider, modify the source candidate, accept an experimental
intent as canonical, mutate SpecPM accepted sources, mutate registry truth,
publish a package, or create a SpecPM pull request.
