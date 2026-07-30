# P55-T7 Validation Report

## Result

PASS

## Delivered

- Deterministic static-versus-AI semantic projections for summaries, purpose,
  capabilities, interfaces, evidence, observed-intent reuse, and experimental
  intent proposals.
- Human-readable Workbench comparison panels that render all candidate and
  provider content as inert text.
- Explicit `accepted`, `edited`, `rejected`, and `deferred` semantic review
  controls with bounded claim selection and edited text.
- Digest-bound semantic reviewer edits persisted inside the existing immutable
  candidate decision history and portable exchange.
- Service-side validation of candidate packet, semantic record, proposal,
  source bundle, reviewer identity, claim selection, edit shape, and optimistic
  prior-decision bindings.
- Updated schemas, CLI, GitHub Markdown, DocC, capability inventory, and focused
  regression coverage.

## Validation

- `uv run pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90 -q`
  - `1258 passed, 1 skipped`
  - total coverage: `90.01%`
  - `local_candidate_review_details.py`: `91%`
  - `local_review_decision_service.py`: `92%`
  - `semantic_review.py`: `98%`
- Focused semantic, detail, browser, decision-service, schema, and docs tests:
  - `284 passed`
- `uv run ruff check src tests`
  - passed
- `uv run ruff format --check src tests`
  - `181 files already formatted`
- `git diff --check`
  - passed
- `python -m json.tool` for both changed schema bundles
  - passed
- `swift package dump-package`
  - passed
- `swift build --target SpecHarvesterDocs`
  - passed with the repository's existing unhandled DocC resource warning

## Authority Boundary

The Workbench records local reviewer evidence only. It does not invoke a
provider, materialize a candidate revision, mutate SpecPM accepted sources,
accept experimental intents as canonical, mutate registry truth, or publish a
package. The model proposal has no path to record its own decision.
