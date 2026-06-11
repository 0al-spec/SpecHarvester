from __future__ import annotations

import json
import urllib.request
from pathlib import Path

import pytest

from spec_harvester.cli import main
from spec_harvester.package_set_ai_enrichment import (
    PACKAGE_SET_AI_ENRICHMENT_API_VERSION,
    PACKAGE_SET_AI_ENRICHMENT_KIND,
    OpenAICompatibleProvider,
    PackageSetAIEnrichmentError,
    PackageSetAIEnrichmentOptions,
    build_package_set_ai_enrichment_proposal,
    model_request_records,
    normalize_local_provider_base_url,
    parse_model_json_object,
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


def test_package_set_ai_enrichment_rejects_escaping_manifest_source(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    checkout = smoke / "fixture" / "xyflow"
    private_notes = checkout / "packages" / "private-notes.md"
    private_notes.write_text("must not reach model input\n", encoding="utf-8")
    react_manifest = checkout / "packages" / "react" / "package.json"
    manifest_payload = json.loads(react_manifest.read_text(encoding="utf-8"))
    manifest_payload["source"] = "../private-notes.md"
    react_manifest.write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    requests = model_request_records(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=checkout,
        )
    )

    react = next(request for request in requests if request["packageId"] == "xyflow.react")
    evidence_paths = {item["path"] for item in react["evidence"]}
    evidence_text = "\n".join(item["text"] for item in react["evidence"])
    assert "packages/private-notes.md" not in evidence_paths
    assert "must not reach model input" not in evidence_text


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
    assert report["stopPolicySummary"]["decision"] == "stop_for_author_review"
    assert report["stopPolicySummary"]["subjectCount"] == 4
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
    assert react["interfaces"][0]["kind"] == "component"
    assert "intentIds" not in react["interfaces"][0]


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
    assert report["stopPolicySummary"]["decision"] == "continue_generation"
    assert "model_evidence_path_unsupported" in {item["code"] for item in report["diagnostics"]}
    react = next(item for item in report["proposals"] if item["packageId"] == "xyflow.react")
    assert react["capabilities"][0]["evidencePaths"] == [
        "packages/react/README.md",
        "packages/react/src/index.ts",
    ]


def test_package_set_ai_enrichment_normalizes_package_local_evidence_paths(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    model_output = write_model_output(smoke, unsupported_path=False)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    react = next(item for item in payload["proposals"] if item["packageId"] == "xyflow.react")
    react["interfaces"][0]["evidencePaths"] = ["harvest.json"]
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_enrichment_proposal(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=smoke / "fixture" / "xyflow",
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert "model_evidence_path_unsupported" not in {item["code"] for item in report["diagnostics"]}
    react = next(item for item in report["proposals"] if item["packageId"] == "xyflow.react")
    assert react["interfaces"][0]["evidencePaths"] == ["xyflow.react/harvest.json"]


def test_package_set_ai_enrichment_trims_package_local_evidence_paths(
    tmp_path: Path,
) -> None:
    smoke = write_xyflow_smoke(tmp_path)
    add_source_export_fixture(smoke)
    model_output = write_model_output(smoke, unsupported_path=False)
    payload = json.loads(model_output.read_text(encoding="utf-8"))
    react = next(item for item in payload["proposals"] if item["packageId"] == "xyflow.react")
    react["interfaces"][0]["evidencePaths"] = [" harvest.json\n", "   "]
    model_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = build_package_set_ai_enrichment_proposal(
        PackageSetAIEnrichmentOptions(
            bundle_set=smoke / "package-set",
            source_checkout=smoke / "fixture" / "xyflow",
            model_output=model_output,
        )
    )

    assert report["status"] == "completed"
    assert "model_evidence_path_unsupported" not in {item["code"] for item in report["diagnostics"]}
    react = next(item for item in report["proposals"] if item["packageId"] == "xyflow.react")
    assert react["interfaces"][0]["evidencePaths"] == ["xyflow.react/harvest.json"]


def test_openai_compatible_provider_receipt_uses_configured_provider_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeResponse:
        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "model": "test-model",
                    "choices": [{"message": {"content": '{"packageId":"xyflow.react"}'}}],
                    "usage": {"total_tokens": 7},
                }
            ).encode("utf-8")

    monkeypatch.setattr(urllib.request, "urlopen", lambda *_args, **_kwargs: FakeResponse())
    provider = OpenAICompatibleProvider(
        base_url="http://localhost:1234",
        provider_name="local_test_provider",
        model="test-model",
        timeout_seconds=1,
        max_output_tokens=128,
        temperature=0,
    )

    _payload, receipt = provider.complete_json({"packageId": "xyflow.react"})
    assert receipt["providerName"] == "local_test_provider"


def test_parse_model_json_object_wraps_invalid_json() -> None:
    try:
        parse_model_json_object("not json")
    except PackageSetAIEnrichmentError as exc:
        assert "valid JSON" in str(exc)
    else:
        raise AssertionError("expected PackageSetAIEnrichmentError")


def test_normalize_local_provider_base_url_rejects_extra_url_components() -> None:
    for value in (
        "http://user:pass@localhost:1234",
        "http://localhost:1234?token=secret",
        "http://localhost:1234#fragment",
        "http://localhost:1234;params",
    ):
        try:
            normalize_local_provider_base_url(value)
        except ValueError:
            continue
        raise AssertionError(f"expected local provider URL rejection for {value}")


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
