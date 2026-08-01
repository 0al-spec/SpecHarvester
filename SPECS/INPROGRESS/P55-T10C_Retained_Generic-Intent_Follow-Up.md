# P55-T10C Retained Generic-Intent Follow-Up

## Objective

Run Codex 5.3 Spark only over the 46 immutable P55-T10 repository records that
account for 48 reused generic observed-intent references, and compare the bounded follow-up with the original
campaign, and expose the resulting complete and rejected proposals for explicit
maintainer review without granting materialization or publication authority.
When the Spark account usage limit prevents a target from receiving any model
result, recover only that frozen target with `gpt-5.6-luna` at `low` reasoning
under a separate digest-bound provider scope.

## Dependencies

- P55-T10 retained-corpus report and deterministic 100-record archive.
- P55-T10A digest-bound reuse-versus-novelty policy.
- P55-T10B plan-bound calibration evidence and transition decision.
- P53-T14 portable candidate packets and pinned P53 source checkouts.
- P54 local Workbench and immutable reviewer-decision service.

## Deliverables

- A frozen follow-up plan that binds:
  - exactly the 46 P55-T10 generic-reuse repository records, all 48 generic
    references, and their record digests;
  - the P55-T10 report/archive and campaign-input digests;
  - unchanged repository, revision, packet, candidate, provider, and model
    identities;
  - P55-T10A decision-policy and P55-T5 quality-policy digests;
  - provider attempt, JSON repair, timeout, and output-size budgets.
- A resumable sequential Codex 5.3 Spark runner that rebuilds each input from
  the pinned packet and git revision, invokes no repository code or package
  manager, and writes one terminal record per target.
- A separate Luna Light recovery runner that accepts only the three verified
  all-`codex_nonzero_exit` Spark records, preserves the initial report/archive
  as immutable provenance, and recomputes effective metrics without rerunning
  any completed or semantic-failure record.
- Deterministic baseline-versus-follow-up metrics covering generic-intent
  reduction, evidence-supported experimental intents, justified reuse,
  unjustified novelty, duplicate IDs and semantic stems, provider failures,
  quality status, reviewer edit burden, duration, and token availability.
- A digest-bound follow-up archive and summary that retain complete and
  rejected proposal records while excluding raw prompts, raw responses, hidden
  reasoning, credentials, and machine-local paths.
- A Workbench overlay path that shows T10C records for the 46 targets and T10
  baseline records for the remaining corpus, with visible provenance and no
  authority change.
- A deterministic representative review sample spanning experimental proposals,
  retained generic reuse, rejected quality outcomes, and recovered provider
  attempts where available. Review decisions must come from an explicit
  maintainer action; the runner must not synthesize acceptance evidence.
- Durable JSON evidence, Markdown and DocC results, focused tests, validation,
  archive, and structured review artifacts.

## Execution Plan

1. Validate the P55-T10 report/archive pair, derive exactly 46 generic-reuse
   repository bindings covering 48 references, and freeze their ordered digest set.
2. Reconstruct the original retained-corpus target scope and prove every T10C
   repository, source revision, packet digest, and candidate identity matches
   its P55-T10 baseline record.
3. Add unit tests for scope drift, resumability, failure denominators,
   baseline comparison, duplicate ID/stem detection, false-novelty accounting,
   privacy boundaries, and Workbench overlay integrity.
4. Run Codex 5.3 Spark sequentially with at most two provider attempts and one
   JSON repair per attempt, retaining one terminal record for every target.
5. If a verified Spark usage limit prevents model execution, run only those
   failed targets through `gpt-5.6-luna` at `low` effort under the same bounded
   attempt limits and retain separate recovery provenance.
6. Finalize the comparison report and deterministic archive, generate the
   representative review sample and Workbench detail overlay, and obtain
   explicit maintainer review evidence before recording the final task verdict.
7. Run all repository quality gates and archive the task under FLOW.

## Acceptance Criteria

- The target set contains exactly the 46 P55-T10 repository records whose
  completed proposals account for all 48 frozen generic-intent references; no
  other repository runs.
- Every target preserves the P55-T10 repository ID, revision, packet digest,
  candidate ID, and baseline record digest. Any Luna Light recovery is limited
  to the frozen quota-failure set and records its own model and reasoning effort.
- Every target has exactly one completed or failed terminal record; provider
  retries remain bounded and all failures remain in denominators.
- The report compares the follow-up with the immutable P55-T10 baseline and
  records generic-intent reduction, useful experimental intents, justified
  reuse, false novelty, duplicate exact IDs and semantic stems, provider
  failures, quality status, and edit burden without changing frozen thresholds.
- Experimental intent differentiation uses the explicit nearby-intent claim
  bindings introduced by P55-T10A review fixes.
- Complete and rejected follow-up records are visible in the local Workbench as
  an overlay with baseline, Spark follow-up, and Luna recovery provenance.
- A representative sample is selected deterministically and any accepted,
  edited, rejected, or deferred evidence is recorded only through an explicit
  maintainer action with reviewer identity and digest bindings.
- Raw prompts, raw responses, hidden reasoning, credentials, and machine-local
  paths are not persisted.
- No candidate or intent is accepted, materialized, canonicalized, written to
  SpecPM or registry truth, or published by the follow-up runner.
- Python tests pass with at least 90% coverage; Ruff lint and format, JSON and
  diff integrity, Swift manifest, and Swift documentation checks are recorded.

## Non-Goals

- Re-running static harvesting or the 54 P55-T10 records without generic reuse.
- Re-downloading source repositories or changing pinned revisions.
- Running LM Studio or comparing provider transport conformance.
- Rerunning completed Spark records or Spark semantic-policy failures with Luna.
- Automatically treating an experimental intent as canonical or sufficient.
- Fabricating maintainer decisions from model output or quality diagnostics.
- Materializing, accepting, promoting, or publishing candidate changes.
