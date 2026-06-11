# P27-T4 Validation Report — Author Review Viewer and Handoff Checklist

**Date:** 2026-06-12  
**Verdict:** PASS

## Scope

P27-T4 adds a producer-side `authorReview` surface for package-set viewer and
handoff artifacts. It derives author review checklists, weak claims, evidence
gaps, recommended edits, and member action summaries from existing
`authorReadyDraftSummary` and member quality reports.

The task does not change generated `specpm.yaml` or `specs/*.spec.yaml`
contents, does not run LLM providers, and does not add SpecPM acceptance
authority.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_docs_contracts.py tests/test_author_ready_quality_report.py tests/test_package_set_handoff_proposal.py tests/test_static_spec_renderer.py -q
```

Result: `75 passed in 0.78s`.

```bash
PYTHONPATH=src pytest -q
```

Result: `578 passed, 1 skipped in 5.37s`.

```bash
PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90
```

Result: `578 passed, 1 skipped`; total coverage `90.17%`; required coverage
`90%` reached.

```bash
PYTHONPATH=src ruff check .
PYTHONPATH=src ruff format --check src tests
git diff --check
```

Result: all passed; `96 files already formatted`.

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('src/spec_harvester/static_spec_renderer_assets.py').read_text()
match = re.search(r'VIEWER_JS = """(.*)"""\n$', text, re.S)
if not match:
    raise SystemExit('VIEWER_JS block not found')
Path('/tmp/spec-renderer.js').write_text(match.group(1))
PY
node --check /tmp/spec-renderer.js
```

Result: passed.

```bash
swift build --target SpecHarvesterDocs
```

Result: passed.

```bash
rm -rf .docc-build && \
swift package --allow-writing-to-directory ./.docc-build generate-documentation \
  --target SpecHarvester \
  --output-path ./.docc-build \
  --transform-for-static-hosting \
  --hosting-base-path SpecHarvester; \
rc=$?; rm -rf .docc-build; exit $rc
```

Result: passed. DocC emitted existing unrelated warnings for
`AcceptedPackageUpdateProposals` and inline command references in
`RealRepositoryQualityReport`.

```bash
rm -rf /tmp/specharvester-p27-t4-smoke && \
PYTHONPATH=src python -m spec_harvester xyflow-package-set-smoke \
  --output /tmp/specharvester-p27-t4-smoke
```

Result: passed. Synthetic `xyflow` package set produced `4` candidates,
`3` `contains` relations, and bundle-set preflight status `passed`.

```bash
rm -rf /tmp/specharvester-p27-t4-smoke/handoff && \
mkdir -p /tmp/specharvester-p27-t4-smoke/handoff && \
PYTHONPATH=src python -m spec_harvester package-set-handoff-proposal \
  --bundle-set /tmp/specharvester-p27-t4-smoke/package-set \
  --viewer /tmp/specharvester-p27-t4-smoke/viewer \
  --output /tmp/specharvester-p27-t4-smoke/handoff/package-set-handoff-proposal.json \
  --proposal-body /tmp/specharvester-p27-t4-smoke/handoff/package-set-handoff-proposal.md
```

Follow-up assertion:

```bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path('/tmp/specharvester-p27-t4-smoke')
proposal = json.loads((root / 'handoff/package-set-handoff-proposal.json').read_text())
viewer = json.loads((root / 'viewer/package-set.json').read_text())
markdown = (root / 'handoff/package-set-handoff-proposal.md').read_text()
assert proposal['authorReview']['decision'] == 'stop_for_author_review'
assert proposal['authorReview']['checklist']
assert proposal['authorReview']['weakClaims']
assert proposal['authorReview']['recommendedEdits']
assert viewer['authorReview']['decision'] == 'stop_for_author_review'
for needle in ['## Author Review Checklist', '## Weak Claims and Evidence Gaps', '## Recommended Edits']:
    assert needle in markdown, needle
print('author review handoff smoke ok')
PY
```

Result: `author review handoff smoke ok`.

## Acceptance Mapping

- Package-set viewer JSON exposes aggregate `authorReview`.
- Static viewer assets render aggregate checklist, weak claims, evidence gaps,
  recommended edits, and per-member author review lines.
- Handoff JSON and Markdown include the same author review surface.
- Docs and DocC describe `authorReview` as producer-side review evidence.
- Boundary language remains explicit: this is not SpecPM registry acceptance,
  maintainer approval, upstream endorsement, or public registry publication.
