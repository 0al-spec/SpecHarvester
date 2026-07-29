# Local Candidate Review Browser

Render the static browser from a P54-T3 catalog with the
`render-local-candidate-review-browser` command.

The browser is candidate-only: it does not represent, modify, or merge with
SpecPM's accepted public index. It offers corpus totals, search, all catalog
facets, and a URL/local-storage-backed review queue. Untrusted values are
inserted through text nodes, and its CSP permits only local static assets.

An optional P54-T5 detail set adds a selected-candidate panel for verified
provenance, generated package files, diagnostics, and proposal-only
static-versus-Codex Spark comparison evidence.
