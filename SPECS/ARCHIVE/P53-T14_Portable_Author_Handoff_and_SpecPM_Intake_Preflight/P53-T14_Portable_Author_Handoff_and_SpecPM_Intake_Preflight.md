# P53-T14 Portable Author Handoff and SpecPM Intake Preflight

Status: In progress
Phase: Phase 53. Mass Popular Repository Parsing and Candidate Production
Owner: SpecHarvester producer evidence and SpecPM consumer preflight

## Motivation

P53-T13 selected all 100 frozen repositories for author review, but historical
static candidate roots and most Codex Spark proposal bodies were retained only
in temporary workspaces. Summary records and digests remain durable; missing
bodies must not be represented as portable evidence.

Phase 54 needs a stable local-review input contract that does not depend on
`/tmp`, machine-specific checkout paths, or mutable source repositories.

## Goal

Create one portable, digest-bound packet manifest per selected repository,
create an aggregate selected-candidate handoff accepted by the current SpecPM
consumer preflight, and record exactly which candidate and AI artifacts are
present, reconstructed, or unavailable.

## Deliverables

- Add a reusable P53 portable handoff builder and CLI.
- Validate P53-T13 identity, authority, status, source count, dispositions,
  privacy, source metadata digest, and per-repository proposal records.
- Copy only allowlisted candidate/evidence files into repo-relative packet
  roots and record SHA-256 for every copied file.
- Reject path traversal, symlinks, duplicate identities, digest drift,
  `preview_only` removal, and undeclared files.
- Record AI proposal bodies as `present` only when their bytes match the T13
  digest; otherwise record `summary_only_not_portable` without fabricating
  content.
- Emit an aggregate legacy-compatible selected-candidate handoff with 100
  selected candidates, zero deferred candidates, explicit external registry
  acceptance, and producer-only authority.
- Run SpecPM
  `producer-bundle preflight-selected-candidate-handoff` against the generated
  aggregate artifact and retain the sanitized report.
- Add focused tests, documentation contracts, and a representative committed
  fixture without committing the full generated 100-packet corpus.

## Acceptance Criteria

- Exactly 100 frozen repository identities are represented once.
- Every packet path is relative to its packet root and every packet file has a
  verified SHA-256 digest.
- Every candidate remains `preview_only`.
- The aggregate handoff passes SpecPM consumer preflight with zero errors and
  zero warnings when the repository root is supplied.
- Missing historical AI proposal bodies remain explicit and do not block
  deterministic candidate intake preflight.
- Raw prompts, raw provider responses, secrets, session state, and
  chain-of-thought are not copied or persisted.
- No package manager, candidate code, trusted adapter, plugin, or model is
  executed by the handoff builder.

## Non-Goals

- Do not accept packages or relations.
- Do not publish or mutate SpecPM registry metadata.
- Do not create a SpecPM pull request.
- Do not infer missing AI proposal content from summaries.
- Do not remove `preview_only`.
- Do not define the Phase 54 review UI or reviewer-decision storage.
