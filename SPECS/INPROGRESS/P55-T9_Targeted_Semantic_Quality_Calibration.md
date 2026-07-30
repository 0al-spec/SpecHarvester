# P55-T9 Targeted Semantic Quality Calibration

## Objective

Run a bounded, provider-separated semantic-author calibration on repositories
whose user purpose is poorly represented by generic static intents.

## Target Set

- `rtk-ai/rtk`: token and context reduction utility.
- `openai/codex`: coding agent.
- `BurntSushi/ripgrep`: recursive regular-expression text search utility.
- `junegunn/fzf`: interactive fuzzy finder and filter.

The retained P53 source revisions and P53-T14 static candidates are the only
repository inputs.

## Deliverables

- A digest-bound target rubric with required purpose concept groups and
  repository-specific capability/intent terms.
- A repeatable targeted runner that assembles bounded P55-T3 packs from retained
  candidate YAML, harvest metadata, and allowlisted README evidence.
- Independent Codex 5.3 Spark and LM Studio runs under the P55-T4 contract.
- Deterministic P55-T5 quality reports plus rubric evaluation for purpose
  accuracy, evidence support, schema validity, capability specificity, intent
  reuse, experimental-intent quality, and reviewer edit burden.
- Provider-separated aggregate metrics evaluated against the frozen P55-T5
  policy digest without changing its thresholds.
- Durable normalized evidence excluding raw prompts, raw responses, hidden
  reasoning, credentials, and machine-local paths.
- Result documentation, tests, validation report, and an explicit decision on
  whether P55-T10 is unblocked.

## Acceptance Criteria

- All four targets are accounted for once per provider.
- Codex uses `gpt-5.3-codex-spark`; LM Studio uses the locally loaded
  `openai/gpt-oss-20b` model.
- Provider failures remain explicit and are not converted into quality passes.
- Purpose accuracy, evidence support, schema validity, and reviewer burden are
  evaluated against policy
  `687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82`.
- Capability, intent reuse, and experimental-intent quality remain reported
  diagnostic metrics and do not silently redefine the frozen gate.
- Raw provider content and machine-local paths do not enter durable evidence.
- No proposal is automatically accepted, materialized, promoted, or published.
- Full tests pass with at least 90% coverage; Ruff, formatting, diff, Swift
  manifest, and DocC checks pass.

## Non-Goals

- The retained 100-repository semantic run reserved for P55-T10.
- Threshold changes, canonical intent governance, broad materialization,
  registry mutation, or publication.
