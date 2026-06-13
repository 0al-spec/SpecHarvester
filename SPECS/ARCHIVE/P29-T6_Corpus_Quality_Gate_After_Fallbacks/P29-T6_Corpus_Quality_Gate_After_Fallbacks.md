# P29-T6 Corpus Quality Gate After Fallbacks

## Objective

Re-run the mixed local Flask/Gin/xyflow corpus after deterministic
single-package fallback and bounded LM Studio JSON repair support, then record
whether the autonomous candidate MVP is ready for larger popular-library
scraping.

The task produces durable review evidence. It does not promote packages to
SpecPM, seed baselines, remove `preview_only`, or publish registry metadata.

## Background

`P29-T3` established the first mixed corpus baseline:

- Flask and Gin collected deterministic evidence but produced `0` candidates.
- xyflow produced a reviewable package-set candidate, but the live LM Studio
  draft path exposed malformed JSON handling gaps.

`P29-T4` fixed the deterministic fallback for Flask/Gin-style single-package
repositories. `P29-T5` added bounded JSON repair/retry diagnostics for live
LM Studio/OpenAI-compatible model output.

P29-T6 is the product checkpoint: it must verify that those mitigations improve
the mixed corpus enough to justify broader operator-driven scraping, while
keeping the result as producer preview evidence.

## Deliverables

- Run `autonomous-candidate-batch` over local checkouts:
  - `/Users/egor/Development/GitHub/flask`
  - `/Users/egor/Development/GitHub/gin`
  - `/Users/egor/Development/GitHub/xyflow`
- Record deterministic `--skip-ai` results after fallback support.
- Record live LM Studio results when the local provider is reachable.
- Add a machine-readable post-mitigation quality gate fixture.
- Add docs and DocC coverage describing:
  - corpus revisions;
  - deterministic candidate counts;
  - relation counts;
  - preflight status;
  - author-ready decisions;
  - AI draft/enrichment statuses;
  - JSON repair summaries;
  - product verdict for larger scraping readiness.
- Add regression tests for the fixture/docs contract.
- Update Workplan, next task, archive, and review artifacts.

## Acceptance Criteria

- Flask produces at least one preview candidate (`flask.core`).
- Gin produces at least one preview candidate (`gin.core`).
- xyflow still produces the expected workspace/member package-set shape.
- Deterministic preflight passes for every repository.
- Live LM Studio mode either completes AI proposal generation or records bounded
  structured AI diagnostics without losing deterministic artifacts.
- The fixture explicitly preserves `producer_preview_evidence_only`,
  `preview_only`, no package acceptance, no relation acceptance, and no registry
  publication boundaries.
- The product verdict states whether the MVP is ready for larger
  popular-library scraping and which follow-up, if any, remains.

## Implementation Plan

1. Create a temporary source manifest for the pinned local Flask/Gin/xyflow
   checkouts.
2. Run deterministic `autonomous-candidate-batch --skip-ai`.
3. Probe local LM Studio and run live `autonomous-candidate-batch` with
   `openai/gpt-oss-20b` if available.
4. Summarize both outputs into a committed fixture and documentation.
5. Add docs-contract tests for the new quality gate artifact.
6. Run the Flow validation gates.

## Non-Goals

- No repository cloning or network scraping.
- No dependency installation, package manager execution, builds, tests, or
  package scripts inside harvested repositories.
- No accepted-source update and no SpecPM registry mutation.
- No curated package quality rewrite.
- No promise that generated specs are semantically final; the goal remains
  valid starter packages for author/maintainer review.
