from __future__ import annotations

import json
from pathlib import Path

import yaml

from spec_harvester.ai_enrichment_candidate_patch import (
    AI_ENRICHMENT_CANDIDATE_PATCH_API_VERSION,
    AI_ENRICHMENT_CANDIDATE_PATCH_KIND,
    AIEnrichmentCandidatePatchOptions,
    build_ai_enrichment_candidate_patch,
)
from spec_harvester.candidate_bundle_preflight import (
    CandidateBundlePreflightOptions,
    run_candidate_bundle_preflight,
)
from spec_harvester.cli import main
from spec_harvester.producer_receipt import digest_record, sha256_file


def test_ai_enrichment_candidate_patch_applies_clean_proposal_to_copy(tmp_path: Path) -> None:
    candidate = write_candidate(tmp_path / "candidate")
    proposal = write_proposal(tmp_path / "ai" / "proposal.json")
    before = file_digests(candidate)

    report = build_ai_enrichment_candidate_patch(
        AIEnrichmentCandidatePatchOptions(
            proposal=proposal,
            candidate=candidate,
            output=tmp_path / "enriched" / "fastapi.core",
            package_id="fastapi.core",
        )
    )

    assert report["apiVersion"] == AI_ENRICHMENT_CANDIDATE_PATCH_API_VERSION
    assert report["kind"] == AI_ENRICHMENT_CANDIDATE_PATCH_KIND
    assert report["status"] == "prepared"
    assert report["subject"]["sourceMutated"] is False
    assert report["subject"]["previewOnly"] is True
    assert "not SpecPM registry acceptance" in " ".join(report["nonAuthority"])
    assert file_digests(candidate) == before

    enriched = tmp_path / "enriched" / "fastapi.core"
    manifest = yaml.safe_load((enriched / "specpm.yaml").read_text(encoding="utf-8"))
    spec = yaml.safe_load((enriched / "specs" / "fastapi.spec.yaml").read_text(encoding="utf-8"))
    assert manifest["preview_only"] is True
    assert manifest["metadata"]["summary"].startswith("FastAPI Core is")
    assert "fastapi.core.openapi_generation" in manifest["index"]["provides"]["capabilities"]
    capabilities = {item["id"]: item for item in spec["provides"]["capabilities"]}
    assert capabilities["fastapi.core"]["summary"].startswith("FastAPI Core is")
    assert capabilities["fastapi.core.openapi_generation"]["role"] == "secondary"
    assert capabilities["fastapi.core.openapi_generation"]["intentIds"] == [
        "intent.metadata.schema_validation"
    ]
    assert (
        "provides.capabilities.fastapi.core.openapi_generation" in spec["evidence"][0]["supports"]
    )
    interfaces = {item["id"]: item for item in spec["interfaces"]["inbound"]}
    assert interfaces["package.fastapi.core"]["summary"] == (
        "Public Python package exposing FastAPI framework APIs."
    )
    assert (enriched / "ai-enrichment-candidate-patch.json").is_file()

    preflight = run_candidate_bundle_preflight(CandidateBundlePreflightOptions(enriched))
    assert preflight["status"] == "passed"


def test_ai_enrichment_candidate_patch_cli_writes_report(tmp_path: Path) -> None:
    candidate = write_candidate(tmp_path / "candidate")
    proposal = write_proposal(tmp_path / "ai" / "proposal.json")
    output = tmp_path / "cli-output"
    report = tmp_path / "reports" / "patch.json"

    status = main(
        [
            "apply-ai-enrichment-proposal",
            "--proposal",
            str(proposal),
            "--candidate",
            str(candidate),
            "--package-id",
            "fastapi.core",
            "--output",
            str(output),
            "--report",
            str(report),
        ]
    )

    assert status == 0
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "prepared"
    assert payload["subject"]["enrichedCandidate"] == str(output.resolve())
    assert (output / "specpm.yaml").is_file()


def test_ai_enrichment_candidate_patch_rejects_warning_report(tmp_path: Path) -> None:
    candidate = write_candidate(tmp_path / "candidate")
    proposal = write_proposal(tmp_path / "ai" / "proposal.json", report_status="warning")

    status = main(
        [
            "apply-ai-enrichment-proposal",
            "--proposal",
            str(proposal),
            "--candidate",
            str(candidate),
            "--output",
            str(tmp_path / "out"),
        ]
    )

    assert status == 2
    assert not (tmp_path / "out").exists()


def test_ai_enrichment_candidate_patch_rejects_unresolved_package_diagnostics(
    tmp_path: Path,
) -> None:
    candidate = write_candidate(tmp_path / "candidate")
    proposal = write_proposal(
        tmp_path / "ai" / "proposal.json",
        diagnostics=[
            {
                "severity": "warning",
                "code": "model_evidence_path_unsupported",
                "message": "Unsupported evidence path.",
                "packageId": "fastapi.core",
            }
        ],
    )

    status = main(
        [
            "apply-ai-enrichment-proposal",
            "--proposal",
            str(proposal),
            "--candidate",
            str(candidate),
            "--output",
            str(tmp_path / "out"),
        ]
    )

    assert status == 2
    assert not (tmp_path / "out").exists()


def test_ai_enrichment_candidate_patch_rejects_package_id_mismatch(tmp_path: Path) -> None:
    candidate = write_candidate(tmp_path / "candidate", package_id="other.core")
    proposal = write_proposal(tmp_path / "ai" / "proposal.json")

    status = main(
        [
            "apply-ai-enrichment-proposal",
            "--proposal",
            str(proposal),
            "--candidate",
            str(candidate),
            "--package-id",
            "fastapi.core",
            "--output",
            str(tmp_path / "out"),
        ]
    )

    assert status == 2
    assert not (tmp_path / "out").exists()


def test_ai_enrichment_candidate_patch_rejects_output_inside_source(tmp_path: Path) -> None:
    candidate = write_candidate(tmp_path / "candidate")
    proposal = write_proposal(tmp_path / "ai" / "proposal.json")

    status = main(
        [
            "apply-ai-enrichment-proposal",
            "--proposal",
            str(proposal),
            "--candidate",
            str(candidate),
            "--package-id",
            "fastapi.core",
            "--output",
            str(candidate / "enriched"),
        ]
    )

    assert status == 2
    assert not (candidate / "enriched").exists()


def write_candidate(root: Path, *, package_id: str = "fastapi.core") -> Path:
    root.mkdir(parents=True)
    (root / "specs").mkdir()
    (root / "harvest.json").write_text('{"status":"ok"}\n', encoding="utf-8")
    (root / "validation-report.json").write_text(
        json.dumps({"status": "valid", "warningCount": 0, "errorCount": 0}) + "\n",
        encoding="utf-8",
    )
    (root / "diagnostics.json").write_text(
        json.dumps({"status": "clean", "entries": []}) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "apiVersion": "specpm.dev/v0.1",
        "kind": "SpecPackage",
        "metadata": {
            "id": package_id,
            "name": "Fastapi Core",
            "version": "0.1.0",
            "summary": "Generated FastAPI starter package.",
        },
        "preview_only": True,
        "specs": [{"path": "specs/fastapi.spec.yaml"}],
        "index": {
            "provides": {
                "capabilities": ["fastapi.core"],
                "intents": ["intent.web.http_routing"],
            },
            "requires": {"capabilities": []},
        },
    }
    spec = {
        "apiVersion": "specpm.dev/v0.1",
        "kind": "BoundarySpec",
        "metadata": {
            "id": "fastapi.core",
            "title": "Fastapi Core Generated Boundary",
            "version": "0.1.0",
            "status": "draft",
        },
        "intent": {"summary": "Generated FastAPI starter package."},
        "scope": {"boundedContext": "fastapi", "includes": [], "excludes": []},
        "provides": {
            "capabilities": [
                {
                    "id": "fastapi.core",
                    "role": "primary",
                    "summary": "Generated FastAPI starter package.",
                    "intentIds": ["intent.web.http_routing"],
                }
            ]
        },
        "requires": {"capabilities": []},
        "interfaces": {
            "inbound": [
                {
                    "id": "package.fastapi.core",
                    "kind": "library",
                    "summary": "Observed public interface for fastapi.core.",
                }
            ],
            "outbound": [],
        },
        "effects": {"sideEffects": []},
        "constraints": [],
        "evidence": [
            {
                "id": "semantic_intent_static_evidence",
                "kind": "documentation",
                "path": "harvest.json",
                "supports": ["intent.summary", "provides.capabilities"],
            }
        ],
    }
    write_yaml(root / "specpm.yaml", manifest)
    write_yaml(root / "specs" / "fastapi.spec.yaml", spec)
    write_receipt(root)
    return root


def write_receipt(root: Path) -> None:
    manifest = yaml.safe_load((root / "specpm.yaml").read_text(encoding="utf-8"))
    package_id = manifest["metadata"]["id"]
    receipt = {
        "apiVersion": "specpm.receipts/v0",
        "kind": "SpecPMProducerReceipt",
        "schemaVersion": 1,
        "receiptProfile": "generated_spec_package_v0",
        "subject": {
            "packageId": package_id,
            "packageVersion": "0.1.0",
            "packageApiVersion": "specpm.dev/v0.1",
            "packageRoot": ".",
            "boundarySpecs": ["specs/fastapi.spec.yaml"],
            "candidateStatus": "review-ready",
        },
        "producer": {"name": "SpecHarvester"},
        "inputs": [
            {
                "kind": "harvested_evidence",
                "path": "harvest.json",
                "location": "bundle",
                "digest": digest_record(sha256_file(root / "harvest.json")),
            }
        ],
        "configuration": {"mode": "test"},
        "outputs": [
            output(root, "diagnostics.json", "diagnostics"),
            output(root, "specpm.yaml", "manifest"),
            output(root, "specs/fastapi.spec.yaml", "boundary_spec"),
            output(root, "validation-report.json", "validation_report"),
        ],
        "validation": {
            "status": "valid",
            "warningCount": 0,
            "errorCount": 0,
            "reportPath": "validation-report.json",
            "reportDigest": digest_record(sha256_file(root / "validation-report.json")),
        },
        "diagnostics": {
            "status": "clean",
            "path": "diagnostics.json",
            "digest": digest_record(sha256_file(root / "diagnostics.json")),
        },
        "humanReview": {"status": "required", "requiredFor": ["public_index_acceptance"]},
    }
    (root / "producer-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def output(root: Path, path: str, role: str) -> dict[str, object]:
    return {"path": path, "role": role, "digest": digest_record(sha256_file(root / path))}


def write_proposal(
    path: Path,
    *,
    report_status: str = "completed",
    diagnostics: list[dict[str, object]] | None = None,
) -> Path:
    payload = {
        "apiVersion": "spec-harvester.package-set-ai-enrichment/v0",
        "kind": "SpecHarvesterPackageSetAIEnrichmentProposal",
        "schemaVersion": 1,
        "status": report_status,
        "authority": "proposal_only_not_registry_acceptance",
        "provider": {
            "name": "lm_studio",
            "model": "openai/gpt-oss-20b",
            "execution": "operator_opt_in_local",
        },
        "diagnostics": diagnostics or [],
        "proposals": [
            {
                "packageId": "fastapi.core",
                "status": "proposed",
                "refinedSummary": (
                    "FastAPI Core is a statically evidenced Python web framework "
                    "for HTTP routing and OpenAPI documentation."
                ),
                "overallConfidence": "high",
                "capabilities": [
                    {
                        "id": "fastapi.core.openapi_generation",
                        "summary": "Automatically generates OpenAPI schemas from Python types.",
                        "intentIds": ["intent.metadata.schema_validation"],
                        "evidencePaths": ["fastapi.core/specs/fastapi.spec.yaml"],
                        "confidence": "high",
                    }
                ],
                "interfaces": [
                    {
                        "id": "package.fastapi.core",
                        "kind": "library",
                        "summary": "Public Python package exposing FastAPI framework APIs.",
                        "evidencePaths": ["fastapi.core/specpm.yaml"],
                        "confidence": "high",
                    }
                ],
                "evidenceGaps": [],
                "providerReceipt": {
                    "responseDigest": "sha256:test",
                    "usage": {"total_tokens": 42},
                },
            }
        ],
    }
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_yaml(path: Path, value: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def file_digests(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
