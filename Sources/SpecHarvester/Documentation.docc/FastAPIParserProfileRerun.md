# FastAPI Parser Profile Rerun

Status: P36-T4 validation record.

This page records the practical FastAPI rerun after enabling the
`python.web_framework.v0` repository parsing profile.

## Source

- Repository: `https://github.com/fastapi/fastapi`
- Local checkout revision: `9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263`
- Package id: `fastapi.core`
- Parser profile: `python.web_framework.v0`
- Live model provider: LM Studio
- Model: `openai/gpt-oss-20b`

## Evidence Delta

| Run | Entrypoints | Symbols | `docs_src/*` entrypoints | `fastapi/*` entrypoints |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 1121 | 6009 | 454 | 48 |
| Profiled | 48 | 298 | 0 | 48 |

The profile removes `docs_src/*` tutorial files from
`public-interface-index.json` while preserving the FastAPI package surface.

## AI Run Result

The autonomous candidate batch passed with `openai/gpt-oss-20b` through LM
Studio. Bundle-set preflight passed, and the generated candidate reported
`author_ready_draft`.

The AI proposal artifacts still had warning-level gaps:

- AI draft status: `warning`;
- AI enrichment status: `warning`;
- AI enriched preview status: `skipped`.

The parser profile improves the public API evidence boundary, but the result
is not a clean registry handoff. It is a better author-ready starter package
that still requires author/operator review.

## Verdict

The output is closer to registry-review quality on public interface evidence:

- `docs_src/*` no longer inflates public API evidence;
- package entrypoints remain intact;
- the generated candidate is still valid and author-ready.

The output is not registry-ready by itself because SpecPM acceptance still
requires explicit maintainer review.

Durable report fixture:

```text
tests/fixtures/fastapi_parser_profile_rerun/p36-t4-fastapi-parser-profile-rerun.example.json
```

## Boundary

This report is producer-side evidence only. It is not SpecPM registry
acceptance, maintainer approval, or upstream FastAPI endorsement. It does not
publish registry metadata, remove `preview_only`, or treat AI output as
registry truth.

In plain terms, it does not treat AI output as registry truth.
