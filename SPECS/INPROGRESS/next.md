# Next Task: P31-T1 Selected Candidate Handoff Proposal Contract

**Status:** Selected
**Selected:** 2026-06-13
**Task:** P31-T1 Selected Candidate Handoff Proposal Contract
**Phase:** Phase 31. Selected Candidate SpecPM Intake Handoff
**Last Archived:** P30-T5 Selected Candidate Handoff Dry Run

## Recently Archived

- `P30-T1` defined the limited popular-library corpus plan in
  `docs/LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`,
  `<doc:LimitedPopularLibraryCorpusPlan>`, and
  `inputs/limited-popular-libraries/repositories.yml`.
- `P30-T2` recorded deterministic `--skip-ai` evidence for all 6 limited
  corpus repositories with 9 preview candidates, 3 relation proposals, and
  passing bundle-set preflight.
- `P30-T3` recorded the live LM Studio run with `openai/gpt-oss-20b`,
  preserved deterministic candidate/relation counts, needed no JSON repair, and
  produced candidate-layer findings for triage.
- `P30-T4` recorded the candidate-layer triage report with verdict
  `ready_for_selected_handoff_dry_run`: `flask.core`, `gin.core`, and
  `docc2context.core` were selected, while 6 deferred candidates remained
  `needs_regeneration`.
- `P30-T5` recorded the selected handoff dry run in
  `docs/LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`,
  `<doc:LimitedPopularLibrarySelectedHandoffDryRun>`, and
  `SpecHarvesterLimitedPopularLibrarySelectedHandoffDryRun`. The product
  verdict was `selected_handoff_dry_run_ready`, with passing producer
  preflight, static viewer evidence, required bundle file digests, and
  `external_required` registry acceptance decisions for the 3 selected
  candidates. The output remained `producer_preview_evidence_only` and not
  SpecPM acceptance.

## Outcome

Phase 30 is complete. The next gap is not another scrape: it is the handoff
envelope between selected producer evidence and future SpecPM-side intake.

P30-T5 recorded a dry-run evidence fixture, but it did not define a portable
proposal contract that can be attached to SpecPM review or consumed by future
consumer-side preflight.

## Next Step

Implement `P31-T1`: define
`SpecHarvesterSelectedCandidateHandoffProposal` as a stable producer evidence
contract for selected candidates. Preserve `preview_only`,
`producer_preview_evidence_only`, and external SpecPM acceptance authority.
Do not create a SpecPM pull request, accept packages, accept relations, seed
baselines, or publish registry metadata.
