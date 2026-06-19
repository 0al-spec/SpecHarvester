# Roadmap

Status: Functional alpha roadmap
Updated: 2026-06-10

SpecHarvester is a bounded producer pipeline for reviewable SpecPM candidate
packages. It reads public repository checkouts as untrusted metadata, collects
static evidence, drafts candidate specs, and emits machine-readable review
artifacts. SpecPM remains the validator, registry authority, and accepted-source
owner.

## Maturity Snapshot

SpecHarvester has moved beyond bootstrap. It is a functional alpha operator
tool that can run an end-to-end producer loop for selected public repositories
and can hand package-set evidence to SpecPM.

It is not yet a self-service harvesting service. It does not accept packages
into SpecPM, execute repository-owned scripts, crawl private repositories, trust
LLM output as registry truth, or own public registry governance.

## Current Functional Alpha Baseline

Implemented surfaces:

- deterministic static evidence collection from allowlisted repository files;
- conservative `SpecPackage` and `BoundarySpec` candidate drafting;
- SpecPM validation before proposal or promotion;
- `producer-receipt.json`, `validation-report.json`, and `diagnostics.json`
  emission for generated candidate bundles;
- candidate bundle preflight and bundle-set preflight;
- static candidate and package-set viewer output;
- workspace inventory for monorepos;
- proposal-only LLM package-set draft selection from deterministic workspace
  inventory;
- package-set and scoped member candidate drafting;
- producer-observed package relation proposals;
- `xyflow-package-set-smoke` for the local reference package-set path;
- package-set handoff proposal JSON and Markdown for SpecPM review evidence;
- fresh candidate refresh run export for SpecPM
  `prepare-refresh-decision` compare inputs;
- trusted `propose-to-specpm.yml` workflow boundaries for single-package and
  dry-run package-set evidence;
- proposal-only package-set AI enrichment through local OpenAI-compatible
  providers such as LM Studio.

## Roadmap Principles

- Treat all harvested repository content as untrusted data.
- Do not execute package scripts, install dependencies, run tests, or treat
  repository text as host instructions during harvesting.
- Keep deterministic evidence and digests ahead of model-assisted draft
  proposals and enrichment.
- Keep model output proposal-only and review-gated.
- Keep SpecPM validation and maintainer acceptance outside generated receipts.
- Prefer reproducible local fixtures and real-repository dry runs before adding
  broader automation.

## Milestone 1: Producer Bundle Reliability

Status: complete for the current alpha loop.

Completed scope:

- generated candidate bundle layout;
- producer receipts with input/output roles and SHA-256 digests;
- validation and diagnostics reports;
- candidate bundle preflight;
- static viewer panels for receipts, diagnostics, validation, and privacy
  notes;
- end-to-end local bundle smoke.

Success criteria:

- a generated candidate bundle can be reviewed without trusting the generator
  runtime;
- output hashes and report digests make post-generation mutation visible;
- validation failures and diagnostics are machine-readable.

## Milestone 2: SpecPM Handoff Boundary

Status: complete for current alpha handoff artifacts, still evolving with
SpecPM policy.

Completed scope:

- SpecPM handoff docs and examples;
- producer evidence links in proposal artifacts;
- shared fixture policy with SpecPM;
- external registry acceptance decision boundary;
- external SpecPM registry acceptance decision records referenced from handoff
  artifacts without writing maintainer approval into generated receipts;
- stable producer evidence layout and `producerEvidenceLinks` role vocabulary
  for a future optional SpecPM CI preflight gate;
- package-set handoff proposal JSON and Markdown;
- `SpecHarvesterFreshCandidateRefreshRun` JSON for exporting generated
  package-set bundles into the SpecPM
  `specpm-public-index-generated-root/v0` layout;
- trusted workflow mode that uploads package-set evidence without using
  SpecPM write credentials on untrusted PR events.

Success criteria:

- SpecHarvester can produce review evidence that SpecPM can preflight without
  executing producer tools;
- fresh generated roots use `<package_id>/<version>/specpm.yaml` and
  `specs/*.spec.yaml` so SpecPM can compare contract-bearing files
  mechanically;
- the real `xyflow` refresh compare run produced
  `status: no_update_required`, `updateNeeded: false`, and
  `reason: no_contract_delta` after verifying 8 generated contract-file
  digests;
- the real `TanStack/query` refresh compare run produced a 39-candidate
  package-set with 38 relation proposals and a structured SpecPM
  missing-baseline result, proving the producer handoff is not `xyflow`-specific
  while clarifying that first-submission workflows are separate from refresh
  comparison;
- `--role-profile generic_monorepo` selects workspace/member package-set output
  for generic monorepos and reproduced the useful TanStack/query 39-candidate /
  38-relation shape without raw `--role member_package` operator knowledge;
- `SpecHarvesterBaselineSubmissionHandoff` records first-submission or
  seeded-baseline review evidence when SpecPM reports
  `refresh_decision_prepare_current_contract_files_missing`;
- `SPECPM_PROPOSAL_TOKEN` remains limited to trusted workflows;
- generated receipts never claim maintainer acceptance.

Next focus:

- SpecPM-side intake policy for baseline submission handoff artifacts.

## Milestone 3: Package Sets and Monorepo Discovery

Status: complete for the `xyflow` reference shape and ready for broader
calibration.

Completed scope:

- Package-set contract alignment is documented before runtime monorepo
  discovery implementation, mapping SpecPM contracts to workspace inventory,
  package-set candidates, scoped member packages, relation proposals,
  bundle-set preflight, static viewer previews, and the `xyflow` smoke
  scenario;
- workspace inventory with repository revision, package manifests, package
  roles, source paths, and proposed SpecPM package IDs;
- aggregate package-set candidates such as `xyflow.workspace`;
- scoped member candidates such as `xyflow.react`, `xyflow.svelte`, and
  `xyflow.system`;
- producer-observed `contains` relation proposals;
- bundle-set preflight across members, relation endpoints, and digests;
- static package-set viewer;
- local `xyflow` smoke scenario.

Success criteria:

- a monorepo can preserve aggregate discovery intent without collapsing scoped
  package subjects into one over-broad candidate;
- relation proposals remain producer evidence until SpecPM maintainers accept
  them;
- skipped example, tooling, and test packages remain visible as review context
  rather than primary package members.

## Milestone 4: Proposal-Only AI Enrichment

Status: alpha-ready for local operator use.

Completed scope:

- package-set AI enrichment proposal command;
- deterministic application of clean AI enrichment proposals into copied
  preview candidates;
- opt-in autonomous batch output for AI-enriched preview candidates;
- compact evidence request generation;
- live local OpenAI-compatible provider path for LM Studio;
- external model-output mode;
- provider usage metadata;
- package-local evidence path normalization;
- diagnostics for unsupported evidence paths and package ID drift;
- no raw prompt or response persistence in normal proposal output.

Success criteria:

- AI enrichment can suggest summaries, capabilities, interfaces, confidence,
  and evidence gaps without mutating generated specs;
- autonomous AI-enabled runs can emit copied enriched preview candidates with
  `ai-enrichment-candidate-patch.json` while preserving `preview_only`;
- SpecPM can consume AI enrichment as proposal-only evidence through its own
  preflight and review policy;
- private or unsupported evidence paths are rejected or downgraded to
  diagnostics.

## Milestone 5: Author-Ready Valid Drafts

Status: active product-quality focus.

Goal: define when SpecHarvester should stop drafting and hand a valid starter
package to the repository author.

Tasks:

- document the author-ready draft quality bar;
- emit `author-ready-draft-quality-report.json` with an `authorReadyDraft`
  verdict, hard gates, dimensions, and author action items;
- aggregate member quality reports into `authorReadyDraftSummary` for
  package-set handoff and viewer outputs;
- derive `authorReview` checklists, weak claims, evidence gaps, recommended
  edits, and member action summaries for viewer and handoff review;
- run a real-repository author-ready calibration matrix that records estimated
  author edits, edit categories, and repeated generator gaps;
- treat validation success as a hard gate, not a semantic quality score;
- define stop policy for AI draft and enrichment loops;
- record author action items, weak claims, and evidence gaps explicitly;
- keep final semantic curation with the author and their agent.

Success criteria:

- generated output is described as a valid starter package, not a final
  accepted spec;
- receipts include a digest for the author-ready quality report as
  `outputs[].role: quality_report`;
- operators can tell when additional model iteration is no longer useful;
- authors receive a reviewable handoff with clear edit points and evidence
  context.
- maintainers can distinguish normal author curation from repeated generator
  weaknesses before broadening intake.

## Milestone 6: Multi-Repository Quality Calibration

Status: next practical focus.

Goal: measure generated candidate quality across several real repositories
before expanding public intake automation.

Tasks:

- run the current producer pipeline across 5-10 real repositories from
  different ecosystems and repository shapes;
- record quality ratings for package identity, summaries, capabilities,
  interfaces, evidence supports, diagnostics, relation proposals, and skipped
  packages;
- compare deterministic output with optional LM Studio enrichment and human
  review notes;
- identify repeated generator failure modes that should become deterministic
  fixes instead of one-off curation;
- feed confirmed SpecPM-side policy gaps back into SpecPM rather than
  overloading SpecHarvester with registry authority.

Success criteria:

- maintainers can see where SpecHarvester output is reliable, shallow, or
  misleading;
- generator improvements are justified by repeated evidence across repositories;
- candidate quality is measured before public self-service submission is
  broadened.

## Milestone 7: Ecosystem Analyzer Depth

Goal: improve deterministic evidence quality before relying on model output.

Tasks:

- deepen JavaScript/TypeScript public interface extraction;
- add richer language/package profiles for Python, Swift, Go, Rust, and other
  high-value ecosystems;
- record analyzer versions, source digests, and confidence consistently;
- keep analyzer outputs advisory unless the analyzer policy explicitly grants
  stronger evidence status;
- keep package scripts, tests, and dependency installation out of the default
  pipeline.

Success criteria:

- candidate interfaces and compatibility claims are grounded in static
  evidence;
- diagnostics explain missing or weak evidence;
- model enrichment has better deterministic evidence to cite.

## Milestone 8: Operator UX and Governance Reports

Goal: make operator review cheaper without turning SpecHarvester into registry
authority.

Tasks:

- refresh stale `SPECS/INPROGRESS/next.md` state after completed SpecPM-side
  intake work;
- summarize producer run quality in compact reports;
- expose namespace, upstream, license, provenance, and duplicate-intent risks
  beside generated candidate bundles;
- make PR-ready handoff artifacts easier to attach to SpecPM review;
- keep acceptance decisions external to generated receipts.

Success criteria:

- operators can identify what needs human review first;
- handoff evidence is complete enough for SpecPM maintainers;
- review reports do not imply automatic acceptance.

## Milestone 9: Autonomous Candidate Harvest MVP

Status: MVP runner in progress.

Goal: let operators run cost-controlled autonomous popular-library scraping
against local public checkouts while keeping generated output as preview
evidence.

Tasks:

- run repository source manifests through collection, workspace inventory,
  package-set drafting, and bundle-set preflight with one command;
- use local LM Studio/OpenAI-compatible execution for schema-bound AI draft and
  enrichment proposals when the operator supplies a model id;
- write one batch report that summarizes candidate counts, relation counts,
  preflight status, AI proposal status, author-ready stop-policy status, and
  non-authority boundaries;
- keep CI provider-free through `--skip-ai`;
- feed only reviewed candidate-layer evidence into later SpecPM-side intake
  policy.
- document the SpecPM-facing candidate-layer intake policy before expanding
  autonomous corpus scraping.

Technical-debt follow-up from the first mixed corpus check:

- record a durable Flask/Gin/xyflow corpus baseline and gap report;
- add a single-package candidate fallback for popular repositories that are not
  workspaces;
- add bounded LM Studio/OpenAI-compatible JSON repair/retry for malformed
  local model output, with `jsonRepair` summaries and safe diagnostics;
- re-run the mixed corpus as a quality gate before expanding autonomous
  scraping.

Success criteria:

- operators can process a small popular-library set without manual command
  chaining;
- no harvested repository code is executed and no dependencies are installed;
- generated artifacts stay `preview_only` until author/maintainer review;
- SpecPM remains the acceptance and registry authority.

See [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md).
See also
[`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md).
The current mixed-corpus baseline is recorded in
[`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md),
including Flask/Gin `single_package_fallback_needed` outcomes and the xyflow
`ai_json_repair_needed` LM Studio diagnostic.
The Flask/Gin deterministic fallback is documented in
[`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md).
The post-fallback quality gate is recorded in
[`AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`](AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md)
with verdict `ready_for_limited_popular_library_scraping`.

## Milestone 10: Limited Popular-Library Scraping Batch

Status: Complete.

Goal: expand the autonomous candidate MVP from the three-repository quality
gate into a bounded 5-10 repository corpus while keeping every output as
candidate-layer preview evidence.

Tasks:

- define a small shape-diverse seed corpus and source manifest before running a
  larger scrape;
- run deterministic `--skip-ai` scraping with pinned local checkouts;
- run live LM Studio/OpenAI-compatible AI draft and enrichment with explicit
  cost, time, and repair bounds;
- produce a candidate-layer triage report before any SpecPM handoff;
- prepare SpecPM handoff dry-run evidence only for selected candidates.

Success criteria:

- operators can repeat the limited batch from a committed manifest and runbook;
- every repository outcome is classified as `candidate_layer_review_required`,
  `needs_regeneration`, `blocked`, or `not_for_intake`;
- generated packages remain `preview_only` and
  `producer_preview_evidence_only`;
- SpecPM remains the validation, acceptance, relation, and registry authority.

See
[`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md).
The deterministic `--skip-ai` corpus result is recorded in
[`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md)
with verdict `ready_for_live_lm_studio_limited_corpus`.
The live LM Studio corpus result is recorded in
[`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md)
with verdict `ready_for_candidate_layer_triage`: all six repositories
processed, nine preview candidates preserved, three relation proposals
preserved, JSON repair not needed, and model findings bounded to candidate
review diagnostics.
The candidate-layer triage result is recorded in
[`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md)
with verdict `ready_for_selected_handoff_dry_run`: `flask.core`, `gin.core`,
and `docc2context.core` are selected for P30-T5 dry-run handoff, while xyflow,
Cupertino, and NavigationSplitView candidates remain deferred until targeted
regeneration or package-identity fixes.
The selected handoff dry run is recorded in
[`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md)
with verdict `selected_handoff_dry_run_ready`: `flask.core`, `gin.core`, and
`docc2context.core` have passing producer preflight reports, static viewer
digests, and `external_required` registry acceptance decisions while all
deferred candidates stay out of the handoff.

## Milestone 11: Selected Candidate SpecPM Intake Handoff

Status: Complete.

Goal: turn selected candidate dry-run evidence into portable SpecPM review
evidence while preserving the boundary that SpecHarvester is only the producer
of preview artifacts.

Tasks:

- define `SpecHarvesterSelectedCandidateHandoffProposal`;
- implement a producer helper that emits JSON and Markdown handoff artifacts;
- run the helper on the real P30 selected candidates;
- define downstream SpecPM-side preflight expectations;
- record targeted regeneration requirements for deferred P30 candidates.

Success criteria:

- selected candidates, deferred candidates, required evidence roles, producer
  preflight status, static viewer status, and external registry acceptance
  decisions are machine-readable;
- passing producer preflight remains review evidence only;
- no proposal accepts packages, accepts relations, seeds baselines, removes
  `preview_only`, publishes registry metadata, or creates a SpecPM pull
  request.

See
[`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md).
The helper command is `selected-candidate-handoff-proposal` and writes
`selected-candidate-handoff-proposal.json` plus
`selected-candidate-handoff-proposal.md` from the selected handoff dry-run
source evidence.

P31-T3 records the real selected candidate helper run in
`tests/fixtures/selected_candidate_handoff_proposal/p31-t3-real-selected-candidate-handoff.example.json`
and [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md).
That artifact covers `flask.core`, `gin.core`, and `docc2context.core` only;
the deferred P30 candidates remain excluded until regeneration.

P31-T4 records downstream SpecPM-side preflight expectations in
[`SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`](SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md).
The expected future report is `SpecPMSelectedCandidateHandoffPreflightReport`
with `apiVersion: specpm.selected-candidate-handoff-preflight/v0`, and a pass
means internally consistent review evidence, not package acceptance.

P31-T5 records deferred selected-candidate regeneration requirements in
[`DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`](DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md)
and the
`SpecHarvesterDeferredSelectedCandidateRegenerationRequirements` fixture with
`apiVersion: spec-harvester.deferred-selected-candidate-regeneration-requirements/v0`.
The requirements cover package-set identity regeneration, warning-bearing
enrichment regeneration, and identity-drift resolution before deferred
candidates can enter selected handoff.

P26-T3 records the package-set proposal intake checklist in
[`PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md`](PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md).
It names `SpecHarvesterPackageSetHandoffProposal`,
`spec-harvester.package-set-handoff-proposal/v0`, the required evidence roles,
and the boundary between package member acceptance and relation acceptance.

## Milestone 12: Autonomous Deferred Candidate Regeneration

Status: Planned.

Goal: convert the P30/P31 deferred candidate findings into a bounded
regeneration and intake-readiness sequence before any broader popular-library
scraping is attempted.

Tasks:

- record the autonomous deferred candidate work plan;
- write a deferred candidate regeneration runbook
  ([`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md));
- run xyflow package-set identity regeneration as a dry run
  ([`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md));
- run single-package deferred candidate regeneration or repair for
  `cupertino.core` and `navigation_split_view.core`;
- refresh candidate-layer triage and selected handoff evidence;
- record the merged SpecPM-side selected candidate handoff preflight;
- record a limited corpus intake readiness decision.

Success criteria:

- all six deferred P30 candidates remain explicitly tracked until regenerated,
  repaired, blocked, or rejected;
- regeneration uses local pinned checkouts and does not clone, fetch, install
  dependencies, execute harvested code, publish registry metadata, accept
  packages, accept relations, seed baselines, or remove `preview_only`;
- SpecPM-side preflight remains consumer review evidence only;
- the project does not expand to broad autonomous popular-library scraping
  until the limited corpus has clean selected handoff evidence or documented
  deferrals.

See [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md).
P32-T2 records the regeneration runbook in
[`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md).
P32-T3 records the xyflow package-set identity regeneration dry run in
[`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md).
P32-T4 records the single-package deferred regeneration dry run in
[`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md).
P32-T5 records the refreshed selected handoff result in
[`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md):
eight candidates are ready for SpecPM-side selected handoff preflight, while
`cupertino.core` remains deferred on `refined_summary_missing`.
P32-T6 records that the SpecPM preflight was merged in
[`0al-spec/SpecPM#140`](https://github.com/0al-spec/SpecPM/pull/140) and that
the P32-T5 fixture passes with eight selected candidates, one deferred
candidate, and three source digests verified.
P32-T7 records the intake readiness decision in
[`LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`](LIMITED_CORPUS_INTAKE_READINESS_DECISION.md):
the selected preview candidates are ready for author/maintainer review,
`cupertino.core` remains deferred, and broader autonomous scraping requires a
separate follow-up task.

## Milestone 13: Bounded Corpus Expansion Planning

Status: Complete.

Goal: define the next autonomous candidate corpus as a bounded, local-only,
operator-selected batch before any new scrape runs and stop at reviewable
producer evidence.

Tasks:

- record `P33-T1`, the bounded corpus expansion plan
  ([`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md));
- add `P33-T2`, the next-corpus source manifest fixture with pinned local checkout
  requirements
  ([`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md),
  `inputs/p33-next-corpus/repositories.yml`);
- record `P33-T3`, the deterministic collection and draft generation run without AI
  ([`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md));
- record `P33-T4`, the live local-model draft/enrichment run with bounded JSON
  repair and provider receipts
  ([`NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`](NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md));
- record `P33-T5`, the candidate-layer triage and selected handoff readiness
  evidence
  ([`NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`](NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md));
- run or coordinate SpecPM-side selected handoff preflight and record the next
  intake readiness decision
  ([`NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`](NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md)).
- create durable selected handoff evidence for the selected scope and prove it
  passes SpecPM selected handoff preflight
  ([`NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`](NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md));
- record `P33-T8`, the final intake readiness decision for the preflighted
  selected scope
  ([`NEXT_CORPUS_INTAKE_READINESS_DECISION.md`](NEXT_CORPUS_INTAKE_READINESS_DECISION.md)).

Success criteria:

- the next corpus is capped at five repositories;
- the source manifest exists before collection and forbids clone/fetch,
  dependency installation, harvested code execution, and network discovery;
- deterministic, live-model, candidate-layer, and SpecPM-side gates are
  recorded before any registry-facing handoff;
- P33-T6 records that the current P33-T5 triage artifact is not a supported
  SpecPM selected handoff payload and requires a durable selected handoff
  follow-up before maintainer intake review;
- P33-T7 records that the durable selected handoff artifact passes SpecPM
  selected handoff preflight with two selected candidates, three deferred
  candidates, and zero warnings or errors;
- P33-T8 records `ready_for_author_maintainer_review_with_explicit_deferral`:
  `serena.core` and `specpm.core` are ready for author/maintainer review,
  while `transmission.core`, `mcpm.system`, and `specgraph.system` remain
  deferred;
- the result remains review evidence only and does not accept packages, accept
  relations, seed baselines, remove `preview_only`, publish registry metadata,
  or treat AI output as registry truth.

## Milestone 14: Curated Multi-Ecosystem Corpus Selection

Status: Planned.

Goal: define how SpecHarvester selects important library repositories and
package families across ecosystems before running autonomous harvesting, so the
project grows through bounded curated corpora rather than open-ended registry
crawling.

Tasks:

- document `P35-T1`, the corpus selection policy, including importance
  signals, exclusion rules, ecosystem quotas, local checkout requirements, and
  the producer-evidence boundary
  ([`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md));
- define `P35-T2`, a machine-readable `SpecHarvesterCorpusPlan` format with
  selected-because reason codes, excluded-subpackage reason codes, source
  checkout pins, categories, package-family targets, and non-authority
  statements
  ([`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md),
  `tests/fixtures/corpus_plan/p35-t2-corpus-plan.example.json`);
- plan `P35-T3`, candidate source classification for primary packages,
  package-set roots, plugins, examples, tooling, type-only packages, generated
  artifacts, internal utilities, and deprecated sources
  ([`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md),
  `tests/fixtures/source_classifier_plan/p35-t3-source-classifier-plan.example.json`);
- create `P35-T4`, the first bounded multi-ecosystem seed corpus plan across
  JavaScript/TypeScript, Python, Rust, Go, and at least one additional
  ecosystem
  ([`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md),
  `tests/fixtures/multi_ecosystem_seed_corpus_plan/p35-t4-seed-corpus-plan.example.json`);
- add `P35-T5`, an explainable corpus selection report that records selected,
  rejected, and deferred sources with importance signals, exclusion reasons,
  quota decisions, and the downstream autonomous-batch command plan
  ([`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md),
  `tests/fixtures/explainable_corpus_selection_report/p35-t5-selection-report.example.json`);
- run or document `P35-T6`, a dry-run readiness check proving every selected
  source has a pinned local checkout, package-family target, expected analyzer
  coverage, and explicit stop condition before author/maintainer review
  ([`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md),
  `tests/fixtures/selected_corpus_readiness/p35-t6-readiness.example.json`).

Success criteria:

- corpus expansion remains operator-selected, bounded, and explainable;
- the Phase 35 seed corpus is blocked until operator-provided pinned local
  checkouts are verified;
- selection uses multiple signals instead of raw registry search ranking:
  dependency centrality, registry usage, public API richness, ecosystem
  archetype coverage, release health, source availability, license clarity,
  security/supply-chain relevance, and author review value;
- internal utilities, types-only packages, generated-only packages, deprecated
  sources, examples, test fixtures, build tooling, and search noise are
  excluded or deferred with machine-readable reasons;
- the corpus plan does not clone/fetch repositories, install dependencies,
  execute harvested code, publish registry metadata, accept packages, accept
  relations, seed baselines, remove `preview_only`, or treat AI output as
  registry truth.

### Repository Parsing Plugin System

Phase 36 records the next precision layer after the FastAPI AI-enabled rerun:
repository parsing plugins should classify repository paths by evidence role
before public interface indexes are assembled.

`P36-T1` defines
[`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md).
The contract separates public API evidence from semantic usage/documentation
evidence, uses FastAPI `docs_src/*` over-capture as the motivating case, and
keeps the intended Python web-framework parser profile reusable rather than
repository-specific.

Completed follow-ups:

- `P36-T2`: add a machine-readable Python web-framework parser profile
  fixture;
- `P36-T3`: implement the first plugin-aware source classification hook;
- `P36-T4`: rerun FastAPI with the parser profile and compare evidence volume
  and claim quality.

The P36-T4 FastAPI rerun is recorded in
[`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md). It shows
`docs_src/*` public interface entrypoints dropping from `454` to `0` while
FastAPI package entrypoints stay at `48`. The output is closer to
registry-review quality on evidence boundary, but AI proposal artifacts still
had warning-level gaps, so the result remains an author-ready starter package
rather than a clean registry handoff.

Plugin decisions remain producer-side evidence only: no registry publication,
no package or relation acceptance, no baseline seeding, no `preview_only`
removal, and no AI output as registry truth.

### Repository Profile Plugin Selection

Phase 37 plans the next layer after parser profiles: deciding which repository
profile plugin, if any, should be applied to a given checkout.

The planned work starts with `P37-T1`,
[`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md),
a language- and framework-agnostic selection contract. The shared model is:

```text
detect candidates -> score evidence -> select or fallback -> record decision
```

Planned follow-ups:

- `P37-T2`: define a machine-readable
  `SpecHarvesterRepositoryProfileDetection` fixture format;
- `P37-T3`: add an opt-in detection CLI/report surface that emits profile
  decisions without collecting source, invoking AI, or drafting packages;
- `P37-T4`: connect profile selection to autonomous candidate batch through
  explicit `auto | none | <profile-id>` modes and sidecar
  `repository-profile-detection.json` artifacts;
- `P37-T5`: define generic workspace/member discovery hints for package-set
  roots, members, meta packages, primary packages, CLI/bridge packages,
  plugin packages, examples, tests, docs, generated artifacts, internal
  utilities, and evidence-only sources through
  [`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md)
  and `SpecHarvesterRepositoryProfileHintVocabulary`;
- `P37-T6`: add cross-ecosystem fixtures so the subsystem is not tied to one
  language or framework through
  [`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md);
- `P37-T7`: rerun a real repository with profile auto-selection and compare
  it against manual targeting through
  [`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md);
- `P37-T8`: make repository profile detection consume harvested package
  manifest evidence when workspace inventory has no manifest records.

The motivating FastMCP dry run showed why this layer is needed: generic
repository-wide collection can over-include docs/examples, while manual member
targets can produce better author-ready starter packages. FastMCP remains a
validation case, not a hardcoded profile rule.

P37-T7 confirmed that finding on a real FastMCP checkout. Auto-selection passed
and explained its fallback, but it did not improve targeting: `harvest.json`
found `pyproject.toml`, `workspace-inventory.json` had no manifest records, and
manual `fastmcp_slim` targeting reduced public interface entrypoints from `772`
to `260`.

P37-T8 closes that generic evidence-routing gap by supplementing empty
workspace inventory evidence with already-collected static manifest paths from
`harvest.json`.

Selection decisions remain producer-side evidence only. Profile selection does
not clone or fetch repositories, install dependencies, execute harvested code,
invoke package managers, run AI, publish registry metadata, accept packages or
relations, remove `preview_only`, or accept plugin decisions as registry
truth. Profile selection does not treat AI output as registry truth.

### Repository Plugin Subsystem

Phase 38 turns parser profiles and repository profiles into a broader
language- and framework-agnostic plugin subsystem contract.

The first step is `P38-T1`,
[`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md),
which defines plugin identity, plugin roles, registration metadata, static
evidence inputs, applicability reports, deterministic selection boundaries,
output artifact categories, diagnostics, and authority limits. The shared
model is:

```text
register plugins -> collect static evidence -> evaluate applicability
  -> select, fallback, or block -> emit producer-side evidence
```

P38-T2 adds the first `SpecHarvesterRepositoryPluginRegistry` registry fixture in
[`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md)
and `tests/fixtures/repository_plugins/generic-registry.example.json`.

P38-T3 adds the first `SpecHarvesterRepositoryPluginApplicabilityReport`
fixture in
[`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md)
and
`tests/fixtures/repository_plugins/generic-applicability-report.example.json`.
It records selected, rejected, fallback, and blocked plugin decisions from
static evidence without running plugin code.

P38-T4 connects registry/applicability output to
[`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md) as
`repositoryPluginApplicability` sidecar producer evidence. The batch copies the
applicability report to
`reports/repository-plugin-applicability/repository-plugin-applicability-report.json`
and records path, digest, authority, summary counts, and diagnostic codes while
keeping `appliedToDrafting: false` and `registryAuthority: false`.

P38-T5 adds a cross-ecosystem static fixture matrix in
[`REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md)
and `tests/fixtures/repository_plugins/cross_ecosystem/`. The matrix covers
manifest-backed single-package, workspace, documentation-heavy, nested package
root, and ambiguous mixed repository shapes while keeping plugin applicability
producer-side and language/framework agnostic.

P38-T6 records a real FastMCP plugin evidence comparison in
[`REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`](REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md)
and
`tests/fixtures/repository_plugins/real_runs/p38-t6-fastmcp-plugin-evidence-comparison.example.json`.
The run shows current repository profile selection choosing
`generic.single_package.v0` and autonomous batch recording
`repositoryPluginApplicability` as sidecar evidence with
`appliedToDrafting: false` and `registryAuthority: false`.

Phase 39 starts with
[`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md).
P39-T3 adds the deterministic helper, P39-T4 adds
`repository-plugin-applicability-detect`, and P39-T5 connects the same evaluator
to `autonomous-candidate-batch` through explicit
`--repository-plugin-registry` and
`--repository-plugin-static-evidence-envelope` opt-in inputs. Together they
derive `SpecHarvesterRepositoryPluginApplicabilityReport` from a static
evidence envelope rather than hand-authored sidecars. The helper, CLI, and
batch integration remain producer-side evidence only: they do not load plugins,
execute plugins, read repository source files, run package managers, install
dependencies, invoke AI, auto-attach generated reports to autonomous batch
output without explicit operator opt-in, accept packages or relations, publish
registry metadata, remove `preview_only`, or treat plugin decisions as registry
truth.

P39-T2 adds
[`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md)
and
`tests/fixtures/repository_plugins/static-evidence-envelope.example.json`.
The fixture records `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope`,
safe relative evidence paths, SHA-256 digests, `evidenceKinds[]`, advisory
signals, and `appliedToDrafting: false` / `registryAuthority: false` sidecar
boundaries as the bounded input to the P39-T3 helper, P39-T4 CLI, and P39-T5
batch opt-in path.

P39-T6 records a real multi-repository validation in
[`REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md`](REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md)
and
`tests/fixtures/repository_plugins/real_runs/p39-t6-multi-repository-static-evaluator-validation.example.json`.
The run covers FastMCP, FastAPI, and xyflow local checkouts, exercises both
`repository-plugin-applicability-detect` and
`autonomous-candidate-batch --repository-plugin-registry
--repository-plugin-static-evidence-envelope`, and confirms that generated
sidecars remain `sourceMode: auto_static_evaluator`,
`appliedToDrafting: false`, and `registryAuthority: false`.

Phase 40 starts with `P40-T1`,
[`REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`](REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md).
The phase turns the static plugin selection work into a language- and
framework-agnostic boundary for future adapter implementations: adapter
identity, versioned manifests, declared input evidence, output artifacts,
execution modes, sandbox expectations, diagnostics, and authority limits.
Static applicability remains the default safe path. Adapter execution stays
disabled until a future task adds explicit operator-controlled execution
policy, manifest preflight, and safe evidence handoff rules.

P40-T2 records the first machine-readable adapter manifest fixture in
[`REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md)
and `tests/fixtures/repository_plugins/adapter-manifest.example.json`.
P40-T3 records the first adapter preflight report fixture in
[`REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md)
and `tests/fixtures/repository_plugins/adapter-preflight-report.example.json`,
covering allowed, rejected, fallback, and blocked adapter decisions without
loading or executing adapter code.
P40-T4 records the adapter execution policy in
[`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md):
execution is disabled by default, `static_only` remains the only current safe
mode, and future `trusted_local_tool` requires explicit operator opt-in, path
allowlists, bounded resources, no dependency installation, no package manager
invocation, no network discovery, and no harvested code execution.
P40-T5 connects operator-supplied adapter manifest and preflight evidence to
[`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md) through
`--repository-plugin-adapter-manifest` and
`--repository-plugin-adapter-preflight`. The batch records
`repositoryPluginAdapterEvidence` with copied paths, SHA-256 digests,
allowed/rejected/fallback/blocked counts, diagnostics, `appliedToDrafting:
false`, `registryAuthority: false`, and `adapterExecution: not_run` while
preserving the existing static evaluator path unless an operator explicitly
supplies adapter evidence.

Python, JavaScript, FastAPI, FastMCP, npm, Cargo, Go, SwiftPM, Maven, Gradle,
and other ecosystems remain examples, not normative plugin rules. Repository
plugins and future adapters must not clone or fetch repositories, install
dependencies, execute harvested code, invoke package managers, run AI, publish
registry metadata, accept packages or relations, remove `preview_only`, or
treat plugin output as registry truth or treat adapter output as registry
truth.

## Non-Goals

SpecHarvester does not:

- publish packages into SpecPM;
- mutate the public SpecPM registry;
- grant namespace ownership;
- execute harvested repository code;
- treat AI output as accepted package truth;
- decide package-set relation acceptance;
- replace SpecPM validation or maintainer review.

## References

- `SPECS/Workplan.md`
- `docs/PRODUCER_CANDIDATE_BUNDLE.md`
- `docs/SPECPM_HANDOFF.md`
- `docs/SPECPM_PACKAGE_SET_ALIGNMENT.md`
- `docs/WORKSPACE_INVENTORY.md`
- `docs/PACKAGE_SET_DRAFTING.md`
- `docs/BUNDLE_SET_PREFLIGHT.md`
- `docs/PACKAGE_SET_AI_ENRICHMENT.md`
- `docs/AUTONOMOUS_CANDIDATE_BATCH.md`
- `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`
- `docs/SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`
- `docs/XYFLOW_PACKAGE_SET_SMOKE.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`
