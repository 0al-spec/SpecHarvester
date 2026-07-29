# Local Candidate Review Workbench E2E Validation

P54-T9 runs the complete local Workbench over the pinned 100-candidate P53
portable handoff.

The `validate-local-candidate-review-workbench` command verifies four
`25/25/25/25` campaign waves, representative reviewer dispositions, restart
hydration, portable exchange, malformed packets, path traversal, digest drift,
stale decisions, interrupted writes, and the read-only SpecPM intake bridge.

The hostile candidate markup remains inert text under the restrictive Content
Security Policy. Candidate-origin and invalid CSRF requests receive `403`, and
candidate content cannot submit a reviewer decision.

Only a current `accept_for_intake` decision with `evidence_verified` reaches
SpecPM validation. The result preserves `preview_only`, has no registry
authority, and reports zero registry mutations.
