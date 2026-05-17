from __future__ import annotations

import json

import pytest

from spec_harvester.interface_index import (
    PUBLIC_INTERFACE_INDEX_KIND,
    PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION,
    analyzer_record,
    evidence_record,
    new_public_interface_index,
    public_interface_index_errors,
    render_public_interface_index_json,
    validate_public_interface_index,
)


def test_public_interface_index_minimal_shape_is_deterministic() -> None:
    index = new_public_interface_index(
        source_revision="abc123",
        analyzers=[
            analyzer_record(
                analyzer_id="python-ast-public-api",
                version="0.1.0",
                execution="none",
                confidence="high",
            )
        ],
    )

    assert index == {
        "schemaVersion": PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION,
        "kind": PUBLIC_INTERFACE_INDEX_KIND,
        "sourceRevision": "abc123",
        "analyzers": [
            {
                "id": "python-ast-public-api",
                "version": "0.1.0",
                "execution": "none",
                "networkAccess": "none",
                "packageScripts": "not_run",
                "confidence": "high",
            }
        ],
        "packages": [],
        "diagnostics": [],
        "summary": {
            "packageCount": 0,
            "entrypointCount": 0,
            "symbolCount": 0,
            "diagnosticCount": 0,
        },
    }
    assert json.loads(render_public_interface_index_json(index)) == index
    assert render_public_interface_index_json(index) == render_public_interface_index_json(index)


def test_public_interface_index_validates_package_entrypoint_symbol_evidence() -> None:
    index = new_public_interface_index(
        source_revision="abc123",
        analyzers=[analyzer_record("typescript-export-indexer", "0.1.0")],
        packages=[
            {
                "id": "@example/core",
                "path": "packages/core",
                "language": "typescript",
                "entrypoints": [
                    {
                        "path": "packages/core/src/index.ts",
                        "symbols": [
                            {
                                "name": "createGraph",
                                "kind": "function",
                                "visibility": "public",
                                "signature": "createGraph(nodes: Node[]): Graph",
                                "evidence": evidence_record(
                                    "packages/core/src/index.ts",
                                    "a" * 64,
                                ),
                            }
                        ],
                    }
                ],
            }
        ],
    )

    validate_public_interface_index(index)
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 1,
        "diagnosticCount": 0,
    }


def test_public_interface_index_rejects_bad_top_level_shape() -> None:
    index = new_public_interface_index()
    index["kind"] = "WrongKind"
    index["schemaVersion"] = "1"

    errors = public_interface_index_errors(index)

    assert "kind must be SpecHarvesterPublicInterfaceIndex" in errors
    assert "schemaVersion must be 1" in errors
    with pytest.raises(ValueError, match="Invalid PublicInterfaceIndex"):
        validate_public_interface_index(index)


def test_public_interface_index_rejects_non_object_and_missing_lists() -> None:
    assert public_interface_index_errors([]) == ["index must be an object"]  # type: ignore[arg-type]

    errors = "\n".join(
        public_interface_index_errors(
            {
                "schemaVersion": PUBLIC_INTERFACE_INDEX_SCHEMA_VERSION,
                "kind": PUBLIC_INTERFACE_INDEX_KIND,
                "sourceRevision": 123,
                "summary": {},
            }
        )
    )

    assert "sourceRevision must be a string or null" in errors
    assert "analyzers must be a list" in errors
    assert "packages must be a list" in errors
    assert "diagnostics must be a list" in errors
    assert "summary must equal" in errors


def test_public_interface_index_rejects_unsafe_analyzer_policy() -> None:
    index = new_public_interface_index(
        analyzers=[
            {
                "id": "unsafe",
                "version": "0.1.0",
                "execution": "package_script",
                "networkAccess": "full",
                "packageScripts": "run",
                "confidence": "certain",
            }
        ]
    )

    errors = public_interface_index_errors(index)

    assert "analyzers[0].execution must be one of" in "\n".join(errors)
    assert "analyzers[0].networkAccess must be one of" in "\n".join(errors)
    assert "analyzers[0].packageScripts must be one of" in "\n".join(errors)
    assert "analyzers[0].confidence must be one of" in "\n".join(errors)


def test_public_interface_index_rejects_non_object_nested_records() -> None:
    index = new_public_interface_index(
        analyzers=["not-an-object"],  # type: ignore[list-item]
        packages=[
            "not-an-object",  # type: ignore[list-item]
            {
                "id": "@example/core",
                "path": "packages/core",
                "language": 1,
                "entrypoints": "not-a-list",
            },
            {
                "id": "@example/ui",
                "path": "packages/ui",
                "entrypoints": [
                    "not-an-object",
                    {
                        "path": "packages/ui/src/index.ts",
                        "symbols": "not-a-list",
                    },
                    {
                        "path": "packages/ui/src/empty.ts",
                        "symbols": ["not-an-object"],
                    },
                ],
            },
        ],
        diagnostics=["not-an-object"],  # type: ignore[list-item]
    )

    errors = "\n".join(public_interface_index_errors(index))

    assert "analyzers[0] must be an object" in errors
    assert "packages[0] must be an object" in errors
    assert "packages[1].language must be a string" in errors
    assert "packages[1].entrypoints must be a list" in errors
    assert "packages[2].entrypoints[0] must be an object" in errors
    assert "packages[2].entrypoints[1].symbols must be a list" in errors
    assert "packages[2].entrypoints[2].symbols[0] must be an object" in errors
    assert "diagnostics[0] must be an object" in errors


def test_public_interface_index_rejects_malformed_symbol_evidence() -> None:
    index = new_public_interface_index(
        packages=[
            {
                "id": "@example/core",
                "path": "packages/core",
                "entrypoints": [
                    {
                        "path": "packages/core/src/index.ts",
                        "symbols": [
                            {
                                "name": "createGraph",
                                "kind": "macro",
                                "visibility": "public",
                                "evidence": {"path": "", "sha256": "short"},
                            }
                        ],
                    }
                ],
            }
        ],
        diagnostics=[{"level": "fatal", "message": ""}],
    )

    errors = "\n".join(public_interface_index_errors(index))

    assert "packages[0].entrypoints[0].symbols[0].kind must be one of" in errors
    assert "packages[0].entrypoints[0].symbols[0].evidence.path must be non-empty" in errors
    assert (
        "packages[0].entrypoints[0].symbols[0].evidence.sha256 must be a sha256 hex digest"
        in errors
    )
    assert "diagnostics[0].level must be one of" in errors
    assert "diagnostics[0].message must be non-empty" in errors


def test_public_interface_index_rejects_optional_field_type_errors() -> None:
    index = new_public_interface_index(
        packages=[
            {
                "id": "@example/core",
                "path": "packages/core",
                "entrypoints": [
                    {
                        "path": "packages/core/src/index.ts",
                        "symbols": [
                            {
                                "name": "",
                                "kind": "unknown",
                                "visibility": "",
                                "signature": 1,
                                "doc": 2,
                                "evidence": [],
                            }
                        ],
                    }
                ],
            }
        ],
        diagnostics=[
            {
                "level": "warning",
                "message": "parse warning",
                "path": "",
                "evidence": [],
            },
            {
                "level": "info",
                "message": "parse note",
                "evidence": {"path": "README.md", "sha256": "bad"},
            },
        ],
    )

    errors = "\n".join(public_interface_index_errors(index))

    assert "packages[0].entrypoints[0].symbols[0].name must be non-empty" in errors
    assert "packages[0].entrypoints[0].symbols[0].visibility must be non-empty" in errors
    assert "packages[0].entrypoints[0].symbols[0].signature must be a string" in errors
    assert "packages[0].entrypoints[0].symbols[0].doc must be a string" in errors
    assert "packages[0].entrypoints[0].symbols[0].evidence must be an object" in errors
    assert "diagnostics[0].path must be non-empty when present" in errors
    assert "diagnostics[0].evidence must be an object" in errors
    assert "diagnostics[1].evidence.sha256 must be a sha256 hex digest" in errors
