# Package-Set Proposal Intake Checklist

Status: P26-T3 SpecPM-facing package-set intake checklist.

This checklist defines what SpecPM maintainers should verify when reviewing a
`SpecHarvesterPackageSetHandoffProposal`.

The proposal identity is:

```json
{
  "apiVersion": "spec-harvester.package-set-handoff-proposal/v0",
  "kind": "SpecHarvesterPackageSetHandoffProposal",
  "schemaVersion": 1
}
```

SpecHarvester produces review evidence. SpecPM owns package acceptance,
relation acceptance, public registry metadata, accepted-source mutation, and
maintainer decisions.

## Intake Inputs

Before a maintainer considers package members or relations, the proposal should
link:

- `package_set_draft`;
- `package_relation_proposals`;
- `bundle_set_preflight`;
- `package_set_viewer`;
- `member_candidate_bundle`;
- `member_manifest`;
- `member_boundary_spec`;
- `member_producer_receipt`;
- `member_validation_report`;
- `member_diagnostics`;
- `member_quality_report`;
- `package_relation_summary`.

The reviewer should also inspect `authorReadyDraftSummary` and `authorReview`
to decide whether the producer loop should stop for author review, continue
generation, or block until inputs change.

## Package Member Checklist

For every proposed package member:

- verify package identity, namespace, version, and repository provenance;
- verify `preview_only` remains present until explicit SpecPM acceptance;
- verify `member_manifest`, `member_boundary_spec`, and
  `member_producer_receipt` evidence;
- verify `member_validation_report` and `member_diagnostics` have reviewable
  status and no hidden hard failures;
- verify `member_quality_report` and `authorReadyDraftSummary` support author
  review rather than automatic acceptance;
- verify `bundle_set_preflight` did not report member count or digest drift;
- decide member package acceptance independently from relation acceptance.

Package member acceptance requires a SpecPM-owned registry decision outside the
producer proposal.

## Relation Checklist

For every proposed relation:

- verify relation type, subject, object, and scope;
- verify relation endpoints exist in the proposed member set;
- verify `package_relation_proposals` and `package_relation_summary` agree;
- verify package-set topology is evidence-backed, for example
  `xyflow.workspace contains xyflow.react`;
- reject unknown relation types or relation endpoints that are not present in
  the reviewed package set;
- decide relation acceptance separately from member package acceptance.

Relation acceptance requires a SpecPM-owned registry decision outside the
producer proposal.

Package member acceptance is separate from relation acceptance.

## Acceptance Boundary

The proposal must preserve:

`registryAcceptanceDecision.status: external_required` is required for package-set intake.

```json
{
  "registryAcceptanceDecision": {
    "status": "external_required",
    "requiredFor": ["public_index_acceptance", "package_relation_acceptance"],
    "producerAuthority": "evidence_only"
  }
}
```

`public_index_acceptance` applies to package members.
`package_relation_acceptance` applies to relations.
`producerAuthority: evidence_only` means the producer artifact is review
evidence, not acceptance authority.

Passing producer preflight or package-set intake review does not:

- accept packages;
- accept relations;
- publish registry metadata;
- mutate SpecPM sources;
- remove `preview_only`;
- replace maintainer review;
- create or merge a SpecPM pull request.

In short, package-set intake review does not accept packages, accept
relations, publish registry metadata, mutate SpecPM sources, remove
`preview_only`, or create or merge a SpecPM pull request.

## Suggested SpecPM Report

A future SpecPM implementation may emit a consumer-side report such as:

```json
{
  "apiVersion": "specpm.package-set-handoff-intake/v0",
  "kind": "SpecPMPackageSetHandoffIntakeReport",
  "schemaVersion": 1,
  "authority": "specpm_consumer_preflight",
  "input": {
    "kind": "SpecHarvesterPackageSetHandoffProposal",
    "digest": "sha256:<proposal-json-digest>"
  },
  "summary": {
    "memberPackageCount": 3,
    "relationProposalCount": 3,
    "memberAcceptanceDecisionRequired": true,
    "relationAcceptanceDecisionRequired": true
  },
  "status": "passed"
}
```

That report would still be consumer preflight evidence only. It would not be
package acceptance, relation acceptance, or registry publication.

See also:

- [`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md)
- [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md)
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md)
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md)
- [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md)
