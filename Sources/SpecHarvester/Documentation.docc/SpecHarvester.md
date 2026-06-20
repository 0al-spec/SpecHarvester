# ``SpecHarvester``

AI-assisted harvesting pipeline for turning public repository metadata into
reviewable SpecPM candidate packages.

## Overview

SpecHarvester is a producer pipeline, not a package substrate. It collects
bounded evidence from public repository checkouts, drafts deterministic SpecPM
candidate files, validates them with SpecPM, and prepares them for controlled
promotion.

The current bootstrap supports:

- safe evidence collection from allowlisted static files;
- deterministic `harvest.json` snapshots with provenance and file digests;
- conservative draft generation for `specpm.yaml` and `specs/*.spec.yaml`;
- SpecPM validation before promotion;
- controlled promotion into accepted-source staging;
- trusted proposal automation that can prepare a pull request against
  `0al-spec/SpecPM`.

SpecHarvester does not execute harvested repository code, install harvested
dependencies, or publish generated candidates directly into a public registry.

## Source Documents

The canonical source files remain in the repository:

- `README.md`
- `docs/README.md`
- `docs/CAPABILITIES.md`
- `docs/HOW_IT_WORKS.md`
- `docs/ARCHITECTURE.md`
- `docs/TRUST_BOUNDARY.md`
- `docs/ANALYZER_SANDBOX_REQUIREMENTS.md`
- `docs/TRUSTED_CLASSIFIER_EVALUATION.md`
- `docs/CODEGRAPH_SOURCE_GRAPH_ADAPTER.md`
- `docs/CODEGRAPH_COMPATIBILITY_GUARD.md`
- `docs/LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`
- `docs/REPOSITORY_PARSING_PLUGIN_CONTRACT.md`
- `docs/REPOSITORY_PROFILE_SELECTION_CONTRACT.md`
- `docs/REPOSITORY_PROFILE_DISCOVERY_HINTS.md`
- `docs/REPOSITORY_PROFILE_CROSS_ECOSYSTEM_FIXTURES.md`
- `docs/REPOSITORY_PROFILE_REAL_RUN_FASTMCP.md`
- `docs/REPOSITORY_PLUGIN_SUBSYSTEM_CONTRACT.md`
- `docs/REPOSITORY_PLUGIN_REGISTRY_FIXTURE.md`
- `docs/REPOSITORY_PLUGIN_APPLICABILITY_REPORT_FIXTURE.md`
- `docs/REPOSITORY_PLUGIN_CROSS_ECOSYSTEM_FIXTURES.md`
- `docs/REPOSITORY_PLUGIN_REAL_RUN_FASTMCP.md`
- `docs/STATIC_REPOSITORY_PLUGIN_APPLICABILITY_EVALUATOR.md`
- `docs/REPOSITORY_PLUGIN_STATIC_EVIDENCE_ENVELOPE_FIXTURE.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_CONTRACT.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_MANIFEST_FIXTURE.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_PREFLIGHT_REPORT_FIXTURE.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_EXECUTION_POLICY.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_CROSS_ECOSYSTEM_FIXTURE_MATRIX.md`
- `docs/REPOSITORY_PLUGIN_ADAPTER_REAL_LOCAL_VALIDATION.md`
- `docs/TRUSTED_LOCAL_ADAPTER_RUNTIME_READINESS.md`
- `docs/TRUSTED_LOCAL_ADAPTER_RUN_REQUEST_FIXTURE.md`
- `docs/TRUSTED_LOCAL_ADAPTER_RUN_PREFLIGHT_REPORT_FIXTURE.md`
- `docs/TRUSTED_LOCAL_ADAPTER_RUNNER_SKELETON.md`
- `docs/TRUSTED_LOCAL_ADAPTER_REAL_LOCAL_READINESS_VALIDATION.md`
- `docs/TRUSTED_LOCAL_ADAPTER_RUNTIME_SANDBOX_PLAN.md`
- `docs/OPERATIONAL_MVP_VALIDATION_PLAN.md`
- `docs/OPERATIONAL_MVP_VALIDATION_PLAN_FIXTURE.md`
- `docs/OPERATIONAL_MVP_VALIDATION_REPORT_FIXTURE.md`
- `docs/OPERATIONAL_MVP_STATIC_ONLY_BASELINE.md`
- `docs/OPERATIONAL_MVP_AI_ENABLED_COMPARISON.md`
- `docs/OPERATIONAL_MVP_AUTHOR_HANDOFF_SUMMARIES.md`
- `docs/AUTONOMOUS_CANDIDATE_BATCH.md`
- `docs/REPOSITORY_SOURCE_MANIFESTS.md`
- `docs/BATCH_COLLECTION.md`
- `docs/BATCH_VALIDATION_REPORTS.md`
- `docs/SPECPM_PROPOSAL_AUTOMATION.md`
- `docs/ACCEPTED_MANIFEST_ENTRIES.md`
- `docs/ACCEPTED_PACKAGE_UPDATE_LIFECYCLE.md`
- `docs/ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md`
- `docs/ACCEPTED_CANDIDATE_DIFF_REPORTS.md`
- `docs/GOVERNANCE_REPORTS.md`
- `docs/NAMESPACE_UPSTREAM_REPORTS.md`
- `docs/LICENSE_PROVENANCE_RISK_REPORTS.md`
- `docs/CODE_DUPLICATION_REPORTS.md`
- `docs/ARCHITECTURE_LINT_GUARDRAILS.md`
- `docs/PROCEDURAL_STYLE_REPORT.md`
- `docs/EO_REFACTORING_STRATEGY.md`
- `docs/LOCAL_SMOKE_FIXTURES.md`
- `docs/SPECNODE_INTEGRATION_CONTRACT.md`
- `docs/SPECNODE_REFINE_PREVIEW_CONTRACT.md`
- `docs/SPECNODE_REFINEMENT_PROMPT_CONTRACT.md`
- `docs/SPECNODE_SEMANTIC_REVIEW_CONTRACT.md`
- `docs/SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md`
- `docs/SPECNODE_PROVIDER_ADAPTER_CONTRACT.md`
- `docs/SPECNODE_PATCH_PROPOSAL_CONTRACT.md`
- `docs/SPECNODE_PROVIDER_SMOKE_COVERAGE.md`
- `docs/REAL_REPOSITORY_REFINEMENT_VALIDATION.md`
- `docs/REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md`
- `docs/REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md`
- `docs/AUTHOR_READY_DRAFT_QUALITY_BAR.md`
- `docs/AUTHOR_READY_DRAFT_QUALITY_REPORT.md`
- `docs/AUTHOR_READY_CALIBRATION_MATRIX.md`
- `docs/STATIC_SPEC_RENDERER.md`
- `docs/PRODUCER_CANDIDATE_BUNDLE.md`
- `docs/SPECPM_HANDOFF.md`
- `docs/SPECPM_SHARED_FIXTURE_POLICY.md`
- `docs/SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md`
- `docs/SPECPM_REGISTRY_ACCEPTANCE_DECISION.md`
- `docs/SPECPM_PACKAGE_SET_ALIGNMENT.md`
- `docs/WORKSPACE_INVENTORY.md`
- `docs/PACKAGE_SET_DRAFTING.md`
- `docs/PACKAGE_RELATION_PROPOSALS.md`
- `docs/BUNDLE_SET_PREFLIGHT.md`
- `docs/PACKAGE_SET_VIEWER.md`
- `docs/XYFLOW_PACKAGE_SET_SMOKE.md`
- `docs/PACKAGE_SET_HANDOFF_PROPOSAL.md`
- `docs/PACKAGE_SET_PROPOSAL_INTAKE_CHECKLIST.md`
- `docs/FRESH_CANDIDATE_REFRESH_RUN.md`
- `docs/BASELINE_SUBMISSION_HANDOFF.md`
- `docs/PACKAGE_SET_AI_DRAFT_PROPOSAL.md`
- `docs/PACKAGE_SET_AI_ENRICHMENT.md`
- `docs/AI_ENRICHMENT_CANDIDATE_PATCH.md`
- `docs/AUTONOMOUS_CANDIDATE_INTAKE_POLICY.md`
- `docs/AUTONOMOUS_CANDIDATE_TECH_DEBT_PLAN.md`
- `docs/BOUNDED_CORPUS_EXPANSION_PLAN.md`
- `docs/NEXT_CORPUS_SOURCE_MANIFEST.md`
- `docs/NEXT_CORPUS_DETERMINISTIC_DRY_RUN.md`
- `docs/NEXT_CORPUS_LIVE_LOCAL_MODEL_BATCH.md`
- `docs/NEXT_CORPUS_CANDIDATE_LAYER_TRIAGE.md`
- `docs/NEXT_CORPUS_SPECPM_PREFLIGHT_INTAKE_DECISION.md`
- `docs/NEXT_CORPUS_DURABLE_SELECTED_HANDOFF.md`
- `docs/NEXT_CORPUS_INTAKE_READINESS_DECISION.md`
- `docs/CORPUS_SELECTION_POLICY.md`
- `docs/SPECHARVESTER_CORPUS_PLAN.md`
- `docs/CANDIDATE_SOURCE_CLASSIFIER_PLAN.md`
- `docs/MULTI_ECOSYSTEM_SEED_CORPUS_PLAN.md`
- `docs/EXPLAINABLE_CORPUS_SELECTION_REPORT.md`
- `docs/SELECTED_CORPUS_DRY_RUN_READINESS.md`
- `docs/XYFLOW_PACKAGE_SET_IDENTITY_REGENERATION_DRY_RUN.md`
- `docs/SINGLE_PACKAGE_DEFERRED_CANDIDATE_REGENERATION_DRY_RUN.md`
- `docs/AUTONOMOUS_CANDIDATE_CORPUS_BASELINE.md`
- `docs/SINGLE_PACKAGE_CANDIDATE_FALLBACK.md`
- `docs/LIMITED_POPULAR_LIBRARY_CORPUS_PLAN.md`
- `docs/LIMITED_POPULAR_LIBRARY_DETERMINISTIC_BATCH.md`
- `docs/LIMITED_POPULAR_LIBRARY_LIVE_LM_STUDIO_BATCH.md`
- `docs/LIMITED_POPULAR_LIBRARY_CANDIDATE_LAYER_TRIAGE.md`
- `docs/LIMITED_POPULAR_LIBRARY_SELECTED_HANDOFF_DRY_RUN.md`
- `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL.md`
- `docs/SELECTED_CANDIDATE_HANDOFF_PROPOSAL_P31_T3.md`
- `docs/SELECTED_CANDIDATE_HANDOFF_PREFLIGHT_EXPECTATIONS.md`
- `docs/DEFERRED_SELECTED_CANDIDATE_REGENERATION_REQUIREMENTS.md`
- `docs/ROADMAP.md`

This DocC site is a navigable documentation mirror built from those contracts.

## Boundary Statements

Generated package content is candidate metadata, not upstream-endorsed truth.

Package content can describe desired outputs. Package content cannot command
the host.

## Topics

### Start Here

- <doc:GettingStarted>
- <doc:Capabilities>
- <doc:Workflow>
- <doc:RepositorySourceManifests>
- <doc:BatchCollection>
- <doc:BatchValidationReports>
- <doc:AcceptedManifestEntries>
- <doc:AcceptedPackageUpdateLifecycle>
- <doc:AcceptedPackageUpdateProposals>
- <doc:AcceptedCandidateDiffReports>
- <doc:AcceptedCandidateImpactClassificationReports>
- <doc:GovernanceReports>
- <doc:NamespaceUpstreamReports>
- <doc:LicenseProvenanceRiskReports>
- <doc:CodeDuplicationReports>
- <doc:CodeGraphSourceGraphAdapter>
- <doc:CodeGraphCompatibilityGuard>
- <doc:RepositoryParsingPluginContract>
- <doc:RepositoryProfileSelectionContract>
- <doc:RepositoryProfileDiscoveryHints>
- <doc:RepositoryProfileCrossEcosystemFixtures>
- <doc:RepositoryProfileRealRunFastMCP>
- <doc:RepositoryPluginSubsystemContract>
- <doc:RepositoryPluginRegistryFixture>
- <doc:RepositoryPluginApplicabilityReportFixture>
- <doc:RepositoryPluginCrossEcosystemFixtures>
- <doc:RepositoryPluginRealRunFastMCP>
- <doc:StaticRepositoryPluginApplicabilityEvaluator>
- <doc:RepositoryPluginStaticEvidenceEnvelopeFixture>
- <doc:RepositoryPluginMultiRepositoryStaticEvaluatorValidation>
- <doc:RepositoryPluginAdapterContract>
- <doc:RepositoryPluginAdapterManifestFixture>
- <doc:RepositoryPluginAdapterPreflightReportFixture>
- <doc:RepositoryPluginAdapterExecutionPolicy>
- <doc:RepositoryPluginAdapterCrossEcosystemFixtureMatrix>
- <doc:RepositoryPluginAdapterRealLocalValidation>
- <doc:TrustedLocalAdapterRuntimeReadiness>
- <doc:TrustedLocalAdapterRunRequestFixture>
- <doc:TrustedLocalAdapterRunPreflightReportFixture>
- <doc:TrustedLocalAdapterRunnerSkeleton>
- <doc:TrustedLocalAdapterRuntimeSandboxPlan>
- <doc:TrustedLocalAdapterSandboxContractFixture>
- <doc:TrustedLocalAdapterSandboxPreflightReportFixture>
- <doc:TrustedLocalAdapterSandboxRunnerValidation>
- <doc:TrustedLocalAdapterSyntheticSandboxRunFixture>
- <doc:TrustedLocalAdapterSyntheticSandboxRunVerifier>
- <doc:TrustedLocalAdapterRealLocalSandboxRunReadiness>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestFixture>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunRequestPreflightFixture>
- <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRunnerSkeleton>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRunnerEvidenceHandoff>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewGate>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxOperatorApprovalBinding>
- <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeInvocationSkeleton>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeInvocationEvidenceHandoff>
- <doc:TrustedLocalAdapterExplicitRealLocalSandboxRuntimeImplementationReviewPacket>
- <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeImplementationSkeleton>
- <doc:TrustedLocalAdapterDisabledExplicitRealLocalSandboxRuntimeImplementationSkeletonVerifier>
- <doc:OperationalMVPValidationPlan>
- <doc:OperationalMVPValidationPlanFixture>
- <doc:OperationalMVPValidationReportFixture>
- <doc:OperationalMVPStaticOnlyBaseline>
- <doc:OperationalMVPAIEnabledComparison>
- <doc:OperationalMVPAuthorHandoffSummaries>
- <doc:AutonomousCandidateBatch>
- <doc:FastAPIParserProfileRerun>
- <doc:ArchitectureLintGuardrails>
- <doc:ProceduralStyleReport>
- <doc:EORefactoringStrategy>
- <doc:LocalSmokeFixtures>
- <doc:SpecNodeIntegrationContract>
- <doc:SpecNodeRefinePreviewContract>
- <doc:SpecNodeRefinementPromptContract>
- <doc:SpecNodeSemanticReviewContract>
- <doc:SpecNodeRefinementRetryOrchestration>
- <doc:SpecNodeProviderAdapterContract>
- <doc:SpecNodePatchProposalContract>
- <doc:SpecNodeProviderSmokeCoverage>
- <doc:RealRepositoryRefinementValidation>
- <doc:RealRepositoryQualityReport>
- <doc:RealRepositoryRefinementValidationRunner>
- <doc:RealRepositoryLocalValidationMatrix>
- <doc:AuthorReadyDraftQualityBar>
- <doc:AuthorReadyDraftQualityReport>
- <doc:AuthorReadyCalibrationMatrix>
- <doc:StaticSpecRenderer>
- <doc:ProducerCandidateBundle>
- <doc:SpecPMHandoff>
- <doc:SpecPMSharedFixturePolicy>
- <doc:SpecPMCiPreflightGateSupport>
- <doc:SpecPMRegistryAcceptanceDecision>
- <doc:SpecPMPackageSetAlignment>
- <doc:WorkspaceInventory>
- <doc:PackageSetDrafting>
- <doc:PackageRelationProposals>
- <doc:BundleSetPreflight>
- <doc:PackageSetViewer>
- <doc:XyflowPackageSetSmoke>
- <doc:PackageSetHandoffProposal>
- <doc:PackageSetProposalIntakeChecklist>
- <doc:FreshCandidateRefreshRun>
- <doc:BaselineSubmissionHandoff>
- <doc:PackageSetAIDraftProposal>
- <doc:PackageSetAIEnrichment>
- <doc:AIEnrichmentCandidatePatch>
- <doc:AutonomousCandidateBatch>
- <doc:AutonomousCandidateIntakePolicy>
- <doc:AutonomousCandidateTechDebtPlan>
- <doc:BoundedCorpusExpansionPlan>
- <doc:NextCorpusSourceManifest>
- <doc:NextCorpusDeterministicDryRun>
- <doc:NextCorpusLiveLocalModelBatch>
- <doc:NextCorpusCandidateLayerTriage>
- <doc:NextCorpusSpecPMPreflightIntakeDecision>
- <doc:NextCorpusDurableSelectedHandoff>
- <doc:NextCorpusIntakeReadinessDecision>
- <doc:CorpusSelectionPolicy>
- <doc:SpecHarvesterCorpusPlan>
- <doc:CandidateSourceClassifierPlan>
- <doc:MultiEcosystemSeedCorpusPlan>
- <doc:ExplainableCorpusSelectionReport>
- <doc:SelectedCorpusDryRunReadiness>
- <doc:DeferredCandidateRegenerationRunbook>
- <doc:XyflowPackageSetIdentityRegenerationDryRun>
- <doc:SinglePackageDeferredCandidateRegenerationDryRun>
- <doc:RefreshedCandidateLayerSelectedHandoff>
- <doc:LimitedCorpusIntakeReadinessDecision>
- <doc:AutonomousCandidateCorpusBaseline>
- <doc:AutonomousCandidateCorpusQualityGate>
- <doc:LimitedPopularLibraryCorpusPlan>
- <doc:LimitedPopularLibraryDeterministicBatch>
- <doc:LimitedPopularLibraryLiveLMStudioBatch>
- <doc:LimitedPopularLibraryCandidateLayerTriage>
- <doc:LimitedPopularLibrarySelectedHandoffDryRun>
- <doc:SelectedCandidateHandoffProposal>
- <doc:SelectedCandidateHandoffProposalP31T3>
- <doc:SelectedCandidateHandoffPreflightExpectations>
- <doc:DeferredSelectedCandidateRegenerationRequirements>
- <doc:SinglePackageCandidateFallback>
- <doc:ProposalAutomation>

### Architecture

- <doc:HarvesterArchitecture>
- <doc:TrustBoundary>
- <doc:AnalyzerSandboxRequirements>
- <doc:TrustedClassifierEvaluation>
- <doc:LanguageNeutralSemanticExtraction>
- <doc:RepositoryParsingPluginContract>
- <doc:FastAPIParserProfileRerun>
- <doc:TreeSitterEvaluation>
- <doc:Roadmap>
