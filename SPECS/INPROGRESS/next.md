# Next Task: Phase 36 Complete

**Status:** Complete
**Phase:** Phase 36. Repository Parsing Plugin System
**Last Archived:** P36-T4 FastAPI AI-Enabled Parser Profile Rerun

## Recently Archived

- `P36-T4` reran FastAPI with `--parser-profile python.web_framework.v0`
  and live LM Studio model `openai/gpt-oss-20b`.
- Baseline public interface evidence had `1121` entrypoints, `6009` symbols,
  and `454` `docs_src/*` entrypoints.
- Profiled public interface evidence had `48` entrypoints, `298` symbols, and
  `0` `docs_src/*` entrypoints.
- FastAPI package entrypoints stayed at `48`, proving the profile removed
  tutorial evidence without dropping the package surface.
- The autonomous candidate batch passed with one candidate and bundle-set
  preflight passed.
- The candidate reported `author_ready_draft`.
- AI draft and AI enrichment artifacts had warning-level gaps, so the result
  is closer to registry-review quality on evidence boundary but is not a clean
  registry handoff.
- The durable report fixture is
  `tests/fixtures/fastapi_parser_profile_rerun/p36-t4-fastapi-parser-profile-rerun.example.json`.

## Phase Result

Phase 36 is complete:

- `P36-T1` documented the repository parsing plugin contract.
- `P36-T2` added the Python web-framework parser profile fixture.
- `P36-T3` implemented the opt-in plugin-aware source classification hook.
- `P36-T4` verified the hook on a real FastAPI AI-enabled run.

## Boundary

The Phase 36 outputs are producer-side evidence only. They do not publish
registry metadata, accept packages or relations, remove `preview_only`, or
treat AI output as registry truth.

In plain terms, Phase 36 does not publish registry metadata and does not treat
AI output as registry truth.

## Suggested Next Work

No next task is selected. A future phase can generalize parser profiles beyond
Python web frameworks or add additional technology-specific profile fixtures.
