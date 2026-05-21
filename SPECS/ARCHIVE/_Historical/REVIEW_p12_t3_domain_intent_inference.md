## REVIEW REPORT — P12-T3 Domain Intent Inference

**Scope:** `origin/main..HEAD`
**Files:** 14

### Summary Verdict

- [x] Approve
- [ ] Approve with comments
- [ ] Request changes
- [ ] Block

### Critical Issues

- None.

### Secondary Issues

- None.

### Architectural Notes

- The implementation keeps the trust boundary intact: drafting consumes
  harvested documentation metadata and `PublicInterfaceIndex` JSON only. It does
  not inspect raw source checkouts, execute package code, run package managers,
  run tests/builds, or contact networks.
- Web framework clusters use explicit score thresholds above the default where
  broad terms could otherwise overmatch. This is important because `request`,
  `response`, `handler`, and `route` can appear in unrelated API libraries.
- Interface-index-derived semantic matches are not emitted as documentation
  paths. Clusters record `evidenceKinds`, and the separate
  `public_interface_index` evidence record remains responsible for interface
  artifact provenance.
- Public interface semantic token extraction is bounded by hard term and text
  size limits, and does not expand signatures into semantic terms.
- Strong domain clusters such as `intent.web.*`, `intent.swift.*`, and
  `intent.ios.*` can replace generic manifest capability intents. Broad
  language-neutral API/tooling clusters remain advisory evidence for
  manifest-backed packages unless no manifest capability exists.
- Generic advisory clusters can still appear alongside `intent.web.*` when the
  static evidence supports them. This is acceptable for `P12-T3`; it prevents
  Flask/Gin from collapsing to only generic claims without trying to solve
  taxonomy pruning in this task.

### Tests

- `PYTHONPATH=src python -m pytest` passed with `223 passed in 3.33s`.
- `ruff check src tests` passed.
- `ruff format --check src tests` passed with `43 files already formatted`.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  passed with total coverage `90.46%`.
- `swift package dump-package >/dev/null` passed.
- `swift build --target SpecHarvesterDocs` passed.
- Local Flask/Gin smoke passed and generated `intent.web.framework_surface`,
  `intent.web.http_routing`, `intent.web.middleware_pipeline`, and
  `intent.web.request_response_context` for both repositories.

### Next Steps

- FOLLOW-UP skipped: no actionable review findings.
- Continue with `P12-T4` to align generated `public_interface_index` evidence
  with the SpecPM validation contract.
