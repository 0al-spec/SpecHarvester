# P15-T1 Validation Report

Task: `P15-T1` Real-Repository Refinement Validation Plan
Date: 2026-05-23
Verdict: PASS

## Summary

Implemented the SpecHarvester-side real-repository refinement validation plan.
The plan documents safe local manifests, command sequencing, expected
non-committed outputs, quality scoring, and cross-repository ownership routing
without assigning SpecNode runtime/provider responsibilities to SpecHarvester.

## Scope Validated

- GitHub documentation page:
  `docs/REAL_REPOSITORY_REFINEMENT_VALIDATION.md`.
- DocC mirror:
  `Sources/SpecHarvester/Documentation.docc/RealRepositoryRefinementValidation.md`.
- Documentation index and workflow links.
- Docs contract coverage for SpecHarvester/SpecNode/Platform/SpecPM/`.0al`
  boundary statements.

## Quality Gates

| Gate | Command | Result |
| --- | --- | --- |
| Docs contract tests | `PYTHONPATH=src python -m pytest tests/test_docs_contracts.py -q` | PASS, 17 passed |
| Tests | `PYTHONPATH=src python -m pytest` | PASS, 268 passed, 1 skipped |
| Lint | `ruff check src tests` | PASS |
| Format | `ruff format --check src tests` | PASS, 47 files already formatted |
| Diff hygiene | `git diff --check` | PASS |
| Coverage | `PYTHONPATH=src python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90` | PASS, 268 passed, 1 skipped, 90.43% total coverage |
| Swift manifest | `swift package dump-package >/dev/null` | PASS |
| Swift docs target | `swift build --target SpecHarvesterDocs` | PASS |

## Acceptance Criteria

- PASS: GitHub docs and DocC mirror document the real-repository validation
  plan.
- PASS: The plan rejects harvested code execution, dependency installation,
  package script execution, registry calls, generated candidate commits, raw
  prompts, provider transcripts, secrets, and model chain-of-thought.
- PASS: SpecNode remains an external contract boundary. SpecHarvester does not
  claim ownership of runtime, provider discovery, model execution, scheduling,
  provider lifecycle, or provider-specific orchestration.
- PASS: The plan includes local manifest examples, command examples, expected
  `.smoke/output` artifacts, quality scoring categories, and routing rules.
- PASS: Manifest examples use supported source-manifest keys such as
  `packageId`, and document strict public mode as `collect-batch` CLI policy
  rather than a manifest key.
- PASS: Routing distinguishes SpecHarvester, SpecNode, Platform, SpecPM, and
  `.0al` ownership.
- PASS: Existing docs contract tests and full Flow quality gates pass.

## Notes

- No generated real-repository outputs were produced or committed by this task.
- No sibling repository files were modified.
- Review follow-up corrected the source-manifest example after detecting
  unsupported `package_id` and `strict_public` keys.
