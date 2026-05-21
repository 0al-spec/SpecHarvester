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
        assert "raw documentation" in text


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
