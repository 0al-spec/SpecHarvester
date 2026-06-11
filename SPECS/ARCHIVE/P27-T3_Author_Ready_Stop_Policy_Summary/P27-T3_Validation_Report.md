# P27-T3 Validation Report

Task: `P27-T3 Author-Ready Stop Policy Summary`

## Result

PASS.

## Scope Validated

- Added deterministic author-ready stop decisions:
  - `stop_for_author_review`;
  - `continue_generation`;
  - `blocked_until_inputs_change`.
- Single `draft_spec_package` results expose `authorReadyDraftSummary`.
- `package-set-draft.json`, package-set handoff proposals, and static
  package-set viewer JSON expose aggregate `authorReadyDraftSummary`.
- Package-set summaries include `memberCounts`, per-member decisions,
  `blockingReasons`, `reviewableDimensions`, `topAuthorActionItems`, and
  non-authority notes.
- AI draft and AI enrichment proposals expose `stopPolicySummary` for model-loop
  decisions without claiming package acceptance.
- GitHub docs, DocC, roadmap, Workplan, and `next.md` document the boundary.

## Commands

```bash
PYTHONPATH=src pytest tests/test_author_ready_quality_report.py tests/test_collector.py::test_draft_spec_package_writes_candidate_files tests/test_candidate_bundle_e2e.py tests/test_package_set_drafter.py::test_package_set_drafter_writes_scoped_candidate_bundles tests/test_package_set_handoff_proposal.py tests/test_static_spec_renderer.py::test_static_package_set_renderer_writes_review_site tests/test_package_set_ai_draft_proposal.py tests/test_package_set_ai_enrichment.py -q
```

Result: `37 passed`.

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_package_set_handoff_proposal tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_report -q
```

Result after archive pointer update: `3 passed`.

```bash
PYTHONPATH=src pytest -q
```

Initial result before archive pointer update: failed because `next.md` was
temporarily `In Progress` during the Flow run.

Final result after selecting P27-T4: `576 passed, 1 skipped`.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `576 passed, 1 skipped`; total coverage `90.16%`.

```bash
PYTHONPATH=src ruff check .
```

Result: passed.

```bash
PYTHONPATH=src ruff format --check src tests
```

Result: passed.

```bash
git diff --check
```

Result: passed.

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc
```

Result: passed with pre-existing unrelated DocC warnings for
`AcceptedPackageUpdateProposals` and inline command links.

```bash
rm -rf /tmp/specharvester-p27-t3-smoke && PYTHONPATH=src python -m spec_harvester xyflow-package-set-smoke --output /tmp/specharvester-p27-t3-smoke
```

Result: `status: passed`.

Additional summary check:

```text
package-set/package-set-draft.json author_ready_draft stop_for_author_review
viewer/package-set.json author_ready_draft stop_for_author_review
```

## Notes

- The stop-policy summary is producer-side review evidence only.
- Clean summaries tell operators to stop model iteration and hand off for
  author review; they do not imply SpecPM registry acceptance, maintainer
  approval, relation acceptance, or upstream endorsement.
- P27-T4 is the next UI/handoff task: render author review checklists, weak
  claims, evidence gaps, and recommended edits from these stable JSON surfaces.
