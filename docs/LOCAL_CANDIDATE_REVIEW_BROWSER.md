# Local Candidate Review Browser

Render the static browser from a P54-T3 catalog:

```bash
spec-harvester render-local-candidate-review-browser \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --output review-workspace/browser
```

To include P54-T5 detail records, first generate the verified detail set and
then pass it to the renderer:

```bash
spec-harvester build-local-candidate-review-details \
  --archive SPECS/EVIDENCE/P53-T14/P53-T14_Portable_Handoff.tar.gz \
  --expected-sha256 db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63 \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --output review-workspace/details.json
spec-harvester render-local-candidate-review-browser \
  --catalog SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json \
  --details review-workspace/details.json \
  --output review-workspace/browser
```

Serve the output from a local static server. The browser is candidate-only: it
does not represent, modify, or merge with SpecPM's accepted public index.

It exposes corpus totals, search, readiness, warning, correction, ecosystem,
package-shape, preflight, and review-state facets. The selected queue item is
kept in URL state and browser local storage, so review resumes after a reload.
All untrusted values are inserted through text nodes, and its CSP permits only
its own static script, styles, and catalog data.
When included, the selected candidate opens a local detail panel with verified
source provenance, static evidence, generated files, diagnostics, and a
proposal-only static-versus-Codex Spark comparison.
