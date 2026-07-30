# P55-T6 Complete Portable Semantic Proposal Records

## Objective

Carry complete, validated P55 semantic proposals from provider execution into
portable author handoff packets and candidate detail bundles without retaining
raw provider data or granting application authority.

## Dependencies

- P53-T14 portable author handoff packet generation.
- P54-T5 candidate detail records and static-versus-AI comparison.
- P55-T3 bounded semantic author input packs.
- P55-T4 provider-neutral semantic author pass and allowlisted receipts.
- P55-T5 deterministic proposal quality reports.

## Deliverables

- A canonical, self-digesting portable semantic proposal record containing the
  complete proposal, deterministic quality report, allowlisted provider
  receipt, and candidate/source/proposal/receipt bindings.
- Fail-closed reconstruction that revalidates P55-T3/T4/T5 records, recomputes
  proposal, receipt, quality, and portable-record digests, and rejects binding
  drift or rejected quality reports.
- Optional P53 handoff integration that writes
  `semantic-proposal-record.json` into each packet and records its digest while
  preserving compatibility with packets that have no P55 semantic run.
- P54 candidate detail integration that exposes the complete record as inert
  JSON and reports semantic proposal, quality, and provider receipt digests in
  the comparison record.
- Updated schema, CLI option, GitHub Markdown, DocC documentation, and focused
  valid, absent, stale, sensitive-field, and detail-propagation tests.

## Portable Input Layout

When semantic records are supplied, each candidate directory contains:

- `input-pack.json`: the P55-T3 bounded input pack;
- `semantic-pass.json`: the P55-T4 normalized proposal and provider receipt;
- `quality-report.json`: the P55-T5 deterministic quality report.

These source records are revalidated but are not copied wholesale. The portable
record retains only the complete proposal, quality report, allowlisted receipt,
and digest bindings needed for later review.

## Integrity and Privacy

- Recompute the provider receipt digest excluding `receiptSha256`.
- Recompute the proposal digest excluding `proposalSha256`.
- Re-run P55-T5 evaluation and require exact equality with the supplied report.
- Bind the portable record to candidate ID, source bundle, proposal, receipt,
  and quality-report digests, then compute its own digest.
- Reject unknown receipt fields, raw prompts, raw responses, hidden reasoning,
  credentials, machine-local paths, rejected quality status, and any digest or
  identity drift.
- Keep generated JSON inert in the detail bundle; never interpret candidate
  markup or provider output as host instructions.

## Acceptance Criteria

- A valid P55-T3/T4/T5 triplet produces byte-identical portable records across
  repeated runs.
- Complete proposals, quality diagnostics, and provider receipts survive
  handoff and detail generation with all bindings intact.
- Missing semantic input remains explicitly `not_available` and does not break
  existing P53/P54 archives.
- Tampered evidence, proposal, receipt, quality report, or packet binding fails
  closed.
- No raw prompt, raw response, chain-of-thought, credential, or provider-local
  path is persisted.
- Full tests pass with at least 90% coverage; Ruff, formatting, diff, Swift
  manifest, and DocC checks pass.

## Non-Goals

- Provider invocation or corpus calibration.
- Browser-side comparison controls reserved for P55-T7.
- Reviewer edits or materialization reserved for P55-T8.
- SpecPM mutation, canonical intent acceptance, registry mutation, or
  publication.
