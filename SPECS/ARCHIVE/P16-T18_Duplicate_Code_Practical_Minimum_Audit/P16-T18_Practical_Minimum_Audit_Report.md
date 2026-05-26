# P16-T18 Practical-Minimum Duplicate-Code Audit

Date: 2026-05-26
Branch: `feature/P16-T18-duplicate-code-practical-minimum-audit`

## Decision

The duplicate-code refactoring goal has reached a practical and reasonable
minimum for `src/spec_harvester`.

No additional code refactor is warranted in this audit pass.

## Evidence

| Detector | Scope | Duplicate Blocks | Duplicate Occurrences | Status |
|----------|-------|------------------|-----------------------|--------|
| builtin | `src/spec_harvester` | 0 | 0 | ok |
| `pylint` `R0801` | `src/spec_harvester` | 0 | 0 | ok |

Commands:

- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend builtin --output /tmp/p16t18-dup-builtin.json`
- `PYTHONPATH=src python -m spec_harvester code-duplication-report --path src/spec_harvester --backend pylint --output /tmp/p16t18-dup-pylint.json`

## Refactoring Progression

| Step | Main Target | Builtin Duplicate Blocks After Step | `pylint` Duplicate Blocks After Step |
|------|-------------|--------------------------------------|--------------------------------------|
| P16-T14 | semantic keyword taxonomy | 10 | 0 |
| P16-T15 | public API analyzer options | 9 | 0 |
| P16-T16 | upstream issue evaluation | 7 | 0 |
| P16-T17 | real repository quality rating policy | 0 | 0 |

## Architecture Lint State

Architecture lint still reports one advisory:

- `manifest_parser_pattern` in `src/spec_harvester/license_provenance_reports.py`

This is not a duplicate-code finding and does not block the duplicate-code
goal. It remains useful architectural signal for a future report-layer cleanup
task if that file changes again.

## Practical-Minimum Criteria

- Trusted established detector (`pylint` `R0801`) reports zero duplicate blocks.
- Project builtin detector reports zero duplicate windows at the configured
  eight-line threshold.
- The remaining advisory signal is architecture-specific, not duplicate-code
  duplication.
- Further changes would be speculative cleanup rather than evidence-driven
  duplicate reduction.

## Follow-Up Decision

- Do not add another duplicate-code refactor task now.
- Keep future duplicate-code work limited to periodic baseline checks or detector
  improvements such as the already-planned multi-language backend evaluation.
- Resume non-duplicate signal-quality work from the existing workplan after this
  audit is merged.
