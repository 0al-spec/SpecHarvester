# P36-T1 Repository Parsing Plugin Contract

## Motivation

The FastAPI live AI rerun produces a valid `author_ready_draft`, but it also
shows a quality gap: Python public API evidence currently includes
documentation tutorial files such as `docs_src/*`. Those files are useful for
intent, usage, and semantic enrichment, but they should not inflate the public
API boundary for `fastapi.core`.

This should not become a FastAPI-specific exclusion. Repository layouts differ
by ecosystem, language, framework, and packaging convention, so SpecHarvester
needs a plugin-shaped parsing policy layer that can classify repository paths
before analyzer output becomes candidate evidence.

## Goal

Document the repository parsing plugin contract.

The contract should define how future parser profiles can separate:

- public interface evidence;
- semantic usage evidence;
- documentation;
- examples and tutorials;
- tests;
- generated artifacts;
- tooling;
- internal implementation;
- ignored paths.

## Deliverables

- Add GitHub Markdown documentation for the repository parsing plugin contract.
- Add a DocC mirror for the same contract.
- Link the contract from documentation entrypoints, capabilities, and roadmap.
- Record the intended follow-up sequence in the workplan.
- Add regression coverage so the contract remains discoverable.

## Non-Goals

- Do not implement parser plugins in this task.
- Do not change Python analyzer behavior in this task.
- Do not add FastAPI-specific hardcoded filtering.
- Do not rerun the FastAPI candidate batch as acceptance evidence in this task.
- Do not publish registry metadata, accept packages or relations, remove
  `preview_only`, or treat AI output as registry truth.

## Acceptance Criteria

- The contract describes plugin inputs, outputs, rule precedence, fallback
  behavior, evidence roles, decision reports, and safety boundaries.
- The FastAPI `docs_src` problem is framed as the motivating case for a
  reusable Python web-framework parser profile.
- Documentation clearly preserves documentation/tutorial files as semantic
  usage evidence rather than public API evidence.
- Docs-contract tests verify GitHub docs, DocC docs, entrypoint links,
  roadmap/capability references, workplan tasks, and active next-task state.

## Validation Plan

- `PYTHONPATH=src pytest tests/test_docs_contracts.py -q`
- `PYTHONPATH=src pytest -q`
- `PYTHONPATH=src ruff check .`
- `PYTHONPATH=src ruff format --check src tests`
- `git diff --check`
- `swift build --target SpecHarvesterDocs`
- DocC static generation
