# SpecHarvester Documentation

This directory is the operator and design entrypoint for SpecHarvester.

Use it the same way the SpecPM repository uses GitHub-facing documentation:
start from the workflow, then drill into architecture, trust boundaries, and
automation details.

Published DocC site:
[https://0al-spec.github.io/SpecHarvester/](https://0al-spec.github.io/SpecHarvester/).

## Read This First

1. [`../README.md`](../README.md): repository overview and GitHub workflow surface
2. [`CAPABILITIES.md`](CAPABILITIES.md): current capability map, maturity
   boundary, and non-goals
3. [`HOW_IT_WORKS.md`](HOW_IT_WORKS.md): end-to-end operator flow
4. [`TRUST_BOUNDARY.md`](TRUST_BOUNDARY.md): non-negotiable execution rules
5. [`ANALYZER_SANDBOX_REQUIREMENTS.md`](ANALYZER_SANDBOX_REQUIREMENTS.md):
   requirements for future metadata-tool and build-tool analyzers
6. [`TRUSTED_CLASSIFIER_EVALUATION.md`](TRUSTED_CLASSIFIER_EVALUATION.md):
   registry and trust contract for optional external classifiers
7. [`CODEGRAPH_SOURCE_GRAPH_ADAPTER.md`](CODEGRAPH_SOURCE_GRAPH_ADAPTER.md):
   optional CodeGraph evidence normalization into `source_graph_index`
8. [`CODEGRAPH_COMPATIBILITY_GUARD.md`](CODEGRAPH_COMPATIBILITY_GUARD.md):
   offline pinned CodeGraph interface compatibility guard
9. [`LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`](LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md):
   bounded README/API-contract semantic hints for manifest-poor repositories
10. [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md):
   repository path classification contract for future language/framework
   parser profiles
11. [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md):
   language- and framework-agnostic repository profile selection contract
12. [`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md):
   generic advisory path-role hints emitted by repository profiles
13. [`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md):
   fixture coverage proving repository profile selection is not tied to one
   language or framework
14. [`REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`](REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md):
   real FastMCP auto-selection comparison against manual targeting, including
   the P37-T8 manifest-evidence follow-up
15. [`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md):
   practical FastAPI rerun showing the Python web-framework parser profile
   removing `docs_src/*` from public interface evidence
14. [`REPOSITORY_SOURCE_MANIFESTS.md`](REPOSITORY_SOURCE_MANIFESTS.md):
   batch harvesting input manifest schema
11. [`BATCH_COLLECTION.md`](BATCH_COLLECTION.md): deterministic batch snapshot
   collection from local checkouts
12. [`BATCH_VALIDATION_REPORTS.md`](BATCH_VALIDATION_REPORTS.md): advisory
   confidence and policy reports for batch output
13. [`ACCEPTED_MANIFEST_ENTRIES.md`](ACCEPTED_MANIFEST_ENTRIES.md): prepare
   PR-ready accepted package manifest entries
11. [`GOVERNANCE_REPORTS.md`](GOVERNANCE_REPORTS.md): detect duplicate intent
   and capability claims across accepted and candidate metadata
12. [`NAMESPACE_UPSTREAM_REPORTS.md`](NAMESPACE_UPSTREAM_REPORTS.md): review
   namespace consistency and upstream relationship metadata across roots
13. [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md): trusted
    proposal automation with preflight validation and diff-scope guardrails
14. [`ACCEPTED_PACKAGE_UPDATE_LIFECYCLE.md`](ACCEPTED_PACKAGE_UPDATE_LIFECYCLE.md):
   accepted package version immutability and update decision policy
15. [`ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md`](ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md):
   build PR-ready accepted package update artifacts
16. [`ACCEPTED_CANDIDATE_DIFF_REPORTS.md`](ACCEPTED_CANDIDATE_DIFF_REPORTS.md):
    compare accepted and candidate package metadata before update proposals
17. [`ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md`](ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md):
    classify accepted-candidate diff output by metadata, interface, license,
    provenance, capability, and intent impact
18. [`LICENSE_PROVENANCE_RISK_REPORTS.md`](LICENSE_PROVENANCE_RISK_REPORTS.md):
    review candidate and accepted packages for licensing and provenance risk
19. [`CODE_DUPLICATION_REPORTS.md`](CODE_DUPLICATION_REPORTS.md):
    advisory duplicate-code quality reports for local source review
20. [`ARCHITECTURE_LINT_GUARDRAILS.md`](ARCHITECTURE_LINT_GUARDRAILS.md):
    advisory project-specific architecture lint guardrails before structural
    refactors
21. [`PROCEDURAL_STYLE_REPORT.md`](PROCEDURAL_STYLE_REPORT.md):
    advisory procedural-style metrics for EO refactoring baselines
22. [`EO_REFACTORING_STRATEGY.md`](EO_REFACTORING_STRATEGY.md):
    phased Elegant Objects refactoring strategy and acceptance metrics
23. [`LOCAL_SMOKE_FIXTURES.md`](LOCAL_SMOKE_FIXTURES.md): reproducible local
    smoke fixtures for adjacent real repository checkouts
24. [`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md):
    typed artifact bundle and job contract for future SpecNode-assisted
    candidate refinement
25. [`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md):
    bounded `refine-preview` planning contract for compact model input
26. [`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md):
    versioned prompt contract for schema-bound SpecNode refinement
27. [`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md):
    clean-context semantic review contract for generated SpecNode proposals
28. [`SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`](SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md):
    feedback-driven retry orchestration for bounded SpecNode refinement loops
29. [`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md):
    OpenAI-compatible provider adapter boundary for local SpecNode execution
30. [`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md):
    schema-validated candidate patch proposal output contract
31. [`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md):
    local SpecNode-compatible provider smoke coverage and deterministic
    provider-unavailable fallback
32. [`REAL_REPOSITORY_REFINEMENT_VALIDATION.md`](REAL_REPOSITORY_REFINEMENT_VALIDATION.md):
    local-only real repository validation plan for SpecHarvester-side evidence,
    draft, reporting, and external SpecNode contract boundary checks
33. [`REAL_REPOSITORY_QUALITY_REPORT.md`](REAL_REPOSITORY_QUALITY_REPORT.md):
    structured quality report format for real-repository refinement runs,
    covering intent accuracy, capability evidence, SpecPM status, retry
    effectiveness, token usage, analyzer coverage, and human-review notes
34. [`AUTHOR_READY_DRAFT_QUALITY_BAR.md`](AUTHOR_READY_DRAFT_QUALITY_BAR.md):
    author-ready valid starter package quality bar, stop policy, review
    dimensions, and handoff expectations for repository authors
35. [`AUTHOR_READY_DRAFT_QUALITY_REPORT.md`](AUTHOR_READY_DRAFT_QUALITY_REPORT.md):
    machine-readable `authorReadyDraft` verdict, hard gates, dimensions, and
    author action items for generated starter packages
36. [`AUTHOR_READY_CALIBRATION_MATRIX.md`](AUTHOR_READY_CALIBRATION_MATRIX.md):
    real-repository author-ready calibration matrix for estimated author edits,
    edit categories, review priorities, and repeated generator gaps
37. [`REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md`](REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md):
    local-only runner for deterministic orchestration of real-repository checks
38. [`REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md`](REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md):
    compact P15-T4 local validation matrix across Swift/SPM, JS/TS, Python,
    Go, and documentation-first repository shapes
38. [`STATIC_SPEC_RENDERER.md`](STATIC_SPEC_RENDERER.md): static HTML/JS preview
    for generated SpecPM candidate packages from `specpm.yaml` and referenced
    `specs/*.spec.yaml`
39. [`PRODUCER_CANDIDATE_BUNDLE.md`](PRODUCER_CANDIDATE_BUNDLE.md):
    SpecPM Producer Candidate Bundle output plan for `producer-receipt.json`,
    validation reports, diagnostics, hashes, and human review handoff
40. [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md): operator handoff guide for
    drafting, preflighting, rendering, and reviewing generated candidate
    bundles before SpecPM acceptance
41. [`SPECPM_SHARED_FIXTURE_POLICY.md`](SPECPM_SHARED_FIXTURE_POLICY.md):
    shared fixture policy for keeping SpecPM contract examples and
    SpecHarvester generated bundle examples aligned
42. [`SPECPM_PACKAGE_SET_ALIGNMENT.md`](SPECPM_PACKAGE_SET_ALIGNMENT.md):
    package-set contract alignment for monorepo discovery, scoped member
    candidates, relation proposals, bundle-set preflight, viewer output, and
    the `xyflow` reference scenario
43. [`WORKSPACE_INVENTORY.md`](WORKSPACE_INVENTORY.md): deterministic
    `workspace-inventory.json` producer evidence for monorepo package-set
    discovery
44. [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md): preview
    `draft-package-set` generation of aggregate and scoped member candidates
    from workspace inventory
45. [`PACKAGE_RELATION_PROPOSALS.md`](PACKAGE_RELATION_PROPOSALS.md):
    deterministic `contains` relation proposals for package-set candidate
    bundle review
46. [`BUNDLE_SET_PREFLIGHT.md`](BUNDLE_SET_PREFLIGHT.md):
    producer-side `preflight-bundle-set` verification for generated
    package-set outputs, member candidate bundles, relation proposals, and
    digest references
47. [`PACKAGE_SET_VIEWER.md`](PACKAGE_SET_VIEWER.md):
    static `render-package-set-site` review surface for package-set summaries,
    member package cards, relation proposal badges, and result scope examples
48. [`XYFLOW_PACKAGE_SET_SMOKE.md`](XYFLOW_PACKAGE_SET_SMOKE.md):
    local `xyflow-package-set-smoke` scenario for workspace inventory,
    package-set drafting, relation proposals, bundle-set preflight, and viewer
    output
49. [`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md):
    package-set handoff proposal JSON and Markdown for future SpecPM review
    automation
50. [`FRESH_CANDIDATE_REFRESH_RUN.md`](FRESH_CANDIDATE_REFRESH_RUN.md):
    producer-side package-set export into the SpecPM
    `prepare-refresh-decision` fresh generated-root layout
51. [`BASELINE_SUBMISSION_HANDOFF.md`](BASELINE_SUBMISSION_HANDOFF.md):
    first-submission or seeded-baseline handoff evidence for repositories
    without current SpecPM generated artifacts
52. [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md):
    proposal-only local AI enrichment for generated package-set candidates,
    compact evidence, provider receipts, bounded JSON repair, and unsupported
    evidence diagnostics
53. [`AI_ENRICHMENT_CANDIDATE_PATCH.md`](AI_ENRICHMENT_CANDIDATE_PATCH.md):
    apply clean AI enrichment proposals into copied preview candidates with a
    machine-readable patch report while preserving SpecPM authority boundaries
54. [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md):
    MVP autonomous popular-library scraping runner over local source manifests,
    package-set preview bundles, local LM Studio proposals, bounded JSON repair,
    optional copied AI-enriched preview candidates, and batch reports
54. [`AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`](AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md):
    SpecPM-facing candidate-layer intake policy for autonomous batch output,
    review states, maintainer checks, and authority boundaries
55. [`AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`](AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md):
    current autonomous candidate technical-debt plan: completed P29 fallback
    and JSON-repair debt plus Phase 32 deferred candidate regeneration and
    SpecPM intake-readiness work
56. [`DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md`](DEFERRED_CANDIDATE_REGENERATION_RUNBOOK.md):
    P32 operator runbook for deferred candidate regeneration classes, safe
    local commands, expected artifacts, stop conditions, and re-entry criteria
57. [`XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`](XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md):
    P32-T3 xyflow-only package-set identity regeneration dry-run evidence,
    relation topology, preflight/viewer proof, and candidate-layer decision
58. [`SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`](SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md):
    P32-T4 Cupertino and NavigationSplitView single-package regeneration
    dry-run evidence, canonical id decision, preflight/viewer proof, and
    refreshed candidate-layer decisions
59. [`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md):
    P32-T5 refreshed candidate-layer selected handoff, selected/deferred
    decisions, source fixture digests, and SpecPM-side preflight boundary
60. [`LIMITED_CORPUS_INTAKE_READINESS_DECISION.md`](LIMITED_CORPUS_INTAKE_READINESS_DECISION.md):
    P32-T7 limited corpus intake readiness decision, selected/deferred
    dispositions, SpecPM preflight result, and expansion boundary
61. [`BOUNDED_CORPUS_EXPANSION_PLAN.md`](BOUNDED_CORPUS_EXPANSION_PLAN.md):
    P33-T1 bounded next-corpus expansion plan with source manifest
    requirements, five-repository limit, validation gates, stop conditions, and
    non-authority boundary
62. [`NEXT_CORPUS_SOURCE_MANIFEST.md`](NEXT_CORPUS_SOURCE_MANIFEST.md):
    P33-T2 next-corpus source manifest fixture for `serena`, `transmission`,
    `mcpm-sh`, `specgraph`, and `specpm` with pinned local checkout revisions
    and no network discovery behavior
63. [`NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`](NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md):
    P33-T3 deterministic `--skip-ai` dry-run evidence for the next bounded
    corpus, including candidate counts, preflight outcomes, package-id review
    signals, and live local-model readiness
64. [`NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`](NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md):
    P33-T4 live LM Studio next-corpus dry-run evidence, including provider
    receipts, JSON repair outcome, AI draft/enrichment diagnostics,
    candidate-layer findings, and triage readiness
65. [`NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`](NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md):
    P33-T5 candidate-layer triage for the next corpus, including selected and
    deferred candidates, finding classifications, selected handoff readiness,
    and non-authority boundaries
66. [`NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`](NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md):
    P33-T6 SpecPM selected handoff preflight result, intake readiness decision,
    durable handoff follow-up, selected/deferred scope, and non-authority
    boundary
67. [`NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`](NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md):
    P33-T7 durable selected handoff artifact, committed evidence roles,
    passing SpecPM selected handoff preflight, selected/deferred scope, and
    non-authority boundary
68. [`NEXT_CORPUS_INTAKE_READINESS_DECISION.md`](NEXT_CORPUS_INTAKE_READINESS_DECISION.md):
    P33-T8 intake readiness decision, selected candidates ready for
    author/maintainer review, explicit deferred candidates, passing SpecPM
    selected handoff preflight, and non-authority boundary
69. [`CAPABILITIES.md`](CAPABILITIES.md):
    current product capability map, supported repository shapes,
    author-ready draft boundary, AI boundary, SpecPM boundary, and maturity
    table
70. [`CORPUS_SELECTION_POLICY.md`](CORPUS_SELECTION_POLICY.md):
    Phase 35 policy for bounded multi-ecosystem source selection, importance
    signals, exclusion rules, ecosystem quotas, pinned local checkout
    requirements, and non-authority boundaries
71. [`SPECHARVESTER_CORPUS_PLAN.md`](SPECHARVESTER_CORPUS_PLAN.md):
    machine-readable `SpecHarvesterCorpusPlan` contract for curated source
    batches, selected/deferred/rejected decisions, reason codes, expected
    analyzer coverage, stop conditions, and non-authority statements
72. [`CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`](CANDIDATE_SOURCE_CLASSIFIER_PLAN.md):
    Phase 35 classifier plan for package-set roots, primary packages, plugins,
    examples, tooling, type-only packages, generated artifacts, internal
    utilities, deprecated sources, evidence-only units, and allowed actions
73. [`MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`](MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md):
    first bounded Phase 35 seed corpus plan across JavaScript/TypeScript,
    Python, Rust, Go, and Swift
74. [`EXPLAINABLE_CORPUS_SELECTION_REPORT.md`](EXPLAINABLE_CORPUS_SELECTION_REPORT.md):
    Phase 35 report contract for selected, deferred, and rejected source
    explanations, quota decisions, and downstream command planning
75. [`SELECTED_CORPUS_DRY_RUN_READINESS.md`](SELECTED_CORPUS_DRY_RUN_READINESS.md):
    Phase 35 readiness report proving selected seed sources are blocked until
    pinned local checkouts are verified
60. [`AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`](AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md):
    first mixed Flask/Gin/xyflow corpus baseline with deterministic and live
    LM Studio gap classifications
61. [`AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md`](AUTONOMOUS_CANDIDATE_CORPUS_QUALITY_GATE.md):
    post-fallback Flask/Gin/xyflow quality gate and limited scraping readiness
    verdict
62. [`LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`](LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md):
    P30 bounded popular-library corpus selection, source manifest, runbook,
    stop conditions, and non-authority boundaries
63. [`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md):
    P30 deterministic `--skip-ai` limited corpus result, candidate counts,
    preflight outcomes, author-ready decisions, and product verdict
64. [`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md):
    P30 live LM Studio limited corpus result, AI draft/enrichment statuses,
    JSON repair summary, provider token usage, and candidate-layer triage verdict
65. [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md):
    P30 candidate-layer triage report, selected P30-T5 candidates,
    regeneration decisions, and non-authority boundaries
66. [`LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`](LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md):
    P30 selected candidate handoff dry-run evidence, preflight/viewer digests,
    deferred candidates, and external registry acceptance boundary
67. [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md):
    portable selected candidate handoff proposal contract and helper for SpecPM
    review evidence, selected/deferred candidates, required evidence roles,
    `selected-candidate-handoff-proposal` JSON/Markdown output, and
    non-authority boundaries
67. [`SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`](SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md):
    P31-T3 generated selected candidate handoff proposal Markdown companion for
    the real P30 selected candidates
68. [`SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`](SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md):
    downstream SpecPM-side preflight expectations for selected candidate
    handoff proposal evidence
69. [`SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`](SINGLE_PACKAGE_CANDIDATE_FALLBACK.md):
    deterministic fallback for Flask/Gin-style repositories with no workspace
    package records
70. [`../SPECS/README.md`](../SPECS/README.md): Flow workflow for planning,
    implementing, validating, and archiving tasks

## Design References

- [`ARCHITECTURE.md`](ARCHITECTURE.md): component model and non-goals
- [`ROADMAP.md`](ROADMAP.md): implementation phases and future tracks
- [`TREE_SITTER_EVALUATION.md`](TREE_SITTER_EVALUATION.md): decision record for
  Tree-sitter as an optional syntax indexing layer
- [`TRUSTED_CLASSIFIER_EVALUATION.md`](TRUSTED_CLASSIFIER_EVALUATION.md):
  evaluation record for Linguist-compatible classifiers, Syft, ScanCode,
  Universal Ctags, and Tree-sitter
- [`LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`](LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md):
  README/API-contract semantic extraction for manifest-poor repositories
- [`REPOSITORY_PARSING_PLUGIN_CONTRACT.md`](REPOSITORY_PARSING_PLUGIN_CONTRACT.md):
  repository path classification contract for future language/framework parser
  profiles
- [`REPOSITORY_PROFILE_SELECTION_CONTRACT.md`](REPOSITORY_PROFILE_SELECTION_CONTRACT.md):
  language- and framework-agnostic selection contract for repository profile
  plugins
- [`REPOSITORY_PROFILE_DISCOVERY_HINTS.md`](REPOSITORY_PROFILE_DISCOVERY_HINTS.md):
  generic advisory path-role hints for repository profile output
- [`REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md):
  cross-ecosystem fixture coverage for generic repository profile selection
- [`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md):
  FastAPI parser profile rerun with evidence volume and AI quality verdict
- [`SPECPM_PROPOSAL_AUTOMATION.md`](SPECPM_PROPOSAL_AUTOMATION.md): trusted
  automation for proposing accepted-source diffs into SpecPM
- [`SPECNODE_INTEGRATION_CONTRACT.md`](SPECNODE_INTEGRATION_CONTRACT.md):
  trust boundary for future model-assisted candidate refinement through
  SpecNode
- [`SPECNODE_REFINE_PREVIEW_CONTRACT.md`](SPECNODE_REFINE_PREVIEW_CONTRACT.md):
  deterministic `refine-preview` plan shape for compact model input
- [`SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`](SPECNODE_REFINEMENT_PROMPT_CONTRACT.md):
  versioned prompt contract for target-package intent inference, evidence
  references, negative claims, confidence calibration, and schema-bound output
- [`SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`](SPECNODE_SEMANTIC_REVIEW_CONTRACT.md):
  clean-context semantic review pass with typed verdicts and findings for
  generated `SpecNodeRefinementResult` proposals
- [`SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`](SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md):
  bounded feedback-driven retry controller that converts semantic review
  findings into deterministic retry directives
- [`SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`](SPECNODE_PROVIDER_ADAPTER_CONTRACT.md):
  LM Studio/OpenAI-compatible provider discovery, health, model listing, and
  execution policy boundary for SpecNode
- [`SPECNODE_PATCH_PROPOSAL_CONTRACT.md`](SPECNODE_PATCH_PROPOSAL_CONTRACT.md):
  schema-validated `candidatePatchProposal`, provenance, usage receipt, and
  rejection reason output boundary
- [`SPECNODE_PROVIDER_SMOKE_COVERAGE.md`](SPECNODE_PROVIDER_SMOKE_COVERAGE.md):
  executable local provider-stub smoke coverage for compact weak-model inputs,
  structural validation, and deterministic fallback
- [`REAL_REPOSITORY_REFINEMENT_VALIDATION.md`](REAL_REPOSITORY_REFINEMENT_VALIDATION.md):
  real repository validation plan that keeps SpecHarvester on deterministic
  evidence, artifact bundle, validation, and reporting responsibilities while
  treating SpecNode as an external contract boundary
- [`REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md`](REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md):
  local runner for executing real-repository validation steps from manifests
- [`STATIC_SPEC_RENDERER.md`](STATIC_SPEC_RENDERER.md): static HTML/JS renderer
  for local candidate package review before SpecPM acceptance
- [`PRODUCER_CANDIDATE_BUNDLE.md`](PRODUCER_CANDIDATE_BUNDLE.md):
  machine-verifiable SpecPM handoff layout, producer receipt profile, digest
  expectations, diagnostics, privacy caveats, and review boundary
- [`SPECPM_HANDOFF.md`](SPECPM_HANDOFF.md): practical operator workflow for
  generating, preflighting, rendering, and reviewing candidate bundles before
  public index acceptance
- [`SPECPM_SHARED_FIXTURE_POLICY.md`](SPECPM_SHARED_FIXTURE_POLICY.md): shared
  fixture policy for SpecPM contract examples and SpecHarvester generated
  bundle examples
- [`SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`](SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md):
  SpecHarvester-side evidence layout and role contract for a future optional
  SpecPM CI preflight gate
- [`SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`](SPECPM_REGISTRY_ACCEPTANCE_DECISION.md):
  external SpecPM registry acceptance decision record boundary for maintainer
  approval or override outside generated receipts
- [`SPECPM_PACKAGE_SET_ALIGNMENT.md`](SPECPM_PACKAGE_SET_ALIGNMENT.md):
  package-set contract mapping from SpecPM to SpecHarvester monorepo discovery
  implementation work
- [`WORKSPACE_INVENTORY.md`](WORKSPACE_INVENTORY.md): deterministic
  workspace/package discovery artifact for package-set producer review
- [`PACKAGE_SET_DRAFTING.md`](PACKAGE_SET_DRAFTING.md): package-set and scoped
  member candidate drafting from workspace inventory
- [`PACKAGE_RELATION_PROPOSALS.md`](PACKAGE_RELATION_PROPOSALS.md):
  producer-observed package relation proposals for package-set review
- [`PACKAGE_SET_VIEWER.md`](PACKAGE_SET_VIEWER.md): static package-set review
  viewer for aggregate and scoped member package previews
- [`XYFLOW_PACKAGE_SET_SMOKE.md`](XYFLOW_PACKAGE_SET_SMOKE.md): local
  end-to-end package-set smoke scenario for the `xyflow` reference path
- [`PACKAGE_SET_HANDOFF_PROPOSAL.md`](PACKAGE_SET_HANDOFF_PROPOSAL.md):
  package-set handoff proposal artifact for SpecPM review evidence
- [`PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md`](PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md):
  SpecPM-facing checklist for package member and relation review from
  package-set handoff proposals
- [`PACKAGE_SET_AI_DRAFT_PROPOSAL.md`](PACKAGE_SET_AI_DRAFT_PROPOSAL.md):
  proposal-only LLM package-set draft selection from deterministic workspace
  inventory
- [`PACKAGE_SET_AI_ENRICHMENT.md`](PACKAGE_SET_AI_ENRICHMENT.md):
  proposal-only local AI enrichment for package-set candidates
- [`AUTHOR_READY_CALIBRATION_MATRIX.md`](AUTHOR_READY_CALIBRATION_MATRIX.md):
  author-ready calibration matrix for real-repository edit counts and repeated
  generator gaps
- [`LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`](LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md):
  deterministic P30 corpus result before live LM Studio comparison
- [`LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`](LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md):
  live P30 LM Studio result and candidate-layer triage input
- [`LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`](LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md):
  P30 triage decisions and selected dry-run handoff candidates
- [`DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`](DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md):
  P31-T5 requirements for regenerating deferred package-set, warning-bearing,
  and identity-drift candidates before selected handoff
- [`REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md`](REFRESHED_CANDIDATE_LAYER_SELECTED_HANDOFF.md):
  P32-T5 refreshed selected/deferred handoff evidence for the limited corpus

## GitHub Process Surface

- Pull requests: [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md)
- Issue forms: [`.github/ISSUE_TEMPLATE`](../.github/ISSUE_TEMPLATE)
- CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Cross-repository proposal automation:
  [`.github/workflows/propose-to-specpm.yml`](../.github/workflows/propose-to-specpm.yml)

## Operator Checklist

- Start from a public repository checkout pinned to a revision.
- Collect bounded static evidence into `harvest.json`.
- Draft deterministic candidate SpecPM files.
- Validate the candidate with SpecPM.
- Review provenance, scope, and inferred metadata.
- Prepare PR-ready accepted manifest entries for reviewed candidates.
- Promote only reviewed candidates into accepted-source staging.
