# P16-T5 Validation Report

Task: `P16-T5 — Rerun Representative Local Validation Matrix`
Date: 2026-05-28
Branch: `feature/P16-T5-rerun-local-validation-matrix`
Verdict: PASS

## Local Matrix Inputs

The local validation manifest and generated outputs were kept under ignored
`.smoke/` paths and were not committed.  The rerun used the same six
operator-managed public checkout paths as P15-T4.

| Repository | Shape | Revision | Staged preflight |
|---|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `65dcae238d30cfbd0d9d15ae10f7b8c67575c19b` | pass |
| `navigation-split-view` | Swift/SPM + Xcode project | `2c88df50b8f587560b91f6027e9ea275aee17060` | pass |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `a58568f11bc0e1a1bdca1b3549e959e2e1ca0cdd` | pass |
| `flask` | Python `pyproject.toml` web framework | `954f5684e4841aad84a8eec7ace7b81a0d3f6831` | pass |
| `gin` | Go module web framework | `5f4f9643258dc2a65e684b63f12c8d543c936c67` | pass |
| `docc2context` | Swift/SPM documentation-first CLI | `a2babcc4910c87bbd1b65f9a4221097f5ae4b753` | pass |

## Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/p16-t5-inputs
```

Result: pass.  Six repository source entries validated.

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p16-t5-inputs \
  --out .smoke/output/p16-t5-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p16-t5-analyzer-cache \
  --skip-specpm-validation
```

Result: pass.  Runner status `ok`; six packages collected and drafted.

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p16-t5-local-validation/run-report.json \
  --candidates-root .smoke/output/p16-t5-local-validation \
  --output .smoke/output/p16-t5-local-validation/quality-report.json
```

Result: pass.  Quality summary: 6 pass, 0 review, 0 fail, 0 unscored.

```bash
PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src \
  python -m specpm.cli validate ".smoke/output/p16-t5-local-validation/<id>" --json
```

Result: warning-only for all six generated candidates.  Each candidate reported
only the expected `preview_only_package` warning and no errors.

## Matrix Outcome

| Repository | Runner | Public interface index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|
| `cupertino` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | warning-only | residual specific web intent overlap |
| `navigation-split-view` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | warning-only | none |
| `xyflow` | `ok` | yes | `pass` (`strong`/`strong`/`strong`) | warning-only | none |
| `flask` | `ok` | yes | `pass` (`strong`/`strong`/`partial`) | warning-only | low `collected_unknown_license_evidence` |
| `gin` | `ok` | yes | `pass` (`strong`/`strong`/`partial`) | warning-only | none |
| `docc2context` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | warning-only | residual specific web intent overlap |

Smoke triage status: `attention_required`.

Advisory counts:

- 0 batch errors
- 0 batch warnings
- 4 duplicate intent claims
- 0 duplicate claim issues
- 1 license/provenance issue
- 0 namespace issues
- 5 total advisory issues

## Delta from P15-T4

| Signal | P15-T4 baseline | P16-T5 rerun | Result |
|---|---:|---:|---|
| Total advisory issues | 12 | 5 | improved |
| Duplicate intent claims | 9 | 4 | improved |
| License/provenance issues | 2 | 1 | improved |
| Namespace/upstream issues | 1 | 0 | cleared |
| Quality pass count | 6 | 6 | preserved |

The broad language-neutral duplicate intent noise from P15-T4 is gone from
`duplicates.intent`.  Remaining duplicate intent findings are specific web
claims: `intent.web.framework_surface`, `intent.web.http_routing`,
`intent.web.middleware_pipeline`, and `intent.web.request_response_context`.

## Safety Checks

- No harvested package scripts, dependency installers, tests, or builds were
  run.
- No package registry calls were made.
- No SpecNode runtime, provider discovery, provider execution, or model call was
  invoked.
- Generated `.smoke/` inputs and outputs remained ignored and uncommitted.

## Quality Gates

- `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q`
  - PASS: 24 passed.
- `PYTHONPATH=src python -m pytest`
  - PASS: 418 passed, 1 skipped.
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
  - PASS: 418 passed, 1 skipped, total coverage 91.87%.
- `ruff check src tests`
  - PASS.
- `ruff format --check src tests`
  - PASS: 68 files already formatted.
- `swift package dump-package >/dev/null`
  - PASS.
- `swift build --target SpecHarvesterDocs`
  - PASS.
- `git diff --check`
  - PASS.
