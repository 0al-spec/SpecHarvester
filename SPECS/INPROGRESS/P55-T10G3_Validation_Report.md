# P55-T10G3 Validation Report

## Verdict

PARTIAL

## Live Execution

- Frozen plan SHA-256:
  `376001a3ea1053afb5908bf1b7cb8125b95da4eebf2d76a6422e733f06844a11`.
- Provider: Codex 5.3 Spark through `codex exec`.
- Targets: the same ten ordered P55-T10G repositories.
- Terminal records: 10 completed, 0 failed, 11 provider attempts.
- JSON repair records: 4; failed provider attempts: 1.
- Experimental intents: 9; retained generic intents: 1 from baseline 7.

## Frozen Gates

| Gate | Result | Required | Status |
| --- | ---: | ---: | --- |
| Purpose accuracy | 0.70 | >= 0.85 | FAIL |
| Evidence-supported claims | 1.00 | >= 0.95 | PASS |
| Schema-valid proposals | 1.00 | 1.00 | PASS |
| Reviewer edit burden | 0.40 | <= 0.25 | FAIL |
| Generic intent reduction | 6 | > 0 | PASS |
| Repaired generic-case improvement | 5 cases | >= 1 | PASS |
| False novelty | 0 | 0 | PASS |
| Duplicate IDs / semantic stems | 0 / 0 | 0 / 0 | PASS |

## Durable Evidence

- Report digest: `a87f2cab127306faad03245fb0c249b1316c31a4014541c5815c78e34954fbcb`.
- Purpose assessment digest:
  `d205379cfa75f6de30720cf1f41ac0a2e5009bd27077ea46244f9dc1ead33f06`.
- Portable archive digest:
  `134159f0c395e01fc2eb68b1f8700669bcc2899012031eb04903e20ca95f98fb`.

## Decision and Boundaries

P55-T10H remains blocked because not every frozen gate passed. The run executed
no repository code or package manager and performed no acceptance,
materialization, canonicalization, SpecPM mutation, registry mutation, or
publication. Durable evidence persists no raw prompts, raw responses, hidden
reasoning, credentials, or machine-local paths.
