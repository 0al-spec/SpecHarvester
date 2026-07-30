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
| Codex 5.3 Spark | 2/4 | 2/4 | 0.25 | 0.50 | 0.50 | 0.125 |
| LM Studio `openai/gpt-oss-20b` | 0/4 | 4/4 | 0.00 | 0.00 | 0.00 | 0.00 |

Failed provider records count as failures in the denominator. The apparently
low LM Studio edit burden therefore does not indicate quality; no proposal
completed for review.

## Observations

- `openai/codex` was Spark's strongest result. Its purpose described a coding
  agent/assistant, evidence bindings were complete, and capability wording was
  repository-specific. It still reused a generic observed intent and therefore
  remained `review_required`.
- Spark's `rtk-ai/rtk` proposal was schema-valid and evidence-bound, but its
  purpose did not describe token/context reduction. It also proposed a
  capability outside the candidate package namespace, so deterministic quality
  status was `rejected`.
- Spark returned malformed proposal shapes for `ripgrep` and `claude-mem`,
  including an unexpected request wrapper and wrong API identity.
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
