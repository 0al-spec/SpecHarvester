# Package-Set Proposal Intake Checklist

This page mirrors `docs/PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md`.

It defines the SpecPM-facing intake checklist for
`SpecHarvesterPackageSetHandoffProposal` evidence with
`apiVersion: spec-harvester.package-set-handoff-proposal/v0`.

SpecHarvester produces review evidence. SpecPM owns package acceptance,
relation acceptance, public registry metadata, accepted-source mutation, and
maintainer decisions.

## Evidence Roles

Before maintainers consider package members or relations, the proposal should
link `package_set_draft`, `package_relation_proposals`,
`bundle_set_preflight`, `package_set_viewer`, `member_candidate_bundle`,
`member_manifest`, `member_boundary_spec`, `member_producer_receipt`,
`member_validation_report`, `member_diagnostics`, `member_quality_report`, and
`package_relation_summary`.

The reviewer should inspect `authorReadyDraftSummary` and `authorReview` to
decide whether generation should stop for author review, continue generation,
or block until inputs change.

## Member and Relation Checks

Package member review verifies identity, namespace, version, repository
provenance, `preview_only`, member manifests, boundary specs, producer
receipts, validation reports, diagnostics, quality reports, and
`bundle_set_preflight` status.

Relation review verifies relation type, subject, object, scope, relation
endpoints, `package_relation_proposals`, `package_relation_summary`, and
evidence-backed topology such as `xyflow.workspace contains xyflow.react`.

Package member acceptance is separate from relation acceptance.

## Acceptance Boundary

The proposal must preserve `registryAcceptanceDecision.status:
external_required` with `public_index_acceptance`,
`package_relation_acceptance`, and `producerAuthority: evidence_only`.

Passing producer preflight or package-set intake review does not accept
packages, accept relations, publish registry metadata, mutate SpecPM sources,
remove `preview_only`, replace maintainer review, or create or merge a SpecPM
pull request.

A future consumer report may use
`SpecPMPackageSetHandoffIntakeReport` with
`apiVersion: specpm.package-set-handoff-intake/v0` and authority
`specpm_consumer_preflight`. That report would still be preflight evidence
only, not package acceptance, relation acceptance, or registry publication.

See also <doc:PackageSetHandoffProposal>, <doc:PackageSetAIEnrichment>,
<doc:PackageSetAIDraftProposal>, <doc:SpecPMHandoff>, and
<doc:ProposalAutomation>.
