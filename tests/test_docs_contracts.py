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
            "batch-validation.json",
            "governance-upstream-report",
            "governance-license-provenance-report",
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
