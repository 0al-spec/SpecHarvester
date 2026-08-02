# P55-T10G6 Repeat Ten-Repository Semantic Calibration

P55-T10G6 repeated the immutable ten-repository calibration with Codex 5.3
Spark after outcome-anchor ranking and capability namespace repair. The target
set, revisions, P55-T10C baseline, purpose rubric, thresholds, and budgets
were unchanged.

## Result

The campaign completed all ten targets. Every retained proposal was schema
valid, evidence support was 1.00, all seven baseline generic intent reuses were
removed, and no false novelty or duplicate experimental intent IDs or semantic
stems were observed. Six records used the bounded JSON repair path; one of the
eleven provider attempts failed, but all ten terminal records completed.

The frozen exit gate is **PARTIAL**, not PASS:

| Metric | Result | Gate |
| --- | ---: | ---: |
| Purpose accuracy | 0.80 | >= 0.85 |
| Evidence-supported claims | 1.00 | >= 0.95 |
| Schema-valid proposals | 1.00 | = 1.00 |
| Reviewer edit burden | 0.30 | <= 0.25 |

The independent reviewer marked the Bitcoin Core proposal inaccurate because
it described manifest discovery rather than the package outcome. The Electron
dialog-helper proposal likewise described generic import mechanics rather than
its concrete user-facing outcome. Those two assessments and Firecrawl's
`purpose_outcome_anchor_missing` quality diagnostic make three records require
review, keeping reviewer burden above the frozen threshold. Six records used
the bounded JSON repair path, but repair usage alone does not determine this
metric.

## Transport Prerequisites

The first run exposed two deterministic adapter-contract defects before model
quality could be measured:

- `safePath` rejected the valid scoped package path
  `packages/@n8n/agents/package.json`.
- Codex structured output requires every declared property to be required;
  `capabilityNamespaceRepairs` was optional after P55-T10G5.

Both were fixed with regression coverage. The final run used the original
frozen plan and no recovery provider. Raw prompts, raw provider responses,
chain-of-thought, credentials, and machine-local paths remain absent from
durable evidence.

## Decision

`P55-T10H` remains blocked. A targeted follow-up must improve outcome-level
purpose grounding for the identified Bitcoin, Electron, and Firecrawl-style
cases before the exact 46-repository scope is
revalidated.
