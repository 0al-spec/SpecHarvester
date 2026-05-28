# P16-T4 — Reduce Broad Duplicate Semantic Intent Claims

Branch: `feature/P16-T4-reduce-broad-semantic-intents`
Review subject: `p16_t4_reduce_broad_semantic_intent_claims`

## Context

P15-T4 recorded real-repository smoke noise from broad documentation/API intent
duplication. The current governance duplicate-claim report compares every
`intent.*` ID equally, including language-neutral semantic intents such as API
contract, metadata schema validation, workflow automation, developer tooling,
documentation knowledge base, and public repository metadata.

Those broad intents are valid record-level evidence, but they are weak duplicate
signals across unrelated packages. The report should preserve them in `records`
while excluding them from duplicate intent findings.

## Scope

- Add a behavior-rich governance intent comparison policy for duplicate-claim
  reporting.
- Exclude known broad language-neutral semantic intents from
  `duplicates.intent` comparison.
- Preserve duplicate capability behavior and non-broad duplicate intent behavior.
- Preserve report schema, trust boundary, deterministic ordering, and parsed
  `records`.
- Document the filtering policy in GitHub docs and DocC mirror.

## Non-Goals

- Do not change generated `specpm.yaml` manifests.
- Do not remove broad semantic intents from candidate records.
- Do not execute harvested repository code, analyzers, package scripts, or
  network calls.
- Do not introduce a model prompt change.
- Do not make governance reports blocking.

## Acceptance Criteria

- Duplicate broad language-neutral semantic intent claims remain visible in
  `records` but are not counted in `duplicates.intent`.
- Non-broad duplicate intents and duplicate capabilities are still reported.
- Governance report tests cover broad-intent filtering.
- Docs describe the record-vs-finding distinction.
- Full Flow validation passes.

## Validation Plan

- `PYTHONPATH=src python -m pytest tests/test_governance_reports.py -q`
- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `ruff check src tests`
- `ruff format --check src tests`
- `swift package dump-package >/dev/null`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t4-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t4-dup-pylint.json`
- `PYTHONPATH=src python -m spec_harvester architecture-lint --path src/spec_harvester --output /tmp/p16t4-architecture-lint.json`
