# P55-T10 Retained-Corpus Semantic Author and Review Flow

## Objective

Run the validated evidence-grounded semantic-author flow through Codex 5.3
Spark over every retained P53 repository, preserve complete proposal-only
records for local review, and publish deterministic campaign accounting without
granting acceptance, materialization, canonicalization, registry, or
publication authority.

## Dependencies

- P53-T14 retained 100-repository source and candidate handoff.
- P54 local candidate review catalog and portable reviewer decisions.
- P55-T3 semantic author input packs.
- P55-T5 quality diagnostics and frozen threshold policy.
- P55-T6 portable semantic proposal records.
- P55-T9A provider conformance evidence with both calibrated providers passing.

## Deliverables

- A resumable retained-corpus campaign runner that:
  - binds the P53 source manifest, P53-T14 candidate corpus, and P55-T9A
    readiness evidence by SHA-256;
  - validates each retained checkout against its pinned revision before reading
    allowlisted evidence;
  - invokes Codex 5.3 Spark with bounded timeout, output, repair, and provider
    attempt budgets;
  - writes one digest-bound, proposal-only result per repository and safely
    resumes completed records;
  - accounts for all 100 unique manifest repositories before a full campaign
    may be reported complete;
  - never executes harvested code or package managers.
- Deterministic aggregate evidence reporting:
  - completed and failed provider outcomes;
  - eligible, review-required, and rejected quality states;
  - purpose accuracy, evidence-supported proposal rate, schema validity, and
    reviewer edit-burden indicators;
  - generic-intent reuse, capability-namespace, duplicate experimental-intent,
    and other deterministic diagnostics;
  - provider attempt, JSON repair, token, cost-availability, and runtime
    budgets;
  - accepted, edited, rejected, deferred, and unreviewed counts derived only
    from valid reviewer evidence.
- Complete portable proposal records suitable for the Phase 54 Workbench.
- GitHub Markdown and DocC operational documentation, durable campaign
  evidence, validation, archive, and review artifacts.

## Execution Plan

1. Build and test the deterministic campaign runner without provider execution.
2. Execute Codex 5.3 Spark in small resumable waves against the pinned corpus.
3. Retry only within recorded bounded attempt limits; preserve terminal failures
   rather than retrying until success.
4. Merge the 100 unique per-repository records into one portable evidence file.
5. Compute provider, semantic quality, intent, diagnostics, reviewer-decision,
   token/cost/runtime, privacy, and authority summaries.
6. Run repository quality gates and archive the exact observed outcome.

## Acceptance Criteria

- The campaign scope contains exactly the 100 unique repositories from the
  pinned P53 mass-corpus manifest and no unpinned source revision.
- Every repository has exactly one terminal completed or failed campaign
  record; subset or incomplete output cannot claim campaign completion.
- P55-T9A readiness, the source manifest, and candidate corpus are digest-bound
  in durable evidence.
- Codex 5.3 Spark is the mass-campaign worker. LM Studio calibration remains
  referenced but is not silently represented as a 100-repository run.
- Complete proposals retain evidence, receipt, source, candidate, proposal,
  quality, and record digest bindings while raw prompts, raw responses, hidden
  reasoning, credentials, and machine-local paths remain absent.
- Reviewer disposition counts come only from valid reviewer evidence. Missing
  reviewer decisions are reported as `unreviewed`, not inferred as acceptance,
  rejection, or deferral.
- Duplicate experimental intent IDs and deterministic quality diagnostics are
  visible and do not become canonical intents automatically.
- Provider attempts are capped at two per repository and JSON repair attempts
  at one per provider attempt. Terminal failures remain in denominators.
- No proposal is accepted, materialized, promoted, canonicalized, published, or
  written into SpecPM or registry truth by the campaign.
- Python tests pass with at least 90% coverage; Ruff, formatting, diff integrity,
  Swift manifest, and Swift documentation checks pass.

## Non-Goals

- Running LM Studio over the full retained corpus.
- Automatically making reviewer decisions or materializing candidate revisions.
- Canonicalizing experimental intents or changing SpecPM taxonomy/governance.
- Mutating accepted package sources, registry truth, or public publication
  output.
- Executing harvested repositories or installing their dependencies.
