# Local Candidate Review Browser

Render the static browser from a P54-T3 catalog:

```bash
spec-harvester render-local-candidate-review-browser \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --output review-workspace/browser
```

Serve the output from a local static server. The browser is candidate-only: it
does not represent, modify, or merge with SpecPM's accepted public index.

It exposes corpus totals, search, readiness, warning, correction, ecosystem,
package-shape, preflight, and review-state facets. The selected queue item is
kept in URL state and browser local storage, so review resumes after a reload.
All untrusted values are inserted through text nodes, and its CSP permits only
its own static script, styles, and catalog data.
