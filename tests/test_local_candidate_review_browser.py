from __future__ import annotations

import json
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.local_candidate_review_browser import (
    LocalCandidateReviewBrowserOptions,
    catalog_summary,
    load_local_candidate_review_catalog,
    render_local_candidate_review_browser,
)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "SPECS/EVIDENCE/P54-T3/P54-T3_Candidate_Review_Catalog.json"
DETAILS = ROOT / "SPECS/EVIDENCE/P54-T5/P54-T5_Candidate_Review_Details.json"


def test_catalog_load_and_summary_cover_retained_corpus() -> None:
    catalog = load_local_candidate_review_catalog(CATALOG)

    assert catalog_summary(catalog) == {
        "candidateCount": 100,
        "readyCount": 100,
        "warningCount": 0,
        "correctedCount": 2,
        "preflightPassedCount": 100,
    }


def test_browser_renderer_writes_inert_static_bundle(tmp_path: Path) -> None:
    result = render_local_candidate_review_browser(
        LocalCandidateReviewBrowserOptions(catalog=CATALOG, output=tmp_path / "browser")
    )

    assert result["status"] == "passed"
    assert result["candidateCount"] == 100
    index = (tmp_path / "browser/index.html").read_text()
    script = (tmp_path / "browser/workbench.js").read_text()
    assert "Candidate evidence only" in index
    assert "accept_for_intake" in index
    assert 'id="csrf-token"' in index
    assert "innerHTML" not in script
    assert "localStorage" in script
    assert "/v0/actions" in script
    assert "/v0/export" in script
    assert "/v0/import" in script
    for review_state in (
        "unreviewed",
        "in_review",
        "accept_for_intake",
        "request_revision",
        "defer",
        "do_not_promote",
    ):
        assert review_state in script
    assert "p54-t6-test-token" not in index + script
    assert json.loads((tmp_path / "browser/catalog.json").read_text())["items"]


def test_browser_copies_valid_detail_set(tmp_path: Path) -> None:
    details = tmp_path / "details.json"
    details.write_text(DETAILS.read_text())
    result = render_local_candidate_review_browser(
        LocalCandidateReviewBrowserOptions(CATALOG, tmp_path / "browser", details)
    )
    assert result["detailCount"] == 100
    assert (tmp_path / "browser/details.json").is_file()
    presentations = json.loads((tmp_path / "browser/presentations.json").read_text())
    assert len(presentations["presentations"]) == 100
    first = presentations["presentations"][0]
    assert first["health"]["preflight"] == "passed"
    assert first["health"]["validation"] == "valid"
    assert {document["kind"] for document in first["documents"]} == {
        "BoundarySpec",
        "SpecPackage",
    }
    assert any(document["path"].endswith("specpm.yaml") for document in first["documents"])
    package = next(document for document in first["documents"] if document["kind"] == "SpecPackage")
    boundary = next(
        document for document in first["documents"] if document["kind"] == "BoundarySpec"
    )
    assert package["parsed"]["metadata"]["summary"]
    assert package["parsed"]["index"]["provides"]["capabilities"]
    assert boundary["parsed"]["constraints"]
    assert boundary["parsed"]["evidence"]
    assert boundary["parsed"]["scope"]["includes"]
    comparison = next(
        section
        for section in first["supporting"]
        if section["id"] == "static-versus-ai-comparison.json"
    )
    assert json.loads(comparison["content"])["ai"]["status"] == "summary_only_not_portable"
    script = (tmp_path / "browser/workbench.js").read_text()
    assert "Spec health" in script
    assert "Package specifications" in script
    assert "Supporting evidence" in script
    assert "Raw YAML" in script


def test_browser_rejects_invalid_yaml_presentation(tmp_path: Path) -> None:
    details = json.loads(DETAILS.read_text())
    yaml_section = next(
        section
        for section in details["details"][0]["sections"]
        if section["contentType"] == "application/yaml"
    )
    yaml_section["content"] = "metadata: [unterminated"
    path = tmp_path / "details.json"
    path.write_text(json.dumps(details))

    with pytest.raises(ValueError, match="YAML presentation is invalid"):
        render_local_candidate_review_browser(
            LocalCandidateReviewBrowserOptions(CATALOG, tmp_path / "browser", path)
        )


def test_browser_rejects_detail_set_with_wrong_bundle_binding(tmp_path: Path) -> None:
    details = json.loads(DETAILS.read_text())
    details["sourceBundleSha256"] = "0" * 64
    path = tmp_path / "details.json"
    path.write_text(json.dumps(details))

    with pytest.raises(ValueError, match="detail set is invalid"):
        render_local_candidate_review_browser(
            LocalCandidateReviewBrowserOptions(CATALOG, tmp_path / "browser", path)
        )


@pytest.mark.parametrize("record_type", ["details", "comparisons"])
def test_browser_rejects_detail_set_with_wrong_packet_binding(
    tmp_path: Path, record_type: str
) -> None:
    details = json.loads(DETAILS.read_text())
    details[record_type][0]["binding"]["packetSha256"] = "0" * 64
    path = tmp_path / "details.json"
    path.write_text(json.dumps(details))

    with pytest.raises(ValueError, match="bindings differ"):
        render_local_candidate_review_browser(
            LocalCandidateReviewBrowserOptions(CATALOG, tmp_path / "browser", path)
        )


def test_browser_rejects_catalog_with_missing_or_duplicate_identity(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text())
    payload["items"][1]["candidateId"] = payload["items"][0]["candidateId"]
    catalog = tmp_path / "invalid.json"
    catalog.write_text(json.dumps(payload))

    with pytest.raises(ValueError, match="identity"):
        load_local_candidate_review_catalog(catalog)


@pytest.mark.parametrize("payload", [[], {"items": []}])
def test_browser_rejects_non_catalog_payloads(tmp_path: Path, payload: object) -> None:
    catalog = tmp_path / "invalid.json"
    catalog.write_text(json.dumps(payload))

    with pytest.raises(ValueError, match="catalog"):
        load_local_candidate_review_catalog(catalog)


def test_browser_rejects_item_with_invalid_warning_count(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text())
    payload["items"][0]["warningCount"] = -1
    catalog = tmp_path / "invalid.json"
    catalog.write_text(json.dumps(payload))

    with pytest.raises(ValueError, match="schema"):
        load_local_candidate_review_catalog(catalog)

    payload = json.loads(CATALOG.read_text())
    payload["items"][0]["corrected"] = "false"
    catalog.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="schema"):
        load_local_candidate_review_catalog(catalog)


def test_browser_rejects_schema_invalid_catalog_values(tmp_path: Path) -> None:
    payload = json.loads(CATALOG.read_text())
    payload["sourceBundleSha256"] = "not-a-digest"
    payload["items"][0]["ecosystem"] = 3
    catalog = tmp_path / "invalid.json"
    catalog.write_text(json.dumps(payload))

    with pytest.raises(ValueError, match="schema"):
        load_local_candidate_review_catalog(catalog)


def test_browser_cli_renders_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output = tmp_path / "browser"
    assert (
        main(
            [
                "render-local-candidate-review-browser",
                "--catalog",
                str(CATALOG),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["candidateCount"] == 100
    assert (output / "index.html").is_file()
