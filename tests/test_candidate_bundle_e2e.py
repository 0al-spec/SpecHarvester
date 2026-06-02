from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.collector import HarvestOptions, collect_local_repository
from spec_harvester.drafter import DraftOptions, draft_spec_package
from spec_harvester.static_spec_renderer import write_static_spec_site


def test_candidate_bundle_e2e_smoke_collects_drafts_preflights_and_renders(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "fixture-repo"
    repo.mkdir()
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@example/candidate-bundle",
                "version": "1.2.3",
                "description": "Reviewable candidate bundle workflow fixture.",
                "license": "MIT",
                "exports": {".": "./src/index.js"},
            }
        ),
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        "# Candidate Bundle\n\nBuilds reviewable SpecPM candidate bundles.\n",
        encoding="utf-8",
    )
    (repo / "LICENSE").write_text(
        "MIT License\n\nPermission is hereby granted, free of charge.\nCopyright Example.\n",
        encoding="utf-8",
    )
    (repo / "src").mkdir()
    (repo / "src" / "index.js").write_text(
        "export function buildCandidateBundle() { return true; }\n",
        encoding="utf-8",
    )

    snapshot = collect_local_repository(
        HarvestOptions(
            source=repo,
            repository="https://github.com/example/candidate-bundle",
            revision="abc123",
        )
    )
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "harvest.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    draft = draft_spec_package(
        DraftOptions(
            snapshot=candidate,
            out=candidate,
            package_id="example.candidate_bundle",
        )
    )
    preflight = run_candidate_bundle_preflight(CandidateBundlePreflightOptions(candidate=candidate))
    site = write_static_spec_site(candidate, tmp_path / "site")

    receipt = json.loads((candidate / "producer-receipt.json").read_text(encoding="utf-8"))
    validation = json.loads((candidate / "validation-report.json").read_text(encoding="utf-8"))
    diagnostics = json.loads((candidate / "diagnostics.json").read_text(encoding="utf-8"))
    rendered = json.loads((tmp_path / "site" / "spec-package.json").read_text(encoding="utf-8"))

    assert draft["status"] == "ok"
    assert draft["producerReceipt"] == str(candidate / "producer-receipt.json")
    assert draft["validationReport"] == str(candidate / "validation-report.json")
    assert draft["diagnosticsReport"] == str(candidate / "diagnostics.json")
    assert preflight["status"] == "passed"
    assert preflight["summary"] == {"diagnosticCount": 0, "errorCount": 0, "warningCount": 0}
    assert site["status"] == "ok"
    assert site["written"] == [
        "assets/spec-renderer.css",
        "assets/spec-renderer.js",
        "index.html",
        "spec-package.json",
    ]

    assert receipt["subject"]["packageId"] == "example.candidate_bundle"
    assert receipt["validation"]["status"] == validation["status"]
    assert receipt["diagnostics"]["status"] == diagnostics["status"]
    assert receipt["humanReview"] == {
        "handoff": "pull_request",
        "requiredFor": ["public_index_acceptance"],
        "status": "required",
    }
    assert "producer-receipt.json" not in {item["path"] for item in receipt["outputs"]}

    rendered_producer = rendered["producer"]
    assert rendered["package"]["id"] == receipt["subject"]["packageId"]
    assert rendered["package"]["id"] == validation["subject"]["packageId"]
    assert rendered_producer["status"] == "available"
    assert rendered_producer["subject"]["packageId"] == receipt["subject"]["packageId"]
    assert rendered_producer["validation"]["status"] == receipt["validation"]["status"]
    assert rendered_producer["diagnostics"]["status"] == receipt["diagnostics"]["status"]
    assert rendered_producer["humanReview"] == receipt["humanReview"]
    assert rendered_producer["outputs"] == receipt["outputs"]
    assert "not SpecPM acceptance" in rendered_producer["trustBoundary"]
