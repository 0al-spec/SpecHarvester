from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_analyzer_sandbox_requirements_docs_cover_required_controls() -> None:
    github_doc = ROOT / "docs" / "ANALYZER_SANDBOX_REQUIREMENTS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AnalyzerSandboxRequirements.md"
    )

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "execution: none",
            "metadata_tool_only",
            "build_tool_sandboxed",
            "no network",
            "no package scripts",
            "no harvested dependency installation",
            "no secret access",
            "pinned analyzer",
            "bounded filesystem",
            "deterministic output",
            "source digest evidence",
            "diagnostics",
            "audit log",
            "collect-local",
            "untrusted evidence",
        ):
            assert required in text


def test_docc_topics_link_analyzer_sandbox_requirements() -> None:
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    trust_boundary = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"

    assert "<doc:AnalyzerSandboxRequirements>" in root_page.read_text(encoding="utf-8")
    assert "<doc:AnalyzerSandboxRequirements>" in trust_boundary.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_trusted_classifier_evaluation() -> None:
    github_doc = ROOT / "docs" / "TRUSTED_CLASSIFIER_EVALUATION.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustedClassifierEvaluation.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    trust_boundary = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "classifierPolicy",
            "ProjectProfile",
            "manifest-first",
            "advisory untrusted metadata",
            "go-enry",
            "Syft",
            "ScanCode",
            "Universal Ctags",
            "Tree-sitter",
            "pinned tool version",
            "no network",
            "no package scripts",
            "no harvested dependency installation",
            "source digest evidence",
        ):
            assert required in text

    assert "TRUSTED_CLASSIFIER_EVALUATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:TrustedClassifierEvaluation>" in root_page.read_text(encoding="utf-8")
    assert "<doc:TrustedClassifierEvaluation>" in trust_boundary.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_project_profile_analyzer_orchestration() -> None:
    github_doc = ROOT / "docs" / "BATCH_COLLECTION.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BatchCollection.md"
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "--emit-interface-indexes",
            "ProjectProfile.analyzerPlan",
            "public-interface-index.json",
            "spec_harvester.python_public_api",
            "spec_harvester.js_ts_public_api",
            "spec_harvester.go_public_api",
            "manifest_only",
            "advisory",
            "kind: public_interface_index",
            "artifactKind: SpecHarvesterPublicInterfaceIndex",
            "SpecPM `0.2.0+`",
        ):
            assert required in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "--emit-interface-indexes",
            "--analyzer-cache-dir",
            "PublicInterfaceIndex",
            "does not install dependencies",
            "run package scripts",
            "execute checkout files",
            "contact networks",
            "kind: public_interface_index",
            "artifactKind: SpecHarvesterPublicInterfaceIndex",
            "SpecPM `0.2.0+`",
        ):
            assert required in text


def test_docc_and_github_docs_cover_language_neutral_semantic_extraction() -> None:
    github_doc = ROOT / "docs" / "LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LanguageNeutralSemanticExtraction.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "semanticHints",
            "language-neutral",
            "README",
            "API contract",
            "OpenAPI",
            "schema validation",
            "workflow automation",
            "developer tooling",
            "web framework",
            "documentation knowledge base",
            "semantic_intent_static_evidence",
            "declared SpecPM support targets",
            "provides.capabilities.<capability_id>",
            "provides.capabilities.intentIds",
            "intent.web.framework_surface",
            "intent.api.contract_surface",
            "intent.metadata.schema_validation",
            "manifest-poor",
            "raw documentation bodies",
        ):
            assert required in text

    assert "LANGUAGE_NEUTRAL_SEMANTIC_EXTRACTION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:LanguageNeutralSemanticExtraction>" in root_page.read_text(encoding="utf-8")
    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "semanticHints" in text
        assert "intent.web.framework_surface" in text
        assert "intent.api.contract_surface" in text
        assert "provides.capabilities.<capability_id>" in text
        assert "provides.capabilities.intentIds" in text
        assert "raw documentation" in text


def test_docc_and_github_docs_cover_specnode_integration_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    trust_doc = ROOT / "docs" / "TRUST_BOUNDARY.md"
    trust_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "TrustBoundary.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecNodeRefinementJob",
            "candidatePatchProposal",
            "usageReceipt",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "modelNetworkAccess: provider_only",
            "allowedTools",
            "candidateMutation: proposal_only",
            "rawSourceAccess: none",
            "secretAccess: none",
            "proposal_only",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "public-interface-index.json",
            "harvest.json",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "no authority",
            "cannot run shell commands",
            "mutate files",
            "read raw repository source",
            "read secrets",
            "install dependencies",
            "run package scripts",
            "expand network access",
            "SpecPM validation",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_INTEGRATION_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeIntegrationContract>" in root_page.read_text(encoding="utf-8")

    for path in (architecture_doc, architecture_docc, trust_doc, trust_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNode" in text
        assert "SpecHarvesterSpecNodeArtifactBundle" in text
        assert "SpecNodeRefinementJob" in text
        assert "modelFilesystemAccess: none" in text
        assert "modelShellAccess: none" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNode" in text
        assert "SpecHarvesterSpecNodeArtifactBundle" in text
        assert "SpecNodeRefinementJob" in text
        assert "candidatePatchProposal" in text
        assert "usageReceipt" in text


def test_docc_and_github_docs_cover_refine_preview_planning_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterRefinePreviewPlan",
            "refine-preview",
            "compactModelInput",
            "harvestSummary",
            "projectProfile",
            "publicInterfaceSummary",
            "semanticEvidenceIndex",
            "validationSummaries",
            "draftCandidateMetadata",
            "artifactDigests",
            "promptBudget",
            "maxPromptBytes",
            "maxPromptTokens",
            "maxPublicSymbols",
            "maxSemanticClusters",
            "truncationPolicy",
            "redactionPolicy",
            "rawRepositorySource: excluded",
            "documentationBodies: excluded",
            "providerLogs: excluded",
            "arbitraryPrompts: excluded",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "candidateMutation: proposal_only",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecNodeRefinementJob",
            "harvest.json",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "public-interface-index.json",
            "SpecHarvesterEvidenceSnapshot",
            "does not execute models",
            "deterministic local planning step",
            "perform network fetches",
        ):
            assert required in text

    assert "SPECNODE_REFINE_PREVIEW_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinePreviewContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecHarvesterRefinePreviewPlan" in text
        assert "compactModelInput" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecHarvesterRefinePreviewPlan" in text
        assert "compactModelInput" in text
        assert "PublicInterfaceIndex" in text


def test_docc_and_github_docs_cover_specnode_refinement_prompt_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementPromptContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    smoke_doc = ROOT / "docs" / "SPECNODE_PROVIDER_SMOKE_COVERAGE.md"
    smoke_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderSmokeCoverage.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeRefinementPromptContract",
            "promptContractVersion",
            "SpecNodeRefinementPromptTemplate",
            "SpecNodeRefinementPromptInput",
            "SpecNodeRefinementPromptInstructions",
            "compactModelInput",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementResult",
            "SpecNodeCandidatePatchProposal",
            "SpecNodeRejectionReason",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "generate_specpm",
            "target package behavior",
            "evidence_reference_rules",
            "negative_claim_policy",
            "confidence_calibration",
            "Evidence Reference Rules",
            "Negative-Claim Policy",
            "Confidence Calibration",
            "unknown IDs",
            "collapsed ranges",
            "invented evidence references",
            "no network calls",
            "no authentication",
            "chain-of-thought",
            "provider logs",
            "raw repository source",
            "arbitrary prompts",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "candidateMutation: proposal_only",
            "schema validation",
            "SpecPM validation",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinementPromptContract>" in root_page.read_text(encoding="utf-8")

    for path in (
        refine_doc,
        refine_docc,
        provider_doc,
        provider_docc,
        patch_doc,
        patch_docc,
        smoke_doc,
        smoke_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeRefinementPromptContract" in text
            or "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "target-package intent inference" in text
        assert "unsupported negative claims" in text
        assert "overconfident" in text


def test_docc_and_github_docs_cover_specnode_semantic_review_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeSemanticReviewContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    prompt_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_PROMPT_CONTRACT.md"
    prompt_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementPromptContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeSemanticReviewContract",
            "semanticReviewContractVersion",
            "SpecNodeSemanticReviewJob",
            "SpecNodeSemanticReviewRubric",
            "SpecNodeSemanticReviewResult",
            "SpecNodeSemanticReviewFinding",
            "SpecNodeSemanticReviewVerdict",
            "SpecNodeRefinementResult",
            "compactModelInput",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "approve",
            "needs_revision",
            "reject",
            "wrong_package_intent",
            "unsupported_capability_claim",
            "missing_evidence_reference",
            "overconfident_confidence_score",
            "unsafe_negative_claim",
            "schema_policy_mismatch",
            "authority_boundary_violation",
            "prompt_contract_violation",
            "generate_specpm",
            "firstPassPromptTranscript: excluded",
            "chainOfThought: excluded",
            "firstPassProviderLogs: excluded",
            "providerLogs: excluded",
            "rawRepositorySource: excluded",
            "arbitraryPrompts: excluded",
            "candidateMutation: none",
            "candidatePatchProposal",
            "operations",
            "retryDirective",
            "rawUnifiedDiff",
            "shellCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "reviewed_refinement_result",
            "semantic_evidence_index",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeSemanticReviewContract>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        prompt_doc,
        prompt_docc,
        patch_doc,
        patch_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeSemanticReviewContract" in text
            or "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeSemanticReviewRubric" in text
        assert "SpecNodeSemanticReviewFinding" in text
        assert "wrong_package_intent" in text
        assert "authority_boundary_violation" in text
        assert "direct file writes" in text


def test_docc_and_github_docs_cover_specnode_provider_adapter_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeOpenAICompatibleProviderAdapter",
            "SpecNodeProviderDiscoveryResult",
            "SpecNodeProviderHealth",
            "SpecNodeModelListing",
            "SpecNodeGenerationPolicy",
            "SpecNodeProviderUsageReceipt",
            "OpenAI-compatible",
            "LM Studio",
            "lm_studio",
            "http://127.0.0.1:1234",
            "http://localhost:1234",
            "baseUrl",
            "defaultHeaders",
            "authPolicy",
            "endpointAllowlist",
            "/v1/models",
            "/v1/chat/completions",
            "Endpoint joining rule",
            "localhost_only",
            "allowRemoteEndpoints",
            "modelNetworkAccess: provider_only",
            "toolNetworkAccess: none",
            "timeoutPolicy",
            "retryPolicy",
            "maxBackoffSeconds",
            "temperature",
            "maxOutputTokens",
            "promptBudget",
            "maxPromptTokens",
            "maxPromptBytes",
            "inputTokens",
            "outputTokens",
            "totalTokens",
            "responseSha256",
            "redactionPolicy",
            "allowedTools: []",
            "modelFilesystemAccess: none",
            "modelShellAccess: none",
            "rawSourceAccess: none",
            "secretAccess: none",
            "candidateMutation: proposal_only",
            "SpecHarvesterRefinePreviewPlan",
            "usageReceipt",
            "SpecHarvester does not contact providers",
            "explicit operator opt-in",
            "openai/gpt-oss-20b",
            "response_format.type: json_schema",
            "SpecNodeRefinementResult",
            "response_format.type: json_object",
            "json_object",
            "<|message|>",
            "multiple objects",
            "raw repository source",
            "provider logs",
        ):
            assert required in text

    assert "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeProviderAdapterContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text
        assert "SpecNodeProviderUsageReceipt" in text
        assert "timeoutPolicy" in text
        assert "retryPolicy" in text
        assert "SpecHarvester" in text

    for path in (refine_doc, refine_docc, architecture_doc, architecture_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderAdapterContract" in text
            or "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in text
        )
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderAdapterContract" in text
            or "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md" in text
        )
        assert "SpecNodeOpenAICompatibleProviderAdapter" in text
        assert "/v1/models" in text
        assert "/v1/chat/completions" in text
        assert "SpecHarvester does not contact providers" in text


def test_docc_and_github_docs_cover_specnode_patch_proposal_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeCandidatePatchProposal",
            "candidatePatchProposal",
            "SpecNodeCandidatePatchOperation",
            "SpecNodeProposalProvenance",
            "SpecNodeProposalUsageReceipt",
            "SpecNodeProviderUsageReceipt",
            "SpecNodeRejectionReason",
            "reviewNotes",
            "usageReceipt",
            "SpecNodeRefinementResult",
            "SpecNodeRefinementJob",
            "baseCandidateDigest",
            "sourceJobDigest",
            "sourcePreviewPlanDigest",
            "sourceArtifactDigests",
            "providerReceiptDigest",
            "policyDigest",
            "promptBudget",
            "redactionPolicy",
            "inputTokens",
            "outputTokens",
            "totalTokens",
            "responseSha256",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "expectedCurrentValueSha256",
            "targetPointer",
            "evidenceRefs",
            "add_field",
            "replace_field",
            "remove_field",
            "append_unique",
            "replace_list_item_by_id",
            "remove_list_item_by_id",
            "rawUnifiedDiff",
            "fullFileReplacement",
            "shellCommand",
            "gitCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "raw repository source",
            "provider logs",
            "insufficient_evidence",
            "prompt_budget_exceeded",
            "provider_unavailable",
            "model_output_invalid",
            "policy_violation",
            "unsupported_candidate_shape",
            "schema_validation_failed",
            "safety_boundary_triggered",
            "SpecPM validation",
        ):
            assert required in text

    assert "SPECNODE_PATCH_PROPOSAL_CONTRACT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodePatchProposalContract>" in root_page.read_text(encoding="utf-8")

    for path in (integration_doc, integration_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeCandidatePatchProposal" in text
        assert "SpecNodeProposalUsageReceipt" in text
        assert "SpecNodeRejectionReason" in text
        assert "validation-before-apply" in text

    for path in (refine_doc, refine_docc, provider_doc, provider_docc):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodePatchProposalContract" in text or "SPECNODE_PATCH_PROPOSAL_CONTRACT.md" in text
        )

    for path in (architecture_doc, architecture_docc, workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeCandidatePatchProposal" in text
        assert "SpecNodeRejectionReason" in text
        assert "direct file writes" in text


def test_docc_and_github_docs_cover_specnode_provider_smoke_coverage() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_PROVIDER_SMOKE_COVERAGE.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderSmokeCoverage.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    refine_doc = ROOT / "docs" / "SPECNODE_REFINE_PREVIEW_CONTRACT.md"
    refine_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinePreviewContract.md"
    )
    provider_doc = ROOT / "docs" / "SPECNODE_PROVIDER_ADAPTER_CONTRACT.md"
    provider_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeProviderAdapterContract.md"
    )
    patch_doc = ROOT / "docs" / "SPECNODE_PATCH_PROPOSAL_CONTRACT.md"
    patch_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodePatchProposalContract.md"
    )
    architecture_doc = ROOT / "docs" / "ARCHITECTURE.md"
    architecture_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "HarvesterArchitecture.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecNodeProviderSmokeRun",
            "SpecNode-compatible provider",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementJob",
            "SpecNodeRefinementResult",
            "SpecNodeCandidatePatchProposal",
            "SpecNodeRejectionReason",
            "provider_unavailable",
            "compactModelInput",
            "weak-model",
            "rawRepositorySource: excluded",
            "documentationBodies: excluded",
            "dependencyDirectories: excluded",
            "providerLogs: excluded",
            "secrets: excluded",
            "arbitraryPrompts: excluded",
            "usageReceipt",
            "SpecNodeProviderUsageReceipt",
            "requiresSchemaValidation: true",
            "requiresHumanReview: true",
            "requiresSpecPMValidationAfterApply: true",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "rawUnifiedDiff",
            "fullFileReplacement",
            "shellCommand",
            "gitCommand",
            "networkFetch",
            "providerCall",
            "packageManagerCommand",
            "testRunnerCommand",
            "buildToolCommand",
            "direct file writes",
            "does not call LM Studio",
            "does not mutate candidate files",
            "SpecHarvester does not contact providers",
            "openai/gpt-oss-20b",
            "response_format.type: json_schema",
            "response_format.type: json_object",
            "parse_specnode_model_json_object",
            "<|message|>",
            "multiple object payloads",
            "trailing non-JSON text",
        ):
            assert required in text

    assert "SPECNODE_PROVIDER_SMOKE_COVERAGE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeProviderSmokeCoverage>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        refine_doc,
        refine_docc,
        provider_doc,
        provider_docc,
        patch_doc,
        patch_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeProviderSmokeCoverage" in text or "SPECNODE_PROVIDER_SMOKE_COVERAGE.md" in text
        )

    for path in (architecture_doc, architecture_docc, workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeProviderSmokeRun" in text
        assert "SpecNodeRefinementResult" in text
        assert "provider_unavailable" in text


def test_docc_and_github_docs_cover_accepted_candidate_impact_classification() -> None:
    github_doc = ROOT / "docs" / "ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AcceptedCandidateImpactClassificationReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "accepted-candidate-impact-classification-report",
            "metadata",
            "interface",
            "license",
            "provenance",
            "capability",
            "intent",
        ):
            assert required in text

    assert "<doc:AcceptedCandidateImpactClassificationReports>" in root_page.read_text(
        encoding="utf-8"
    )
    assert "ACCEPTED_CANDIDATE_IMPACT_CLASSIFICATION_REPORTS.md" in docs_index.read_text(
        encoding="utf-8"
    )


def test_docc_and_github_docs_cover_accepted_package_update_proposals() -> None:
    github_doc = ROOT / "docs" / "ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AcceptedPackageUpdateProposals.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "accepted-package-update-proposal",
            "sourceRevision",
            "evidenceDigests",
            "oldPackageVersion",
            "newPackageVersion",
            "changedClaims",
            "validationStatus",
            "reviewerNotes",
            "updateKind",
        ):
            assert required in text

    assert "<doc:AcceptedPackageUpdateProposals>" in root_page.read_text(encoding="utf-8")
    assert "<doc:AcceptedPackageUpdateProposals>" in workflow_page.read_text(encoding="utf-8")
    assert "ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md" in docs_index.read_text(encoding="utf-8")


def test_local_smoke_fixture_docs_cover_reproducible_controls() -> None:
    github_doc = ROOT / "docs" / "LOCAL_SMOKE_FIXTURES.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "LocalSmokeFixtures.md"
    docs_index = ROOT / "docs" / "README.md"
    root_readme = ROOT / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    gitignore = ROOT / ".gitignore"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            ".smoke/inputs",
            ".smoke/output",
            "Cupertino".lower(),
            "xyflow",
            "docc2context",
            "Puzzle".lower(),
            "collect-batch",
            "--relaxed-private",
            "batch-validation.json",
            "staged git changes",
            "missing_license_file",
            "multi-language smoke matrix",
            "synthetic",
            "npm",
            "SPM",
            "Gradle/Maven",
            "Go modules",
            "Composer",
            "CMake",
            "Xcode/CocoaPods",
            "RubyGems",
            "Python packaging",
            "documentation-first",
            "manifest-poor",
            "ProjectProfile",
            "semanticHints",
            "semantic_intent_static_evidence",
            "Flask",
            "Gin",
            "LICENSE.txt",
            "popular-smoke",
            "--emit-interface-indexes",
            "public-interface-index.json",
            "SpecPM validation",
            "preview_only_package",
            "unknown_evidence_kind",
            "evidence_support_target_unknown",
            "smoke-triage-summary",
            "governance-upstream-report",
            "governance-license-provenance-report",
            "generated smoke outputs",
            "Do not install harvested dependencies",
            "Do not run harvested package scripts",
            "Do not execute harvested repository code",
        ):
            assert required in text

    assert "LOCAL_SMOKE_FIXTURES.md" in docs_index.read_text(encoding="utf-8")
    assert "LOCAL_SMOKE_FIXTURES.md" in root_readme.read_text(encoding="utf-8")
    assert "<doc:LocalSmokeFixtures>" in docc_root.read_text(encoding="utf-8")

    ignored_paths = gitignore.read_text(encoding="utf-8")
    assert ".smoke/" in ignored_paths
    assert "smoke-inputs/" in ignored_paths
    assert "smoke-output*/" in ignored_paths
