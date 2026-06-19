# P39-T5 Validation Report

Task: Repository Plugin Applicability Batch Integration
Date: 2026-06-19
Verdict: PASS

## Summary

P39-T5 integrates the deterministic repository plugin applicability evaluator
into `autonomous-candidate-batch` as an explicit opt-in sidecar path.

The batch now supports:

- copying an explicit `--repository-plugin-applicability` sidecar as before;
- generating the same sidecar from `--repository-plugin-registry` plus
  `--repository-plugin-static-evidence-envelope`;
- preserving explicit sidecar precedence when both modes are provided;
- rejecting partial auto-input pairs with an actionable error;
- preserving `appliedToDrafting: false` and `registryAuthority: false`.

The generated sidecar remains producer evidence only. It does not execute
plugins, load third-party plugin code, read repository source files, run package
managers, invoke AI, change parser/profile behavior, accept packages or
relations, publish registry metadata, or remove `preview_only`.

## Acceptance Evidence

- Default batch behavior still records `repositoryPluginApplicability.status:
  not_provided` and `repositoryPluginApplicabilitySidecarCount: 0`.
- Explicit `--repository-plugin-applicability` remains the highest-precedence
  source and records `sourceMode: explicit_sidecar`.
- `--repository-plugin-registry` plus
  `--repository-plugin-static-evidence-envelope` generates
  `reports/repository-plugin-applicability/repository-plugin-applicability-report.json`
  and records `sourceMode: auto_static_evaluator`.
- Providing only one auto-input fails before report emission.
- Invalid static evidence envelope paths fail before report emission.
- GitHub docs and DocC document the explicit precedence and trust boundary.

## Validation Commands

```bash
PYTHONPATH=src pytest tests/test_autonomous_candidate_batch.py tests/test_repository_plugin_applicability_evaluator.py tests/test_repository_plugin_applicability_cli.py tests/test_docs_contracts.py::test_autonomous_candidate_batch_docs_cover_local_lm_studio_boundary tests/test_docs_contracts.py::test_static_repository_plugin_applicability_evaluator_plan_is_documented -q
PYTHONPATH=src ruff format src tests
PYTHONPATH=src ruff check --fix src tests
PYTHONPATH=src ruff check src tests
PYTHONPATH=src ruff format --check src tests
git diff --check
PYTHONPATH=src pytest -q
swift build --target SpecHarvesterDocs
PYTHONPATH=src pytest --cov=src --cov-report=term-missing -q
rm -rf .docc-build && swift package --allow-writing-to-directory ./.docc-build generate-documentation --target SpecHarvester --output-path ./.docc-build --transform-for-static-hosting --hosting-base-path SpecHarvester; rc=$?; rm -rf .docc-build; exit $rc
```

## Results

- Targeted tests: `33 passed`.
- Full tests: `781 passed, 1 skipped`.
- Coverage: `91%`.
- Ruff check: passed.
- Ruff format check: passed.
- Whitespace check: passed.
- Swift docs build: passed.
- DocC static generation: passed.

## Out Of Scope

P39-T5 does not run a real multi-repository validation corpus. That remains
P39-T6.
