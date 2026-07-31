# P55-T9A Semantic Provider Output Conformance Follow-Up

## Objective

Harden the provider-neutral semantic-author transport against the exact
conformance failures observed in P55-T9, then repeat the unchanged four-target
calibration through Codex 5.3 Spark and LM Studio.

## Dependencies

- P55-T9 targeted rubric, normalized evidence, and frozen gate decision.
- P55-T4 provider-neutral semantic author pass.
- P55-T5 deterministic quality diagnostics and frozen policy digest.

## Deliverables

- A bounded provider-output conformance layer that:
  - accepts the exact proposal object or unwraps only explicitly recognized
    single-proposal envelopes;
  - rejects request echoes, wrong API identities, and schema/meta-schema
    fragments in proposal value fields;
  - supplies deterministic schema/conformance diagnostics to the existing
  bounded repair path;
  - uses the same behavior for Codex Spark and LM Studio.
- A semantic-author prompt/payload that prioritizes repository purpose and
  package-owned capability wording from allowlisted evidence and the frozen
  target rubric without manufacturing evidence or weakening validation.
- Focused malformed-wrapper, wrong-identity, schema-fragment, retry,
  provider-parity, evidence-binding, and privacy regression tests.
- An exact P55-T9 rerun over:
  - `rtk-ai/rtk`;
  - `openai/codex`;
  - `BurntSushi/ripgrep`;
  - `thedotmack/claude-mem`.
- Provider-separated normalized evidence evaluated against the unchanged
  P55-T5 policy digest and an explicit P55-T10 readiness decision.
- GitHub Markdown, DocC, validation, archive, and structured review artifacts.

## Acceptance Criteria

- The target rubric, four repositories, source revisions, provider separation,
  policy digest, thresholds, and failure denominators are unchanged.
- Both providers receive the same semantic proposal contract and bounded
  conformance semantics.
- A schema-valid but semantically invalid proposal remains rejected by the
  deterministic P55-T5 quality layer; conformance repair does not rewrite
  claims after provider execution.
- RTK purpose quality is improved through explicit evidence-grounded authoring
  guidance, not hard-coded output or relaxed namespace/evidence checks.
- Every provider/target attempt is explicitly counted, including prior bounded
  failures; no provider/target pair receives more than two execution attempts.
- P55-T10 is unblocked only if every frozen gate passes for both providers.
- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths are absent from durable evidence.
- No proposal is accepted, materialized, promoted, published, or treated as
  registry truth.
- Full tests pass with at least 90% coverage; Ruff, formatting, diff, Swift
  manifest, Swift docs, and DocC checks pass.

## Non-Goals

- Changing the P55-T5 policy, rubric, target set, or quality thresholds.
- Retrying until a provider passes, silently converting failures to successes,
  or applying deterministic claim substitutions. Execution retries are capped
  at two attempts and remain visible in evidence.
- Running P55-T10, materializing the wider corpus, canonicalizing intents,
  mutating SpecPM, or publishing packages.

---
**Archived:** 2026-07-31
**Verdict:** PASS
