# P54-T9 Validation Report

## Result

`PASS`

The Local Candidate Review Workbench completed a deterministic end-to-end
validation against the full 100-candidate P53 portable handoff corpus.

## Corpus Accounting

| Measure | Result |
| --- | ---: |
| Candidates | 100 |
| Detail records | 100 |
| Comparison records | 100 |
| Wave 1 | 25 |
| Wave 2 | 25 |
| Wave 3 | 25 |
| Wave 4 | 25 |
| Source bundle SHA-256 | `db2593d7b17fd3f0da348b3fce72ea86b510d7c562b82b78047b926608709e63` |

## Review Lifecycle

One deterministic representative from every campaign wave exercised a different
bounded disposition:

| Wave | Candidate | Disposition |
| --- | --- | --- |
| 1 | `affaan-m-ecc` | `accept_for_intake` |
| 2 | `airbnb-javascript` | `request_revision` |
| 3 | `clash-verge-rev-clash-verge-rev` | `defer` |
| 4 | `addyosmani-agent-skills` | `do_not_promote` |

The decision store reported four reviewed and 96 unreviewed candidates. Restart
hydration and portable export/import reproduced the same current state. A stale
decision was rejected, and an interrupted atomic write left no partial current
decision or temporary decision file.

## Integrity And Security

- All 100 archive packet digests were recomputed and compared with the catalog,
  detail, and comparison bindings before any passing report was emitted.
- Malformed packet shape, path traversal, detail digest drift, stale decision,
  and interrupted-write scenarios failed closed. The interrupted-write check
  commits replacement history first, fails the current-decision replacement,
  and proves rollback preserves the prior current decision and export.
- Candidate-origin and invalid-CSRF writes returned `403`; an allowed
  reviewer-origin write returned `201`.
- The browser bundle retains restrictive CSP directives, uses `textContent` for
  candidate data, has no inline script, and does not persist the CSRF token.
- Injected hostile markup remained inert text in `presentations.json` and was
  absent from executable assets.
- No package manager, harvested repository code, trusted adapter, AI provider,
  registry acceptance, or public-index publication path executed.
- Raw prompts, raw responses, and hidden reasoning were not persisted.

## SpecPM Boundary

Only the current `accept_for_intake` representative reached the real local
SpecPM validation command. One package passed, preview-only behavior remained
active, and `registryMutationCount` was `0`.

The sibling SpecPM worktree status digest was identical before and after the
validation:

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Browser Validation

Fresh Browser Preview checks covered desktop and narrow viewports:

- Desktop rendered the detail surface and a separate right-side queue with all
  100 candidate buttons.
- Narrow layout moved the queue above detail content and retained all 100
  candidates without horizontal document overflow or queue/detail overlap.
- Health metrics, human-readable package and BoundarySpec content, raw YAML
  drawers, supporting evidence, and decision-service status were visible.
- `Next` changed the selected candidate from `addyosmani-agent-skills` to
  `affaan-m-ecc` and synchronized the URL cursor.
- Browser console warnings and errors: `0`.

Evidence:

- `SPECS/EVIDENCE/P54-T9/P54-T9_Workbench_E2E_Report.json`
- `SPECS/EVIDENCE/P54-T9/P54-T9_Workbench_Desktop.png`
- `SPECS/EVIDENCE/P54-T9/P54-T9_Workbench_Mobile.png`

## Quality Gates

```text
uv run pytest tests/test_local_candidate_review_workbench_e2e.py tests/test_docs_contracts.py -q
205 passed

uv run pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
1162 passed, 1 skipped
Total coverage: 90.02%

uv run ruff check src tests
All checks passed

uv run ruff format --check src tests
170 files already formatted

swift package dump-package >/dev/null
passed

swift build --target SpecHarvesterDocs
Build complete
```

SwiftPM emitted the repository's existing warning that the DocC directory is
not declared as a target resource. It did not affect the successful build.
