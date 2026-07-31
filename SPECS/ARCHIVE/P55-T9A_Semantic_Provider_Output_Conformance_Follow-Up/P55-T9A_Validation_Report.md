# P55-T9A Validation Report

## Result

PASS

P55-T9A hardened the provider-output boundary and repeated the exact P55-T9
calibration. Codex 5.3 Spark and LM Studio each completed all four targets and
passed every frozen gate, so P55-T10 is unblocked without changing the target
rubric, policy, thresholds, or failure denominators.

## Calibration Result

| Provider | Completed | Failed | Purpose accuracy | Evidence support | Schema validity | Edit burden | Capability specificity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex 5.3 Spark | 4/4 | 0/4 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 |
| LM Studio `openai/gpt-oss-20b` | 4/4 | 0/4 | 1.00 | 1.00 | 1.00 | 0.00 | 1.00 |

- Both providers used the same proposal contract and bounded conformance
  semantics.
- Both providers reached zero measured reviewer edit burden under the frozen
  rubric; the retained-corpus run must still report this metric rather than
  treating a four-target result as unlimited readiness.
- Deterministic diagnostics remain visible. RTK and ripgrep retain
  `capability_namespace_violation`; Codex and claude-mem retain
  `generic_intent_reuse`. Passing the calibration does not accept or publish
  these proposals.

## Decision

- `p55T10Unblocked: true`
- `thresholdsRedefined: false`
- Frozen policy digest:
  `687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82`
- Baseline P55-T9 evidence digest:
  `2c5f74daa4cd30ffd91c2d3e8479285b9e9970f1cede0f7c78726fbf9c1c3834`
- Target rubric digest:
  `3346390190767c20c8067c0aa3dc71860173d044c4175afda88d27387e6c34ff`
- No proposal was accepted, materialized, promoted, or published.

## Implementation

- Parsed but nonconforming JSON now enters the same bounded repair path as
  malformed JSON, with safe deterministic diagnostics.
- Codex receives an ephemeral request-bound output schema; LM Studio receives
  the same shallow strict transport schema before full semantic validation.
- Only recognized single-proposal envelopes are unwrapped. Request echoes,
  wrong identities, schema fragments, invalid evidence references, and invalid
  intent branches fail closed or receive a bounded repair attempt.
- The provider-neutral input now carries the unchanged semantic-focus rubric
  and explicit evidence-grounded purpose and capability guidance.
- The calibration runner supports bounded diagnostic subsets while preventing
  subset runs from unblocking P55-T10.
- Full runs cap provider execution attempts at two, account for every attempt,
  and retain prior failure codes. The accepted run completed every record on
  its first provider attempt.

## Durable Evidence

- Evidence:
  `SPECS/EVIDENCE/P55-T9A/P55-T9A_Semantic_Provider_Output_Conformance_Follow-Up.json`
- Evidence SHA-256:
  `b6c90f8a086c19eb48df282233ba2d71618d2f89a2e6d5b3e71a11de6fb8d051`
- Codex aggregate provider duration: `58,749 ms`.
- LM Studio aggregate provider duration: `201,726 ms`.
- LM Studio usage: `15,721` prompt tokens, `2,701` completion tokens,
  `18,422` total tokens. Codex CLI did not expose token usage in its retained
  receipt contract.
- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths are absent from durable evidence.

## Validation

- Exact provider-separated live calibration:
  - eight target/provider outcomes accounted for;
  - Codex 5.3 Spark `4/4` complete and all frozen gates passed;
  - LM Studio `4/4` complete and all frozen gates passed;
  - P55-T10 recorded as unblocked without threshold changes.
- Focused semantic-author, P55-T9A, and docs-contract tests: `240 passed`.
- Full test and coverage gate: `1284 passed, 1 skipped`; total coverage
  `90.00%`.
- Ruff lint and format checks: passed; `185 files already formatted`.
- `git diff --check`: passed.
- Evidence JSON parsing and `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed.
- DocC static documentation build: passed with three pre-existing unresolved
  documentation-link warnings.

## Boundary Verification

The run used retained pinned P53 sources and P53-T14 candidates. It did not
clone or fetch repositories, execute harvested code, install harvested
dependencies, mutate SpecPM accepted sources, change registry truth, publish
packages, or grant either provider review or materialization authority.
