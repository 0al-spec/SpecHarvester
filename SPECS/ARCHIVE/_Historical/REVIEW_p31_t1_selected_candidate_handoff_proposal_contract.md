## REVIEW REPORT — P31-T1 Selected Candidate Handoff Proposal Contract

**Scope:** `codex/p30-t5-selected-candidate-handoff-dry-run...HEAD`
**Files:** 17

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

None.

### Secondary Issues

None.

### Architectural Notes

- The new `SpecHarvesterSelectedCandidateHandoffProposal` contract preserves
  the existing producer/consumer boundary: SpecHarvester emits preview evidence
  and SpecPM remains responsible for validation, acceptance, maintainer
  decision, and registry metadata.
- The fixture keeps selected candidates and deferred candidates explicit. That
  reduces the risk that package-set or warning-bearing candidates are silently
  pulled into a selected single-package intake path.
- The required evidence-role vocabulary is intentionally stable and narrow.
  P31-T2 can now implement a helper against this shape without inventing
  acceptance semantics.

### Tests

Validation recorded in the archived P31-T1 validation report:

- JSON fixture parse: passed.
- Docs contract tests: `67 passed`.
- Full tests: `635 passed, 1 skipped`.
- Coverage gate: `635 passed, 1 skipped`, total coverage `90.58%`.
- Ruff check: passed.
- Ruff format check: passed.
- Diff whitespace check: passed.
- Swift package dump: passed.
- Swift docs target build: passed.
- Static DocC generation: passed with pre-existing unrelated warnings only.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with P31-T2: implement the producer helper that emits JSON and
  Markdown selected candidate handoff proposal artifacts from real selected
  candidate bundles, producer preflight reports, and static viewer outputs.
