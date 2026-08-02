from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.semantic_product_profile import (
    build_semantic_product_profile,
    validate_semantic_product_profile,
    write_semantic_product_profile,
)


def document(evidence_path: str, source_path: str, content: bytes) -> dict:
    return {
        "evidencePath": evidence_path,
        "sourcePath": source_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "byteCount": len(content),
        "harvestSha256": "f" * 64,
    }


def harvest() -> dict:
    return {
        "source": {
            "repository": "https://github.com/n8n-io/n8n",
            "revision": "a" * 40,
            "target": {
                "kind": "folder",
                "path": "packages/@n8n/agents",
                "label": "agents",
            },
        },
        "projectProfile": {
            "languages": [
                {
                    "id": "javascript",
                    "confidence": "high",
                    "evidencePaths": ["packages/@n8n/agents/package.json"],
                }
            ],
            "ecosystems": [
                {
                    "id": "npm",
                    "language": "javascript",
                    "packageManager": "pnpm",
                    "confidence": "high",
                    "evidencePaths": ["packages/@n8n/agents/package.json"],
                }
            ],
            "manifests": [{"path": "packages/@n8n/agents/package.json"}],
            "analyzerPlan": [{"id": "javascript.public_api"}],
        },
        "files": [
            {
                "path": "packages/@n8n/agents/package.json",
                "package": {
                    "name": "@n8n/agents",
                    "description": "AI agent SDK for a code-first execution engine",
                },
            }
        ],
    }


def test_builds_digest_bound_nested_package_product_profile(tmp_path: Path) -> None:
    profile = build_semantic_product_profile(
        repository_id="n8n-io-n8n",
        candidate_id="n8n_io_n8n.agents",
        harvest=harvest(),
        root_document=document("README.md", "README.md", b"n8n workflow automation"),
        package_document=document(
            "PACKAGE_README.md",
            "packages/@n8n/agents/README.md",
            b"Build AI agents",
        ),
        manifest_metadata={
            "sourcePath": "packages/@n8n/agents/package.json",
            "sha256": "b" * 64,
            "name": "@n8n/agents",
            "description": "AI agent SDK for n8n's code-first execution engine",
            "keywords": ["agents", "workflow", "agents"],
        },
    )

    assert profile["repository"]["owner"] == "n8n-io"
    assert profile["repository"]["name"] == "n8n"
    assert profile["package"]["role"] == "member_package"
    assert profile["package"]["targetPath"] == "packages/@n8n/agents"
    assert profile["package"]["description"].startswith("AI agent SDK")
    assert profile["package"]["descriptionProvenance"] == {
        "sourcePath": "packages/@n8n/agents/package.json",
        "sha256": "b" * 64,
        "field": "description",
        "normalizedValueSha256": hashlib.sha256(
            b"AI agent SDK for n8n's code-first execution engine"
        ).hexdigest(),
        "extractor": "pinned_manifest_metadata/v1",
    }
    assert profile["package"]["keywords"] == ["agents", "workflow"]
    assert profile["technology"]["languages"][0]["id"] == "javascript"
    assert profile["technology"]["analyzerSignals"] == ["javascript.public_api"]
    assert [item["role"] for item in profile["documents"]] == [
        "repository_root",
        "package_local",
    ]
    output = tmp_path / "profile.json"
    write_semantic_product_profile(output, profile)
    assert output.read_text().endswith("\n")


def test_shared_root_and_package_document_reuse_one_source_binding() -> None:
    shared = document("README.md", "packages/demo/README.md", b"Shared purpose")
    package = document("PACKAGE_README.md", "packages/demo/README.md", b"Shared purpose")

    profile = build_semantic_product_profile(
        repository_id="demo",
        candidate_id="demo.core",
        harvest={"source": {"target": {"path": "packages/demo"}}},
        root_document=shared,
        package_document=package,
    )

    assert [item["role"] for item in profile["documents"]] == [
        "repository_root",
        "package_local",
    ]
    assert [item for item in profile["sourceBindings"] if item["sourcePath"] != "harvest.json"] == [
        {
            "sourcePath": "packages/demo/README.md",
            "sha256": hashlib.sha256(b"Shared purpose").hexdigest(),
        }
    ]


def test_profile_validation_rejects_stale_digest_and_unsafe_paths() -> None:
    profile = build_semantic_product_profile(
        repository_id="demo",
        candidate_id="demo.core",
        harvest={"source": {"target": {"path": "."}}},
        root_document=document("README.md", "README.md", b"Demo"),
    )
    stale = copy.deepcopy(profile)
    stale["package"]["description"] = "changed"
    with pytest.raises(ValueError, match="digest is stale"):
        validate_semantic_product_profile(stale)

    invalid = copy.deepcopy(profile)
    invalid["documents"][0]["sourcePath"] = "../README.md"
    invalid["profileSha256"] = digest_without_profile_sha(invalid)
    with pytest.raises(ValueError, match="unsafe semantic product profile path"):
        validate_semantic_product_profile(invalid)

    invalid_binding = copy.deepcopy(profile)
    invalid_binding["sourceBindings"][0]["sha256"] = "bad"
    invalid_binding["profileSha256"] = digest_without_profile_sha(invalid_binding)
    with pytest.raises(ValueError, match="source binding is malformed"):
        validate_semantic_product_profile(invalid_binding)


def test_profile_rejects_invalid_identity_and_document_digest() -> None:
    with pytest.raises(ValueError, match="identity is invalid"):
        build_semantic_product_profile(
            repository_id="",
            candidate_id="demo.core",
            harvest={},
            root_document=document("README.md", "README.md", b"Demo"),
        )
    broken = document("README.md", "README.md", b"Demo")
    broken["sha256"] = "bad"
    with pytest.raises(ValueError, match="document digest is invalid"):
        build_semantic_product_profile(
            repository_id="demo",
            candidate_id="demo.core",
            harvest={},
            root_document=broken,
        )


def test_profile_rejects_missing_harvest_and_manifest_bindings() -> None:
    missing_harvest = document("README.md", "README.md", b"Demo")
    missing_harvest.pop("harvestSha256")
    with pytest.raises(ValueError, match="harvest binding is invalid"):
        build_semantic_product_profile(
            repository_id="demo",
            candidate_id="demo.core",
            harvest={},
            root_document=missing_harvest,
        )

    with pytest.raises(ValueError, match="manifest binding is invalid"):
        build_semantic_product_profile(
            repository_id="demo",
            candidate_id="demo.core",
            harvest={},
            root_document=document("README.md", "README.md", b"Demo"),
            manifest_metadata={"sha256": "b" * 64},
        )


def test_python_39_toml_backport_is_declared() -> None:
    pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text()

    assert "tomli>=1.1.0; python_version < '3.11'" in pyproject


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda value: value.update({"kind": "Wrong"}), "identity is invalid"),
        (lambda value: value.update({"sourceBindings": []}), "content is malformed"),
        (
            lambda value: value["sourceBindings"].__setitem__(0, "bad"),
            "source binding is malformed",
        ),
        (
            lambda value: value["documents"][0].update({"untrusted": False}),
            "document binding is malformed",
        ),
        (
            lambda value: value["documents"][0].update({"byteCount": -1}),
            "document digest is invalid",
        ),
        (
            lambda value: value["package"].update({"manifestSha256": "b" * 64}),
            "manifest binding is invalid",
        ),
    ],
)
def test_profile_validation_fails_closed_on_malformed_records(mutate, message: str) -> None:
    profile = build_semantic_product_profile(
        repository_id="demo",
        candidate_id="demo.core",
        harvest={"source": {"target": {"path": "."}}},
        root_document=document("README.md", "README.md", b"Demo"),
    )
    mutate(profile)
    profile["profileSha256"] = digest_without_profile_sha(profile)

    with pytest.raises(ValueError, match=message):
        validate_semantic_product_profile(profile)


def digest_without_profile_sha(profile: dict) -> str:
    value = {key: item for key, item in profile.items() if key != "profileSha256"}
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
