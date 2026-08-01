## REVIEW REPORT - P55-T10F Relevant Intent Routing and Generic Contradiction Gate

**Scope:** `feature/P55-T10E-repository-package-semantic-profile..HEAD`

**Files:** 22 changed files across implementation, tests, documentation, a
pinned observed-intent snapshot, and FLOW artifacts.

### Summary Verdict

- [ ] Approve
- [x] Approve with comments
- [ ] Request changes
- [ ] Block

### Resolved Issues

- [High, resolved] The snapshot, routing, and selected catalog used deterministic
  self-digests, but their validators do not bind all semantic contents back to
  the pinned source. A caller can change an observed capability, replace
  `specificProductTerms`, or substitute a selected intent digest and then
  recompute the local self-digest. The altered evidence remains formally valid,
  which can weaken the generic contradiction gate or let the provider reuse an
  intent record that did not come from the pinned SpecPM snapshot. Pin the exact
  snapshot digest, require canonical normalized routing fields, and reconstruct
  each selected catalog record from the pinned snapshot before accepting it.
  The review follow-up implemented all three checks and also revalidates routing
  semantics in resumed campaign records.

### Critical Issues

None remaining.

### Secondary Issues

None.

### Architectural Notes

- The two-term selection floor is necessary. Representative static smoke showed
  that single-token matching routed Axios to node-identity/editor intents and
  n8n or Codex to passport alignment; the corrected floor removed those false
  neighbors.
- Keeping generic current observations as comparison evidence is appropriate
  when SpecPM has no sufficient observed intent. The contradiction gate then
  requires one bounded proposal-only experimental intent for a specific
  purpose rather than inventing a false observed match.
- The observed snapshot remains retrieval evidence only and does not become a
  canonical taxonomy source.

### Tests

- Full post-review coverage suite: 1376 passed, 1 skipped.
- Coverage: 90.01%.
- Ruff lint and format, Swift manifest, Swift DocC target, and diff integrity
  passed before review.
- Negative tests now reject snapshot, routing, catalog, and campaign-record
  substitutions even when their self-digests are recomputed.

### Next Steps

- The high finding is resolved in the current review follow-up.
- No separate Workplan task is required.
