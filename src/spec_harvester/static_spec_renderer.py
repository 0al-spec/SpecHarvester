from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from yaml.tokens import AliasToken, AnchorToken, TagToken

from spec_harvester.static_spec_renderer_assets import INDEX_HTML, VIEWER_CSS, VIEWER_JS

RENDERER_API_VERSION = "spec-harvester.static-spec-renderer/v0"
RENDERER_SCHEMA_VERSION = 1
RENDERER_NAME = "spec-harvester-static-spec-renderer"


@dataclass(frozen=True)
class StaticSpecRendererOptions:
    candidate: Path
    output: Path


@dataclass(frozen=True)
class RendererDiagnostic:
    severity: str
    code: str
    message: str
    path: str
    field: str | None = None

    def as_dict(self) -> dict[str, str]:
        payload = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }
        if self.field is not None:
            payload["field"] = self.field
        return payload


class StaticSpecRenderError(ValueError):
    def __init__(self, diagnostics: list[RendererDiagnostic]):
        super().__init__("Static spec rendering failed.")
        self.diagnostics = diagnostics


class StaticSpecRenderer:
    def __init__(self, options: StaticSpecRendererOptions):
        self.options = options

    def render(self) -> dict[str, Any]:
        try:
            payload = CandidateSpecPackage(self.options.candidate).payload()
        except StaticSpecRenderError as exc:
            return {
                "status": "error",
                "candidate": str(self.options.candidate),
                "output": str(self.options.output),
                "diagnostics": [diagnostic.as_dict() for diagnostic in exc.diagnostics],
            }

        site = StaticSpecSite(self.options.output)
        written = site.write(payload)
        package = payload["package"]
        return {
            "status": "ok",
            "candidate": str(self.options.candidate),
            "output": str(self.options.output),
            "packageId": package.get("id"),
            "version": package.get("version"),
            "specCount": len(payload["specs"]),
            "diagnosticCount": len(payload["diagnostics"]),
            "written": written,
        }


class CandidateSpecPackage:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def payload(self) -> dict[str, Any]:
        manifest_path = self.root / "specpm.yaml"
        manifest = SpecYamlDocument(self.root, manifest_path).required_mapping()
        spec_refs = ManifestSpecReferences(self.root, manifest).paths()
        specs = [BoundarySpecDocument(self.root, spec_path).payload() for spec_path in spec_refs]
        validation = CandidateValidationSummary(self.root).payload()
        diagnostics = CandidateValidationSummary(self.root).diagnostics()
        return {
            "apiVersion": RENDERER_API_VERSION,
            "schemaVersion": RENDERER_SCHEMA_VERSION,
            "kind": "SpecHarvesterStaticSpecPackage",
            "renderer": {
                "name": RENDERER_NAME,
                "schemaVersion": RENDERER_SCHEMA_VERSION,
                "trustBoundary": "YAML parsed locally as untrusted data; no package code executed.",
            },
            "package": ManifestDocument(self.root, manifest).payload(),
            "specs": specs,
            "validation": validation,
            "diagnostics": [diagnostic.as_dict() for diagnostic in diagnostics],
        }


class SpecYamlDocument:
    def __init__(self, root: Path, path: Path):
        self.root = root
        self.path = path

    def required_mapping(self) -> dict[str, Any]:
        self.ensure_readable_inside_root()
        text = self.path.read_text(encoding="utf-8")
        try:
            for token in yaml.scan(text):
                if isinstance(token, AnchorToken):
                    raise StaticSpecRenderError(
                        [
                            self.diagnostic(
                                "yaml_anchor_unsupported",
                                "YAML anchors are not supported by the static renderer.",
                            )
                        ]
                    )
                if isinstance(token, AliasToken):
                    raise StaticSpecRenderError(
                        [
                            self.diagnostic(
                                "yaml_alias_unsupported",
                                "YAML aliases are not supported by the static renderer.",
                            )
                        ]
                    )
                if isinstance(token, TagToken):
                    raise StaticSpecRenderError(
                        [
                            self.diagnostic(
                                "yaml_tag_unsupported",
                                "YAML custom tags are not supported by the static renderer.",
                            )
                        ]
                    )
        except yaml.YAMLError as exc:
            raise StaticSpecRenderError(
                [self.diagnostic("yaml_parse_error", f"YAML parse error: {exc}")]
            ) from exc

        try:
            documents = list(yaml.safe_load_all(text))
        except yaml.YAMLError as exc:
            raise StaticSpecRenderError(
                [self.diagnostic("yaml_parse_error", f"YAML parse error: {exc}")]
            ) from exc
        if len(documents) != 1:
            raise StaticSpecRenderError(
                [
                    self.diagnostic(
                        "yaml_multiple_documents",
                        "Expected exactly one YAML document.",
                    )
                ]
            )
        document = documents[0]
        json_issue = JsonCompatibleValue(document).issue_path()
        if json_issue is not None:
            raise StaticSpecRenderError(
                [
                    self.diagnostic(
                        "yaml_non_json_value",
                        f"YAML value is not JSON-compatible at {json_issue}.",
                    )
                ]
            )
        if not isinstance(document, dict):
            raise StaticSpecRenderError(
                [self.diagnostic("yaml_mapping_required", "YAML document must be a mapping.")]
            )
        return document

    def ensure_readable_inside_root(self) -> None:
        if not self.path.exists():
            raise StaticSpecRenderError(
                [self.diagnostic("file_missing", "Required file is missing.")]
            )
        if self.path.is_symlink():
            raise StaticSpecRenderError(
                [self.diagnostic("symlink_unsupported", "Spec renderer refuses symlinked input.")]
            )
        resolved = self.path.resolve()
        if not path_is_inside(resolved, self.root):
            raise StaticSpecRenderError(
                [self.diagnostic("path_escape", "Referenced file escapes the candidate root.")]
            )
        if not resolved.is_file():
            raise StaticSpecRenderError(
                [self.diagnostic("file_not_regular", "Referenced path is not a regular file.")]
            )

    def diagnostic(self, code: str, message: str) -> RendererDiagnostic:
        return RendererDiagnostic(
            severity="error",
            code=code,
            message=message,
            path=relative_display_path(self.root, self.path),
        )


class JsonCompatibleValue:
    def __init__(self, value: Any):
        self.value = value

    def issue_path(self) -> str | None:
        return self._issue_path(self.value, "$")

    def _issue_path(self, value: Any, path: str) -> str | None:
        if value is None or isinstance(value, (str, int, float, bool)):
            return None
        if isinstance(value, list):
            for index, item in enumerate(value):
                issue = self._issue_path(item, f"{path}.{index}")
                if issue is not None:
                    return issue
            return None
        if isinstance(value, dict):
            for key, item in value.items():
                if not isinstance(key, str):
                    return f"{path}.{key}"
                issue = self._issue_path(item, f"{path}.{key}")
                if issue is not None:
                    return issue
            return None
        return path


class ManifestSpecReferences:
    def __init__(self, root: Path, manifest: dict[str, Any]):
        self.root = root
        self.manifest = manifest

    def paths(self) -> list[Path]:
        specs = self.manifest.get("specs")
        if not isinstance(specs, list) or not specs:
            raise StaticSpecRenderError(
                [
                    RendererDiagnostic(
                        severity="error",
                        code="spec_references_missing",
                        message="specpm.yaml must declare at least one specs[].path entry.",
                        path="specpm.yaml",
                        field="specs",
                    )
                ]
            )
        paths = []
        diagnostics = []
        for index, item in enumerate(specs):
            raw_path = item.get("path") if isinstance(item, dict) else None
            if not isinstance(raw_path, str) or not raw_path.strip():
                diagnostics.append(
                    RendererDiagnostic(
                        severity="error",
                        code="spec_reference_invalid",
                        message="Each specs entry must be a mapping with a non-empty path.",
                        path="specpm.yaml",
                        field=f"specs.{index}.path",
                    )
                )
                continue
            spec_path = (self.root / raw_path).resolve(strict=False)
            if not path_is_inside(spec_path, self.root):
                diagnostics.append(
                    RendererDiagnostic(
                        severity="error",
                        code="spec_reference_path_escape",
                        message="Referenced spec path escapes the candidate root.",
                        path="specpm.yaml",
                        field=f"specs.{index}.path",
                    )
                )
                continue
            paths.append(spec_path)
        if diagnostics:
            raise StaticSpecRenderError(diagnostics)
        return paths


class ManifestDocument:
    def __init__(self, root: Path, manifest: dict[str, Any]):
        self.root = root
        self.manifest = manifest

    def payload(self) -> dict[str, Any]:
        metadata = mapping_value(self.manifest.get("metadata"))
        index = mapping_value(self.manifest.get("index"))
        provides = mapping_value(index.get("provides"))
        requires = mapping_value(index.get("requires"))
        specs = [
            {"path": item.get("path")}
            for item in list_value(self.manifest.get("specs"))
            if isinstance(item, dict) and isinstance(item.get("path"), str)
        ]
        return {
            "apiVersion": string_value(self.manifest.get("apiVersion")),
            "kind": string_value(self.manifest.get("kind")),
            "id": string_value(metadata.get("id")),
            "version": string_value(metadata.get("version")),
            "metadata": metadata,
            "previewOnly": bool(self.manifest.get("preview_only", False)),
            "manifestPath": "specpm.yaml",
            "specs": specs,
            "capabilities": string_list(provides.get("capabilities")),
            "intents": string_list(provides.get("intents")),
            "requiredCapabilities": string_list(requires.get("capabilities")),
            "compatibility": mapping_value(self.manifest.get("compatibility")),
            "foreignArtifacts": list_value(self.manifest.get("foreignArtifacts")),
            "keywords": string_list(self.manifest.get("keywords")),
        }


class BoundarySpecDocument:
    def __init__(self, root: Path, path: Path):
        self.root = root
        self.path = path

    def payload(self) -> dict[str, Any]:
        spec = SpecYamlDocument(self.root, self.path).required_mapping()
        return {
            "path": relative_display_path(self.root, self.path),
            "apiVersion": string_value(spec.get("apiVersion")),
            "kind": string_value(spec.get("kind")),
            "metadata": mapping_value(spec.get("metadata")),
            "intent": mapping_value(spec.get("intent")),
            "scope": mapping_value(spec.get("scope")),
            "provides": mapping_value(spec.get("provides")),
            "requires": mapping_value(spec.get("requires")),
            "interfaces": mapping_value(spec.get("interfaces")),
            "effects": mapping_value(spec.get("effects")),
            "constraints": list_value(spec.get("constraints")),
            "evidence": list_value(spec.get("evidence")),
            "provenance": mapping_value(spec.get("provenance")),
            "foreignArtifacts": list_value(spec.get("foreignArtifacts")),
            "keywords": string_list(spec.get("keywords")),
        }


class CandidateValidationSummary:
    def __init__(self, root: Path):
        self.root = root

    def payload(self) -> dict[str, Any]:
        path = self.path()
        if path is None:
            return {
                "status": "not_provided",
                "source": "none",
                "message": "SpecPM validation JSON was not found beside the rendered candidate.",
            }
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return {
                "status": "invalid",
                "source": relative_display_path(self.root, path),
                "message": f"Validation JSON could not be read: {exc}",
            }
        error_count = integer_value(loaded.get("error_count"))
        warning_count = integer_value(loaded.get("warning_count"))
        return {
            "status": "ok" if error_count == 0 else "error",
            "source": relative_display_path(self.root, path),
            "errorCount": error_count,
            "warningCount": warning_count,
            "raw": loaded,
        }

    def diagnostics(self) -> list[RendererDiagnostic]:
        validation = self.payload()
        if validation["status"] != "invalid":
            return []
        return [
            RendererDiagnostic(
                severity="warning",
                code="validation_json_unreadable",
                message=validation["message"],
                path=validation["source"],
            )
        ]

    def path(self) -> Path | None:
        for name in ("specpm-validation.json", "validation.json"):
            candidate = self.root / name
            if candidate.is_file() and not candidate.is_symlink():
                return candidate
        return None


class StaticSpecSite:
    def __init__(self, output: Path):
        self.output = output

    def write(self, payload: dict[str, Any]) -> list[str]:
        self.output.mkdir(parents=True, exist_ok=True)
        assets = self.output / "assets"
        if assets.exists():
            shutil.rmtree(assets)
        assets.mkdir(parents=True)
        serialized_payload = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
        files = {
            self.output / "index.html": INDEX_HTML.replace(
                "__SPEC_PACKAGE_JSON__",
                script_safe_json(serialized_payload),
            ),
            assets / "spec-renderer.css": VIEWER_CSS,
            assets / "spec-renderer.js": VIEWER_JS,
            self.output / "spec-package.json": serialized_payload + "\n",
        }
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
        return sorted(relative_display_path(self.output, path) for path in files)


def render_static_spec_site(options: StaticSpecRendererOptions) -> dict[str, Any]:
    return StaticSpecRenderer(options).render()


def write_static_spec_site(candidate: Path, output: Path) -> dict[str, Any]:
    return render_static_spec_site(StaticSpecRendererOptions(candidate=candidate, output=output))


def path_is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def relative_display_path(root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str) and item)


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) else 0


def script_safe_json(serialized_payload: str) -> str:
    return (
        serialized_payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    )
