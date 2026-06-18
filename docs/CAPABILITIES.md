# SpecHarvester Capabilities

Status: current product capability map.

SpecHarvester is a producer pipeline for turning pinned public repository
checkouts into reviewable SpecPM candidate packages. Its current goal is not to
write final registry truth. Its goal is to produce a valid, evidence-backed
starter package that an author or maintainer can review, correct, and hand off
to SpecPM.

Short form:

```text
local repository checkout
  -> bounded evidence
  -> candidate package or package-set draft
  -> optional local AI proposal
  -> validation, quality report, and static viewer
  -> selected/deferred handoff evidence
  -> SpecPM-side preflight and maintainer review
```

## What It Can Do Now

| Capability | Current support | Main docs |
| --- | --- | --- |
| Static evidence collection | Collect allowlisted metadata, file digests, provenance, and analyzer-policy records from local checkouts. | [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md), [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md) |
| Deterministic single-package drafting | Produce `specpm.yaml`, `specs/*.spec.yaml`, validation reports, diagnostics, receipts, quality reports, and preview output. | [`PRODUCER_CANDIDATE_BUNDLE.md`](PRODUCER_CANDIDATE_BUNDLE.md), [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md) |
| Workspace and package-set drafting | Detect workspace/member package shape, draft aggregate package-set candidates, draft scoped members, and emit `contains` relation proposals. | [`WORKSPACE_INVENTORY.md`](WORKSPACE_INVENTORY.md), [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md), [`PACKAGE_RELATION_PROPOSALS.md`](PACKAGE_RELATION_PROPOSALS.md) |
| Package-set preflight and viewer | Check member bundles, relation proposals, evidence digests, and render static review pages for package-set output. | [`BUNDLE_SET_PREFLIGHT.md`](BUNDLE_SET_PREFLIGHT.md), [`PACKAGE_SET_VIEWER.md`](PACKAGE_SET_VIEWER.md) |
| Author-ready quality reporting | Classify generated output as `author_ready_draft`, `needs_regeneration`, or `blocked`, with hard gates, review dimensions, and action items. | [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md), [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md) |
| Local AI draft and enrichment proposals | Use local OpenAI-compatible providers such as LM Studio for proposal-only package-set drafting and enrichment. | [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md), [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md) |
| AI-enriched preview candidate copies | Apply clean AI enrichment proposals into copied preview candidates with patch reports for review. | [`AI_ENRICHMENT_CANDIDATE_PATCH.md`](AI_ENRICHMENT_CANDIDATE_PATCH.md) |
| Selected/deferred candidate triage | Separate review-ready candidates from candidates that need targeted regeneration, repair, or explicit deferral. | [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md), [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md) |
| SpecPM handoff evidence | Emit portable JSON/Markdown review evidence that SpecPM can preflight without rerunning SpecHarvester. | [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md), [`SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`](SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md) |
| Bounded corpus runs | Select important multi-ecosystem repository/package-family targets with explicit importance signals and exclusion rules, record the machine-readable corpus plan, explainable selection report, and dry-run readiness gate, then run operator-selected local checkout batches with deterministic and optional live local-model paths. | [`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md), [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md), [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md), [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md), [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md) |
| Repository parsing profile hook | Opt-in path classification for language/framework parser profiles, with `python.web_framework.v0` validated on FastAPI to separate public interface evidence from semantic usage/documentation evidence. | [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md), [`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md) |
| Repository profile detection evidence | Opt-in `repository-profile-detect` command and `autonomous-candidate-batch --repository-profile-selection` sidecar artifacts that emit `SpecHarvesterRepositoryProfileDetection` from static evidence before parser path classification, plus a generic discovery hint vocabulary, cross-ecosystem fixture coverage, and a real FastMCP comparison showing the current manifest-evidence gap. | [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md), [`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md), [`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md), [`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md), [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md), [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md) |
| Optional CodeGraph input boundary | Normalize pre-existing CodeGraph artifacts into source graph evidence and check pinned interface compatibility offline. | [`CODEGRAPH_SOURCE_GRAPH_ADAPTER.md`](CODEGRAPH_SOURCE_GRAPH_ADAPTER.md), [`CODEGRAPH_COMPATIBILITY_GUARD.md`](CODEGRAPH_COMPATIBILITY_GUARD.md) |

## Repository Shapes

SpecHarvester currently has useful coverage for:

- manifest-backed single-package repositories;
- manifest-poor repositories with README/API-contract semantic hints;
- JavaScript/TypeScript package or workspace layouts;
- package-set or monorepo layouts where a workspace/root package should contain
  selected member packages;
- bounded local corpus runs over operator-selected checkouts.

The `xyflow` reference path is the current package-set calibration case:

```text
xyflow.workspace
  contains xyflow.react
  contains xyflow.svelte
  contains xyflow.system
```

The limited and next-corpus evidence pages record broader calibration runs. They
are evidence for pipeline quality, not permission to ingest arbitrary public
repositories into SpecPM automatically.

[`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md) defines the Phase 35
boundary for choosing important libraries across ecosystems. The policy treats
repository/package-family selection as a curated operator decision, not a raw
registry search crawl.

[`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md) defines the
machine-readable plan shape for selected, deferred, and rejected source
decisions before any autonomous batch run starts.

[`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md)
defines how package-like units inside selected repositories should be
classified before drafting.

[`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md)
records the first bounded seed set across JavaScript/TypeScript, Python, Rust,
Go, and Swift. It is a plan for future local-checkout runs, not permission to
clone repositories or publish registry metadata.

[`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md)
explains selected, deferred, and rejected seed sources, quota decisions, and
the downstream command plan before any readiness check or autonomous batch.

[`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md)
records that the Phase 35 seed corpus is blocked until operator-provided pinned
local checkouts are verified.

[`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md)
defines the Phase 36 plugin contract for repository path classification.
[`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md)
defines the Phase 37 contract and the `repository-profile-detect` CLI report
surface plus autonomous batch sidecar evidence for selecting repository
profile plugins before path classification.
[`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md)
defines generic path-role hints such as `package_set_root`, `member_package`,
`example_package`, `internal_utility`, and `evidence_only`.
[`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md)
records workspace-shaped, single-package, nested-package, and ambiguous
multi-signal fixtures for the same generic profile selection contract.
[`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md)
records the first real FastMCP auto-selection comparison. The run passed, but
auto-selection fell back to `generic.repository.v0`; manual `fastmcp_slim`
targeting produced a much narrower public interface index. P37-T8 should make
profile detection consume harvested manifest evidence when workspace inventory
has no manifest records.
[`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md) records
the first practical profile run. The profile keeps documentation, tutorials,
examples, and tests available as semantic usage
evidence while keeping public interface indexes focused on package surfaces
intended for consumers.

## Author-Ready Draft Boundary

The current product quality target is:

```text
valid starter package, not final accepted spec
```

SpecHarvester should stop when remaining work is better done by the library
author, a maintainer, or a reviewing agent with project-specific context.

An author-ready draft should provide:

- valid SpecPM package files;
- bounded evidence links and digests;
- conservative intent and capability claims;
- diagnostics and validation output;
- quality report verdict and author action items;
- static review surface;
- handoff evidence for SpecPM-side preflight where relevant.

It is acceptable for a draft to require author edits. It is not acceptable for a
draft to hide failed validation, fabricate evidence, remove `preview_only`, or
present AI output as registry truth.

## AI and Local Model Boundary

Local model support is proposal-only.

SpecHarvester can use local OpenAI-compatible providers, including LM Studio, to
draft or enrich package-set candidates from compact evidence. The resulting AI
artifacts remain review evidence:

- provider receipts are provenance, not authority;
- raw prompts or responses are not persisted as registry truth;
- model JSON is schema checked and may pass through bounded repair;
- package identity, evidence paths, privacy flags, and interface kinds must
  still pass deterministic checks;
- clean enrichment proposals may be applied only into copied preview candidates
  through [`AI_ENRICHMENT_CANDIDATE_PATCH.md`](AI_ENRICHMENT_CANDIDATE_PATCH.md);
- accepted registry output still requires maintainer review.

## SpecPM Boundary

SpecHarvester produces reviewable candidate bundles. SpecPM remains the
validator, registry authority, and public-index publisher.

Passing SpecHarvester preflight or SpecPM-side handoff preflight means:

```text
the evidence is internally consistent enough for review
```

It does not mean:

```text
the package is accepted into the registry
```

Promotion requires a separate maintainer decision, accepted-source PR, and
SpecPM validation/indexing flow.

## What It Intentionally Does Not Do

SpecHarvester does not:

- clone or discover repositories on its own during documented corpus runs;
- execute harvested repository code;
- install harvested dependencies;
- run package scripts or tests from harvested projects;
- access secrets or private credentials;
- treat generated candidates as upstream-endorsed truth;
- accept packages, accept relations, seed baselines, or remove `preview_only`
  without an explicit maintainer flow;
- publish directly into the SpecPM public registry.

## Current Maturity

| Area | Maturity |
| --- | --- |
| Single-package deterministic candidate loop | Working MVP |
| Package-set drafting and relation proposals | Working MVP, calibrated on `xyflow` |
| Author-ready quality report | Working MVP |
| Static candidate and package-set viewer | Working review surface |
| Local LM Studio proposal path | Working, proposal-only |
| Selected/deferred handoff | Working review evidence path |
| SpecPM consumer preflight integration | Working for supported handoff artifacts |
| Curated multi-ecosystem corpus selection | Planned policy boundary |
| Repository parsing plugin profiles | Working explicit hook for one parser profile; broader selection still planned |
| Repository profile selection | Working standalone report, autonomous batch evidence layer, generic hint vocabulary, cross-ecosystem fixtures, and real FastMCP evidence; manifest-evidence fallback gap remains |
| Broad autonomous public-library scraping | Not ready; bounded local corpus only |
| Final accepted spec authoring | Out of scope for SpecHarvester |

## Operator Reading Path

For a practical path through the current system:

1. Start with [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md).
2. Check [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md) before adding analyzers or
   model providers.
3. Use [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md)
   to understand the stop policy.
4. Use [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md) and
   [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md) for monorepos.
5. Use [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md)
   and [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md) when preparing SpecPM review.
6. Use [`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md),
   [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md),
   [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md),
   [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md),
   [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md),
   and [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md)
   before running any larger corpus.
