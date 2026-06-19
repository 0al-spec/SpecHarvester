# REVIEW P39-T4 Repository Plugin Applicability Detect CLI

## Verdict

PASS.

## Findings

No blocking findings.

## Scope Review

- The PR adds `repository-plugin-applicability-detect` to the existing
  `argparse` CLI.
- The command accepts explicit `--registry`, `--static-evidence-envelope`, and
  `--out` inputs.
- The command writes a full
  `SpecHarvesterRepositoryPluginApplicabilityReport` JSON file and prints a
  compact JSON summary.
- CLI errors for invalid registry identity and unsafe static evidence paths
  return exit code `2` with JSON error payloads.

## Boundary Review

The task preserves the intended authority and execution boundary:

- no default autonomous batch behavior change;
- no automatic report attachment to batch output;
- no third-party plugin loading;
- no plugin execution;
- no repository source file reads;
- no clone/fetch behavior;
- no dependency installation;
- no package manager invocation;
- no harvested code execution;
- no AI invocation;
- no package or relation acceptance;
- no registry publication;
- no `preview_only` removal;
- no treatment of plugin decisions as registry truth.

## Tests Reviewed

- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_cli.py -q`
- `PYTHONPATH=src pytest tests/test_repository_plugin_applicability_evaluator.py -q`
- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q -k 'static_repository_plugin_applicability_evaluator_plan or static_plugin_evidence_envelope or current_next_task'`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- `PYTHONPATH=src python -m spec_harvester repository-plugin-applicability-detect --registry tests/fixtures/repository_plugins/generic-registry.example.json --static-evidence-envelope tests/fixtures/repository_plugins/static-evidence-envelope.example.json --out /tmp/specharvester-p39-t4-validation-report.json`

## Follow-Up

No follow-up task is required from this review.

Proceed to P39-T5: opt-in autonomous batch integration while preserving
explicit `--repository-plugin-applicability` precedence.
