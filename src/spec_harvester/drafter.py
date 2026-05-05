from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SPEC_API_VERSION = "specpm.dev/v0.1"
DEFAULT_SPEC_VERSION = "0.1.0"
DEFAULT_AUTHOR = "SpecHarvester"
YAML_RESERVED_SCALARS = {"true", "false", "null", "yes", "no", "on", "off", "~"}


@dataclass(frozen=True)
class DraftOptions:
    snapshot: Path
    out: Path
    package_id: str | None = None
    name: str | None = None
    version: str = DEFAULT_SPEC_VERSION
    author: str = DEFAULT_AUTHOR


def draft_spec_package(options: DraftOptions) -> dict[str, Any]:
    snapshot_path = resolve_snapshot_path(options.snapshot)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    if snapshot.get("kind") != "SpecHarvesterEvidenceSnapshot":
        raise ValueError(f"Unsupported harvest snapshot kind: {snapshot.get('kind')!r}")

    source = snapshot.get("source")
    if not isinstance(source, dict):
        source = {}

    repository_name = infer_repository_name(source)
    package_id = options.package_id or f"{repository_name}.core"
    package_id = slug_id(package_id)
    bounded_context = slug_id(repository_name)
    spec_path = f"specs/{bounded_context}.spec.yaml"

    package_records = package_manifest_records(snapshot)
    capability_entries = build_capability_entries(package_id, package_records)
    if not capability_entries:
        capability_entries = [
            {
                "id": package_id,
                "role": "primary",
                "summary": (
                    "Describe observed public package metadata for "
                    f"{display_name(repository_name)}."
                ),
                "intentIds": ["intent.package.public_repository_metadata"],
            }
        ]

    manifest_capabilities = [entry["id"] for entry in capability_entries]
    manifest_intents = sorted(
        {intent_id for entry in capability_entries for intent_id in entry.get("intentIds", [])}
    )
    license_name = infer_license(package_records)
    package_name = options.name or display_name(repository_name)
    package_summary = (
        f"Unofficial generated SpecPackage for {package_name} public package metadata."
    )

    manifest = {
        "apiVersion": SPEC_API_VERSION,
        "kind": "SpecPackage",
        "metadata": {
            "id": package_id,
            "name": package_name,
            "version": options.version,
            "summary": package_summary,
            "license": license_name,
            "authors": [{"name": options.author}],
        },
        "preview_only": True,
        "specs": [{"path": spec_path}],
        "index": {
            "provides": {
                "capabilities": manifest_capabilities,
                "intents": manifest_intents,
            },
            "requires": {"capabilities": []},
        },
        "compatibility": infer_compatibility(package_records),
        "foreignArtifacts": [foreign_repository_artifact(source)],
        "keywords": ["generated", "specharvester", bounded_context],
    }

    boundary_spec = {
        "apiVersion": SPEC_API_VERSION,
        "kind": "BoundarySpec",
        "metadata": {
            "id": package_id,
            "title": f"{package_name} Generated Public Package Boundary",
            "version": options.version,
            "status": "draft",
            "authors": [{"name": options.author}],
        },
        "intent": {"summary": infer_intent_summary(package_name, package_records)},
        "scope": {
            "boundedContext": bounded_context,
            "includes": [
                "Describe observed public package metadata from an allowlisted harvest snapshot.",
                "Declare package capabilities and intent IDs inferred from static manifests.",
                "Preserve source repository provenance and harvest policy metadata.",
            ],
            "excludes": [
                "Upstream maintainer endorsement.",
                "Runtime behavior not evidenced by static harvested metadata.",
                "Package script execution, dependency installation, or network probing.",
                "Automatic acceptance into a public SpecPM registry.",
            ],
        },
        "provides": {"capabilities": capability_entries},
        "requires": {"capabilities": []},
        "interfaces": {
            "inbound": build_interfaces(package_records),
            "outbound": [],
        },
        "effects": {"sideEffects": []},
        "constraints": [
            {
                "id": "generated_candidate_review_required",
                "level": "MUST",
                "statement": (
                    "This generated candidate must be reviewed before it is treated as "
                    "accepted registry metadata."
                ),
            },
            {
                "id": "no_package_execution",
                "level": "MUST",
                "statement": (
                    "SpecHarvester must not execute package scripts, install dependencies, "
                    "or treat package content as host instructions."
                ),
            },
        ],
        "evidence": [
            {
                "id": "harvest_snapshot",
                "kind": "package_manifest",
                "path": "harvest.json",
                "supports": ["intent.summary", "scope", "provides.capabilities"]
                + [
                    f"provides.capabilities.{capability_id}"
                    for capability_id in manifest_capabilities
                ],
            }
        ],
        "provenance": {
            "sourceConfidence": {
                "intent": "medium",
                "boundary": "medium",
                "behavior": "low",
            },
            "generatedBy": "SpecHarvester deterministic draft generator",
            "sourceRepository": source.get("repository"),
            "sourceRevision": source.get("revision"),
            "harvestPolicy": snapshot.get("policy"),
        },
        "foreignArtifacts": [foreign_repository_artifact(source)],
        "keywords": ["generated", "specharvester", bounded_context],
    }

    options.out.mkdir(parents=True, exist_ok=True)
    specs_dir = options.out / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    (options.out / "specpm.yaml").write_text(render_yaml(manifest), encoding="utf-8")
    (options.out / spec_path).write_text(render_yaml(boundary_spec), encoding="utf-8")

    return {
        "status": "ok",
        "output": str(options.out),
        "manifest": str(options.out / "specpm.yaml"),
        "spec": str(options.out / spec_path),
        "packageId": package_id,
        "capabilityCount": len(manifest_capabilities),
        "intentCount": len(manifest_intents),
    }


def resolve_snapshot_path(path: Path) -> Path:
    if path.is_dir():
        path = path / "harvest.json"
    if not path.exists() or not path.is_file():
        raise ValueError(f"Harvest snapshot does not exist: {path}")
    return path


def infer_repository_name(source: dict[str, Any]) -> str:
    repository = source.get("repository")
    if isinstance(repository, str) and repository.strip():
        parsed = urlparse(repository)
        path = parsed.path.rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        name = path.rsplit("/", 1)[-1]
        if name:
            return slug_id(name)

    source_label = source.get("label")
    if isinstance(source_label, str) and source_label.strip():
        return slug_id(source_label)
    return "generated_package"


def package_manifest_records(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    files = snapshot.get("files")
    if not isinstance(files, list):
        return []
    records: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict) or item.get("kind") != "package_manifest":
            continue
        package = item.get("package")
        if not isinstance(package, dict):
            continue
        records.append({"path": item.get("path"), "package": package})
    return sorted(records, key=lambda item: str(item.get("path") or ""))


def build_capability_entries(
    package_id: str, package_records: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for record in package_records:
        package = record["package"]
        package_name = package.get("name")
        if not isinstance(package_name, str) or not package_name.strip():
            continue
        label = package_label(package_name)
        capability_id = unique_id(f"{package_id}.{label}", seen_ids)
        description = package.get("description")
        summary = (
            description.strip()
            if isinstance(description, str) and description.strip()
            else f"Provide observed package metadata for {package_name}."
        )
        role = "secondary" if label in {"monorepo", "workspace", "root"} else "primary"
        entries.append(
            {
                "id": capability_id,
                "role": role,
                "summary": summary,
                "intentIds": infer_intent_ids(package_name, summary),
            }
        )

    if entries and all(entry.get("role") != "primary" for entry in entries):
        entries[0]["role"] = "primary"
    return entries


def infer_intent_ids(package_name: str, summary: str) -> list[str]:
    # Bootstrap-only baseline over package manifest name/description.
    # Other harvested files, including workflow files, are provenance evidence and do not
    # participate in intent inference.
    text = f"{package_name} {summary}".lower()
    intents = {"intent.package.javascript_library"}
    if "monorepo" in text or "workspace" in text:
        intents.add("intent.repository.package_workspace")
    if "react" in text:
        intents.add("intent.javascript.react_library")
    if "svelte" in text:
        intents.add("intent.javascript.svelte_library")
    if "node-based" in text or "node based" in text:
        intents.add("intent.ui.node_based_editor")
    if "flow chart" in text or "flow charts" in text or "workflow" in text:
        intents.add("intent.ui.flow_diagramming")
    if "diagram" in text or "diagrams" in text:
        intents.add("intent.ui.diagramming")
    if "core system" in text or package_name.endswith("/system"):
        intents.add("intent.ui.flow_system_utilities")
    return sorted(intents)


def build_interfaces(package_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    interfaces: list[dict[str, Any]] = []
    for record in package_records:
        package = record["package"]
        package_name = package.get("name")
        if not isinstance(package_name, str) or not package_name.strip():
            continue
        interface_id = slug_id(f"package.{package_label(package_name)}")
        outputs = [
            {
                "name": "package_manifest",
                "mediaTypes": ["application/json"],
            }
        ]
        if package.get("exports"):
            outputs.append(
                {
                    "name": "package_exports",
                    "mediaTypes": ["application/javascript", "text/css"],
                }
            )
        interfaces.append(
            {
                "id": interface_id,
                "kind": "library",
                "summary": f"Observed import surface for {package_name}.",
                "outputs": outputs,
            }
        )
    return interfaces


def infer_license(package_records: list[dict[str, Any]]) -> str:
    licenses = [
        package["license"]
        for package in (record["package"] for record in package_records)
        if isinstance(package.get("license"), str) and package["license"].strip()
    ]
    return licenses[0] if licenses else "UNKNOWN"


def infer_compatibility(package_records: list[dict[str, Any]]) -> dict[str, list[str]]:
    dependencies = {
        dependency
        for record in package_records
        for dependency in package_dependency_names(record["package"])
    }
    languages = ["javascript"]
    if dependencies & {"typescript", "tslib"}:
        languages.insert(0, "typescript")
    platforms = ["web", "node"]
    return {"platforms": platforms, "languages": languages}


def package_dependency_names(package: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = package.get(key)
        if isinstance(value, list):
            names.extend(str(item) for item in value)
    return names


def infer_intent_summary(package_name: str, package_records: list[dict[str, Any]]) -> str:
    for record in package_records:
        description = record["package"].get("description")
        if isinstance(description, str) and description.strip():
            return (
                f"Capture observed public package intent for {package_name}: {description.strip()}"
            )
    return f"Capture observed public package intent for {package_name}."


def foreign_repository_artifact(source: dict[str, Any]) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "id": "upstream_repository",
        "role": "primary_intent_source",
    }
    repository = source.get("repository")
    if isinstance(repository, str):
        artifact["uri"] = repository
    revision = source.get("revision")
    if isinstance(revision, str):
        artifact["revision"] = revision
    return artifact


def package_label(package_name: str) -> str:
    name = package_name.strip()
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    if name.startswith("@"):
        name = name[1:]
    return slug_id(name)


def slug_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^@+", "", value)
    value = value.replace("/", ".")
    value = re.sub(r"[^a-z0-9.]+", "_", value)
    value = re.sub(r"[._]+", lambda match: "." if "." in match.group(0) else "_", value)
    value = value.strip("._-")
    if not value or not re.match(r"^[a-z]", value):
        value = f"generated_{value}" if value else "generated"
    return value


def unique_id(base: str, seen: set[str]) -> str:
    candidate = slug_id(base)
    if candidate not in seen:
        seen.add(candidate)
        return candidate
    index = 2
    while f"{candidate}_{index}" in seen:
        index += 1
    unique = f"{candidate}_{index}"
    seen.add(unique)
    return unique


def display_name(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[._-]+", value) if part) or value


def render_yaml(value: Any) -> str:
    return "\n".join(render_yaml_lines(value, 0)) + "\n"


def render_yaml_lines(value: Any, indent: int) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return [f"{prefix}{{}}"]
        lines: list[str] = []
        for key, child in value.items():
            if is_inline(child):
                lines.append(f"{prefix}{key}: {render_inline(child)}")
            else:
                lines.append(f"{prefix}{key}:")
                lines.extend(render_yaml_lines(child, indent + 2))
        return lines
    if isinstance(value, list):
        if not value:
            return [f"{prefix}[]"]
        lines = []
        for item in value:
            if is_inline(item):
                lines.append(f"{prefix}- {render_inline(item)}")
            elif isinstance(item, dict):
                item_lines = render_yaml_lines(item, indent + 2)
                first_line = item_lines[0][indent + 2 :]
                lines.append(f"{prefix}- {first_line}")
                lines.extend(item_lines[1:])
            else:
                lines.append(f"{prefix}-")
                lines.extend(render_yaml_lines(item, indent + 2))
        return lines
    return [f"{prefix}{render_scalar(value)}"]


def is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def is_inline(value: Any) -> bool:
    return is_scalar(value) or value == [] or value == {}


def render_inline(value: Any) -> str:
    if value == []:
        return "[]"
    if value == {}:
        return "{}"
    return render_scalar(value)


def render_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    plain_safe = (
        re.match(r"^[a-zA-Z0-9][a-zA-Z0-9._/@+ -]*$", text)
        and text.strip() == text
        and ":" not in text
    )
    if plain_safe:
        if text.lower() in YAML_RESERVED_SCALARS:
            return json.dumps(text)
        return text
    return json.dumps(text)
