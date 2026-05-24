# P15-T4 Validation Report

Task: `P15-T4`
Date: 2026-05-24
Branch: `feature/P15-T4-local-validation-matrix`

## Local Matrix Inputs

The local validation manifest was kept under ignored `.smoke/` paths and was
not committed.  The matrix used six operator-managed public checkout paths:

| Repository | Shape | Revision |
|---|---|---|
| `cupertino` | Swift/SPM + Xcode workspace | `65dcae720527d0d1beef88ef3b479f966b41922c` |
| `navigation-split-view` | Swift/SPM + Xcode project | `2c88df206b5ce7234cd33d6b88113e3da64625ce` |
| `xyflow` | JavaScript/TypeScript npm/pnpm monorepo | `a585680d8a2d407b7891101b62a84a35cb2d1937` |
| `flask` | Python `pyproject.toml` web framework | `954f5681f405182d852bb24d1cc68499c7a6b907` |
| `gin` | Go module web framework | `5f4f96401b979708ba0f37c612d9642f9c79d371` |
| `docc2context` | Swift/SPM documentation-first CLI | `a2babcc1780ca034472726d7da4b6ad2d6489f76` |

## Commands

```bash
PYTHONPATH=src python -m spec_harvester source-manifests .smoke/p15-t4-inputs
```

Result: pass.  Six repository source entries validated.

```bash
PYTHONPATH=src python scripts/run_real_repository_validation.py \
  --inputs .smoke/p15-t4-inputs \
  --out .smoke/output/p15-t4-local-validation \
  --emit-interface-indexes \
  --analyzer-cache-dir .smoke/output/p15-t4-analyzer-cache \
  --skip-specpm-validation
```

Result: pass.  Runner status `ok`; six packages collected and drafted.

```bash
PYTHONPATH=src python -m spec_harvester quality-report \
  --run-report .smoke/output/p15-t4-local-validation/run-report.json \
  --output .smoke/output/p15-t4-local-validation/quality-report.json
```

Result: pass.  Quality summary: 6 pass, 0 review, 0 fail, 0 unscored.

```bash
PYTHONPATH=/Users/egor/Development/GitHub/0AL/SpecPM/src \
  python -m specpm.cli validate ".smoke/output/p15-t4-local-validation/<id>" --json
```

Result: pass for all six generated candidates when run manually against the
adjacent local SpecPM checkout.

## Matrix Outcome

| Repository | Runner | Public interface index | Quality verdict | Manual SpecPM | Failure class |
|---|---|---|---|---|---|
| `cupertino` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | pass | broad documentation/API intent duplication |
| `navigation-split-view` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | pass | package identity normalized from hyphen to underscore |
| `xyflow` | `ok` | yes | `pass` (`strong`/`strong`/`partial`) | pass | none |
| `flask` | `ok` | yes | `pass` (`strong`/`strong`/`weak`) | pass | `LICENSE.txt` ambiguous; analyzer coverage undercount |
| `gin` | `ok` | yes | `pass` (`strong`/`strong`/`weak`) | pass | analyzer coverage undercount |
| `docc2context` | `ok` | no (`manifest_only`) | `pass` (`strong`/`strong`/`partial`) | pass | broad documentation/API intent duplication |

Smoke triage status: `attention_required`.

Advisory counts:

- 0 batch errors
- 0 batch warnings
- 9 duplicate intent claims
- 0 duplicate claim issues
- 2 license/provenance issues
- 1 namespace issue
- 12 total advisory issues

## Safety Checks

- No harvested package scripts, dependency installers, tests, or builds were
  run.
- No package registry calls were made.
- No SpecNode runtime, provider discovery, provider execution, or model call was
  invoked.
- Generated `.smoke/` inputs and outputs remained uncommitted.

## Quality Gates

The following gates passed before the EXECUTE checkpoint:

- `PYTHONPATH=src python -m pytest`: 349 passed, 1 skipped
- `ruff check src tests`: passed
- `ruff format --check src tests`: passed after formatting the new docs
  contract test
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`:
  349 passed, 1 skipped; total coverage 90.64%
- `swift package dump-package >/dev/null`: passed
- `swift build --target SpecHarvesterDocs`: passed
