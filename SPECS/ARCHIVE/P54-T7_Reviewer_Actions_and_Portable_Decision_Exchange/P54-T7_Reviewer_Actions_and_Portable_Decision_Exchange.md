# P54-T7 Reviewer Actions and Portable Decision Exchange

## Objective

Add bounded reviewer actions, validated decision reasons, progress summaries,
and non-authoritative portable decision import/export to the local Candidate
Review Workbench.

## Dependencies

- `P54-T2` Local Candidate Review Workbench Schemas
- `P54-T3` Deterministic Local Candidate Review Catalog
- `P54-T5` Candidate Detail Review Surface
- `P54-T6` Local Review-Decision Service and Storage Contract

## Scope

1. Define a versioned reason taxonomy covering `accept_for_intake`,
   `request_revision`, `defer`, and `do_not_promote`.
2. Accept bounded reviewer action payloads and construct schema-valid,
   catalog-bound decisions with optimistic replacement history.
3. Report corpus progress from current decisions without modifying the catalog
   or registry.
4. Export deterministic portable evidence containing complete decision history
   and import it only when source-bundle, packet, reason, and lineage checks
   pass.
5. Add local browser controls for reviewer identity, disposition, reason,
   optional notes, service connection, save, export, and import.
6. Preserve the read-only SpecPM and accepted-registry boundary.

## Out Of Scope

- Automatic acceptance or promotion.
- Mutation of harvested packages, the accepted registry, or SpecPM.
- Remote or multi-user review service deployment.
- Authentication beyond the existing loopback Origin and CSRF boundary.

## Verification

- Unit tests cover every disposition and reason validation.
- Replacement decisions preserve immutable prior history.
- Progress counts reconcile to the complete catalog.
- Export is deterministic and schema-valid.
- Import rejects changed source bundles, stale packet bindings, invalid reason
  mappings, broken lineage, and conflicting local state.
- Browser assets expose all actions while keeping candidate content inert and
  keeping the CSRF token out of generated files.
- Repository lint, type, unit, docs-contract, and full quality gates pass.

## Success Criteria

- A maintainer can record and replace any of the four bounded dispositions.
- Every recorded decision uses an allowed reason code and optional bounded note.
- Current progress and remaining unreviewed count are explicit.
- Review evidence can be moved between machines and restored reproducibly
  without becoming registry truth.
