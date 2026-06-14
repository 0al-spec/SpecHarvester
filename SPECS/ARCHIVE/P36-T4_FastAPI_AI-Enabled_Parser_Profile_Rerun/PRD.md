# P36-T4 FastAPI AI-Enabled Parser Profile Rerun

## Motivation

P36 started from a real FastAPI quality problem: the Python analyzer treated
`docs_src/*` tutorial files as public interface evidence. P36-T3 added an
explicit parser profile hook. P36-T4 must prove that the hook improves the
real FastAPI candidate pipeline, not just unit tests.

## Goal

Run FastAPI through the AI-enabled autonomous candidate pipeline with
`--parser-profile python.web_framework.v0` and record whether the generated
candidate output is closer to registry-review quality.

## Inputs

- Local checkout: `/Users/egor/Development/GitHub/fastapi`
- Revision: `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`
- Parser profile: `python.web_framework.v0`
- Local model endpoint: `http://127.0.0.1:1234`
- Model: `openai/gpt-oss-20b`

## Deliverables

- Run deterministic collection/interface indexing with and without the parser
  profile to compare public interface evidence volume.
- Run the AI-enabled autonomous candidate batch with the parser profile.
- Record a durable report fixture with:
  - source revision;
  - provider/model use;
  - public interface entrypoint and symbol counts;
  - `docs_src/*` exclusion proof;
  - candidate quality/status summary;
  - registry-review quality verdict.
- Update docs/DocC/workplan/archive references.

## Acceptance Criteria

- `docs_src/*` does not appear in `public-interface-index.json` entrypoints
  when `python.web_framework.v0` is selected.
- The comparison records before/after public interface evidence counts.
- The AI-enabled run records provider/model metadata.
- The report states whether the output is closer to registry-review quality.
- The report remains producer-side evidence only and does not imply registry
  acceptance.

## Non-Goals

- Do not publish FastAPI to SpecPM.
- Do not promote generated output to accepted registry metadata.
- Do not clone or fetch repositories during the run.
- Do not install FastAPI dependencies or execute harvested code.

## Validation Plan

- Run `collect-batch` without parser profile for baseline interface evidence.
- Run `collect-batch` with `--parser-profile python.web_framework.v0`.
- Run `autonomous-candidate-batch` with live LM Studio and parser profile.
- Add docs-contract regression coverage for the recorded report.
- Run project tests, lint, format, coverage, and docs build gates.
