# Local Candidate Review Workbench E2E Validation

P54-T9 validates the complete local Workbench against the pinned P53 portable
handoff rather than treating individual component tests as operational proof.

Run:

```bash
python -m spec_harvester validate-local-candidate-review-workbench \
  --archive SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz \
  --expected-sha256 db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63 \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --details SPECS/EVIDENCE/P54-T5/P54-T5_Candidate_Review_Details.json \
  --output workbench-e2e.json
```

The validator recomputes all 100 archive packet digests and compares every
catalog, detail, and comparison binding before accounting for the four
`25/25/25/25` campaign waves. It records one bounded reviewer disposition per
wave, restarts the decision store, round-trips portable decisions, and rejects
stale state, interrupted writes, malformed packets, path traversal, and digest
drift.

Browser checks preserve hostile candidate markup as inert text under the
restrictive Content Security Policy. Candidate content cannot execute script,
persist the CSRF token, or submit a disposition. Candidate-origin and invalid
CSRF requests receive `403`.

Only the representative with a current `accept_for_intake` and
`evidence_verified` decision reaches `specpm validate`. The resulting record is
proposal evidence, preserves `preview_only`, and reports zero registry
mutations. It does not accept or publish packages or relations.

The checked-in example is
`SPECS/EVIDENCE/P54-T9/P54-T9_Workbench_E2E_Report.json`.
