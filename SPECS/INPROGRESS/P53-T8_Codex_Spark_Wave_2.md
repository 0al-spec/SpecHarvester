# P53-T8 Codex Spark Wave 2

Execute the second P53 Codex 5.3 Spark wave only after the recorded P53-T7
`unlock_p53_t8` decision. The run is bounded to the frozen manifest positions
26 through 50 (`wave-2`), with no substitution, expansion, or retry beyond the
campaign's checkpoint policy.

## Deliverables

- A wave-aware runner that preserves the existing wave-1 interface while
  rejecting unknown waves and selecting exactly the metadata-assigned position
  range for the requested wave.
- A live `gpt-5.3-codex-spark` proposal-only run over the 25 wave-2 checkouts,
  after static collection verifies every pinned checkout revision.
- A local report and checkpoint with provider receipts and aggregate outcome
  metrics, without raw prompts, responses, or chain-of-thought.
- Focused tests covering exact wave-2 selection and the prerequisite scale-out
  checkpoint transition.

## Acceptance Criteria

1. The input set is exactly the 25 frozen repository identities at positions
   26-50 and no other manifest entries.
2. Static evidence passes with `verify_checkout_revisions` enabled before any
   Codex invocation.
3. Only `gpt-5.3-codex-spark` runs, at a maximum concurrency of two, using the
   P53-T1 budgets, retry policy, stop policy, and checkpoint semantics.
4. Output remains proposal-only: no package/relation acceptance, registry
   mutation, package-manager execution, harvested-code execution, adapter
   execution, LM Studio, or alternate AI worker.
5. The validation report records source count, completions, schema validity,
   repository specificity, unsupported claims, terminal failures, stop state,
   and stable local artifact digests for P53-T9 review.

## Dependencies and Boundary

- P53-T7 is the sole authorization to unlock `wave-2`; this task does not
  unlock `wave-3`.
- The P53-T1 campaign plan remains the authority for budgets and worker choice.
- Provider output is retained only in the existing sanitized proposal and
  receipt fields; raw prompt/response/reasoning content is not persisted.
