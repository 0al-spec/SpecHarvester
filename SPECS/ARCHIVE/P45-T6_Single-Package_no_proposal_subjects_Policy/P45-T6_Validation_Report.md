# P45-T6 Validation Report

Task: P45-T6 Single-Package no_proposal_subjects Policy
Date: 2026-06-20
Branch: `feature/P45-T6-single-package-no-proposal-subjects-policy`
Verdict: PASS

## Scope

P45-T6 adds a package-set AI draft zero-subject policy. Diagnostic-clean
zero-subject output is non-blocking only when deterministic inventory contains
exactly one package, the validation guard passed, diagnostics are clean, and
package-set identity is stable. Multi-package zero-subject output and
warning/failed single-package output continue to report `no_proposal_subjects`.

## Validation Commands

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q` | PASS, 21 passed |
| `PYTHONPATH=src python -m pytest tests/test_author_ready_quality_report.py -q -k no_subjects` | PASS, 1 passed, 11 deselected |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_specpm_shared_fixture_policy -q` | PASS, 1 passed |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar -q` | PASS, 1 passed |
| `ruff check src/spec_harvester/package_set_ai_draft_proposal.py src/spec_harvester/producer_reports.py tests/test_package_set_ai_draft_proposal.py tests/test_author_ready_quality_report.py tests/test_docs_contracts.py` | PASS |
| `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py src/spec_harvester/producer_reports.py tests/test_package_set_ai_draft_proposal.py tests/test_author_ready_quality_report.py tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |

## Notes

- The default `stop_policy_summary_from_diagnostics` behavior remains
  unchanged; the package-set AI draft layer applies the single-package exception
  after the generic summary is computed.
- P45-T6 does not rerun the operational MVP corpus. P45-T7 owns rerun evidence.
- AI sidecars remain proposal-only and do not accept packages, accept
  relations, publish registry metadata, or persist raw prompts, raw responses,
  secrets, or chain-of-thought.

## Post-Archive Follow-Up Addendum

A preliminary P45-T7 live rerun exposed two bounded input-shape gaps in the
P45-T6 policy surface:

- FastAPI and Gin had source manifests with stable package ids, but their
  generated workspace inventories contained no package manifest records. The AI
  draft request now carries a source-backed package identity fallback so the
  single-package zero-subject policy can evaluate the deterministic package id.
- Xyflow model output can use common relation endpoint aliases such as
  `source` and `target`; relation proposal normalization now maps those aliases
  to `sourcePackageId` and `targetPackageId` before validation.
- A second P45-T7 live rerun showed the same endpoint aliases can be nested
  objects (`sourcePackage` / `targetPackage`) and that successful bounded JSON
  repair can add a warning-level `ai_json_repair_needed` diagnostic without
  changing the single-package proposal subject. Nested endpoint aliases now
  resolve `packageId` or `id`, and successful repair is non-blocking for the
  single-package zero-subject policy when no other diagnostics are present.
- A third P45-T7 live rerun showed xyflow can omit explicit relation target
  fields while keeping an unambiguous selected member package id in the relation
  id. Relation target recovery now also accepts an unambiguous selected member
  id in the relation id or a single-item target list.

Additional validation after the follow-up:

| Command | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest tests/test_package_set_ai_draft_proposal.py -q` | PASS, 28 passed |
| `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py::test_docc_and_github_docs_cover_author_ready_draft_quality_bar -q` | PASS |
| `ruff check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py` | PASS |
| `ruff format --check src/spec_harvester/package_set_ai_draft_proposal.py tests/test_package_set_ai_draft_proposal.py tests/test_docs_contracts.py` | PASS |
| `git diff --check` | PASS |
