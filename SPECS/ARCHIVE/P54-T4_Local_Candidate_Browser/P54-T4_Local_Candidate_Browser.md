# P54-T4 Local Candidate Browser

## Objective

Render a local static browser over a validated P54-T3 catalog so a maintainer
can find, compare, and resume review of portable candidates without contacting
the registry or executing candidate content.

## Deliverables

- Catalog loader that validates the P54-T2 standalone catalog schema.
- Deterministic corpus summary, filtering, search, sorting, and review queue
  model.
- Static local browser bundle with inert text rendering and no network calls.
- CLI command, representative browser fixture, tests, and operator docs.

## Acceptance

- Search and facets cover readiness, warnings, corrections, ecosystem,
  package shape, preflight, and review state.
- Queue position is preserved in browser local storage and URL state.
- Candidate and accepted-public-index domains remain visibly and structurally
  separate; this browser contains candidates only.
- Rendering never injects packet or catalog strings as HTML and never mutates
  review, SpecPM, or registry state.
