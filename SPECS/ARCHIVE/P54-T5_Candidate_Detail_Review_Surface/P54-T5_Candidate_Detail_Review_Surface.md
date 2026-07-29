# P54-T5 Candidate Detail Review Surface

## Objective

Generate digest-bound, inert candidate detail records from the portable P53-T14
archive and add a detail view to the local review browser.

## Acceptance

- Detail records bind to exact packet bytes and expose only verified source
  provenance, revision, license, topology, generated candidate files,
  relations, evidence, diagnostics, and AI summary metadata.
- Candidate file contents are represented as inert text; no repository or
  candidate content executes.
- Browser navigation opens a selected detail record without network access.
- Static and AI evidence remain visibly distinct and proposal-only.
