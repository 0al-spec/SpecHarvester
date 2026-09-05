# P56-T2 Validation Report

Date: 2026-09-06
Verdict: PASS for skill/asset delivery, not for live authoring quality.

## Deliverables

- Self-contained skills/specpm-author-candidate with supported-field guide,
  valid starter and complete fictional Rowpick example.
- Candidate authority, evidence provenance, unknowns, practical interface and
  partial-output behavior stay explicit without new SpecPM schema fields.
- Portable-link/index/source tests plus real SpecPM validation and negative
  source/capability/support-target tests in the integration CI job.

## Executed Checks

- `PYTHONPATH=src .venv/bin/python -m pytest --cov=spec_harvester --cov-report=term-missing --cov-fail-under=90`: 1445 passed, 6 skipped; coverage 90.03%.
- `PYTHONPATH=../SpecPM/src:src .venv/bin/python -m pytest tests/test_authoring_skill_assets.py tests/test_p56_practical_utility_benchmark.py tests/test_docs_contracts.py -q`: 212 passed.
- `PYTHONPATH=../SpecPM/src:src .venv/bin/python -m pytest tests/test_authoring_skill_assets.py -q`: 8 passed, including all five external-validator cases skipped in Python-only testing.
- `PYTHONPATH=../SpecPM/src .venv/bin/python -m specpm.cli validate skills/specpm-author-candidate/assets/template --json`: zero errors, only preview_only_package.
- `PYTHONPATH=../SpecPM/src .venv/bin/python -m specpm.cli validate skills/specpm-author-candidate/assets/example --json`: zero errors, only preview_only_package.
- `quick_validate.py skills/specpm-author-candidate` from the installed skill-creator, run with the repository Python: skill valid.
- `.venv/bin/ruff check src tests`: passed.
- `.venv/bin/ruff format --check src tests`: 204 files formatted.
- `swift package dump-package`: passed.
- `swift build --target SpecHarvesterDocs`: passed with the existing unhandled Documentation.docc warning.
- `git diff --check`: passed.

SpecPM checkout used for local checks: 8a5ce3dece3d18bf8f601a5a599520bd520c7839.
The sixth skip is the existing opt-in SpecNode live test, not a new failure.

## Limits and Ownership

The main agent authored all implementation and reviewed it; no subagent
authored the skill or generated examples. No live provider, target repository
code, package manager in a harvested source, registry or publication action ran.
T1 benchmark content and digests remain unchanged. No personal skill was
installed or modified. The caller-enforced runner remains T3 work.
User-owned untracked uv.lock was left unchanged.
