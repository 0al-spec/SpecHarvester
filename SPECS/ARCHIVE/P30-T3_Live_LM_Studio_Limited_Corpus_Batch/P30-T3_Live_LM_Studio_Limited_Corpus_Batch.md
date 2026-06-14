# P30-T3 Live LM Studio Limited Corpus Batch

## Objective

Run the P30 limited popular-library corpus through the live local
OpenAI-compatible LM Studio provider and record AI draft/enrichment outcomes
against the deterministic P30-T2 baseline.

This task should prove whether `openai/gpt-oss-20b` improves the limited corpus
starter-package workflow without turning model output into SpecPM authority.

## Background

P30-T2 recorded the deterministic baseline in:

```text
docs/LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md
tests/fixtures/limited_popular_library_deterministic_batch/p30-t2-limited-popular-libraries.example.json
```

That run processed all six repositories, generated nine preview candidates,
produced three relation proposals, passed all six bundle-set preflights, and
left one candidate-layer finding:

```text
navigation-split-view.core -> navigation_split_view.core
package_id_hint_mismatch
```

P30-T3 uses the same source manifest:

```text
inputs/limited-popular-libraries/repositories.yml
```

The local provider dependency was checked before planning:

```text
http://127.0.0.1:1234/v1/models includes openai/gpt-oss-20b
```

## Deliverables

- Run:

```bash
PYTHONPATH=src python -m spec_harvester autonomous-candidate-batch \
  inputs/limited-popular-libraries \
  --out <run-root>/live-lm-studio \
  --lm-studio-base-url http://127.0.0.1:1234 \
  --lm-studio-model openai/gpt-oss-20b \
  --json-repair-max-attempts 1
```

- Record a machine-readable fixture for the live limited corpus outcome.
- Compare live status against P30-T2 deterministic counts:
  - repository count;
  - candidate count;
  - relation count;
  - preflight status;
  - author-ready stop-policy status;
  - AI draft/enrichment status;
  - JSON repair status.
- Add GitHub docs and DocC coverage for the live run.
- Update roadmap/workplan/next/archive/review artifacts.
- Add regression tests covering:
  - fixture identity and non-authority boundary;
  - expected repository ids and package ids;
  - provider/model metadata;
  - AI draft/enrichment status and repair summaries;
  - comparison with deterministic P30-T2 baseline;
  - known candidate-layer finding carry-forward.

## Acceptance Criteria

- The live run processes the same six P30 seed repositories or records a
  structured blocked status for any repository that cannot complete.
- Every repository outcome records:
  - deterministic candidate/relation/preflight comparison;
  - AI draft status;
  - AI draft diagnostic codes;
  - AI draft JSON repair status;
  - AI enrichment status;
  - AI enrichment diagnostic codes;
  - AI enrichment JSON repair status;
  - provider usage when available.
- The fixture explicitly states:
  - `producer_preview_evidence_only`;
  - live provider is proposal-only review evidence;
  - no package acceptance;
  - no relation acceptance;
  - no baseline seeding;
  - no registry publication;
  - no `preview_only` removal.
- The product verdict says whether the limited corpus is ready for P30-T4
  candidate-layer triage.
- Any AI draft warnings or malformed JSON repairs are recorded as candidate
  review input, not hidden or treated as success.

## Non-Goals

- No repository clone/fetch.
- No dependency installation, package manager execution, build, test, or
  package script execution inside harvested repositories.
- No SpecPM registry update or accepted-source proposal.
- No curation of generated package semantics.
- No automatic use of AI output as accepted `SpecPackage`, `BoundarySpec`, or
  relation truth.

---
**Archived:** 2026-06-13
**Verdict:** PASS
