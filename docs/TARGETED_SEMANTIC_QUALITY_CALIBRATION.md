# P55-T9 Targeted Semantic Quality Calibration

The targeted calibration ran the same P55 semantic-author contract separately
through Codex 5.3 Spark and LM Studio over four retained repositories:

- `rtk-ai/rtk`;
- `openai/codex`;
- `BurntSushi/ripgrep`;
- `thedotmack/claude-mem`.

`junegunn/fzf` was considered but excluded before provider execution because
its generated BoundarySpec alone was about 199 KB and exceeded the bounded
P55-T3 input pack. The input limit was not relaxed.

## Result

P55-T10 is not unblocked.

| Provider | Completed | Failed | Purpose accuracy | Evidence support | Schema validity | Edit burden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex 5.3 Spark | 4/4 | 0/4 | 0.25 | 1.00 | 1.00 | 0.625 |
| LM Studio `openai/gpt-oss-20b` | 0/4 | 4/4 | 0.00 | 0.00 | 0.00 | 1.00 |

Failed provider records count as maximal reviewer edit burden. LM Studio's
four failed proposals therefore produce an edit burden of `1.00`, not a false
zero-work result.

## Observations

- `openai/codex` was Spark's strongest purpose result. Its purpose described a
  coding agent/assistant and evidence bindings were complete. Exact token
  matching no longer treats `openai_codex.codex` as the rubric term `code`, so
  capability specificity remains false. Generic intent reuse keeps the result
  `review_required`.
- Spark's `rtk-ai/rtk` proposal was schema-valid and evidence-bound, but its
  purpose did not describe token/context reduction. It also proposed a
  capability outside the candidate package namespace, so deterministic quality
  status was `rejected`.
- Spark completed schema-valid, evidence-bound proposals for all four targets,
  but only one purpose met every frozen concept group. RTK and ripgrep retained
  capability namespace violations; Codex and claude-mem retained generic intent
  reuse diagnostics.
- LM Studio returned JSON Schema fragments or pointer-like objects in value
  positions for all four targets. Structured output transport succeeded, but
  the semantic proposal contract did not.

## Gate Decision

None of the providers met the frozen P55-T5 gates:

- purpose accuracy `>= 0.85`;
- evidence-supported claim rate `>= 0.95`;
- schema-valid proposal rate `= 1.0`;
- reviewer edit burden `<= 0.25`.

The threshold policy digest remains
`687b4e2d7dccfb727bf0bd2e25811f26cf28dc539c44b1d996e5c821e3fa1a82`
and was not changed.

Before P55-T10, a bounded follow-up must improve provider output conformance,
prevent schema/meta-schema values from being emitted as proposal data, and
re-run this exact target set. Purpose quality for RTK must also improve without
weakening evidence or namespace validation.

Durable evidence excludes raw prompts, raw responses, hidden reasoning,
credentials, and machine-local paths. No proposal was accepted, materialized,
promoted, or published.

The rerun verified each retained checkout was clean and exactly matched the
pinned revision in `inputs/p53-mass-corpus/repositories.yml` before copying
README evidence.

## P55-T9A Follow-Up

P55-T9A added provider-neutral structured-output conformance and repeated this
exact target set against the unchanged rubric and policy. Codex 5.3 Spark and
LM Studio both completed 4/4 records and passed every frozen gate, so P55-T10
is now unblocked. Static namespace and generic-intent diagnostics remain
review evidence; the follow-up did not promote any proposal.

See
[`SEMANTIC_PROVIDER_OUTPUT_CONFORMANCE_FOLLOW_UP.md`](SEMANTIC_PROVIDER_OUTPUT_CONFORMANCE_FOLLOW_UP.md)
for the transport changes, metrics, and authority boundary.
