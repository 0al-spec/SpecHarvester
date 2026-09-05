# Review: P56-T1 Practical Utility Benchmark

Date: 2026-09-05
Verdict: PASS

## Scope

Protocol, evaluator artifact, integrity test, docs contracts and T2 handoff.
Independent read-only reviewer: GPT 5.6 Luna High; main agent owns disposition.

## Findings and Disposition

1. Different product boundaries could confound a model-quality claim. Resolved:
   primary endpoint explicitly compares end-to-end systems; unchanged baseline,
   common consumer envelope and separate boundary-coverage endpoint are required.
2. Scoring terms were underspecified. Resolved: canonical facts/source spans,
   qualifier-preserving paraphrases, contradiction precedence, independent
   scoring and maintainer adjudication are frozen.
3. Isolation lacked receipts. Resolved in the contract: path/hash allowlists and
   failed-access probes are mandatory T3 deliverables before any generation.
   This review does not claim those runtime controls are implemented in T1.
4. Budget accounting was ambiguous. Resolved: byte ranges, separate generated
   evidence, invocation IDs, monotonic timing, shared retry caps and pre-run
   input/provider locks are required. Missing monetary usage stays unavailable.
5. Aggregate quality could hide weak categories. Resolved with repository and
   category floors plus paired leave-one-out sensitivity. Population confidence
   intervals are not claimed for this purposive five-repository experiment.
6. Source claims needed qualifiers. Main spot-check narrowed Axios provenance
   to attested releases and n8n retention to the webhook sampling rule only.

The independent bounded re-review returned PASS with no remaining blockers.
All referenced source-file hashes were recomputed by the main agent; automated
integrity checks do not independently prove semantic correctness of every fact.

## GitHub Review Addendum

- Review r3941987972 claimed create belongs only to AxiosStatic. Rejected after
  direct `git show 509719387e4993392ca40da03a49678269cdfb90:index.d.ts` inspection:
  AxiosInstance declares create at line 715; AxiosStatic extends AxiosInstance
  at line 762. Clarified the canonical fact and expanded its source span.
- Review r3941987977 correctly noted the 100-minute adoption budget equaled
  the aggregate execution cap. Reduced adoption to 60 model-wall minutes,
  retaining the 100-minute aggregate hard cap, before any generation results.
  Rebound the protocol and benchmark digests.

## Remaining Work

T2 templates/skill, T3 enforced runner and subsequent generation/human evaluation
remain intentionally unimplemented. No new follow-up task is required: these
obligations already belong to the frozen Phase 56 sequence. FOLLOW-UP skipped.
