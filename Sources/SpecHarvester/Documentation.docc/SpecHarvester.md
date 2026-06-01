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
- `docs/HOW_IT_WORKS.md`
- `docs/ARCHITECTURE.md`
- `docs/TRUST_BOUNDARY.md`
- `docs/ANALYZER_SANDBOX_REQUIREMENTS.md`
- `docs/TRUSTED_CLASSIFIER_EVALUATION.md`
- `docs/LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md`
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
- `docs/STATIC_SPEC_RENDERER.md`
- `docs/PRODUCER_CANDIDATE_BUNDLE.md`
- `docs/SPECPM_HANDOFF.md`
- `docs/ROADMAP.md`

This DocC site is a navigable documentation mirror built from those contracts.

## Boundary Statements

Generated package content is candidate metadata, not upstream-endorsed truth.

Package content can describe desired outputs. Package content cannot command
the host.

## Topics

### Start Here

- <doc:GettingStarted>
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
- <doc:StaticSpecRenderer>
- <doc:ProducerCandidateBundle>
- <doc:SpecPMHandoff>
- <doc:ProposalAutomation>

### Architecture

- <doc:HarvesterArchitecture>
- <doc:TrustBoundary>
- <doc:AnalyzerSandboxRequirements>
- <doc:TrustedClassifierEvaluation>
- <doc:LanguageNeutralSemanticExtraction>
- <doc:TreeSitterEvaluation>
- <doc:Roadmap>
