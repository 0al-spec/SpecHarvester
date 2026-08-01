# Ten-Repository Semantic Root-Cause Calibration

P55-T10G ran Codex 5.3 Spark over ten digest-bound P55-T10C cases after the
repair-context, semantic product-profile, relevant-intent-routing, and generic
contradiction changes from P55-T10D through P55-T10F.

## Result

| Measure | P55-T10C baseline | P55-T10G | Gate |
| --- | ---: | ---: | --- |
| Completed records | 9 | 8 | 10 required |
| Generic intent reuse | 7 | 0 | Improved |
| Evidence-supported experimental intents | 0 | 8 | Informational |
| Purpose accuracy | Not independently scored | 0.60 | >= 0.85 |
| Evidence-supported claim rate | Not independently scoped | 0.80 | >= 0.95 |
| Schema-valid proposal rate | 0.90 | 0.80 | 1.00 |
| Reviewer edit burden | At least 0.70 | 0.40 | <= 0.25 |
| False novelty | 0 | 0 | 0 |
| Duplicate experimental IDs/stems | 0 / 0 | 0 / 0 | 0 / 0 |

The repaired pipeline eliminated all seven generic intent references in this
scope. Axios, n8n agents, Firecrawl, Codex, claude-mem, and freeCodeCamp API
received purpose claims judged accurate by a separate digest-bound supervisor
assessment. Angular `adev` and Electron `dialog-helper` passed structural gates
but described package mechanics instead of their concrete user outcomes.

Bitcoin failed both bounded attempts because its specific purpose was still
mapped only to a generic observed intent. Excalidraw failed both attempts
because the proposed experimental identifier leaked the candidate namespace.
Both failures were fail-closed and remain in every denominator.

## Decision

P55-T10G is `PARTIAL` and does not unblock the exact 46-repository P55-T10H
revalidation. The next bounded work must improve outcome-level purpose anchoring
and make repeated contradiction or namespace repair actionable without weakening
the generic-reuse or false-novelty gates.

All records remain proposal-only. No candidate or intent was accepted,
materialized, canonicalized, written to SpecPM or registry truth, or published.
Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
paths are absent from durable evidence.
