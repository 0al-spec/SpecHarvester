# P55-T9A Semantic Provider Output Conformance Follow-Up

P55-T9A hardens the provider-neutral semantic-author transport and repeats the
unchanged P55-T9 target set against the frozen P55-T5 policy.

## What Changed

- `codex exec` now receives an ephemeral, request-bound `--output-schema`.
- LM Studio receives the same shallow strict structured-output schema without
  unresolved `$ref` or unsupported union/containment keywords.
- The complete semantic proposal schema, evidence allowlist, candidate/source
  bindings, observed-intent bindings, and claim references are still checked
  after transport normalization.
- Valid JSON with the wrong shape now enters the same bounded repair
  attempt as malformed JSON and receives only a safe deterministic diagnostic.
- The calibration runner permits at most two explicitly counted provider
  attempts and retains prior failure codes; the accepted rerun needed one
  attempt for every provider/target pair.
- A single recognized `proposal` or `result` envelope may be unwrapped. Request
  echoes, wrong API identities, schema fragments, and unknown wrappers fail.
- The strict transport representation uses one intent record shape. Fields for
  the branch not selected by `state` are transport padding and are removed;
  active intent fields are never rewritten.
- The frozen semantic focus guides purpose and capability authoring but does
  not replace evidence, namespace, schema, or quality validation.

## Exact Rerun Result

| Provider | Completed | Failed | Purpose | Evidence | Schema | Edit burden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex 5.3 Spark | 4/4 | 0/4 | 1.00 | 1.00 | 1.00 | 0.00 |
| LM Studio `openai/gpt-oss-20b` | 4/4 | 0/4 | 1.00 | 1.00 | 1.00 | 0.00 |

Both providers passed every frozen gate. The threshold policy digest remains
`687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82`.
P55-T10 is unblocked.

LM Studio used 15,721 prompt tokens and 2,701 completion tokens across the
four completed records. Recorded provider durations totalled 58.749 seconds for
Spark and 201.726 seconds for LM Studio. These are observed local-run values,
not performance guarantees.

## Remaining Review Diagnostics

Passing the frozen calibration does not make every proposal publishable.
`rtk-ai/rtk` and `BurntSushi/ripgrep` still carry
`capability_namespace_violation` from their static candidate metadata.
`openai/codex` and `thedotmack/claude-mem` still carry
`generic_intent_reuse`. These diagnostics remain visible to the reviewer and
are not suppressed by transport conformance.

## Authority Boundary

The rerun is proposal-only calibration evidence. It does not accept or
materialize proposals, repair static candidates, canonicalize intents, mutate
SpecPM or registry truth, publish packages, or persist raw prompts, raw
responses, hidden reasoning, credentials, or machine-local paths.
