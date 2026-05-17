from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_REPOSITORY_KEYS = {
    "id",
    "repository",
    "revision",
    "ref",
    "checkout",
    "packageId",
    "enabled",
    "labels",
}


def read_repository_source_manifests(
    inputs: Path,
    *,
    include_disabled: bool = False,
) -> list[dict[str, Any]]:
    root = inputs.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Repository source manifest directory does not exist: {inputs}")

    records: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    for manifest_path in sorted(root.glob("*.yml"), key=lambda item: item.name):
        repositories = parse_repository_manifest(manifest_path)
        manifest_relative = manifest_path.relative_to(root).as_posix()
        for entry_index, repository in enumerate(repositories):
            record = normalize_repository_source(repository, manifest_relative, entry_index)
            previous_path = seen_ids.get(record["id"])
            if previous_path is not None:
                raise ValueError(
                    f"Duplicate repository id {record['id']!r} in {manifest_relative}; "
                    f"already defined in {previous_path}"
                )
            seen_ids[record["id"]] = manifest_relative
            if repository.get("enabled") is False and not include_disabled:
                continue
            records.append(record)
    return records


def parse_repository_manifest(path: Path) -> list[dict[str, Any]]:
    rows = significant_rows(path)
    if not rows:
        raise ValueError(f"Repository source manifest is empty: {path}")

    first_line, _first_indent, first_text = rows[0]
    if first_text != "repositories:":
        raise ValueError(f"{path}:{first_line}: expected top-level repositories list")

    repositories: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_keys: dict[str, int] = {}
    for line_number, indent, text in rows[1:]:
        if indent == 2 and text.startswith("-"):
            if current is not None:
                repositories.append(current)
            current = {}
            current_keys = {}
            rest = text[1:].strip()
            if rest:
                key, value = parse_key_value(path, line_number, rest)
                assign_repository_value(path, line_number, current, current_keys, key, value)
            continue
        if indent == 4:
            if current is None:
                raise ValueError(f"{path}:{line_number}: unsupported indentation")
            key, value = parse_key_value(path, line_number, text)
            assign_repository_value(path, line_number, current, current_keys, key, value)
            continue
        raise ValueError(f"{path}:{line_number}: unsupported indentation")

    if current is not None:
        repositories.append(current)
    if not repositories:
        raise ValueError(f"{path}: repositories must contain at least one entry")
    return repositories


def significant_rows(path: Path) -> list[tuple[int, int, str]]:
    rows: list[tuple[int, int, str]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = strip_yaml_comment(raw_line).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        rows.append((line_number, indent, line.strip()))
    return rows


def strip_yaml_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            if in_single:
                in_single = False
            elif quote_starts_scalar(line, index):
                in_single = True
            continue
        if char == '"' and not in_single:
            if in_double:
                in_double = False
            elif quote_starts_scalar(line, index):
                in_double = True
            continue
        if char == "#" and not in_single and not in_double:
            if index == 0 or line[index - 1].isspace():
                return line[:index]
    return line


def quote_starts_scalar(line: str, quote_index: int) -> bool:
    prefix = line[:quote_index].rstrip()
    return not prefix or prefix[-1] in ":,["


def assign_repository_value(
    path: Path,
    line_number: int,
    repository: dict[str, Any],
    seen_keys: dict[str, int],
    key: str,
    value: str,
) -> None:
    previous_line = seen_keys.get(key)
    if previous_line is not None:
        raise ValueError(
            f"{path}:{line_number}: duplicate key {key!r}; first defined on line {previous_line}"
        )
    seen_keys[key] = line_number
    repository[key] = parse_scalar(value)


def parse_key_value(path: Path, line_number: int, text: str) -> tuple[str, str]:
    if ":" not in text:
        raise ValueError(f"{path}:{line_number}: expected key: value")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"{path}:{line_number}: key must be non-empty")
    return key, value.strip()


def parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def normalize_repository_source(
    repository: dict[str, Any],
    manifest_path: str,
    entry_index: int,
) -> dict[str, Any]:
    unknown_keys = sorted(set(repository) - ALLOWED_REPOSITORY_KEYS)
    if unknown_keys:
        raise ValueError(
            f"{manifest_path}[{entry_index}] contains unsupported keys: {', '.join(unknown_keys)}"
        )

    repository_id = required_string(repository, "id", manifest_path, entry_index)
    repository_url = required_string(repository, "repository", manifest_path, entry_index)
    if not (repository_url.startswith("https://") or repository_url.startswith("git@github.com:")):
        raise ValueError(f"{manifest_path}[{entry_index}] has unsupported repository URL")

    revision = optional_string(repository, "revision", manifest_path, entry_index)
    ref = optional_string(repository, "ref", manifest_path, entry_index)
    if (revision is None) == (ref is None):
        raise ValueError(f"{manifest_path}[{entry_index}] requires exactly one of revision or ref")

    enabled = repository.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ValueError(f"{manifest_path}[{entry_index}].enabled must be a boolean")

    labels = repository.get("labels", [])
    if not isinstance(labels, list) or not all(
        isinstance(label, str) and label for label in labels
    ):
        raise ValueError(f"{manifest_path}[{entry_index}].labels must be a list of strings")

    return {
        "id": repository_id,
        "repository": repository_url,
        "revision": revision,
        "ref": ref,
        "checkout": optional_string(repository, "checkout", manifest_path, entry_index),
        "packageId": optional_string(repository, "packageId", manifest_path, entry_index),
        "labels": sorted(labels),
        "sourceManifest": {"path": manifest_path, "entryIndex": entry_index},
    }


def required_string(
    repository: dict[str, Any],
    key: str,
    manifest_path: str,
    entry_index: int,
) -> str:
    value = repository.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{manifest_path}[{entry_index}].{key} must be a non-empty string")
    return value.strip()


def optional_string(
    repository: dict[str, Any],
    key: str,
    manifest_path: str,
    entry_index: int,
) -> str | None:
    value = repository.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{manifest_path}[{entry_index}].{key} must be a non-empty string")
    return value.strip()
