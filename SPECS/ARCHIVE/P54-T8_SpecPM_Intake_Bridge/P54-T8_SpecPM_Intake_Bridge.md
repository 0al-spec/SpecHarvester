# P54-T8 SpecPM Intake Bridge

## Objective

Add a bounded read-only bridge that selects only current
`accept_for_intake` decisions, revalidates their portable packet and immutable
decision bindings, runs SpecPM validation over reconstructed preview candidate
packages, and emits non-authoritative intake proposal evidence.

## Dependencies

- P53-T14 portable author handoff archive and packet digests.
- P54-T3 validated local candidate review catalog.
- P54-T6 immutable local review-decision storage.
- P54-T7 reason-validated reviewer dispositions.

## Deliverables

1. A `build-local-specpm-intake-proposal` CLI command accepting the portable
   archive, expected archive digest, catalog, review workspace, SpecPM command,
   optional SpecPM `PYTHONPATH`, and output path.
2. Revalidation of archive, packet, catalog, and current decision digests before
   any candidate reaches SpecPM.
3. Safe temporary reconstruction of candidate package files from the verified
   packet inventory, with no symlink, traversal, special-file, or undeclared
   archive extraction.
4. Read-only `specpm validate --json` execution for every reconstructed package
   belonging to an approved repository candidate.
5. A deterministic proposal record containing reviewer and digest bindings,
   bounded SpecPM validation summaries, package identities, explicit
   non-authority statements, and zero registry mutations.
6. Documentation and focused tests for approved, skipped, stale, tampered,
   invalid, and no-mutation paths.

## Acceptance Criteria

- Only a current `accept_for_intake` decision with the required
  `evidence_verified` reason is eligible.
- The archive digest, packet digest, catalog binding, immutable decision
  history, and current decision digest are revalidated on every run.
- Every candidate file is reconstructed from an already verified regular
  archive member beneath a temporary root; no repository code, package manager,
  build, test, adapter, or network operation is invoked.
- SpecPM validation receives candidate package directories only and cannot
  mutate SpecPM accepted sources, manifests, public-index files, or the review
  workspace.
- Invalid SpecPM packages remain explicit failed preflight evidence and are not
  represented as intake-ready.
- Output is deterministic for identical archive, catalog, decisions, and
  normalized SpecPM reports, apart from no timestamps or machine-local paths.
- The report records `registryMutationCount: 0`, creates no SpecPM pull request,
  preserves `preview_only`, and does not accept packages or relations.

## Validation

- Focused intake-bridge and decision-store tests.
- CLI coverage for generated output.
- Ruff check and format check.
- Full Python test suite and coverage gate.
- SpecPM integration test through the configured local checkout.

## Non-Goals

- SpecPM package acceptance, accepted-source preparation, manifest updates, or
  public-index publication.
- Automatic reviewer decisions or promotion based on preflight success.
- AI/provider invocation or semantic proposal changes.
- Repository checkout access or harvested-code execution.
