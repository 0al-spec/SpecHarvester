# P54-T1 Local Candidate Review Workbench Product Contract

## Objective

Define the product contract, threat model, reviewer roles, decision lifecycle,
portable input boundary, and acceptance/non-authority rules for a local-first
Workbench that reviews the 100 digest-bound P53-T14 candidate packets.

## Dependencies

- P53-T14 portable handoff execution summary and retained 100-packet archive.
- P53-T15 exit decision authorizing maintainer disposition.
- Phase 54 Workplan security requirements, including inert rendering,
  restrictive CSP, and blocked candidate-origin decision requests.

## Deliverables

- `docs/LOCAL_CANDIDATE_REVIEW_WORKBENCH_CONTRACT.md`.
- Matching DocC article.
- Machine-readable contract fixture with source digests and explicit boundaries.
- Documentation index, capabilities, roadmap, and DocC navigation references.
- Contract tests for source binding, product scope, roles, lifecycle, threats,
  trust zones, security controls, and non-authority.

## Product Boundary

The Workbench is a local maintainer tool for inspecting portable proposal-only
candidates, comparing deterministic and Codex-assisted evidence, recording
review dispositions, and preparing explicitly approved candidates for read-only
SpecPM intake preflight. It is not a registry, publication service, package
manager, model runner, source acquisition system, or automatic acceptance
engine.

## Threat Model

Treat packet archives, manifests, specifications, evidence, diagnostics,
repository metadata, and reviewer notes imported from elsewhere as untrusted.
Cover digest drift, malformed JSON/YAML, archive traversal, symlinks, oversized
input, hostile markup, script execution, decision-service request forgery,
stale decisions, silent overwrite, interrupted writes, and workspace escape.

## Roles

- `operator`: configures a local workspace and imports a verified bundle.
- `reviewer`: inspects candidates and records bounded dispositions.
- `maintainer`: authorizes intake preflight and remains responsible for any
  later SpecPM acceptance action.
- `producer`: supplies proposal evidence but has no review or registry authority.

## Decision Lifecycle

`unreviewed -> in_review -> accept_for_intake | request_revision | defer |
do_not_promote`, with explicit replacement history. Decisions must bind reviewer
identity, timestamp, reason, packet digest, and prior-decision digest. No
Workbench state is registry truth.

## Acceptance Criteria

- Contract and fixture bind P53-T14 and P53-T15 artifacts by SHA-256.
- Exactly 100 portable packets are in the approved initial input scope.
- Offline operation is required after local import.
- Candidate content is inert and cannot invoke the decision service.
- Reads/writes remain within the configured review workspace.
- Decisions are validated, atomic, append-auditable, digest-bound, and
  restart-safe.
- Only `accept_for_intake` may reach a read-only SpecPM preflight bridge.
- No package/relation acceptance, accepted-source mutation, baseline seeding,
  `preview_only` removal, registry publication, or automatic promotion occurs.

## Non-Goals

- Implementing schemas, catalog generation, UI, local decision service, or
  SpecPM bridge.
- Shared multi-user hosting, remote authentication, or cloud synchronization.
- Running Codex, LM Studio, adapters, package managers, builds, tests, plugins,
  or harvested repository code.
- Expanding beyond the P53 corpus.

## Validation

- Focused documentation contract tests.
- Full pytest and coverage threshold.
- Ruff check and scoped format check.
- `git diff --check`.
- Swift package and DocC target checks.
