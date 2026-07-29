from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.semantic_author_input_pack import (
    SemanticAuthorInputPackOptions,
    build_semantic_author_input_pack,
)


def catalog() -> dict:
    value = {
        "sourcePath": "catalog/observed-intents.json",
        "intents": [
            {
                "intentId": "intent.package.javascript_library",
                "sha256": "a" * 64,
            }
        ],
    }
    value["sha256"] = hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return value


def workspace(tmp_path: Path) -> Path:
    (tmp_path / "specs").mkdir(exist_ok=True)
    (tmp_path / "specpm.yaml").write_text(
        "apiVersion: specpm.dev/v0.1\nkind: SpecPackage\nmetadata:\n"
        "  id: demo.package\npreview_only: true\n",
        encoding="utf-8",
    )
    (tmp_path / "specs/core.spec.yaml").write_text(
        "apiVersion: specpm.dev/v0.1\nkind: BoundarySpec\n",
        encoding="utf-8",
    )
    (tmp_path / "harvest.json").write_text('{"source":{"repository":"demo"}}\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("Untrusted repository documentation.\n", encoding="utf-8")
    return tmp_path


def test_builds_deterministic_schema_valid_input_pack(tmp_path: Path) -> None:
    source = workspace(tmp_path)
    options = SemanticAuthorInputPackOptions(document_paths=("README.md",))

    first = build_semantic_author_input_pack(source, catalog(), options=options)
    second = build_semantic_author_input_pack(source, catalog(), options=options)

    assert first == second
    assert first["request"]["candidateId"] == "demo.package"
    assert first["observedIntents"][0]["state"] == "observed"
    assert {item["class"] for item in first["evidence"]} == {
        "validated_candidate_yaml",
        "harvested_repository_metadata",
        "allowlisted_source_documentation",
        "specpm_observed_intent_catalog",
    }
    assert all(
        item["sourceBundleSha256"] == first["sourceBundleSha256"] for item in first["evidence"]
    )
    assert next(item for item in first["evidence"] if item["sourcePath"] == "README.md")[
        "untrusted"
    ]
    assert all(value is False for value in first["executionBoundary"].values())


@pytest.mark.parametrize("path", ("../README.md", "/tmp/README.md"))
def test_rejects_unsafe_document_paths(tmp_path: Path, path: str) -> None:
    with pytest.raises(ValueError, match="unsafe evidence path"):
        build_semantic_author_input_pack(
            workspace(tmp_path),
            catalog(),
            options=SemanticAuthorInputPackOptions(document_paths=(path,)),
        )


def test_rejects_oversized_document_and_stale_catalog(tmp_path: Path) -> None:
    source = workspace(tmp_path)
    (source / "README.md").write_text("x" * 33, encoding="utf-8")
    with pytest.raises(ValueError, match="documentation evidence exceeds byte budget"):
        build_semantic_author_input_pack(
            source,
            catalog(),
            options=SemanticAuthorInputPackOptions(
                document_paths=("README.md",), max_document_bytes=32
            ),
        )
    stale = catalog()
    stale["intents"].append({"intentId": "intent.other", "sha256": "b" * 64})
    with pytest.raises(ValueError, match="catalog digest is stale"):
        build_semantic_author_input_pack(source, stale)


def test_rejects_duplicate_catalog_intent_and_budget_exhaustion(tmp_path: Path) -> None:
    duplicate = catalog()
    duplicate["intents"].append(dict(duplicate["intents"][0]))
    duplicate["sha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in duplicate.items() if key != "sha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="duplicate intent ID"):
        build_semantic_author_input_pack(workspace(tmp_path), duplicate)
    with pytest.raises(ValueError, match="evidence item budget exceeded"):
        build_semantic_author_input_pack(
            workspace(tmp_path),
            catalog(),
            options=SemanticAuthorInputPackOptions(max_evidence_items=1),
        )


@pytest.mark.parametrize(
    ("path", "content", "message"),
    [
        ("specpm.yaml", "kind: Other\n", "preview-only SpecPackage"),
        ("specpm.yaml", "kind: SpecPackage\npreview_only: true\n", "metadata.id"),
        ("specs/core.spec.yaml", "kind: Other\n", "must be a BoundarySpec"),
        ("harvest.json", "[]", "harvest.json must be an object"),
    ],
)
def test_rejects_malformed_candidate_artifacts(
    tmp_path: Path, path: str, content: str, message: str
) -> None:
    source = workspace(tmp_path)
    (source / path).write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        build_semantic_author_input_pack(source, catalog())


def test_rejects_invalid_options_and_catalog_limit(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="budgets must be positive"):
        build_semantic_author_input_pack(
            workspace(tmp_path),
            catalog(),
            options=SemanticAuthorInputPackOptions(max_total_bytes=0),
        )
    oversized = catalog()
    oversized["intents"].append({"intentId": "intent.other", "sha256": "b" * 64})
    oversized["sha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in oversized.items() if key != "sha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    with pytest.raises(ValueError, match="catalog item budget exceeded"):
        build_semantic_author_input_pack(
            workspace(tmp_path),
            oversized,
            options=SemanticAuthorInputPackOptions(max_observed_intents=1),
        )
