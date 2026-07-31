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
package-shape, preflight, and review-state facets. The review surface uses a
two-pane layout: the selected candidate stays in the primary content pane while
the independently scrollable candidate queue remains in the right sidebar.
The selected queue item is kept in URL state and browser local storage, so
review resumes after a reload.
All untrusted values are inserted through text nodes, and its CSP permits only
its own static script, styles, and catalog data.
When included, the selected candidate opens with a compact health summary and
human-readable SpecPackage and BoundarySpec sections for metadata,
capabilities, intent IDs, scope, constraints, and evidence. Raw YAML remains
available in a collapsed drawer. Supporting diagnostics, provenance, generated
files, and proposal-only static-versus-Codex Spark comparison records are
available in separate collapsed evidence drawers below the specifications.

When the detail set contains a complete P55 semantic proposal, the Workbench
adds a side-by-side semantic review panel. It compares static summaries,
capabilities, intent IDs, interfaces, and evidence with AI purpose, capability,
interface, nearby-intent, and non-goal claims. Existing observed-intent reuse
and `intent.experimental.*` proposals are displayed in separate groups.

The reviewer may select proposal claims and record `accepted`, `edited`,
`rejected`, or `deferred`. Edited decisions retain only bounded replacement
text for selected claim IDs; original evidence bindings remain unchanged. The
action is sent to the local decision service and remains review evidence only.
It does not materialize a candidate, accept an experimental intent, mutate
SpecPM, or publish registry truth.
