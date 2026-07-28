# Local Candidate Review Workbench Product Contract

Status: P54-T1 product contract.

P54-T1 defines a local-first tool for reviewing the 100 portable P53 candidate
packets. It is a product and security contract, not the Workbench
implementation.

The machine-readable fixture is:

```text
tests/fixtures/local_candidate_review_workbench_contract/p54-t1-local-candidate-review-workbench-contract.example.json
```

```text
apiVersion: spec-harvester.local-candidate-review-workbench-contract/v0
kind: SpecHarvesterLocalCandidateReviewWorkbenchContract
authority: producer_product_contract_evidence_only
```

## Authorized Input

The initial input is exactly the digest-bound P53-T14 archive containing 100
portable packets. P53-T15 selected
`make_selected_evidence_available_for_maintainer_disposition`; it did not
authorize automatic acceptance or publication.

The Workbench must verify the archive digest, packet count, packet digests, and
schemas before producing a catalog. Absolute paths, traversal members,
symlinks, device files, executable content, and extraction outside the
configured workspace are forbidden. Import must enforce configured archive,
member, extracted-byte, and member-count limits before resource use becomes
unbounded.

## Product Scope

The Workbench lets a maintainer:

- inspect portable candidate manifests, specs, evidence, and diagnostics;
- compare deterministic output with bounded Codex Spark proposal evidence;
- record explicit review dispositions with reasons and history;
- send only `accept_for_intake` candidates to read-only SpecPM preflight.

It is not a registry, publication service, package manager, model runner,
source acquisition system, or automatic acceptance engine. After verified
local import, ordinary review must work without a network connection, Docker
daemon, or model provider.

## Roles

| Role | Responsibility | Authority limit |
| --- | --- | --- |
| Operator | Configure the workspace and import a digest-verified bundle. | Cannot reinterpret invalid input as valid. |
| Reviewer | Inspect inert content and record a bounded disposition. | Cannot accept registry packages or relations. |
| Maintainer | Authorize read-only SpecPM intake preflight. | Later acceptance remains an external SpecPM action. |
| Producer | Supply proposal evidence. | Has no review or registry authority. |

## Trust Zones

```text
immutable import bundle
  -> generated read-only catalog
  -> mutable local review workspace
  -> external read-only SpecPM preflight
```

Every transition requires schema and digest validation. Candidate-controlled
content never crosses a trust boundary as executable content.

## Decision Lifecycle

```text
unreviewed
  -> in_review
  -> accept_for_intake | request_revision | defer | do_not_promote
```

A replacement does not erase history. Every decision binds reviewer identity,
timestamp, reason code, packet digest, and prior-decision digest. Writes are
validated and atomic, silent overwrite is forbidden, and state must survive
restart. A Workbench decision is not registry truth.

## Threat Model

Archive members, packet JSON, `specpm.yaml`, specifications, evidence,
diagnostics, repository metadata, and imported reviewer notes are untrusted.
The implementation must handle digest drift, malformed JSON/YAML, archive path
traversal, symlinks and special files, oversized input, hostile markup, script
execution, decision-request forgery, stale decisions, silent overwrite,
interrupted writes, and workspace escape.

## Browser Security

Every candidate-controlled value is rendered as inert text under a restrictive
Content Security Policy. Inline script is forbidden. Candidate content cannot
execute in the reviewer origin, invoke the decision service, or submit a
disposition. The decision service binds to loopback only and requires origin
validation plus a CSRF token for writes. P54-T9 must prove this with
hostile-markup fixtures.

## SpecPM Boundary

Only a current `accept_for_intake` decision may reach the bridge. The bridge
revalidates packet and decision digests and runs read-only SpecPM preflight.
It does not mutate SpecPM, accepted sources, or the public index.

## Non-Authority

P54-T1 did not clone or fetch repositories, run Codex, run LM Studio, run
adapters or plugins, install dependencies, invoke package managers, or execute
harvested code. It did not accept packages or relations, seed baselines, remove
`preview_only`, mutate accepted sources or registry truth, publish registry
metadata, or automatically promote candidates.

Raw prompts, raw provider responses, secrets, and chain-of-thought are not
persisted.

## Implementation Order

P54-T2 defines schemas before P54-T3 generates a catalog. P54-T4 through P54-T7
implement review UI and decision storage. P54-T8 adds the read-only SpecPM
bridge, P54-T9 validates the complete workflow, and P54-T10 records the exit
decision.
