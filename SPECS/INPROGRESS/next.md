# Next Task: P26-T3 Package-Set Proposal Intake Checklist

**Status:** In Progress
**Selected:** 2026-06-13
**Task:** P26-T3 Package-Set Proposal Intake Checklist
**Phase:** Phase 26. Package-Set SpecPM Handoff Automation
**Last Archived:** P31-T5 Deferred Selected Candidate Regeneration Requirements

## Recently Archived

- `P31-T4` documented the SpecPM-side selected candidate handoff preflight
  expectations in `docs/SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`
  and `<doc:SelectedCandidateHandoffPreflightExpectations>`. It defined the
  future `SpecPMSelectedCandidateHandoffPreflightReport` identity
  `specpm.selected-candidate-handoff-preflight/v0`, checked
  `SpecHarvesterSelectedCandidateHandoffProposal` identity,
  `producer_preview_evidence_only` authority, evidence roles, digests,
  selected/deferred candidate consistency, and non-authority boundaries. A pass
  remains review evidence and not package acceptance.
- `P31-T5` recorded deferred selected-candidate regeneration requirements in
  `docs/DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`,
  `<doc:DeferredSelectedCandidateRegenerationRequirements>`, and the
  `SpecHarvesterDeferredSelectedCandidateRegenerationRequirements` fixture
  `p31-t5-deferred-selected-candidate-regeneration-requirements.example.json`.
  The fixture covers all six deferred P30 candidates, package-set identity
  regeneration, warning-bearing enrichment regeneration, identity-drift
  resolution, source digests, minimum proof before selected handoff, and the
  non-authority boundary. It remains regeneration requirements only and not
  package acceptance.

## Outcome

Phase 31 is complete. The next selected task returns to the older Phase 26
package-set handoff backlog: SpecHarvester already produces package-set
handoff proposal artifacts, but the SpecPM-facing intake checklist and evidence
role expectations still need to be documented on the producer side.

## Next Step

Implement `P26-T3`: define the SpecPM-side package-set proposal intake
checklist and evidence roles required before maintainers accept package
members or relations.

The task should document how a maintainer reviews
`SpecHarvesterPackageSetHandoffProposal` evidence, including package-set
identity, member package evidence, relation proposal evidence, bundle-set
preflight, viewer links, `registryAcceptanceDecision.status: external_required`,
and the boundary that a handoff proposal does not accept packages or relations.
