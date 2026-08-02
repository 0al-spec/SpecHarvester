# P55-T10G4 Validation Report

## Verdict

PASS

## Scope Validated

- Versioned per-anchor source-authority classification and record validation.
- Field-level provenance for descriptive manifest metadata.
- Strong-documentation preference over generated preview and repository
  mechanics.
- Bounded selection that retains strong package-local evidence ahead of a
  saturated weak root preview.
- Weak-only, no-source, and legacy assessments that remain reviewer-visible
  but are not calibration eligible.
- Candidate, source bundle, evidence-content, request, and anchor integrity
  checks before provider invocation, including fixed document topology and
  allowlisted-document evidence bindings, mandatory anchors for profile-bearing
  packs, and exactly parsed pinned manifest bytes for a strong manifest
  description.
- Independent quality evaluation reuses input-pack integrity validation, and
  retained-corpus manifest selection is limited to the selected target path.
- Proposal-only authority and existing provider/repair budget preservation.

## Quality Gates

| Gate | Result |
| --- | --- |
| Focused authority, semantic, campaign, and schema suites | PASS: 117 passed |
| `PYTHONPATH=src python -m pytest` | PASS: 1432 passed, 1 skipped |
| `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term --cov-fail-under=90` | PASS: 90.02% exact coverage |
| `ruff check src tests` | PASS |
| `ruff format --check src tests` | PASS: 201 files already formatted |
| `swift package dump-package` | PASS |
| `swift build --target SpecHarvesterDocs` | PASS |

The Swift target emitted the existing warning that the DocC resource is not
declared, then built successfully.

## Execution Boundary

- No Codex, LM Studio, or other provider was invoked.
- No raw prompt, response, hidden reasoning, credential, or machine-local path
  was persisted.
- No proposal was accepted, materialized, canonicalized, published, or used to
  mutate SpecPM or registry truth.
