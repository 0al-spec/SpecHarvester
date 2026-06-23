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
15. [`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md):
   language- and framework-agnostic contract for future repository plugins,
   registration metadata, applicability reports, and authority boundaries
16. [`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md):
   machine-readable `SpecHarvesterRepositoryPluginRegistry` fixture shape for
   declared producer-side plugin contracts
17. [`REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md):
   machine-readable `SpecHarvesterRepositoryPluginApplicabilityReport` fixture
   shape for selected, rejected, fallback, and blocked plugin decisions from
   static evidence
18. [`REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`](REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md):
   cross-ecosystem repository plugin applicability fixture matrix for single
   package, workspace, documentation-heavy, nested, and ambiguous repository
   shapes
19. [`REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`](REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md):
   real FastMCP plugin evidence comparison proving the applicability sidecar
   path on a pinned local checkout without plugin execution
20. [`STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`](STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md):
   Phase 39 helper, `repository-plugin-applicability-detect` CLI, and
   `autonomous-candidate-batch` opt-in integration for deriving repository
   plugin applicability reports from bounded static evidence instead of
   hand-authored sidecars
21. [`REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`](REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md):
   machine-readable
   `SpecHarvesterRepositoryPluginStaticEvidenceEnvelope` fixture for static
   evidence available to plugin applicability evaluation
22. [`REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md`](REPOSITORY_PLUGIN_MULTI_REPOSITORY_STATIC_EVALUATOR_VALIDATION.md):
   Phase 39 real multi-repository validation for FastMCP, FastAPI, and xyflow
   through the standalone static evaluator and batch auto-sidecar path
23. [`REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`](REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md):
   Phase 40 language- and framework-agnostic adapter contract for future
   manifests, preflight, execution policy, sandbox expectations, and
   review-only adapter output evidence
24. [`REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md):
   machine-readable `SpecHarvesterRepositoryPluginAdapterManifest` fixture
   shape for declared adapter ids, evidence inputs, outputs, execution mode,
   sandbox requirements, capability requests, and non-authority statements
25. [`REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`](REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md):
   machine-readable `SpecHarvesterRepositoryPluginAdapterPreflightReport`
   fixture shape for allowed, rejected, fallback, and blocked adapter
   preflight decisions before adapter code can run
26. [`REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`](REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md):
   disabled-by-default repository plugin adapter execution policy with
   `static_only`, future `trusted_local_tool`, path allowlist, operator
   opt-in, and deny-by-default capability rules
27. [`AUTONOMOUS_CANDIDATE_BATCH.md`](AUTONOMOUS_CANDIDATE_BATCH.md):
   P40-T5 opt-in repository plugin adapter evidence integration through
   `--repository-plugin-adapter-manifest` and
   `--repository-plugin-adapter-preflight`, preserving review-only producer
   authority and `adapterExecution: not_run`
28. [`REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`](REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md):
   P40-T6 static fixture matrix for adapter manifest/preflight expectations
   across single-package, workspace, documentation-heavy, nested-root, and
   ambiguous mixed repository layouts
29. [`REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`](REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md):
   P40-T7 real local adapter-contract validation for FastMCP, FastAPI,
   xyflow, and Gin pinned checkouts, proving adapter evidence remains
   producer-side and `adapterExecution: not_run`
30. [`TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md):
   P41-T1 readiness plan for future trusted local adapter run requests,
   preflight, disabled runner skeleton, review-only evidence handoff, and real
   local readiness validation without enabling adapter execution
31. [`TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md):
   P41-T2 machine-readable `SpecHarvesterTrustedLocalAdapterRunRequest`
   fixture for explicit operator opt-in, adapter manifest/preflight
   references, declared input artifacts, safe read allowlists, output policy,
   resource budgets, and non-authority statements
32. [`TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md):
   P41-T3 machine-readable
   `SpecHarvesterTrustedLocalAdapterRunPreflightReport` fixture for request
   identity, opt-in, digest, path, output, budget, policy, execution-boundary,
   and non-authority checks before any future runner
33. [`TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md):
   P41-T4 disabled `trusted-local-adapter-runner-skeleton` CLI and
   `SpecHarvesterTrustedLocalAdapterRunReport` no-execution report for
   validating request/preflight linkage without loading adapter code or
   running adapter processes
34. [`TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md`](TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md):
   P41-T6 real local readiness validation over FastMCP, FastAPI, xyflow, and
   Gin pinned checkouts, proving the trusted local adapter handoff remains
   explicit review evidence with `adapterExecution: not_run`
35. [`TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md`](TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md):
   P42-T1 sandbox plan for future trusted local adapter runtime execution,
   requiring explicit operator approval, adapter package identity, process
   isolation, sealed environment, network-deny-by-default policy, output
   digests, and review-only authority before any adapter process can run
36. [`TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_CONTRACT_FIXTURE.md):
   P42-T2 machine-readable
   `SpecHarvesterTrustedLocalAdapterSandboxContract` fixture for adapter
   package identity, sandbox policy identity, operator approval requirements,
   filesystem/environment/network/dependency policy, output verification,
   audit requirements, and no-execution/non-authority statements
37. [`TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_PREFLIGHT_REPORT_FIXTURE.md):
   P42-T3 machine-readable
   `SpecHarvesterTrustedLocalAdapterSandboxPreflightReport` fixture for
   sandbox contract identity/digest linkage, accepted/rejected/blocked checks,
   no-execution state, and review-only non-authority statements
38. [`TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md`](TRUSTED_LOCAL_ADAPTER_SANDBOX_RUNNER_VALIDATION.md):
   P42-T4 disabled no-execution
   `SpecHarvesterTrustedLocalAdapterSandboxRunnerValidationReport` for
   sandbox contract/preflight identity and digest linkage before any adapter
   code loading, process spawning, dependency installation, network access, AI,
   or registry authority
39. [`TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_FIXTURE.md):
   P42-T5 machine-readable
   `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRun` fixture for
   explicitly approved synthetic run binding, synthetic output candidates,
   output digests, audit records, and review-only non-authority statements
40. [`TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_VERIFIER.md`](TRUSTED_LOCAL_ADAPTER_SYNTHETIC_SANDBOX_RUN_VERIFIER.md):
   P42-T6
   `SpecHarvesterSyntheticTrustedLocalAdapterSandboxRunVerifierReport` CLI
   gate for linked artifact digests, approval binding, output byte
   sizes/digests, audit references, and no-real-execution boundaries
41. [`TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_SANDBOX_RUN_READINESS.md`](TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_SANDBOX_RUN_READINESS.md):
   P42-T7
   `SpecHarvesterRealLocalTrustedAdapterSandboxRunReadinessReport` CLI gate
   for future real local sandbox run review prerequisites while preserving no
   adapter execution
42. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_FIXTURE.md):
   P42-T8
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequest` fixture for
   future real local sandbox run review requests, verifier/readiness evidence
   references, scoped approval requirements, runtime/output/audit policy, and
   request-only non-authority statements
43. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUN_REQUEST_PREFLIGHT_FIXTURE.md):
   P42-T9
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunRequestPreflightReport`
   fixture for request identity, verifier/readiness evidence requirements,
   scoped approval, runtime/output/audit policy, rejected unsafe shapes, and
   review-only non-authority statements
44. [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_SKELETON.md):
   P42-T10
   `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRunnerReport`
   fixture for P42-T8/P42-T9 request/preflight linkage validation while
   preserving disabled execution, no adapter code loading, no process spawning,
   no network access, no registry authority, and no adapter output acceptance
45. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNNER_EVIDENCE_HANDOFF.md):
   P42-T11
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRunnerEvidenceHandoff`
   fixture for packaging P42-T8/P42-T9/P42-T10 request, preflight, and
   disabled-runner evidence as portable review-only handoff material while
   preserving no adapter execution, no registry authority, and no adapter output
   truth
46. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_GATE.md):
   P42-T12
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewGate`
   fixture for validating the P42-T11 handoff, recording runtime implementation
   prerequisites, and keeping real adapter execution blocked until a separate
   operator-approved runtime task exists
47. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_OPERATOR_APPROVAL_BINDING.md):
   P42-T13
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxOperatorApprovalBinding`
   fixture for binding one future local adapter run approval scope to P42-T12
   runtime prerequisites while still preserving no execution permission, no
   registry authority, and no adapter output truth
48. [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_SKELETON.md):
   P42-T14
   `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationReport`
   fixture for validating the P42-T13 approval binding through a disabled
   invocation skeleton while preserving no runtime invocation, no approval
   consumption, no registry authority, and no adapter output truth
49. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_EVIDENCE_HANDOFF.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_INVOCATION_EVIDENCE_HANDOFF.md):
   P42-T15
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeInvocationEvidenceHandoff`
   fixture for packaging P42-T13 approval binding and P42-T14 disabled
   invocation evidence as portable review material while preserving no
   execution permission, no approval consumption, and no registry authority
50. [`TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_PACKET.md`](TRUSTED_LOCAL_ADAPTER_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_REVIEW_PACKET.md):
   P42-T16
   `SpecHarvesterExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationReviewPacket`
   fixture for packaging P42-T15 runtime invocation evidence handoff and
   implementation prerequisites as review material while preserving no runtime
   implementation, no runtime invocation, no approval consumption, and no
   registry authority
51. [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_SKELETON.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_SKELETON.md):
   P42-T17
   `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationSkeleton`
   fixture for recording the disabled future runtime implementation surface
   from the P42-T16 review packet while preserving no adapter code loading, no
   adapter import, no process spawning, no runtime invocation, no approval
   consumption, and no registry authority
52. [`TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_SKELETON_VERIFIER.md`](TRUSTED_LOCAL_ADAPTER_DISABLED_EXPLICIT_REAL_LOCAL_SANDBOX_RUNTIME_IMPLEMENTATION_SKELETON_VERIFIER.md):
   P42-T18
   `SpecHarvesterDisabledExplicitRealLocalTrustedAdapterSandboxRuntimeImplementationSkeletonVerifierReport`
   fixture for verifying the P42-T17 disabled runtime implementation skeleton
   identity, digest, disabled surface, check counts, execution boundary, and
   non-authority statements while preserving no runtime invocation, no approval
   consumption, and no registry authority
53. [`OPERATIONAL_MVP_VALIDATION_PLAN.md`](OPERATIONAL_MVP_VALIDATION_PLAN.md):
   Phase 43 operational validation plan for proving SpecHarvester on a bounded
   pinned multi-ecosystem corpus before broader autonomous scraping or real
   adapter execution
54. [`OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md):
   machine-readable
   `SpecHarvesterOperationalMVPValidationPlan` fixture for selected corpus
   requirements, pinned local checkout policy, run modes, quality dimensions,
   stop policy, and non-authority boundaries
55. [`OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`](OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md):
   machine-readable
   `SpecHarvesterOperationalMVPValidationReport` fixture for per-repository
   draft status, static-only result, AI-enabled result, author-ready verdict,
   evidence precision notes, stop-policy outcome, and SpecPM handoff readiness
56. [`OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`](OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md):
   P43-T4 real local static-only baseline over xyflow, FastAPI, and Gin pinned
   checkouts, recording passed preflight, author-ready preview candidates,
   quality dimensions, handoff readiness, and non-authority boundaries
57. [`OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`](OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md):
   P43-T5 AI-enabled comparison gate over the same pinned corpus, recording
   local provider unavailability, unchanged static-only handoff readiness,
   proposal-only warnings, and non-authority boundaries
58. [`OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md`](OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md):
   P43-T6 author-facing handoff summaries over the operational MVP corpus,
   showing what is valid, reviewable, needs manual correction, and must not be
   promoted
59. [`OPERATIONAL_MVP_EXIT_REPORT.md`](OPERATIONAL_MVP_EXIT_REPORT.md):
   P43-T7 exit report selecting `needs_quality_hardening` before broader
   autonomous popular-library scraping while preserving the no-authority
   boundary
60. [`OPERATIONAL_MVP_WARNING_TRIAGE.md`](OPERATIONAL_MVP_WARNING_TRIAGE.md):
   P44-T1 warning triage for the P43-T5 `package_set_id_missing` AI draft
   diagnostics
61. [`OPERATIONAL_MVP_AI_PROPOSAL_QUALITY_REVIEW.md`](OPERATIONAL_MVP_AI_PROPOSAL_QUALITY_REVIEW.md):
   P44-T2 proposal-only AI enrichment quality review for xyflow, FastAPI, and
   Gin
62. [`OPERATIONAL_MVP_XYFLOW_CAVEAT_RESOLUTION.md`](OPERATIONAL_MVP_XYFLOW_CAVEAT_RESOLUTION.md):
   P44-T3 xyflow partial interface and fork-origin caveat resolution
63. [`OPERATIONAL_MVP_QUALITY_HARDENED_RERUN.md`](OPERATIONAL_MVP_QUALITY_HARDENED_RERUN.md):
   P44-T4 static-only and AI-enabled quality-hardened rerun comparison
64. [`OPERATIONAL_MVP_POST_HARDENING_READINESS_DECISION.md`](OPERATIONAL_MVP_POST_HARDENING_READINESS_DECISION.md):
   P44-T5 post-hardening readiness decision selecting another quality pass
65. [`OPERATIONAL_MVP_AI_DRAFT_SHAPE_RERUN.md`](OPERATIONAL_MVP_AI_DRAFT_SHAPE_RERUN.md):
   P45-T3 post-fix bounded corpus rerun after AI draft shape hardening
66. [`OPERATIONAL_MVP_POST_FIX_READINESS_DECISION.md`](OPERATIONAL_MVP_POST_FIX_READINESS_DECISION.md):
   P45-T4 readiness decision keeping bounded popular-library scraping
   unapproved until remaining AI draft quality signals are resolved or accepted
   as non-blocking
67. [`OPERATIONAL_MVP_TARGETED_AI_DRAFT_POLICY_RERUN.md`](OPERATIONAL_MVP_TARGETED_AI_DRAFT_POLICY_RERUN.md):
   P45-T7 targeted rerun after P45-T5/P45-T6 showing AI draft blockers
   resolved while preserving proposal-only boundaries for P45-T8
68. [`OPERATIONAL_MVP_TARGETED_HARDENING_READINESS_DECISION.md`](OPERATIONAL_MVP_TARGETED_HARDENING_READINESS_DECISION.md):
   P45-T8 readiness decision selecting Phase 46 bounded popular-library pilot
   start while carrying Gin `model_evidence_path_unsupported` into triage
69. [`BOUNDED_POPULAR_LIBRARY_PILOT_MANIFEST.md`](BOUNDED_POPULAR_LIBRARY_PILOT_MANIFEST.md):
   P46-T1 manifest for the first post-hardening bounded popular-library pilot
   with pinned local checkouts and static-only-first gates
70. [`BOUNDED_POPULAR_LIBRARY_PILOT_STATIC_ONLY_RUN.md`](BOUNDED_POPULAR_LIBRARY_PILOT_STATIC_ONLY_RUN.md):
   P46-T2 real local static-only pilot result over the bounded manifest,
   including candidate/relation counts and no-AI/no-adapter boundaries
71. [`BOUNDED_POPULAR_LIBRARY_PILOT_AI_ENABLED_RUN.md`](BOUNDED_POPULAR_LIBRARY_PILOT_AI_ENABLED_RUN.md):
   P46-T3 real local LM Studio AI-enabled pilot result, proposal-only
   warnings/blockers, and comparison to the P46-T2 static-only baseline
72. [`BOUNDED_POPULAR_LIBRARY_PILOT_OUTPUT_TRIAGE.md`](BOUNDED_POPULAR_LIBRARY_PILOT_OUTPUT_TRIAGE.md):
   P46-T4 triage classifications for reviewable static output, noisy AI
   sidecars, unsupported evidence, evidence gaps, and do-not-promote outputs
73. [`BOUNDED_POPULAR_LIBRARY_PILOT_AUTHOR_HANDOFF.md`](BOUNDED_POPULAR_LIBRARY_PILOT_AUTHOR_HANDOFF.md):
   P46-T5 author-facing handoff summaries separating reviewable static
   evidence from noisy, unsupported, evidence-gap, and do-not-promote sidecars
74. [`BOUNDED_POPULAR_LIBRARY_PILOT_EXIT_DECISION.md`](BOUNDED_POPULAR_LIBRARY_PILOT_EXIT_DECISION.md):
   P46-T6 exit decision selecting a targeted quality pass before any larger
   curated corpus expansion
75. [`TARGETED_PILOT_QUALITY_FOLLOW_UP_PLAN.md`](TARGETED_PILOT_QUALITY_FOLLOW_UP_PLAN.md):
   P47-T1 targeted quality follow-up plan for Gin/docc2context AI draft repair,
   xyflow caveat disposition, and the bounded rerun gate
76. [`TARGETED_PILOT_QUALITY_PASS.md`](TARGETED_PILOT_QUALITY_PASS.md):
   P47-T2 targeted disposition pass that excludes current bad sidecars from
   the bounded rerun gate while keeping larger corpus approval blocked
77. [`TARGETED_PILOT_BOUNDED_RERUN_GATE.md`](TARGETED_PILOT_BOUNDED_RERUN_GATE.md):
   P47-T3 bounded rerun gate showing static pass, AI failure, and continued
   larger corpus block before P47-T4
78. [`TARGETED_PILOT_QUALITY_FOLLOW_UP_EXIT_DECISION.md`](TARGETED_PILOT_QUALITY_FOLLOW_UP_EXIT_DECISION.md):
   P47-T4 exit decision selecting another targeted AI draft blocker pass
   before larger curated corpus planning
79. [`AI_DRAFT_BLOCKER_FOLLOW_UP_PLAN.md`](AI_DRAFT_BLOCKER_FOLLOW_UP_PLAN.md):
   P48-T1 plan for Gin and NavigationSplitView AI draft blocker follow-up
   before another bounded rerun gate
80. [`AI_DRAFT_BLOCKER_FOLLOW_UP_PASS.md`](AI_DRAFT_BLOCKER_FOLLOW_UP_PASS.md):
   P48-T2 evidence-only follow-up pass that disposes Gin and
   NavigationSplitView AI draft blockers for the P48-T3 bounded rerun gate
81. [`AI_DRAFT_BLOCKER_BOUNDED_RERUN_GATE.md`](AI_DRAFT_BLOCKER_BOUNDED_RERUN_GATE.md):
   P48-T3 same-scope bounded rerun gate showing static pass, AI failure on
   `docc2context.aiDraft`, and continued larger corpus block before P48-T4
17. [`FASTAPI_PARSER_PROFILE_RERUN.md`](FASTAPI_PARSER_PROFILE_RERUN.md):
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
- [`REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`](REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md):
  repository plugin subsystem contract for plugin identity, roles,
  registration metadata, static evidence, applicability checks, diagnostics,
  and authority boundaries
- [`REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`](REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md):
  machine-readable registry fixture for declared producer-side plugin
  contracts, safety constraints, static evidence kinds, and output artifacts
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
