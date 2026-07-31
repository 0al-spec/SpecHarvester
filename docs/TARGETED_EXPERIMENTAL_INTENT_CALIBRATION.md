# Targeted Experimental-Intent Calibration

P55-T10B tested the P55-T10A reuse-versus-novelty policy with Codex 5.3 Spark
on four pinned repositories with known semantic gaps: RTK, OpenAI Codex,
ripgrep, and claude-mem. The target set and semantic-focus rubric are unchanged
from P55-T9/P55-T9A; the P55-T5 numerical thresholds are unchanged.

## Result

| Measure | Result |
| --- | ---: |
| Completed / failed targets | 4 / 0 |
| Provider attempts | 5 |
| Evidence-supported experimental intents | 2 |
| Experimental proposal rate | 0.50 |
| Purpose accuracy | 1.00 |
| Evidence-supported claim rate | 1.00 |
| Schema-valid proposal rate | 1.00 |
| Reviewer edit-burden estimate | 0.125 |
| Nearby-intent differentiation rate | 0.50 |
| False novelty | 0 |
| Duplicate experimental IDs / semantic stems | 0 / 0 |

All four frozen P55-T5 gates passed. The calibration therefore unblocks the
bounded P55-T10C follow-up, not automatic materialization or publication.

## Repository Outcomes

- **OpenAI Codex** proposed
  `intent.experimental.local_coding_agent.48e6a87f`, distinguishing local coding
  agent work from the observed JavaScript-library package category.
- **ripgrep** reused `intent.developer.tooling_surface`. The purpose and
  capability claims describe pattern-based text search accurately, but the
  observed intent remains too broad, so this record carries the same explicit
  experimental-intent edit requirement as RTK.
- **claude-mem** proposed
  `intent.experimental.persist_session_context_recall.c6b2134c`, expressing
  retained coding context across sessions. Its first attempt emitted an invalid
  collision-bound identifier and failed closed; the second bounded attempt passed.
- **RTK** reused `intent.developer.tooling_surface`. Its purpose claim accurately
  described reducing command output and LLM token context, but the observed
  intent remained too broad. The result is not counted as justified reuse; it
  carries `experimental_intent_missing_or_unsupported` reviewer edit evidence.

RTK's residual miss is visible in the denominator. It does not invalidate the
calibration because the frozen aggregate reviewer-burden gate remains below
0.25 and the Phase 55 acceptance condition requires at least one useful
experimental intent rather than novelty on every target.

Two records retain pre-existing `capability_namespace_violation` quality status
from their static candidates. Those diagnostics do not alter the experimental
intent result and remain review blockers for materialization.

## Boundaries

The evidence retains complete claims, intent decisions, allowlisted provider
receipts, policy digests, source revisions, and aggregate metrics. Raw prompts,
raw responses, hidden reasoning, credentials, and machine-local paths are not
persisted. No repository code or package manager ran. No proposal was accepted,
materialized, canonicalized, written to SpecPM or registry truth, or published.

The evidence records `maintainerDecisionRecorded: false`: passing this
calibration authorizes P55-T10C only. Experimental intents remain visibly
proposal-only until explicit maintainer review and separate SpecPM governance.
