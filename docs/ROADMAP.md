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
- trusted workflow mode that uploads package-set evidence without using
  SpecPM write credentials on untrusted PR events.

Success criteria:

- SpecHarvester can produce review evidence that SpecPM can preflight without
  executing producer tools;
- `SPECPM_PROPOSAL_TOKEN` remains limited to trusted workflows;
- generated receipts never claim maintainer acceptance.

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
- SpecPM can consume AI enrichment as proposal-only evidence through its own
  preflight and review policy;
- private or unsupported evidence paths are rejected or downgraded to
  diagnostics.

## Milestone 5: Author-Ready Valid Drafts

Status: next product-quality focus.

Goal: define when SpecHarvester should stop drafting and hand a valid starter
package to the repository author.

Tasks:

- document the author-ready draft quality bar;
- treat `specpm validate` success as a hard gate, not a semantic quality score;
- define stop policy for AI draft and enrichment loops;
- record author action items, weak claims, and evidence gaps explicitly;
- keep final semantic curation with the author and their agent.

Success criteria:

- generated output is described as a valid starter package, not a final
  accepted spec;
- operators can tell when additional model iteration is no longer useful;
- authors receive a reviewable handoff with clear edit points and evidence
  context.

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
- `docs/XYFLOW_PACKAGE_SET_SMOKE.md`
