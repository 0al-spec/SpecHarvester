# P55-T10G3 Repeat Ten-Repository Semantic Calibration

P55-T10G3 repeated the exact P55-T10G calibration after outcome-level anchors
and validation-aware repair. It reused the frozen plan, ten ordered repositories,
Codex 5.3 Spark provider, source revisions, candidate packets, P55-T10C baseline,
P55-T5 thresholds, denominators, purpose rubric, and attempt budgets.

## Result

| Metric | P55-T10G | P55-T10G3 | Frozen requirement |
| --- | ---: | ---: | ---: |
| Completed terminal records | 8 / 10 | 10 / 10 | 10 / 10 |
| Purpose accuracy | 0.60 | 0.70 | >= 0.85 |
| Evidence-supported claims | 0.80 | 1.00 | >= 0.95 |
| Schema-valid proposals | 0.80 | 1.00 | 1.00 |
| Reviewer edit burden | 0.40 | 0.40 | <= 0.25 |
| Generic intent references | 0 | 1 | below baseline 7 |
| False novelty | 0 | 0 | 0 |

All ten targets produced terminal records. Nine proposed experimental intents;
one Bitcoin record retained the baseline generic repository-metadata intent and
was independently rejected for capability namespace and generic reuse
diagnostics. There were no duplicate experimental IDs or semantic stems.

## Purpose Review

The unchanged supervisor rubric marked seven purposes accurate. Firecrawl still
described generated preview and package metadata mechanics. Angular still
described the Adev member-package boundary. Electron still described import and
module-boundary mechanics. These three records passed deterministic quality
checks, exposing a remaining weakness in anchor source ranking rather than a
provider transport failure.

## Decision

The result is `PARTIAL`. Schema, evidence, completion, generic reduction, repair
improvement, false-novelty, and duplicate gates passed. Purpose accuracy and
reviewer edit burden failed, so P55-T10H remains blocked.

No threshold was changed. No proposal was accepted, materialized,
canonicalized, written to SpecPM or registry truth, or published. Durable
evidence contains no raw prompts, raw responses, hidden reasoning, credentials,
or machine-local paths.
