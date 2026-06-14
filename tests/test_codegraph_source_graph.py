from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.codegraph_source_graph import (
    CodeGraphSourceGraphOptions,
    build_codegraph_source_graph_index,
)


def test_codegraph_json_evidence_normalizes_source_graph_index(
    tmp_path: Path,
) -> None:
    evidence = tmp_path / "codegraph.json"
    evidence.write_text(
        json.dumps(
            {
                "files": [
                    {
                        "path": "Sources/App.swift",
                        "language": "swift",
                        "contentHash": "sha256:abc",
                        "sizeBytes": 120,
                    }
                ],
                "nodes": [
                    {
                        "id": "node-1",
                        "type": "struct",
                        "name": "App",
                        "qualifiedName": "App",
                        "filePath": "Sources/App.swift",
                        "language": "swift",
                        "startLine": 1,
                        "endLine": 5,
                    }
                ],
                "edges": [
                    {
                        "sourceId": "node-1",
                        "targetId": "node-2",
                        "type": "contains",
                        "provenance": "tree-sitter",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    payload = build_codegraph_source_graph_index(
        CodeGraphSourceGraphOptions(
            input=evidence,
            input_format="json",
            source_repository="https://github.com/example/app",
            source_revision="abc123",
            source_target_kind="folder",
            source_target_path="Sources",
            analyzer_version="0.9.7",
            max_nodes=1,
            max_edges=1,
        )
    )

    assert payload["schemaVersion"] == "spec-harvester-codegraph-v1"
    assert payload["kind"] == "source_graph_index"
    assert payload["trust"] == {
        "analyzer": "codegraph",
        "analyzerVersion": "0.9.7",
        "analyzerLicense": "MIT",
        "trustLevel": "untrusted_optional_tool",
        "classification": "third_party_local_binary",
        "executedRepositoryCode": False,
        "allowedNetwork": False,
        "installation": "out_of_band_required",
    }
    assert payload["source"]["target"] == {"kind": "folder", "path": "Sources"}
    assert payload["source"]["sourceDigests"] == [
        {"path": "Sources/App.swift", "sha256": "sha256:abc"}
    ]
    assert payload["summary"] == {
        "fileCount": 1,
        "nodeCount": 1,
        "edgeCount": 1,
        "languages": ["swift"],
        "truncated": False,
    }
    assert payload["nodes"][0]["range"] == {"startLine": 1, "endLine": 5}
    assert payload["edges"][0]["kind"] == "contains"


def test_codegraph_sqlite_evidence_normalizes_without_running_codegraph(
    tmp_path: Path,
) -> None:
    database = tmp_path / "codegraph.db"
    connection = sqlite3.connect(database)
    try:
        connection.execute(
            "create table files (path text, language text, sha256 text, size_bytes integer)"
        )
        connection.execute("insert into files values ('src/main.py', 'python', 'sha256:def', 42)")
        connection.execute(
            "create table nodes (id text, kind text, name text, file_path text, language text)"
        )
        connection.execute(
            "insert into nodes values ('node-1', 'function', 'main', 'src/main.py', 'python')"
        )
        connection.execute(
            "create table edges (source text, target text, kind text, provenance text)"
        )
        connection.execute("insert into edges values ('node-1', 'node-2', 'calls', 'heuristic')")
        connection.commit()
    finally:
        connection.close()

    payload = build_codegraph_source_graph_index(
        CodeGraphSourceGraphOptions(input=database, input_format="sqlite")
    )

    assert payload["summary"]["fileCount"] == 1
    assert payload["summary"]["languages"] == ["python"]
    assert payload["files"][0]["path"] == "src/main.py"
    assert payload["nodes"][0]["kind"] == "function"
    assert payload["edges"][0]["kind"] == "calls"
    assert payload["trust"]["executedRepositoryCode"] is False


def test_codegraph_source_graph_rejects_unsafe_paths(tmp_path: Path) -> None:
    evidence = tmp_path / "codegraph.json"
    evidence.write_text(
        json.dumps({"files": [{"path": "../secret.py", "language": "python"}]}),
        encoding="utf-8",
    )

    try:
        build_codegraph_source_graph_index(
            CodeGraphSourceGraphOptions(input=evidence, input_format="json")
        )
    except ValueError as exc:
        assert "Unsafe CodeGraph path" in str(exc)
    else:
        raise AssertionError("Expected unsafe CodeGraph path to be rejected")


def test_codegraph_source_graph_rejects_backslash_paths(tmp_path: Path) -> None:
    evidence = tmp_path / "codegraph.json"
    evidence.write_text(
        json.dumps({"files": [{"path": "src\\main.py", "language": "python"}]}),
        encoding="utf-8",
    )

    try:
        build_codegraph_source_graph_index(
            CodeGraphSourceGraphOptions(input=evidence, input_format="json")
        )
    except ValueError as exc:
        assert "Unsafe CodeGraph path" in str(exc)
    else:
        raise AssertionError("Expected backslash CodeGraph path to be rejected")


def test_codegraph_source_graph_cli_writes_output_and_errors_as_json(
    tmp_path: Path,
    capsys,
) -> None:
    evidence = tmp_path / "codegraph.json"
    output = tmp_path / "source-graph-index.json"
    evidence.write_text(json.dumps({"files": [], "nodes": [], "edges": []}), encoding="utf-8")

    result = main(
        [
            "codegraph-source-graph-index",
            "--input",
            str(evidence),
            "--input-format",
            "json",
            "--output",
            str(output),
            "--source-target-kind",
            "file",
            "--source-target-path",
            "src/main.py",
        ]
    )

    assert result == 0
    stdout_payload = json.loads(capsys.readouterr().out)
    output_payload = json.loads(output.read_text(encoding="utf-8"))
    assert stdout_payload == output_payload
    assert output_payload["source"]["target"] == {"kind": "file", "path": "src/main.py"}

    missing_result = main(
        [
            "codegraph-source-graph-index",
            "--input",
            str(tmp_path / "missing.json"),
            "--input-format",
            "json",
        ]
    )
    error_payload = json.loads(capsys.readouterr().out)
    assert missing_result == 2
    assert error_payload["status"] == "error"
    assert "does not exist" in error_payload["message"]
