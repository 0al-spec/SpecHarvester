## REVIEW REPORT — P55-T10A Experimental-Intent Decision Policy

**Scope:** `origin/main..HEAD`
**Files:** 20

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

No release-blocking correctness, security, privacy, authority, or test-coverage
defects were found.

### Critical Issues

None.

### Secondary Issues

None.

### Correctness and Architecture

- The decision policy is versioned, digest-bound, package-distributed, and
  validated before either provider is invoked.
- Codex 5.3 Spark and LM Studio receive the same policy, constraints, schema,
  evidence, and observed-intent bindings.
- Existing observed intents remain reusable. Generic reuse requires an explicit
  evidence-backed comparison, while novelty remains optional and bounded to one
  experimental intent.
- Experimental identifiers are package-neutral and deterministically bound to
  the source bundle digest. Nearby intents, user need, non-goals, and claim
  kinds fail closed when malformed.
- Retained-corpus generic-intent accounting now imports the shared policy
  constant without changing its prior behavior.
- False novelty receives an explicit deterministic failure diagnostic; the
  frozen P55-T5 numerical policy and digest are unchanged.

### Security and Authority

- Provider output cannot weaken or replace the maintainer-authored policy.
- Raw prompts, raw responses, hidden reasoning, credentials, and private paths
  remain excluded from retained artifacts.
- No repository code, package manager, materialization, canonicalization,
  SpecPM mutation, registry mutation, or publication path was added.

### Tests

- Focused policy, provider-pass, and quality suite: `61 passed`.
- Full suite: `1305 passed, 1 skipped`.
- Total coverage: `90.03%`, meeting the `90%` repository gate.
- Ruff lint and format, diff integrity, Swift manifest, and Swift documentation
  target passed.
- DocC target retained the existing unhandled-catalog warning; no build failure
  or new semantic-policy diagnostic was introduced.

### Residual Risk

- String overlap is only a conservative false-novelty signal; actual semantic
  sufficiency and reviewer edit burden require the real P55-T10B calibration.
- The source-digest suffix prevents cross-evidence identifier collision but does
  not make an experimental intent canonical or globally accepted.

### Next Steps

- Run P55-T10B with Codex 5.3 Spark on the fixed semantic-gap target set and
  measure both useful novelty and false novelty against unchanged gates.
- FOLLOW-UP is skipped because this review found no new actionable defect;
  P55-T10B already owns the remaining real-provider calibration risk.
- Keep P55-T10B stacked on this branch until P55-T10A is merged.
