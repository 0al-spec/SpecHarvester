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
    assert "innerHTML" not in script
    assert "localStorage" in script
    assert json.loads((tmp_path / "browser/catalog.json").read_text())["items"]


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
