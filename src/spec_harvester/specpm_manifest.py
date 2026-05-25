from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.promoter import parse_yaml_scalar


@dataclass(frozen=True)
class ManifestArtifact:
    values: dict[str, str]

    def artifact_id(self) -> str:
        artifact_id = str(self.values.get("id", "")).strip()
        if artifact_id:
            return artifact_id
        return str(self.values.get("artifact", "")).strip()

    def uri(self) -> str:
        uri = self.values.get("uri")
        return str(uri).strip() if uri is not None else ""

    def role(self) -> str | None:
        role = self.values.get("role")
        value = str(role).strip() if role is not None else ""
        return value or None

    def revision(self) -> str | None:
        revision = self.values.get("revision")
        value = str(revision).strip() if revision is not None else ""
        return value or None

    def as_dict(self) -> dict[str, str]:
        result = {
            "id": self.artifact_id(),
            "uri": self.uri(),
        }
        role = self.role()
        if role is not None:
            result["role"] = role
        revision = self.revision()
        if revision is not None:
            result["revision"] = revision
        return result


@dataclass(frozen=True)
class SpecPackageManifest:
    path: Path
    metadata: dict[str, Any]
    artifacts: tuple[ManifestArtifact, ...]
    intents: tuple[str, ...]
    capabilities: tuple[str, ...]

    @classmethod
    def from_path(cls, path: Path) -> SpecPackageManifest:
        return cls.from_text(path, path.read_text(encoding="utf-8"))

    @classmethod
    def from_text(cls, path: Path, text: str) -> SpecPackageManifest:
        parser = ManifestParser(path, text)
        return parser.manifest()

    def package_id(self) -> str:
        return str(self.metadata.get("id", "")).strip()

    def package_version(self) -> str:
        return str(self.metadata.get("version", "")).strip()

    def require_identity(self) -> tuple[str, str]:
        package_id = self.package_id()
        package_version = self.package_version()
        if not package_id or not package_version:
            raise ValueError("specpm.yaml must contain metadata.id and metadata.version.")
        return package_id, package_version

    def namespace(self) -> str:
        package_id, _ = self.require_identity()
        return package_id.split(".")[0] if "." in package_id else package_id

    def metadata_strings(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in self.metadata.items():
            if isinstance(value, str):
                result[key] = value
                continue
            if key == "licenseEvidence" and isinstance(value, dict):
                result[key] = ""
        return result

    def license_evidence(self) -> dict[str, Any] | None:
        evidence = self.metadata.get("licenseEvidence")
        return evidence if isinstance(evidence, dict) and evidence else None


class ManifestParser:
    def __init__(self, path: Path, text: str):
        self.path = path
        self.lines = text.splitlines()
        self.metadata: dict[str, Any] = {}
        self.artifacts: list[ManifestArtifact] = []
        self.intents: set[str] = set()
        self.capabilities: set[str] = set()
        self.parse_state = "root"
        self.index_mode = ""
        self.current_artifact: dict[str, str] | None = None
        self.collecting_license_evidence_paths = False

    def manifest(self) -> SpecPackageManifest:
        for raw_line in self.lines:
            self.consume(raw_line)
        self.finish_artifact()
        manifest = SpecPackageManifest(
            path=self.path,
            metadata=dict(self.metadata),
            artifacts=tuple(self.artifacts),
            intents=tuple(sorted(self.intents)),
            capabilities=tuple(sorted(self.capabilities)),
        )
        manifest.require_identity()
        return manifest

    def consume(self, raw_line: str) -> None:
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            return
        indent = len(line) - len(line.lstrip(" "))
        text = line.strip()
        if indent == 0:
            self.consume_root(text)
            return
        if self.parse_state == "metadata":
            self.consume_metadata(indent, text)
            return
        if self.parse_state == "metadata_license_evidence":
            self.consume_license_evidence(indent, text)
            return
        if self.parse_state == "index":
            self.index_mode = self.updated_index_mode(indent, text)
            return
        if self.parse_state == "foreignArtifacts":
            self.consume_artifact(indent, text)

    def consume_root(self, text: str) -> None:
        self.finish_artifact()
        self.index_mode = ""
        self.collecting_license_evidence_paths = False
        if text == "metadata:":
            self.parse_state = "metadata"
        elif text == "index:":
            self.parse_state = "index"
        elif text == "foreignArtifacts:":
            self.parse_state = "foreignArtifacts"
        else:
            self.parse_state = "root"

    def consume_metadata(self, indent: int, text: str) -> None:
        if indent != 2 or ":" not in text:
            return
        key, raw_value = text.split(":", 1)
        key = key.strip()
        if key == "licenseEvidence" and not raw_value.strip():
            self.metadata[key] = {}
            self.parse_state = "metadata_license_evidence"
            self.collecting_license_evidence_paths = False
            return
        self.metadata[key] = parse_yaml_scalar(raw_value.strip())

    def consume_license_evidence(self, indent: int, text: str) -> None:
        evidence = self.metadata.setdefault("licenseEvidence", {})
        if not isinstance(evidence, dict):
            evidence = {}
            self.metadata["licenseEvidence"] = evidence

        if indent == 2:
            self.collecting_license_evidence_paths = False
            self.parse_state = "metadata"
            self.consume_metadata(indent, text)
            return
        if indent == 4 and ":" in text:
            key, raw_value = text.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            self.collecting_license_evidence_paths = False
            if key == "paths":
                evidence["paths"] = self.license_paths_value(value)
                self.collecting_license_evidence_paths = not value
                return
            evidence[key] = parse_yaml_scalar(value)
            return
        if indent == 6 and self.collecting_license_evidence_paths and text.startswith("- "):
            paths = evidence.setdefault("paths", [])
            if isinstance(paths, list):
                paths.append(parse_yaml_scalar(text[2:].strip()))

    def consume_artifact(self, indent: int, text: str) -> None:
        if indent == 2:
            if text.startswith("- "):
                self.finish_artifact()
                self.current_artifact = {}
                item_text = text[2:].strip()
                self.consume_artifact_field(item_text)
                return
            self.finish_artifact()
            self.parse_state = "root"
            return
        if indent >= 4 and self.current_artifact is not None:
            self.consume_artifact_field(text)
            return
        if indent < 4:
            self.finish_artifact()
            self.parse_state = "root"

    def consume_artifact_field(self, text: str) -> None:
        if self.current_artifact is None or ":" not in text:
            return
        key, raw_value = text.split(":", 1)
        self.current_artifact[key.strip()] = str(parse_yaml_scalar(raw_value.strip()))

    def finish_artifact(self) -> None:
        if self.current_artifact is None:
            return
        self.artifacts.append(ManifestArtifact(dict(self.current_artifact)))
        self.current_artifact = None

    def updated_index_mode(self, indent: int, text: str) -> str:
        if indent == 2 and text == "provides:":
            return "provides"
        if indent == 2 and text == "intents:":
            return "intents"
        if self.index_mode == "intents":
            if indent == 4 and text.startswith("- "):
                self.intents.update(scalar_list_item(text))
                return self.index_mode
            if indent <= 2:
                return ""
        if self.index_mode == "provides":
            if indent == 4 and text == "capabilities:":
                return "capabilities"
            if indent == 4 and text == "intents:":
                return "provides_intents"
            if indent <= 2:
                return ""
        if self.index_mode == "capabilities":
            if indent == 6 and text.startswith("- "):
                self.capabilities.update(scalar_list_item(text))
                return self.index_mode
            if indent == 4 and text == "intents:":
                return "provides_intents"
            if indent <= 4:
                return "provides"
        if self.index_mode == "provides_intents":
            if indent == 6 and text.startswith("- "):
                self.intents.update(scalar_list_item(text))
                return self.index_mode
            if indent <= 4:
                return "provides"
        return self.index_mode

    def license_paths_value(self, value: str) -> list[Any]:
        if value == "[]":
            return []
        if value:
            return [parse_yaml_scalar(value)]
        return []


def scalar_list_item(text: str) -> list[str]:
    value = text[2:].strip()
    if not value:
        return []
    parsed = parse_yaml_scalar(value)
    if isinstance(parsed, list):
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [str(parsed).strip()] if str(parsed).strip() else []
