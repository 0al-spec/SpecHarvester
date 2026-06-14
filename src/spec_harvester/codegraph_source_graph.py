from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

SOURCE_GRAPH_SCHEMA_VERSION = "spec-harvester-codegraph-v1"
SOURCE_GRAPH_KIND = "source_graph_index"
DEFAULT_CODEGRAPH_ANALYZER = "codegraph"
DEFAULT_CODEGRAPH_LICENSE = "MIT"
DEFAULT_MAX_NODES = 500
DEFAULT_MAX_EDGES = 1_000


@dataclass(frozen=True)
class CodeGraphSourceGraphOptions:
    input: Path
    input_format: str
    source_repository: str | None = None
    source_revision: str | None = None
    source_target_kind: str = "repository"
    source_target_path: str = "."
    analyzer_version: str | None = None
    executable: Path | None = None
    max_nodes: int = DEFAULT_MAX_NODES
    max_edges: int = DEFAULT_MAX_EDGES


@dataclass(frozen=True)
class CodeGraphSourceGraphIndex:
    options: CodeGraphSourceGraphOptions

    def payload(self) -> dict[str, Any]:
        if self.options.input_format == "json":
            records = CodeGraphJSONEvidence(self.options.input).records()
        elif self.options.input_format == "sqlite":
            records = CodeGraphSQLiteEvidence(self.options.input).records()
        else:
            raise ValueError("input format must be json or sqlite")
        return SourceGraphIndexPayload(self.options, records).payload()


@dataclass(frozen=True)
class CodeGraphJSONEvidence:
    path: Path

    def records(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists() or not self.path.is_file():
            raise ValueError(f"CodeGraph JSON input does not exist: {self.path}")
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid CodeGraph JSON input: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError("CodeGraph JSON input must be an object")
        return {
            "files": object_list(payload.get("files")),
            "nodes": object_list(payload.get("nodes")),
            "edges": object_list(payload.get("edges")),
            "diagnostics": object_list(payload.get("diagnostics")),
        }


@dataclass(frozen=True)
class CodeGraphSQLiteEvidence:
    path: Path

    def records(self) -> dict[str, list[dict[str, Any]]]:
        if not self.path.exists() or not self.path.is_file():
            raise ValueError(f"CodeGraph SQLite input does not exist: {self.path}")
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            tables = sqlite_table_names(connection)
            return {
                "files": sqlite_records(connection, "files") if "files" in tables else [],
                "nodes": sqlite_records(connection, "nodes") if "nodes" in tables else [],
                "edges": sqlite_records(connection, "edges") if "edges" in tables else [],
                "diagnostics": (
                    sqlite_records(connection, "diagnostics") if "diagnostics" in tables else []
                ),
            }
        except sqlite3.DatabaseError as exc:
            raise ValueError(f"Invalid CodeGraph SQLite input: {exc}") from exc
        finally:
            if connection is not None:
                connection.close()


@dataclass(frozen=True)
class SourceGraphIndexPayload:
    options: CodeGraphSourceGraphOptions
    records: dict[str, list[dict[str, Any]]]

    def payload(self) -> dict[str, Any]:
        files = self.normalized_files()
        nodes = bounded_items(self.normalized_nodes(), self.options.max_nodes)
        edges = bounded_items(self.normalized_edges(), self.options.max_edges)
        diagnostics = self.normalized_diagnostics()
        diagnostics.extend(truncation_diagnostics("nodes", nodes, self.options.max_nodes))
        diagnostics.extend(truncation_diagnostics("edges", edges, self.options.max_edges))
        return {
            "schemaVersion": SOURCE_GRAPH_SCHEMA_VERSION,
            "kind": SOURCE_GRAPH_KIND,
            "trust": self.trust_record(),
            "source": self.source_record(files),
            "inputs": [input_record(self.options.input, self.options.input_format)],
            "executable": executable_record(self.options.executable),
            "summary": {
                "fileCount": len(files),
                "nodeCount": len(nodes.items),
                "edgeCount": len(edges.items),
                "languages": sorted(
                    {language for item in files for language in string_values(item, "language")}
                ),
                "truncated": nodes.truncated or edges.truncated,
            },
            "files": files,
            "nodes": nodes.items,
            "edges": edges.items,
            "diagnostics": diagnostics,
        }

    def trust_record(self) -> dict[str, Any]:
        return {
            "analyzer": DEFAULT_CODEGRAPH_ANALYZER,
            "analyzerVersion": self.options.analyzer_version,
            "analyzerLicense": DEFAULT_CODEGRAPH_LICENSE,
            "trustLevel": "untrusted_optional_tool",
            "classification": "third_party_local_binary",
            "executedRepositoryCode": False,
            "allowedNetwork": False,
            "installation": "out_of_band_required",
        }

    def source_record(self, files: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "repository": self.options.source_repository,
            "revision": self.options.source_revision,
            "target": {
                "kind": safe_target_kind(self.options.source_target_kind),
                "path": safe_relative_path(self.options.source_target_path),
            },
            "sourceDigests": source_digests(files),
        }

    def normalized_files(self) -> list[dict[str, Any]]:
        records = [
            normalize_file_record(record)
            for record in self.records.get("files", [])
            if isinstance(record, dict)
        ]
        return sorted(records, key=lambda item: item["path"])

    def normalized_nodes(self) -> list[dict[str, Any]]:
        records = [
            normalize_node_record(record)
            for record in self.records.get("nodes", [])
            if isinstance(record, dict)
        ]
        return sorted(records, key=lambda item: (item["filePath"], item["kind"], item["id"]))

    def normalized_edges(self) -> list[dict[str, Any]]:
        records = [
            normalize_edge_record(record)
            for record in self.records.get("edges", [])
            if isinstance(record, dict)
        ]
        return sorted(records, key=lambda item: (item["kind"], item["source"], item["target"]))

    def normalized_diagnostics(self) -> list[dict[str, Any]]:
        records = [
            normalize_diagnostic_record(record)
            for record in self.records.get("diagnostics", [])
            if isinstance(record, dict)
        ]
        return sorted(records, key=lambda item: (item["level"], item["message"]))


@dataclass(frozen=True)
class BoundedItems:
    items: list[dict[str, Any]]
    original_count: int

    @property
    def truncated(self) -> bool:
        return len(self.items) < self.original_count


def build_codegraph_source_graph_index(
    options: CodeGraphSourceGraphOptions,
) -> dict[str, Any]:
    return CodeGraphSourceGraphIndex(options).payload()


def write_codegraph_source_graph_index(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def normalize_file_record(record: dict[str, Any]) -> dict[str, Any]:
    path = safe_relative_path(first_string(record, "path", "file_path", "filePath") or "")
    normalized: dict[str, Any] = {"path": path}
    for output_key, *input_keys in (
        ("language", "language"),
        ("sha256", "sha256", "hash", "content_hash", "contentHash"),
    ):
        value = first_string(record, *input_keys)
        if value is not None:
            normalized[output_key] = value
    size = first_int(record, "size", "size_bytes", "sizeBytes")
    if size is not None:
        normalized["sizeBytes"] = size
    return normalized


def normalize_node_record(record: dict[str, Any]) -> dict[str, Any]:
    node_id = first_string(record, "id", "node_id", "nodeId") or deterministic_id(record)
    file_path = safe_relative_path(first_string(record, "file_path", "filePath", "path") or "")
    normalized: dict[str, Any] = {
        "id": node_id,
        "kind": first_string(record, "kind", "type") or "unknown",
        "name": first_string(record, "name") or node_id,
        "qualifiedName": first_string(record, "qualified_name", "qualifiedName"),
        "filePath": file_path,
        "language": first_string(record, "language"),
        "visibility": first_string(record, "visibility"),
        "signature": first_string(record, "signature"),
    }
    range_record = source_range(record)
    if range_record:
        normalized["range"] = range_record
    return {key: value for key, value in normalized.items() if value is not None}


def normalize_edge_record(record: dict[str, Any]) -> dict[str, Any]:
    source = first_string(record, "source", "source_id", "sourceId")
    target = first_string(record, "target", "target_id", "targetId")
    if source is None or target is None:
        raise ValueError("CodeGraph edge records require source and target")
    normalized: dict[str, Any] = {
        "source": source,
        "target": target,
        "kind": first_string(record, "kind", "type") or "unknown",
        "provenance": first_string(record, "provenance"),
    }
    return {key: value for key, value in normalized.items() if value is not None}


def normalize_diagnostic_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "level": first_string(record, "level", "severity") or "info",
        "message": first_string(record, "message") or "CodeGraph diagnostic",
        "path": safe_optional_relative_path(first_string(record, "path", "filePath")),
    }


def source_range(record: dict[str, Any]) -> dict[str, int]:
    start_line = first_int(record, "start_line", "startLine", "line")
    end_line = first_int(record, "end_line", "endLine")
    if start_line is None:
        return {}
    return {"startLine": start_line, "endLine": end_line or start_line}


def bounded_items(records: list[dict[str, Any]], limit: int) -> BoundedItems:
    if limit < 1:
        raise ValueError("CodeGraph source graph limits must be positive")
    return BoundedItems(items=records[:limit], original_count=len(records))


def truncation_diagnostics(
    label: str,
    bounded: BoundedItems,
    limit: int,
) -> list[dict[str, Any]]:
    if not bounded.truncated:
        return []
    return [
        {
            "level": "warning",
            "message": f"{label} truncated from {bounded.original_count} to {limit}",
            "path": None,
        }
    ]


def sqlite_table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        "select name from sqlite_master where type = 'table' order by name"
    ).fetchall()
    return {str(row["name"]) for row in rows}


def sqlite_records(connection: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    rows = connection.execute(f'select * from "{table}"').fetchall()
    return [dict(row) for row in rows]


def input_record(path: Path, input_format: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "format": input_format,
        "sha256": file_sha256(path),
    }


def executable_record(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    if not path.exists() or not path.is_file():
        raise ValueError(f"CodeGraph executable does not exist: {path}")
    return {"path": str(path), "sha256": file_sha256(path)}


def source_digests(files: list[dict[str, Any]]) -> list[dict[str, str]]:
    digests = [
        {"path": item["path"], "sha256": item["sha256"]}
        for item in files
        if isinstance(item.get("sha256"), str) and item.get("sha256")
    ]
    return sorted(digests, key=lambda item: item["path"])


def safe_target_kind(value: str) -> str:
    if value not in {"repository", "folder", "file"}:
        raise ValueError("source target kind must be repository, folder, or file")
    return value


def safe_optional_relative_path(value: str | None) -> str | None:
    if value is None:
        return None
    return safe_relative_path(value)


def safe_relative_path(value: str) -> str:
    if not value:
        raise ValueError("CodeGraph path must be a non-empty relative path")
    if "\\" in value:
        raise ValueError(f"Unsafe CodeGraph path: {value}")
    normalized = value
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        if normalized != ".":
            raise ValueError(f"Unsafe CodeGraph path: {value}")
    return normalized


def first_string(record: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def first_int(record: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = record.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
    return None


def string_values(record: dict[str, Any], key: str) -> list[str]:
    value = record.get(key)
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def deterministic_id(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"
