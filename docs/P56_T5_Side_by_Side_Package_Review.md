# P56-T5 Side-by-Side Package Review

The five original P56-T4 candidates can now be compared locally with pinned
README, complete retained package sets and a separately labeled semantic layer.
No candidate was corrected or regenerated. Human utility review is pending.

## Build and Open

From the repository, choose a new output directory outside the checkout:

```sh
python -m spec_harvester.exploratory_comparison --output /tmp/p56-comparison
```

Open the resulting `index.html` locally. For browser previews that block file
URLs, serve only the generated directory on loopback:

```sh
python -m http.server 8025 --bind 127.0.0.1 --directory /tmp/p56-comparison
```

Each repository has a stable `<repository-id>/index.html` route. New content
stays on the left. Reference navigation selects pinned README, retained packages
or the historical semantic record on the right. Mobile stacks the two columns.
The existing static spec renderer supplies Viewer overview; Complete spec puts
purpose first and renders every YAML field, with technical sections collapsible.
Original files offers inert text previews and unchanged downloads.

README is displayed as escaped original text, including Markdown/HTML syntax.
It is not a full GitHub README renderer; images and external resources do not
load. Distinguish this presentation limitation from source-content usefulness
in T6. The original README download preserves bytes for another local viewer.

## Included Surfaces

| Repository | New packages | Retained packages | Semantic layer |
|---|---:|---:|---|
| openai/codex | 1 | 4 | Proposal only, not applied |
| bitcoin/bitcoin | 1 | 1 | Proposal only, not applied |
| rtk-ai/rtk | 1 | 1 | Rejected historical proposal; portable proposal unavailable |
| axios/axios | 1 | 1 | Proposal only, not applied |
| n8n-io/n8n | 1 | 77 | Proposal only, not applied |

All 603 retained candidate-set files remain downloadable, including top-level
collection sidecars, not just the principal member. All 38 new original files
and five pinned READMEs are byte-identical to T4. Historical source-bundle and
member-boundary caveats remain explicit. Do not splice proposals into old YAML.
RTK's material evidence defect and omitted package provenance remain visible.

`SPECS/EVIDENCE/P56-T5/comparison.json` records the five routes, package counts,
pins and bindings to the T4 report/baseline lock. The generated site is local,
not committed as thousands of derivative files; the command reproduces it.

## Human Review Handoff

The local `human-review-template.json` has separate answers and source lookups
for new candidate, README, retained packages and semantic proposal. All answers,
times and dispositions start empty; it is a worksheet, not a save service.
For T6 use supported/partial/missing/incorrect with a source-backed reason;
unavailable baselines are unavailable, not incorrect. Never transfer facts
learned in one surface into another surface's artifact-only answer. Label
agent-assisted notes, record review/edit minutes separately, and preserve originals.

## Trust and Limits

Archive and selected-member digests are checked before rendering. Absolute,
traversal, duplicate and nonregular archive entries are rejected; input size and
entry counts are bounded. Output must be a new directory outside the repository.
All displayed source text is escaped, iframe content is sandboxed without
same-origin privilege, and wrapper pages prohibit remote resource loads. The
existing renderer executes only its own viewer JavaScript, never source code.
Failure can leave an incomplete output directory without a root index; use a new
directory after correcting inputs. Input/source files are never overwritten.

No provider run, acceptance, registry mutation, publication or automatic scoring.
This is an offline handoff around the existing renderer, not a new Workbench
decision service. Draft #372 and historical v1 remain unchanged.
