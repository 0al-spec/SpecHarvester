# P55-T10B Targeted Experimental-Intent Calibration

## Objective

Run Codex 5.3 Spark through the P55-T10A reuse-versus-novelty policy on a fixed
set of repositories with known semantic gaps, then record whether the policy
produces useful experimental intents without forcing synonyms or weakening the
frozen P55 quality gates.

## Dependencies

- P55-T5 frozen semantic proposal quality thresholds.
- P55-T9/P55-T9A four-repository semantic calibration rubric and pinned source
  checkouts.
- P55-T10 retained-corpus baseline with zero generic-intent reduction.
- P55-T10A digest-bound experimental-intent decision policy.

## Deliverables

- A deterministic calibration runner that:
  - reuses the four frozen P55-T9 targets and semantic-focus rubric;
  - invokes only `gpt-5.3-codex-spark` through bounded `codex exec`;
  - validates pinned clean source revisions and candidate/input bindings;
  - retains proposal, receipt, quality, decision-policy, and source digests;
  - accounts for provider attempts and terminal failures once per target;
  - never executes harvested code or package managers.
- Target and aggregate measurements for:
  - justified observed-intent reuse;
  - experimental-intent proposal rate;
  - purpose accuracy and evidence support;
  - nearby-intent differentiation;
  - duplicate, synonym, and false-novelty risk;
  - reviewer edit burden;
  - unchanged P55-T5 numerical gates.
- Durable JSON evidence, Markdown and DocC results, focused tests, validation,
  archive, and review artifacts.

## Execution Plan

1. Bind the T10B run to the T10A decision-policy digest, the unchanged P55-T5
   quality-policy digest, the P55-T9 rubric digest, and pinned source revisions.
2. Test result accounting, novelty classification, false-novelty failure, and
   non-authority boundaries without provider execution.
3. Run Codex 5.3 Spark sequentially over RTK, OpenAI Codex, ripgrep, and
   claude-mem with at most two provider attempts and one JSON repair per attempt.
4. Inspect each completed proposal against repository evidence and record a
   bounded maintainer rubric assessment rather than inferring acceptance.
5. Finalize aggregate evidence and run repository quality gates.

## Acceptance Criteria

- Exactly four pinned targets are accounted for once: `rtk-ai/rtk`,
  `openai/codex`, `BurntSushi/ripgrep`, and `thedotmack/claude-mem`.
- Every target has one terminal completed or failed record; failures remain in
  all denominators.
- At least one completed proposal contains an evidence-supported experimental
  intent that accurately expresses a documented user outcome and distinguishes
  it from observed nearby intents.
- Existing intents may be reused when sufficient, and the evidence records why
  reuse is justified.
- Any duplicate, synonym, unsupported, package-bound, or otherwise false novelty
  is counted as a calibration failure, not accepted or hidden by changing a
  threshold.
- Purpose accuracy, evidence support, schema validity, and reviewer edit burden
  are evaluated against the unchanged P55-T5 thresholds and policy digest.
- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths are not persisted.
- No proposal is accepted, materialized, canonicalized, written to SpecPM or
  registry truth, or published.
- Python tests pass with at least 90% coverage; Ruff lint and format, diff
  integrity, Swift manifest, and Swift documentation checks are recorded.

## Non-Goals

- Running LM Studio or comparing provider transport conformance again.
- Reprocessing the 48 P55-T10 generic-intent cases; that is P55-T10C.
- Automatically deciding that an experimental intent is canonical.
- Changing the P55-T5 calibration thresholds after observing results.
- Materializing, accepting, promoting, or publishing any candidate.
