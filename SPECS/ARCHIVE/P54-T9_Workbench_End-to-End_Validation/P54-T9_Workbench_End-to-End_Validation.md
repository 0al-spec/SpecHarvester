# P54-T9 Workbench End-to-End Validation

## Objective

Validate the complete Local Candidate Review Workbench over the 100-candidate
P53 portable handoff corpus, including representative maintainer decisions from
all four campaign waves, restart behavior, hostile-content containment,
negative integrity cases, and the read-only SpecPM intake boundary.

## Dependencies

- `P53-T14` portable author handoff archive.
- `P54-T3` deterministic candidate review catalog.
- `P54-T5` complete candidate detail and comparison set.
- `P54-T6` restart-safe local decision store and loopback service.
- `P54-T7` reviewer actions and portable decision exchange.
- `P54-T8` read-only SpecPM intake bridge.

## Deliverables

1. A deterministic Workbench E2E validator and CLI command that consume the
   pinned P53 archive, catalog, detail set, and local SpecPM command.
2. A machine-readable report accounting for all 100 candidates and exactly 25
   candidates in each of waves 1 through 4.
3. Representative reviewer actions across all four waves, including all four
   dispositions, immutable history, restart hydration, export/import, and
   progress reconciliation.
4. Negative checks for malformed packet shape, archive/path traversal, source
   and packet digest drift, stale decisions, interrupted atomic writes,
   disallowed browser origin, invalid CSRF, and malformed detail bindings.
5. Browser-security checks proving restrictive CSP, no inline script,
   text-only candidate rendering, no persisted CSRF token, and inert hostile
   markup in both structured and supporting evidence.
6. A read-only SpecPM preflight for an explicitly approved representative,
   with package/report counts and zero registry mutations.
7. Desktop and narrow-viewport browser evidence covering queue navigation,
   human-readable YAML presentation, health summary, supporting evidence, and
   decision-service status without incoherent overlap.
8. Documentation, focused tests, portable example evidence, and a validation
   report.

## Acceptance Criteria

- The source archive, catalog, details, comparisons, and report remain
  digest-bound and deterministic.
- Every retained candidate is accounted for once and wave counts are
  `25/25/25/25`.
- At least one candidate from every Phase 53 wave receives a valid bounded
  disposition; restarting the store reproduces the same current decisions and
  progress.
- Interrupted writes leave neither a partial current decision nor temporary
  decision files and preserve prior immutable state.
- Malformed, traversing, stale, or digest-mismatched inputs fail closed with
  bounded errors.
- Hostile candidate markup remains inert data. It cannot create DOM elements,
  execute script, read the CSRF token, invoke the decision service, or weaken
  the Workbench CSP.
- Requests from a candidate/attacker origin and requests with an invalid CSRF
  token receive `403`; an allowed reviewer-origin action succeeds.
- Only a current `accept_for_intake` decision with `evidence_verified` reaches
  SpecPM validation.
- SpecPM validation operates on temporary reconstructed candidates only and
  produces proposal evidence with `registryMutationCount: 0`.
- No package manager, harvested repository code, adapter, model provider, raw
  prompt, raw response, hidden reasoning, registry mutation, or publication
  path runs.

## Validation

- Focused Workbench E2E and docs-contract tests.
- Desktop and narrow-viewport browser screenshots plus DOM/security checks.
- Full Python tests and coverage gate at 90% or higher.
- Ruff lint and format checks.
- Swift package manifest and DocC target build.
- Real local SpecPM validation with before/after repository-state checks.

## Non-Goals

- Reviewing all 100 candidates manually.
- Accepting or publishing packages or relations.
- Remote or multi-user service deployment.
- Authentication beyond the bounded loopback Origin/CSRF contract.
- AI execution or semantic proposal generation.
