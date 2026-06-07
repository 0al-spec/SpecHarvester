from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.package_set_ai_enrichment import (
    PACKAGE_SET_AI_ENRICHMENT_API_VERSION,
    PACKAGE_SET_AI_ENRICHMENT_KIND,
    PackageSetAIEnrichmentOptions,
    build_package_set_ai_enrichment_proposal,
    model_request_records,
)
from spec_harvester.xyflow_package_set_smoke import (
    XyflowPackageSetSmokeOptions,
    run_xyflow_package_set_smoke,
)


def test_package_set_ai_enrichment_requests_include_compact_source_evidence(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)

    requests = model_request_records(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=smoke / "fixture" / "xyflow",
        )
    )

    react = next(request for request in requests if request["packageId"] == "xyflow.react")
    evidence_paths = {item["path"] for item in react["evidence"]}
    assert "xyflow.react/specpm.yaml" in evidence_paths
    assert "packages/react/package.json" in evidence_paths
    assert "packages/react/README.md" in evidence_paths
    assert "packages/react/src/index.ts" in evidence_paths
    assert react["allowedEvidencePaths"] == [item["path"] for item in react["evidence"]]
    assert "Do not merely repeat current generated capability ids" in " ".join(react["constraints"])


def test_package_set_ai_enrichment_wraps_external_model_output(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    model_output = write_model_output(smoke, unsupported_path=False)

    report = build_package_set_ai_enrichment_proposal(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=smoke / "fixture" / "xyflow",
            model_output=model_output,
        )
    )

    assert report["apiVersion"] == PACKAGE_SET_AI_ENRICHMENT_API_VERSION
    assert report["kind"] == PACKAGE_SET_AI_ENRICHMENT_KIND
    assert report["status"] == "completed"
    assert report["authority"] == "proposal_only_not_registry_acceptance"
    assert report["provider"]["execution"] == "not_run_by_spec_harvester"
    assert report["packageSet"]["id"] == "xyflow.workspace"
    assert report["privacy"]["rawPromptsPersisted"] is False
    assert "SpecPM remains" in " ".join(report["trustBoundary"])
    react = next(item for item in report["proposals"] if item["packageId"] == "xyflow.react")
    assert react["refinedSummary"].startswith("React Flow package")
    assert react["capabilities"][0]["id"] == "xyflow.react.flow_canvas"
    assert react["capabilities"][0]["evidencePaths"] == [
        "packages/react/README.md",
        "packages/react/src/index.ts",
    ]


def test_package_set_ai_enrichment_reports_unsupported_model_evidence_path(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    model_output = write_model_output(smoke, unsupported_path=True)

    report = build_package_set_ai_enrichment_proposal(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=smoke / "fixture" / "xyflow",
            model_output=model_output,
        )
    )

    assert report["status"] == "warning"
    assert "model_evidence_path_unsupported" in {item["code"] for item in report["diagnostics"]}


def test_package_set_ai_enrichment_cli_writes_requests_and_proposal(
    tmp_path: Path,
    capsys,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    model_output = write_model_output(smoke, unsupported_path=False)
    request_output = tmp_path / "ai" / "requests.json"
    proposal_output = tmp_path / "ai" / "proposal.json"

    exit_code = main(
        [
            "package-set-ai-enrichment-proposal",
            "--bundle-set",
            str(smoke / "package-set"),
            "--source-checkout",
            str(smoke / "fixture" / "xyflow"),
            "--model-output",
            str(model_output),
            "--request-output",
            str(request_output),
            "--output",
            str(proposal_output),
        ]
    )

    printed = json.loads(capsys.readouterr().out)
    written = json.loads(proposal_output.read_text(encoding="utf-8"))
    requests = json.loads(request_output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert printed == written
    assert written["status"] == "completed"
    assert requests["kind"] == "SpecHarvesterPackageSetAIEnrichmentRequests"
    assert len(requests["requests"]) == 4


def write_xyflow_smoke(tmp_path: Path) -> Path:
    smoke = tmp_path / "xyflow-smoke"
    report = run_xyflow_package_set_smoke(XyflowPackageSetSmokeOptions(output=smoke))
    assert report["status"] == "passed"
    return smoke


def add_source_export_fixture(smoke: Path) -> None:
    checkout = smoke / "fixture" / "xyflow"
    for package in ("react", "svelte", "system"):
        package_root = checkout / "packages" / package
        package_root.mkdir(parents=True, exist_ok=True)
        (package_root / "README.md").write_text(
            f"# {package}\n\nPublic {package} package evidence.\n",
            encoding="utf-8",
        )
    (checkout / "packages" / "react" / "src").mkdir(parents=True, exist_ok=True)
    (checkout / "packages" / "react" / "src" / "index.ts").write_text(
        "export { ReactFlow } from './ReactFlow';\nexport { useReactFlow } from './hooks';\n",
        encoding="utf-8",
    )
    (checkout / "packages" / "svelte" / "src" / "lib").mkdir(parents=True, exist_ok=True)
    (checkout / "packages" / "svelte" / "src" / "lib" / "index.ts").write_text(
        "export { SvelteFlow } from './SvelteFlow';\n",
        encoding="utf-8",
    )
    (checkout / "packages" / "system" / "src").mkdir(parents=True, exist_ok=True)
    (checkout / "packages" / "system" / "src" / "index.ts").write_text(
        "export * from './xypanzoom';\nexport * from './xydrag';\n",
        encoding="utf-8",
    )


def write_model_output(smoke: Path, *, unsupported_path: bool) -> Path:
    evidence_paths = ["packages/react/README.md", "packages/react/src/index.ts"]
    if unsupported_path:
        evidence_paths.append("packages/react/private-notes.md")
    payload = {
        "proposals": [
            {
                "packageId": "xyflow.workspace",
                "refinedSummary": "Workspace package-set entrypoint for xyflow.",
                "capabilities": [],
                "interfaces": [],
                "evidenceGaps": [],
                "overallConfidence": "medium",
            },
            {
                "packageId": "xyflow.react",
                "refinedSummary": "React Flow package for interactive node-based editors.",
                "capabilities": [
                    {
                        "id": "xyflow.react.flow_canvas",
                        "summary": "Render and control an interactive React flow canvas.",
                        "intentIds": ["intent.javascript.react_library"],
                        "evidencePaths": evidence_paths,
                        "confidence": "high",
                    }
                ],
                "interfaces": [
                    {
                        "id": "react.component.ReactFlow",
                        "kind": "component",
                        "summary": "Primary React component export.",
                        "evidencePaths": ["packages/react/src/index.ts"],
                        "confidence": "high",
                    }
                ],
                "evidenceGaps": [],
                "overallConfidence": "high",
            },
            {
                "packageId": "xyflow.svelte",
                "refinedSummary": "Svelte Flow package for interactive node-based editors.",
                "capabilities": [],
                "interfaces": [],
                "evidenceGaps": [],
                "overallConfidence": "medium",
            },
            {
                "packageId": "xyflow.system",
                "refinedSummary": "Shared framework-agnostic xyflow utility layer.",
                "capabilities": [],
                "interfaces": [],
                "evidenceGaps": [],
                "overallConfidence": "medium",
            },
        ]
    }
    path = smoke / "ai-model-output.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
