from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_current_next_task(next_text: str) -> None:
    assert_p26_t5_archived(next_text)
    assert_p27_t1_recent(next_text)
    assert_p27_t2_recent(next_text)
    assert_p27_t3_recent(next_text)
    if "# Next Task: P27-T4 Author Review Viewer and Handoff Checklist" in next_text:
        assert_p27_t3_last_archived(next_text)
        assert_phase_27_t4_active(next_text)
        return

    assert_p27_t4_last_archived(next_text)
    assert_p27_t4_recent(next_text)
    if "# Next Task: P27-T5 Real Repository Author-Ready Draft Calibration Matrix" in next_text:
        assert_phase_27_t5_active(next_text)
        return

    assert_p27_t5_last_archived(next_text)
    assert_p27_t5_recent(next_text)
    assert_phase_27_complete(next_text)


def assert_p27_t3_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P27-T3 Author-Ready Stop Policy Summary" in next_text


def assert_p27_t4_last_archived(next_text: str) -> None:
    assert "**Last Archived:** P27-T4 Author Review Viewer and Handoff Checklist" in next_text


def assert_p27_t5_last_archived(next_text: str) -> None:
    assert (
        "**Last Archived:** P27-T5 Real Repository Author-Ready Draft Calibration Matrix"
        in next_text
    )


def assert_p26_t5_archived(next_text: str) -> None:
    assert "SpecHarvesterPackageSetAIDraftProposal" in next_text
    assert "LLM + schema" in next_text
    assert "selected members" in next_text
    assert "exclusions" in next_text
    assert "contains" in next_text


def assert_p27_t1_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T1` documented the author-ready draft quality bar" in next_text
    assert "valid starter package" in next_text
    assert "repository authors" in next_text
    assert "final accepted specification" in normalized


def assert_p27_t2_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T2` added `author-ready-draft-quality-report.json`" in next_text
    assert "authorReadyDraft" in next_text
    assert "quality_report" in next_text
    assert "author action items" in normalized


def assert_p27_t3_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T3` added a deterministic stop-policy summary" in next_text
    assert "authorReadyDraftSummary" in next_text
    assert "stopPolicySummary" in next_text
    assert "stop_for_author_review" in next_text
    assert "continue_generation" in next_text
    assert "blocked_until_inputs_change" in next_text
    assert "single draft" in normalized
    assert "AI enrichment" in normalized


def assert_p27_t4_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T4` added author review checklists" in next_text
    assert "authorReview" in next_text
    assert "weak claims" in next_text
    assert "evidence gaps" in next_text
    assert "recommended edits" in next_text
    assert "member action summaries" in normalized


def assert_phase_27_t4_active(next_text: str) -> None:
    assert "# Next Task: P27-T4 Author Review Viewer and Handoff Checklist" in next_text
    assert "**Status:** In Progress" in next_text
    assert "author review checklists" in next_text
    assert "weak claim" in next_text
    assert "evidence-gap" in next_text
    assert "recommended edits" in next_text


def assert_p27_t5_recent(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "`P27-T5` added the author-ready calibration matrix" in next_text
    assert "SpecHarvesterAuthorReadyCalibrationMatrix" in next_text
    assert "estimated author edits" in next_text
    assert "edit categories" in next_text
    assert "repeated generator gaps" in normalized


def assert_phase_27_t5_active(next_text: str) -> None:
    normalized = " ".join(next_text.split())
    assert "# Next Task: P27-T5 Real Repository Author-Ready Draft Calibration Matrix" in next_text
    assert "**Status:** In Progress" in next_text
    assert "real-repository author-ready draft calibration matrix" in next_text
    assert "author edits" in next_text
    assert "curated specs" in normalized


def assert_phase_27_complete(next_text: str) -> None:
    assert "# Next Task: Phase 27 Complete" in next_text
    assert "**Status:** Phase Complete" in next_text
    assert "Author-Ready Valid Drafts" in next_text


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
            "spec_harvester.swift_public_api",
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


def test_docc_and_github_docs_cover_static_spec_renderer() -> None:
    github_doc = ROOT / "docs" / "STATIC_SPEC_RENDERER.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "StaticSpecRenderer.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "render-spec-site",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "spec-package.json",
            "SpecPM remains",
            "validation and registry authority",
            "no package code execution",
            "no package scripts",
            "no dependency installation",
            "no network probes",
            "no browser-side YAML parsing",
            "SpecHarvesterStaticSpecPackage",
            "standalone viewer",
        ):
            assert required in text

    assert "STATIC_SPEC_RENDERER.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:StaticSpecRenderer>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_producer_candidate_bundle_plan() -> None:
    github_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProducerCandidateBundle.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workplan = ROOT / "SPECS" / "Workplan.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Producer Candidate Bundle Contract",
            "candidate/",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "apiVersion: specpm.receipts/v0",
            "kind: SpecPMProducerReceipt",
            "receiptProfile: generated_spec_package_v0",
            "configuration.digest",
            "outputs[]",
            "SHA-256",
            "self-hash problem",
            "humanReview.status: approved",
            "maintainer override",
            "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md"
            if path == github_doc
            else "SpecPMRegistryAcceptanceDecision",
            "privacy.secretsIncluded",
            "unstable generated ID",
            "evidence references",
            "namespace",
            "Producer receipts are evidence, not authority",
            "SPECPM_SHARED_FIXTURE_POLICY.md"
            if path == github_doc
            else "SpecPMSharedFixturePolicy",
        ):
            assert required in normalized

        assert "producer-receipt.json` must not appear in `outputs[]" in text

    assert "PRODUCER_CANDIDATE_BUNDLE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ProducerCandidateBundle>" in root_page.read_text(encoding="utf-8")

    workplan_text = workplan.read_text(encoding="utf-8")
    assert "apiVersion: specpm.receipts/v0" in workplan_text
    assert "kind: SpecPMProducerReceipt" in workplan_text
    assert "apiVersion: specpm.producer_receipt/v1" not in workplan_text


def test_docc_and_github_docs_cover_specpm_handoff_guide() -> None:
    github_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecHarvester produces an evidence-rich candidate",
            "SpecPM validates package shape",
            "public index publishes only reviewed sources",
            "candidate/",
            "specpm.yaml",
            "specs/*.spec.yaml",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "spec-harvester collect-local",
            "spec-harvester draft",
            "preflight-candidate-bundle",
            "render-spec-site",
            'kind": "SpecPMProducerReceipt',
            'receiptProfile": "generated_spec_package_v0',
            "producer-receipt.json` must not appear in `outputs[]",
            "humanReview.status: approved",
            "maintainer override",
            "SpecHarvester evidence can support the decision",
            "It cannot make the decision",
            "registryAcceptanceDecision.status: external_required",
            "SpecPMRegistryAcceptanceDecision",
            "Shared Fixture Policy",
        ):
            assert required in normalized

    assert "SPECPM_HANDOFF.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMHandoff>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_specpm_shared_fixture_policy() -> None:
    github_doc = ROOT / "docs" / "SPECPM_SHARED_FIXTURE_POLICY.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMSharedFixturePolicy.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Shared Fixture Policy",
            "SpecPM contract fixture",
            "SpecHarvester generated fixture",
            "reviewable drift check",
            "generated_spec_package_v0",
            "exact SpecPM commit SHA",
            "root of trust",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "producer preflight",
            "static viewer",
            "proposal body evidence links",
            "Silent drift is not acceptable" if path == github_doc else "silently drift",
            "does not make generated",
        ):
            assert required in normalized

    assert "SPECPM_SHARED_FIXTURE_POLICY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMSharedFixturePolicy>" in root_page.read_text(encoding="utf-8")
    assert "shared fixture policy" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T2` Define a shared cross-repository fixture policy" in workplan_text
    assert "- [x] `P23-T2`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_ci_preflight_gate_support() -> None:
    github_doc = ROOT / "docs" / "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecPMCiPreflightGateSupport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    docc_proposal = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    shared_fixture_doc = ROOT / "docs" / "SPECPM_SHARED_FIXTURE_POLICY.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM CI Preflight Gate Support",
            "future optional SpecPM CI preflight",
            "stable producer evidence layout",
            "SpecPM maintainer review",
            "registry acceptance decision",
            "producerEvidenceLinks",
            "pathScope",
            "accepted_source_bundle",
            "producer_receipt",
            "validation_report",
            "diagnostics",
            "producer_preflight",
            "static_viewer",
            "accepted_source_diff",
            "humanReview.requiredFor",
            "public_index_acceptance",
            "repo_relative",
            "workflow_artifact",
            "pull_request",
            "A pass is not acceptance" if path == docc_doc else "does not require SpecPM",
        ):
            assert required in normalized

    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMCiPreflightGateSupport>" in root_page.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in proposal_doc.read_text(encoding="utf-8")
    assert "<doc:SpecPMCiPreflightGateSupport>" in docc_proposal.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in handoff_doc.read_text(encoding="utf-8")
    assert "SPECPM_CI_PREFLIGHT_GATE_SUPPORT.md" in shared_fixture_doc.read_text(encoding="utf-8")
    assert "optional SpecPM CI preflight gate" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T3` Add SpecHarvester-side support" in workplan_text
    assert "- [x] `P23-T3`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_registry_acceptance_decision() -> None:
    github_doc = ROOT / "docs" / "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecPMRegistryAcceptanceDecision.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    docc_proposal = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    producer_bundle_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Registry Acceptance Decision Record",
            "external registry acceptance decision record",
            "SpecPMRegistryAcceptanceDecision",
            "public_index_acceptance",
            "external_required",
            "evidence_only",
            "pending",
            "approved",
            "rejected",
            "override",
            "withdrawn",
            "SpecHarvester receipt says approved",
            "must not be the root of trust for approval",
        ):
            assert required in normalized

    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMRegistryAcceptanceDecision>" in root_page.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in proposal_doc.read_text(encoding="utf-8")
    assert "<doc:SpecPMRegistryAcceptanceDecision>" in docc_proposal.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in handoff_doc.read_text(encoding="utf-8")
    assert "SPECPM_REGISTRY_ACCEPTANCE_DECISION.md" in producer_bundle_doc.read_text(
        encoding="utf-8"
    )
    assert "external SpecPM registry acceptance decision" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P23-T4` Integrate a future external registry acceptance decision" in workplan_text
    assert "- [x] `P23-T4`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_specpm_package_set_alignment() -> None:
    github_doc = ROOT / "docs" / "SPECPM_PACKAGE_SET_ALIGNMENT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMPackageSetAlignment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "SpecPM Package Set Alignment",
            "Package Sets",
            "Package Relations",
            "Package Set Search",
            "Package Set Registry Metadata",
            "SpecHarvester Monorepo Discovery",
            "Multi-Package Producer Intake",
            "Xyflow Package Set Reference",
            "workspace inventory",
            "package-set candidates",
            "scoped member",
            "relation proposals",
            "bundle-set preflight",
            "static viewer",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "producer_observed",
            "package_id",
            "P25-T2",
            "P25-T7",
            "package script execution",
            "trust inheritance",
        ):
            assert required in normalized

    assert "SPECPM_PACKAGE_SET_ALIGNMENT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecPMPackageSetAlignment>" in root_page.read_text(encoding="utf-8")
    assert "Package-set contract alignment is documented" in roadmap.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P25-T1` Align SpecHarvester planning" in workplan_text
    assert "- [x] `P25-T1`" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_workspace_inventory() -> None:
    github_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "WorkspaceInventory.md"
    batch_doc = ROOT / "docs" / "BATCH_COLLECTION.md"
    batch_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BatchCollection.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "workspace-inventory.json",
            "spec-harvester.workspace-inventory/v0",
            "SpecHarvesterWorkspaceInventory",
            "--emit-workspace-inventory",
            "repository URL",
            "exact revision",
            "workspace manifests",
            "include patterns",
            "package manifest paths",
            "proposed SpecPM package IDs",
            "package roles",
            "digest-backed evidence references",
            "producer evidence",
            "not a SpecPM registry payload",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "P25-T3",
            "preflight-bundle-set",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (batch_doc, batch_docc):
        text = path.read_text(encoding="utf-8")
        assert "--emit-workspace-inventory" in text
        assert "workspace-inventory.json" in text
        assert "SpecHarvesterWorkspaceInventory" in text

    assert "WORKSPACE_INVENTORY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:WorkspaceInventory>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_set_drafting() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetDrafting.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workspace_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "draft-package-set",
            "workspace-inventory.json",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "spec-harvester.package-set-draft/v0",
            "SpecHarvesterPackageSetDraft",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "preview_only",
            "skipped[]",
            "role_not_selected_for_initial_package_set_draft",
            "P25-T4",
            "preflight-bundle-set",
            "not namespace authority",
            "does not execute package scripts",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (workflow_doc, workspace_doc):
        text = path.read_text(encoding="utf-8")
        assert "draft-package-set" in text
        assert "package-set-draft.json" in text

    assert "PACKAGE_SET_DRAFTING.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetDrafting>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_relation_proposals() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageRelationProposals.md"
    )
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workspace_doc = ROOT / "docs" / "WORKSPACE_INVENTORY.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-relation-proposals.json",
            "spec-harvester.package-relation-proposals/v0",
            "SpecHarvesterPackageRelationProposals",
            "contains",
            "xyflow.workspace contains xyflow.system",
            "xyflow.workspace contains xyflow.react",
            "xyflow.workspace contains xyflow.svelte",
            "reviewStatus: producer_observed",
            "workspace-inventory.json",
            "package-set-draft.json",
            "does not hash itself",
            "not SpecPM accepted registry metadata",
            "trust inheritance",
            "preflight-bundle-set",
            "render-package-set-site",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, workflow_doc, workspace_doc):
        assert "package-relation-proposals.json" in path.read_text(encoding="utf-8")

    assert "PACKAGE_RELATION_PROPOSALS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageRelationProposals>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_bundle_set_preflight() -> None:
    github_doc = ROOT / "docs" / "BUNDLE_SET_PREFLIGHT.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "BundleSetPreflight.md"
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    relation_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "preflight-bundle-set",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "spec-harvester.bundle-set-preflight/v0",
            "SpecHarvesterBundleSetPreflightReport",
            "candidate `packageId`",
            "preflight-candidate-bundle",
            "relation source and target",
            "workspace inventory",
            "does not accept packages",
            "does not accept relations",
            "package managers",
            "render-package-set-site",
            "P25-T7",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, relation_doc, workflow_doc):
        assert "preflight-bundle-set" in path.read_text(encoding="utf-8")

    assert "BUNDLE_SET_PREFLIGHT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:BundleSetPreflight>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_package_set_viewer() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_VIEWER.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetViewer.md"
    package_set_doc = ROOT / "docs" / "PACKAGE_SET_DRAFTING.md"
    relation_doc = ROOT / "docs" / "PACKAGE_RELATION_PROPOSALS.md"
    preflight_doc = ROOT / "docs" / "BUNDLE_SET_PREFLIGHT.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "render-package-set-site",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "package-set.json",
            "SpecHarvesterStaticPackageSet",
            "spec-harvester.static-package-set-renderer/v0",
            "authorReadyDraftSummary",
            "authorReview",
            "author review checklist",
            "weak claim",
            "evidence-gap",
            "recommended edits",
            "member action",
            "member package cards",
            "relation proposal badges",
            "result scope examples",
            "producer-observed review status",
            "producer_observed",
            "does not accept packages",
            "does not accept relations",
            "P25-T7",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (package_set_doc, relation_doc, preflight_doc, workflow_doc, workflow_docc):
        text = " ".join(path.read_text(encoding="utf-8").split())
        assert "render-package-set-site" in text
        assert "member package cards" in text
        assert "relation proposal badges" in text

    assert "PACKAGE_SET_VIEWER.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetViewer>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_xyflow_package_set_smoke() -> None:
    github_doc = ROOT / "docs" / "XYFLOW_PACKAGE_SET_SMOKE.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "XyflowPackageSetSmoke.md"
    )
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    alignment_doc = ROOT / "docs" / "SPECPM_PACKAGE_SET_ALIGNMENT.md"
    alignment_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMPackageSetAlignment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "xyflow-package-set-smoke",
            "collect-batch --emit-workspace-inventory",
            "draft-package-set",
            "preflight-bundle-set",
            "render-package-set-site",
            "workspace-inventory.json",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "viewer/package-set.json",
            "xyflow-package-set-smoke.json",
            "spec-harvester.xyflow-package-set-smoke/v0",
            "SpecHarvesterXyflowPackageSetSmokeReport",
            "xyflow.workspace",
            "xyflow.system",
            "xyflow.react",
            "xyflow.svelte",
            "xyflow.workspace contains xyflow.system",
            "xyflow.workspace contains xyflow.react",
            "xyflow.workspace contains xyflow.svelte",
            "xyflow.cli",
            "xyflow.e2e",
            "xyflow.react_examples",
            "xyflow.svelte_examples",
            "does not fetch the real",
            "run package scripts",
            "run package managers",
            "accept packages",
            "accept relations",
            "publish registry metadata",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "XYFLOW_PACKAGE_SET_SMOKE.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:XyflowPackageSetSmoke>" in root_page.read_text(encoding="utf-8")
    for path in (workflow_doc, alignment_doc, alignment_docc):
        text = path.read_text(encoding="utf-8")
        assert "xyflow-package-set-smoke" in text
        assert "xyflow-package-set-smoke.json" in text
        assert "viewer/package-set.json" in text


def test_docc_and_github_docs_cover_package_set_handoff_proposal() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_HANDOFF_PROPOSAL.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetHandoffProposal.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    proposal_doc = ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md"
    proposal_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    )
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-set-handoff-proposal",
            "package-set-draft.json",
            "package-relation-proposals.json",
            "bundle-set-preflight.json",
            "SpecHarvesterPackageSetHandoffProposal",
            "spec-harvester.package-set-handoff-proposal/v0",
            "package_set_draft",
            "package_relation_proposals",
            "bundle_set_preflight",
            "package_set_viewer",
            "member_candidate_bundle",
            "member_manifest",
            "member_producer_receipt",
            "member_quality_report",
            "package_relation_summary",
            "authorReadyDraftSummary",
            "authorReview",
            "Author Review Checklist",
            "Weak Claims and Evidence Gaps",
            "Recommended Edits",
            "Weak claims",
            "Evidence gaps",
            "Recommended edits",
            "stop_for_author_review",
            "registryAcceptanceDecision.status: external_required",
            "public_index_acceptance",
            "package_relation_acceptance",
            "does not accept packages",
            "accept relations",
            "replace SpecPM maintainer review",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (proposal_doc, proposal_docc, handoff_doc, handoff_docc):
        text = path.read_text(encoding="utf-8")
        assert "package-set-handoff-proposal" in text
        assert "external_required" in text

    assert "PACKAGE_SET_HANDOFF_PROPOSAL.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetHandoffProposal>" in root_page.read_text(encoding="utf-8")
    workplan_text = workplan.read_text(encoding="utf-8")
    assert "`P26-T1` Add a package-set handoff proposal artifact" in workplan_text
    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_package_set_ai_enrichment() -> None:
    github_doc = ROOT / "docs" / "PACKAGE_SET_AI_ENRICHMENT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetAIEnrichment.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    handoff_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    workplan = ROOT / "SPECS" / "Workplan.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "package-set-ai-enrichment-proposal",
            "SpecHarvesterPackageSetAIEnrichmentProposal",
            "spec-harvester.package-set-ai-enrichment/v0",
            "openai/gpt-oss-20b",
            "refinedSummary",
            "capabilities",
            "interfaces",
            "evidencePaths",
            "model_evidence_path_unsupported",
            "stopPolicySummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "proposal evidence only",
            "does not mutate",
            "accept packages",
            "accept relations",
            "publish registry metadata",
            "CI must not require",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    for path in (handoff_doc, handoff_docc):
        text = path.read_text(encoding="utf-8")
        assert "package-set-ai-enrichment-proposal" in text
        assert "SpecHarvesterPackageSetAIEnrichmentProposal" in text
        assert "model_evidence_path_unsupported" in text

    assert "PACKAGE_SET_AI_ENRICHMENT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:PackageSetAIEnrichment>" in root_page.read_text(encoding="utf-8")
    assert "`P26-T4` Add proposal-only package-set AI enrichment" in workplan.read_text(
        encoding="utf-8"
    )


def test_docc_and_github_docs_cover_author_ready_draft_quality_bar() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_DRAFT_QUALITY_BAR.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "AuthorReadyDraftQualityBar.md"
    )
    package_set_ai_draft = ROOT / "docs" / "PACKAGE_SET_AI_DRAFT_PROPOSAL.md"
    package_set_ai_draft_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "PackageSetAIDraftProposal.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"
    workplan = ROOT / "SPECS" / "Workplan.md"
    next_task = ROOT / "SPECS" / "INPROGRESS" / "next.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "valid starter package",
            "author-ready draft",
            "SpecHarvester -> valid author-ready draft",
            "author + agent -> semantic completion and curation",
            "SpecPM -> validation, registry acceptance, and public index authority",
            "specpm validate",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "preview",
            "author action items",
            "evidence gaps",
            "not a numeric guarantee of correctness",
            "authorReadyDraftSummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "validation",
            "evidenceCoverage",
            "repositorySpecificity",
            "packageTopology",
            "claimConservatism",
            "authorActionability",
            "authorityBoundary",
            "framework encyclopedia",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_DRAFT_QUALITY_BAR.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityBar>" in docc_root.read_text(encoding="utf-8")
    assert "AUTHOR_READY_DRAFT_QUALITY_BAR.md" in package_set_ai_draft.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityBar>" in package_set_ai_draft_docc.read_text(
        encoding="utf-8"
    )

    roadmap_text = roadmap.read_text(encoding="utf-8")
    roadmap_docc_text = roadmap_docc.read_text(encoding="utf-8")
    assert "Milestone 5: Author-Ready Valid Drafts" in roadmap_text
    assert "valid starter package" in roadmap_text
    assert "Author-Ready Valid Drafts" in roadmap_docc_text
    assert "<doc:AuthorReadyDraftQualityBar>" in roadmap_docc_text

    workplan_text = workplan.read_text(encoding="utf-8")
    assert "Phase 27. Author-Ready Valid Drafts" in workplan_text
    for task_id in ("P27-T1", "P27-T2", "P27-T3", "P27-T4", "P27-T5"):
        assert f"`{task_id}`" in workplan_text
    assert "- [x] `P27-T1`" in workplan_text
    assert "- [x] `P27-T2`" in workplan_text
    assert "- [x] `P27-T3`" in workplan_text
    assert "- [x] `P27-T4`" in workplan_text
    assert "- [ ] `P27-T5`" in workplan_text
    assert "author_ready_draft" in workplan_text
    assert "needs_regeneration" in workplan_text
    assert "blocked" in workplan_text

    next_text = next_task.read_text(encoding="utf-8")
    assert_current_next_task(next_text)


def test_docc_and_github_docs_cover_author_ready_draft_quality_report() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_DRAFT_QUALITY_REPORT.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AuthorReadyDraftQualityReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    producer_doc = ROOT / "docs" / "PRODUCER_CANDIDATE_BUNDLE.md"
    handoff_doc = ROOT / "docs" / "SPECPM_HANDOFF.md"
    package_set_handoff = ROOT / "docs" / "PACKAGE_SET_HANDOFF_PROPOSAL.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "author-ready-draft-quality-report.json",
            "spec-harvester.author-ready-draft-quality/v0",
            "SpecHarvesterAuthorReadyDraftQualityReport",
            "authorReadyDraft.status",
            "author_ready_draft",
            "needs_regeneration",
            "blocked",
            "hardGates",
            "producer_validation",
            "critical_diagnostics",
            "required_bundle_files",
            "producer_receipt_planned",
            "evidence_links_present",
            "authority_boundary",
            "dimensions",
            "authorActionItems",
            "authorReadyDraftSummary",
            "stop_for_author_review",
            "continue_generation",
            "blocked_until_inputs_change",
            "quality_report",
            "not SpecPM registry acceptance",
            "not maintainer approval",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_DRAFT_QUALITY_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyDraftQualityReport>" in docc_root.read_text(encoding="utf-8")
    assert "quality_report" in producer_doc.read_text(encoding="utf-8")
    assert "author-ready-draft-quality-report.json" in handoff_doc.read_text(encoding="utf-8")
    assert "member_quality_report" in package_set_handoff.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_author_ready_calibration_matrix() -> None:
    github_doc = ROOT / "docs" / "AUTHOR_READY_CALIBRATION_MATRIX.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "AuthorReadyCalibrationMatrix.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    quality_doc = ROOT / "docs" / "REAL_REPOSITORY_QUALITY_REPORT.md"
    quality_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "RealRepositoryQualityReport.md"
    )
    roadmap = ROOT / "docs" / "ROADMAP.md"
    roadmap_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Roadmap.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "author-ready-calibration-matrix",
            "quality-report.json",
            "spec-harvester.author-ready-calibration-matrix/v0",
            "SpecHarvesterAuthorReadyCalibrationMatrix",
            "estimatedAuthorEdits",
            "editCategories",
            "authorReadyStatus",
            "reviewPriority",
            "generatorFollowUpReasons",
            "calibrationVerdict",
            "author_curation_ready",
            "mixed_author_ready",
            "generator_follow_up_recommended",
            "blocked_inputs_present",
            "cupertino",
            "navigation-split-view",
            "xyflow",
            "flask",
            "gin",
            "docc2context",
            ".smoke/",
            "must not be committed",
            "SpecPM acceptance",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"

    assert "AUTHOR_READY_CALIBRATION_MATRIX.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in docc_root.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in workflow_docc.read_text(encoding="utf-8")
    assert "AUTHOR_READY_CALIBRATION_MATRIX.md" in quality_doc.read_text(encoding="utf-8")
    assert "<doc:AuthorReadyCalibrationMatrix>" in quality_docc.read_text(encoding="utf-8")
    assert "author-ready calibration matrix" in roadmap.read_text(encoding="utf-8")
    assert "AuthorReadyCalibrationMatrix" in roadmap_docc.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_governance_report_broad_intent_filtering() -> None:
    github_doc = ROOT / "docs" / "GOVERNANCE_REPORTS.md"
    docc_doc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "GovernanceReports.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for required in (
            "Broad language-neutral semantic intents",
            "API contract",
            "metadata schema validation",
            "workflow automation",
            "developer tooling",
            "documentation",
            "public repository metadata",
            "records",
            "duplicate findings",
        ):
            assert required in normalized, f"Required term {required!r} not found in {path}"


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
        assert '"attempts": []' not in text

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


def test_docc_and_github_docs_cover_specnode_retry_orchestration_contract() -> None:
    github_doc = ROOT / "docs" / "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeRefinementRetryOrchestration.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"
    integration_doc = ROOT / "docs" / "SPECNODE_INTEGRATION_CONTRACT.md"
    integration_docc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecNodeIntegrationContract.md"
    )
    semantic_doc = ROOT / "docs" / "SPECNODE_SEMANTIC_REVIEW_CONTRACT.md"
    semantic_docc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "SpecNodeSemanticReviewContract.md"
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
            "SpecNodeRefinementRetryOrchestrationContract",
            "retryOrchestrationContractVersion",
            "SpecNodeRefinementRetryRun",
            "SpecNodeRefinementRetryPolicy",
            "SpecNodeRefinementRetryAttempt",
            "SpecNodeRetryDirectiveSet",
            "SpecNodeRetryDirective",
            "SpecNodeRetryContext",
            "SpecNodeRefinementResult",
            "SpecNodeSemanticReviewResult",
            "SpecNodeSemanticReviewFinding",
            "maxAttempts",
            "attemptCount",
            "artifactReuse: same_bundle_and_preview_plan",
            "sourceBundleDigest",
            "sourcePreviewPlanDigest",
            "sourceSemanticReviewResultDigest",
            "sourceFindingId",
            "boundedInstruction",
            "rawTextPropagation: forbidden",
            "candidateOutputAuthority: proposal_only",
            "approved",
            "retry_scheduled",
            "retry_limit_reached",
            "needs_revision",
            "reject",
            "refocus_target_package_intent",
            "remove_or_evidence_capability_claim",
            "add_evidence_reference_or_drop_claim",
            "lower_confidence_or_add_evidence",
            "remove_unsupported_negative_claim",
            "align_with_schema_policy",
            "remove_authority_request",
            "restore_prompt_contract_boundary",
            "raw repository source",
            "provider logs",
            "first-pass prompt transcripts",
            "chain-of-thought",
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
            "SpecPM validation",
            "human review",
        ):
            assert required in text

    assert "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:SpecNodeRefinementRetryOrchestration>" in root_page.read_text(encoding="utf-8")

    for path in (
        integration_doc,
        integration_docc,
        semantic_doc,
        semantic_docc,
        architecture_doc,
        architecture_docc,
        workflow_doc,
        workflow_docc,
    ):
        text = path.read_text(encoding="utf-8")
        assert (
            "SpecNodeRefinementRetryOrchestration" in text
            or "SPECNODE_REFINEMENT_RETRY_ORCHESTRATION.md" in text
        )

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "SpecNodeRefinementRetryRun" in text
        assert "SpecNodeRetryDirective" in text
        assert "sourceBundleDigest" in text
        assert "sourcePreviewPlanDigest" in text
        assert "maxAttempts" in text


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
            "manual live smoke",
            "scripts/specnode_live_retry_smoke.py",
            "SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE",
            "SPECHARVESTER_LM_STUDIO_BASE_URL",
            "SPECHARVESTER_SPECNODE_MODEL",
            "localhost",
            "127.0.0.1",
            "::1",
            "run_specnode_refinement_retry_orchestration",
            "SpecNodeRetryDirectiveSet",
            "SpecNodeRetryContext",
            "retry context",
            "token usage",
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


def test_docc_and_github_docs_cover_license_provenance_issue_classes() -> None:
    github_doc = ROOT / "docs" / "LICENSE_PROVENANCE_RISK_REPORTS.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "LicenseProvenanceRiskReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterLicenseProvenanceRiskReport",
            "absent_license_evidence",
            "ambiguous_unknown_license",
            "collected_unknown_license_evidence",
            "LICENSE.txt",
            "COPYING.rst",
            "licenseEvidence",
            "governance-license-provenance-report",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "LICENSE_PROVENANCE_RISK_REPORTS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:LicenseProvenanceRiskReports>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_code_duplication_reports() -> None:
    github_doc = ROOT / "docs" / "CODE_DUPLICATION_REPORTS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "CodeDuplicationReports.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterCodeDuplicationReport",
            "code-duplication-report",
            "--backend pylint",
            "--backend jscpd",
            "jscpd-report.json",
            "MIT",
            "npm",
            "supply-chain",
            "R0801",
            "--fail-on-duplicates",
            "advisory",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "CODE_DUPLICATION_REPORTS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:CodeDuplicationReports>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_architecture_lint_guardrails() -> None:
    github_doc = ROOT / "docs" / "ARCHITECTURE_LINT_GUARDRAILS.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ArchitectureLintGuardrails.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterArchitectureLintReport",
            "architecture-lint",
            "--fail-on-issues",
            "Helper",
            "constructor",
            "static/class",
            "specpm.yaml",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "ARCHITECTURE_LINT_GUARDRAILS.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ArchitectureLintGuardrails>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_procedural_style_report() -> None:
    github_doc = ROOT / "docs" / "PROCEDURAL_STYLE_REPORT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProceduralStyleReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvesterProceduralStyleReport",
            "procedural-style-report",
            "--fail-on-hotspots",
            "topLevelFunctionSpan",
            "behaviorRichClassCount",
            "dtoOnlyClassCount",
            "largestTopLevelFunctions",
            "advisory",
            "No repository code execution",
            "No imports from scanned modules",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "PROCEDURAL_STYLE_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:ProceduralStyleReport>" in root_page.read_text(encoding="utf-8")


def test_docc_and_github_docs_cover_eo_refactoring_strategy() -> None:
    github_doc = ROOT / "docs" / "EO_REFACTORING_STRATEGY.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "EORefactoringStrategy.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    root_page = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "behavior-rich objects",
            "ELEGANT_OBJECTS_STYLE.md",
            "AGENTS.md",
            "top-level function",
            "DTO-only dataclasses",
            "characterization tests",
            "SpecNode",
            "Stop Conditions",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "EO_REFACTORING_STRATEGY.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:EORefactoringStrategy>" in root_page.read_text(encoding="utf-8")


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
            "producerEvidenceLinks",
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "oldPackageVersion",
            "newPackageVersion",
            "changedClaims",
            "validationStatus",
            "reviewerNotes",
            "updateKind",
            "accepted source bundle",
            "accepted-source pull request diff",
            "registryAcceptanceDecision",
            "external_required",
            "SpecPMRegistryAcceptanceDecision",
        ):
            assert required in text

    assert "<doc:AcceptedPackageUpdateProposals>" in root_page.read_text(encoding="utf-8")
    assert "<doc:AcceptedPackageUpdateProposals>" in workflow_page.read_text(encoding="utf-8")
    assert "ACCEPTED_PACKAGE_UPDATE_PROPOSALS.md" in docs_index.read_text(encoding="utf-8")


def test_specpm_proposal_automation_links_producer_bundle_evidence() -> None:
    workflow = (ROOT / ".github" / "workflows" / "propose-to-specpm.yml").read_text(
        encoding="utf-8"
    )
    github_doc = (ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md").read_text(encoding="utf-8")
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    ).read_text(encoding="utf-8")
    handoff_doc = (ROOT / "docs" / "SPECPM_HANDOFF.md").read_text(encoding="utf-8")
    docc_handoff = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecPMHandoff.md"
    ).read_text(encoding="utf-8")
    workplan = (ROOT / "SPECS" / "Workplan.md").read_text(encoding="utf-8")
    next_task = (ROOT / "SPECS" / "INPROGRESS" / "next.md").read_text(encoding="utf-8")

    for required in (
        "Build producer evidence artifacts",
        "preflight-candidate-bundle",
        "producer-preflight-report.json",
        "render-spec-site",
        "Upload producer evidence artifacts",
        "actions/upload-artifact@v4",
        "Producer Bundle Evidence",
        "producer-receipt.json",
        "validation-report.json",
        "diagnostics.json",
        "Static viewer evidence",
        "Accepted-source diff",
        "producerEvidenceLinks",
        '"pathScope": "repo_relative"',
        '"pathScope": "workflow_artifact"',
        '"pathScope": "pull_request"',
        "registryAcceptanceDecision",
        '"status": "external_required"',
        '"producerReceiptAuthority": "evidence_only"',
    ):
        assert required in workflow

    for text in (github_doc, docc_doc, handoff_doc, docc_handoff):
        for required in (
            "producer-receipt.json",
            "validation-report.json",
            "diagnostics.json",
            "producer preflight",
            "static viewer",
            "accepted-source diff",
            "review evidence",
            "registryAcceptanceDecision",
            "external_required",
        ):
            assert required in text

    assert "P23-T1" in workplan
    assert "P23-T2" in workplan
    assert "proposal artifacts and SpecPM pull" in workplan
    assert_current_next_task(next_task)


def test_specpm_proposal_automation_supports_package_set_dry_run_boundary() -> None:
    workflow = (ROOT / ".github" / "workflows" / "propose-to-specpm.yml").read_text(
        encoding="utf-8"
    )
    github_doc = (ROOT / "docs" / "SPECPM_PROPOSAL_AUTOMATION.md").read_text(encoding="utf-8")
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "ProposalAutomation.md"
    ).read_text(encoding="utf-8")

    for required in (
        "proposal_kind",
        "single_package",
        "package_set",
        "package_set_bundle_dir",
        "package_set_viewer_dir",
        'default: ""',
        "xyflow-package-set-smoke",
        "Build package-set handoff evidence artifacts",
        "package-set-handoff-proposal",
        "package-set-handoff-proposal.json",
        "package-set-handoff-proposal.md",
        "Upload package-set handoff evidence artifacts",
        "specpm-package-set-proposal-evidence",
        "package_set proposal mode is dry-run artifact generation only",
        "steps.config.outputs.proposal_kind == 'package_set'",
        "steps.config.outputs.proposal_kind == 'single_package'",
        "does not use \\`SPECPM_PROPOSAL_TOKEN\\`",
        "does not create a SpecPM PR",
    ):
        assert required in workflow

    for text in (" ".join(github_doc.split()), " ".join(docc_doc.split())):
        for required in (
            "proposal_kind: package_set",
            "package_set_bundle_dir",
            "package_set_viewer_dir",
            "xyflow-package-set-smoke",
            "committed or downloaded artifacts",
            "package-set-handoff-proposal.json",
            "package-set-handoff-proposal.md",
            "specpm-package-set-proposal-evidence",
            "create_pr=false",
            "SPECPM_PROPOSAL_TOKEN",
            "untrusted",
            "does not create a SpecPM PR",
            "review evidence only",
        ):
            assert required in text


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


def test_real_repository_refinement_validation_docs_cover_boundaries() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_REFINEMENT_VALIDATION.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryRefinementValidation.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_doc = ROOT / "docs" / "HOW_IT_WORKS.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "SpecHarvester-side",
            "external SpecNode contract boundary",
            "SpecNode runtime",
            "provider discovery",
            "model execution",
            "provider lifecycle",
            "packageId",
            "--relaxed-private",
            ".smoke/inputs",
            ".smoke/output",
            "source-manifests",
            "collect-batch",
            "--emit-interface-indexes",
            "draft",
            "smoke-triage-summary",
            "ProjectProfile",
            "PublicInterfaceIndex",
            "semanticEvidenceIndex",
            "SpecHarvesterSpecNodeArtifactBundle",
            "SpecHarvesterRefinePreviewPlan",
            "SpecNodeRefinementRetryRun",
            "SpecPM validation",
            "intent accuracy",
            "capability/evidence support",
            "token usage",
            "Platform",
            "workspace catalog",
            ".0al",
            "Do not install harvested dependencies",
            "Do not run harvested package scripts",
            "Do not execute harvested repository code",
            "Do not commit generated candidates",
        ):
            assert required in text

    assert "REAL_REPOSITORY_REFINEMENT_VALIDATION.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryRefinementValidation>" in docc_root.read_text(encoding="utf-8")

    for path in (workflow_doc, workflow_docc):
        text = path.read_text(encoding="utf-8")
        assert "RealRepositoryRefinementValidation" in text
        assert "SpecHarvester-side" in text
        assert "provider-specific orchestration" in text


def test_real_repository_quality_report_docs_cover_required_fields() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_QUALITY_REPORT.md"
    docc_doc = (
        ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "RealRepositoryQualityReport.md"
    )
    docs_index = ROOT / "docs" / "README.md"

    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "quality-report",
            "intentAccuracy",
            "capabilityEvidenceQuality",
            "specpmStatus",
            "retryOutcome",
            "tokenUsage",
            "analyzerCoverage",
            "public-interface-index.json",
            "SpecHarvesterPublicInterfaceIndex",
            "publicInterfaceIndex",
            "humanReviewNotes",
            "overallVerdict",
            "strong",
            "partial",
            "weak",
            "unscored",
            "passed",
            "failed",
            "not_run",
            "not_attempted",
            "improved",
            "pass",
            "review",
            "fail",
            "--run-report",
            "draft-summary.json",
            "candidateDir",
            "must not be committed",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "REAL_REPOSITORY_QUALITY_REPORT.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryQualityReport>" in docc_root.read_text(encoding="utf-8")


def test_real_repository_refinement_validation_runner_docs_cover_execution_entrypoint() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryRefinementValidationRunner.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "run_real_repository_validation.py",
            "degraded",
            "optional",
            "local-only",
            "run-report.json",
            "draft-summary.json",
            "quality-report",
        ):
            assert required in text

    assert "REAL_REPOSITORY_REFINEMENT_VALIDATION_RUNNER.md" in docs_index.read_text(
        encoding="utf-8"
    )
    assert "<doc:RealRepositoryRefinementValidationRunner>" in workflow_docc.read_text(
        encoding="utf-8"
    )
    assert "<doc:RealRepositoryRefinementValidationRunner>" in docc_root.read_text(encoding="utf-8")


def test_real_repository_local_validation_matrix_docs_cover_observed_results() -> None:
    github_doc = ROOT / "docs" / "REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md"
    docc_doc = (
        ROOT
        / "Sources"
        / "SpecHarvester"
        / "Documentation.docc"
        / "RealRepositoryLocalValidationMatrix.md"
    )
    docs_index = ROOT / "docs" / "README.md"
    workflow_docc = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "Workflow.md"
    docc_root = ROOT / "Sources" / "SpecHarvester" / "Documentation.docc" / "SpecHarvester.md"

    for path in (github_doc, docc_doc):
        text = path.read_text(encoding="utf-8")
        for required in (
            "P16-T5",
            "Delta from P15-T4",
            "cupertino",
            "navigation-split-view",
            "xyflow",
            "flask",
            "gin",
            "docc2context",
            "attention_required",
            "duplicate intent",
            "LICENSE.txt",
            "collected_unknown_license_evidence",
            "navigation_split_view",
            "public-interface-index.json counted",
            "namespaceIssueCount=0",
            "5 total advisory issues",
            "SpecPM validation",
            ".smoke/",
            "No harvested package scripts",
        ):
            assert required in text, f"Required term {required!r} not found in {path}"

    assert "REAL_REPOSITORY_LOCAL_VALIDATION_MATRIX.md" in docs_index.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryLocalValidationMatrix>" in docc_root.read_text(encoding="utf-8")
    assert "<doc:RealRepositoryLocalValidationMatrix>" in workflow_docc.read_text(encoding="utf-8")
