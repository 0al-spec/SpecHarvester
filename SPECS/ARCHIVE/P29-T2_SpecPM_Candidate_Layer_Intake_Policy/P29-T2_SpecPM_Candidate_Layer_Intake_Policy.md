# P29-T2 SpecPM Candidate-Layer Intake Policy

## Objective

Define the SpecPM-facing intake policy for autonomous candidate batch output.
The policy must let SpecPM maintainers review
`SpecHarvesterAutonomousCandidateBatchReport`, package-set preview bundles,
AI draft/enrichment proposals, and author-ready summaries without treating
producer output as registry authority.

This is a documentation and contract task. It does not implement SpecPM
consumer-side preflight and does not promote generated candidates.

## Deliverables

- GitHub docs page for autonomous candidate-layer intake policy.
- DocC mirror and links from the root documentation, roadmap, handoff docs, and
  autonomous batch docs.
- Workplan/next-task updates that preserve the Phase 29 stack.
- Regression docs-contract assertions for the required policy vocabulary.
- Validation report for the completed task.

## Acceptance Criteria

- The policy names the review inputs:
  `SpecHarvesterAutonomousCandidateBatchReport`, package-set preview bundles,
  `SpecHarvesterPackageSetAIDraftProposal`,
  `SpecHarvesterPackageSetAIEnrichmentProposal`, bundle-set preflight, and
  author-ready stop-policy summaries.
- The policy defines admissible review states for each repository:
  `candidate_layer_review_required`, `needs_regeneration`, `blocked`, and
  `not_for_intake`.
- The policy requires maintainers to verify identity, source revision,
  deterministic collection status, candidate counts, relation counts,
  preflight status, AI privacy flags, provider receipts, author-ready decisions,
  and evidence links.
- The policy explicitly states that AI proposals are proposal-only evidence and
  cannot accept packages, accept relations, seed baselines, remove
  `preview_only`, or publish registry metadata.
- The policy explains that single-package fallback and JSON repair/retry are
  known follow-up work, not hidden acceptance requirements for this task.

## Test-First Plan

1. Add docs-contract assertions that look for the new policy document, DocC
   mirror, required artifact names, review states, authority boundaries, and
   follow-up references.
2. Run the targeted docs-contract test and confirm it fails before the docs are
   complete.
3. Implement docs and links until the targeted docs-contract test passes.
4. Run the broader validation gates.

## Execution Plan

### Phase 1 — Policy Shape

Inputs:

- Existing autonomous batch report contract.
- Package-set handoff and AI proposal docs.
- Observed Flask/Gin/xyflow corpus outcomes.

Outputs:

- `docs/AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`
- `Sources/SpecHarvester/Documentation.docc/AutonomousCandidateIntakePolicy.md`

Verification:

- Required vocabulary appears in both docs.
- The boundary is explicit: producer evidence is not SpecPM acceptance.

### Phase 2 — Navigation and Planning Links

Inputs:

- `docs/README.md`
- `docs/SPECPM_HANDOFF.md`
- `docs/AUTONOMOUS_CANDIDATE_BATCH.md`
- `docs/ROADMAP.md`
- DocC root and roadmap pages.

Outputs:

- Linked policy from the handoff and autonomous batch surfaces.
- Phase 29 workplan/next-task updated to archive P29-T2 and select P29-T3.

Verification:

- Docs-contract tests find the policy links and current next-task state.

### Phase 3 — Validation and Flow Closure

Inputs:

- Completed docs and tests.

Outputs:

- `SPECS/INPROGRESS/P29-T2_Validation_Report.md`
- Archived P29-T2 folder.
- Review report and archived review report.

Verification:

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src python -m pytest -q`
- `ruff check src tests`
- `ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`

## Notes

This task intentionally precedes the technical-debt implementation stack:

- `P29-T3` corpus baseline and gap report.
- `P29-T4` single-package fallback.
- `P29-T5` LM Studio JSON repair/retry.
- `P29-T6` corpus quality gate.
