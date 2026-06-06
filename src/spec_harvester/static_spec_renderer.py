from __future__ import annotations

import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from yaml.tokens import AliasToken, AnchorToken, TagToken

from spec_harvester.bundle_set_preflight import (
    BUNDLE_SET_PREFLIGHT_API_VERSION,
    BUNDLE_SET_PREFLIGHT_KIND,
)
from spec_harvester.package_set_drafter import (
    PACKAGE_RELATION_PROPOSALS_API_VERSION,
    PACKAGE_RELATION_PROPOSALS_FILENAME,
    PACKAGE_RELATION_PROPOSALS_KIND,
    PACKAGE_SET_DRAFT_API_VERSION,
    PACKAGE_SET_DRAFT_FILENAME,
    PACKAGE_SET_DRAFT_KIND,
)
from spec_harvester.static_spec_renderer_assets import INDEX_HTML, VIEWER_CSS, VIEWER_JS

RENDERER_API_VERSION = "spec-harvester.static-spec-renderer/v0"
PACKAGE_SET_RENDERER_API_VERSION = "spec-harvester.static-package-set-renderer/v0"
RENDERER_SCHEMA_VERSION = 1
RENDERER_NAME = "spec-harvester-static-spec-renderer"
PACKAGE_SET_PREFLIGHT_FILENAME = "bundle-set-preflight.json"


@dataclass(frozen=True)
class StaticSpecRendererOptions:
    candidate: Path
    output: Path


@dataclass(frozen=True)
class StaticPackageSetRendererOptions:
    bundle_set: Path
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
        written = site.write(payload, data_filename="spec-package.json")
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


class StaticPackageSetRenderer:
    def __init__(self, options: StaticPackageSetRendererOptions):
        self.options = options

    def render(self) -> dict[str, Any]:
        try:
            payload = PackageSetReviewBundle(self.options.bundle_set).payload()
        except StaticSpecRenderError as exc:
            return {
                "status": "error",
                "bundleSet": str(self.options.bundle_set),
                "output": str(self.options.output),
                "diagnostics": [diagnostic.as_dict() for diagnostic in exc.diagnostics],
            }

        site = StaticSpecSite(self.options.output)
        written = site.write(payload, data_filename="package-set.json")
        package_set = payload["packageSet"]
        return {
            "status": "ok",
            "bundleSet": str(self.options.bundle_set),
            "output": str(self.options.output),
            "packageSetId": package_set.get("id"),
            "candidateCount": len(payload["members"]),
            "relationCount": len(payload["relations"]),
            "preflightStatus": payload["preflight"].get("status"),
            "written": written,
        }


class PackageSetReviewBundle:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def payload(self) -> dict[str, Any]:
        draft = JsonRequiredDocument(self.root, PACKAGE_SET_DRAFT_FILENAME).required_mapping()
        relations = JsonRequiredDocument(
            self.root, PACKAGE_RELATION_PROPOSALS_FILENAME
        ).required_mapping()
        self.check_draft_identity(draft)
        self.check_relation_identity(relations)
        candidates = self.candidate_members(draft)
        return {
            "apiVersion": PACKAGE_SET_RENDERER_API_VERSION,
            "schemaVersion": RENDERER_SCHEMA_VERSION,
            "kind": "SpecHarvesterStaticPackageSet",
            "renderer": {
                "name": RENDERER_NAME,
                "schemaVersion": RENDERER_SCHEMA_VERSION,
                "trustBoundary": (
                    "Package-set artifacts parsed locally as untrusted data; "
                    "no package code executed."
                ),
            },
            "packageSet": self.package_set_payload(draft, candidates),
            "members": candidates,
            "relations": relation_payloads(relations),
            "preflight": OptionalBundleSetPreflight(self.root).payload(),
            "diagnostics": [],
        }

    def check_draft_identity(self, draft: dict[str, Any]) -> None:
        expected = {
            "apiVersion": PACKAGE_SET_DRAFT_API_VERSION,
            "kind": PACKAGE_SET_DRAFT_KIND,
            "schemaVersion": 1,
        }
        diagnostics = [
            RendererDiagnostic(
                severity="error",
                code="package_set_draft_identity_invalid",
                message=f"{key} must be {value!r}.",
                path=PACKAGE_SET_DRAFT_FILENAME,
                field=key,
            )
            for key, value in expected.items()
            if draft.get(key) != value
        ]
        if diagnostics:
            raise StaticSpecRenderError(diagnostics)

    def check_relation_identity(self, relations: dict[str, Any]) -> None:
        expected = {
            "apiVersion": PACKAGE_RELATION_PROPOSALS_API_VERSION,
            "kind": PACKAGE_RELATION_PROPOSALS_KIND,
            "schemaVersion": 1,
        }
        diagnostics = [
            RendererDiagnostic(
                severity="error",
                code="package_relation_proposals_identity_invalid",
                message=f"{key} must be {value!r}.",
                path=PACKAGE_RELATION_PROPOSALS_FILENAME,
                field=key,
            )
            for key, value in expected.items()
            if relations.get(key) != value
        ]
        if diagnostics:
            raise StaticSpecRenderError(diagnostics)

    def package_set_payload(
        self,
        draft: dict[str, Any],
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        source = mapping_value(draft.get("source"))
        selection = mapping_value(draft.get("selection"))
        summary = mapping_value(draft.get("summary"))
        workspace = next(
            (candidate for candidate in candidates if candidate.get("role") == "workspace"),
            candidates[0] if candidates else {},
        )
        return {
            "id": string_value(workspace.get("packageId")) or "package-set",
            "status": "producer_preview",
            "reviewStatus": string_value(
                mapping_value(draft.get("relationProposals")).get("reviewStatus")
            ),
            "authority": string_value(draft.get("authority")),
            "repository": string_value(source.get("repository")),
            "exactRevision": string_value(source.get("exactRevision")),
            "selectedRoles": string_list(selection.get("roles")),
            "summary": {
                "candidateCount": integer_value(summary.get("candidateCount")),
                "skippedCount": integer_value(summary.get("skippedCount")),
                "relationProposalCount": integer_value(summary.get("relationProposalCount")),
            },
            "nonGoals": string_list(draft.get("nonGoals")),
        }

    def candidate_members(self, draft: dict[str, Any]) -> list[dict[str, Any]]:
        candidates = list_value(draft.get("candidates"))
        return sorted(
            [
                self.candidate_member(candidate)
                for candidate in candidates
                if isinstance(candidate, dict)
            ],
            key=lambda item: (item["role"] != "workspace", item["packageId"]),
        )

    def candidate_member(self, candidate: dict[str, Any]) -> dict[str, Any]:
        candidate_path = string_value(candidate.get("candidatePath"))
        manifest = self.candidate_manifest(candidate_path)
        metadata = mapping_value(manifest.get("metadata"))
        return {
            "packageId": string_value(candidate.get("packageId")),
            "role": string_value(candidate.get("role")),
            "candidatePath": candidate_path,
            "manifestPath": string_value(candidate.get("manifest")),
            "sourceTargetPath": string_value(candidate.get("sourceTargetPath")),
            "packageManifestPath": string_value(candidate.get("manifestPath")),
            "status": string_value(candidate.get("status")),
            "name": string_value(metadata.get("name")),
            "summary": string_value(metadata.get("summary")),
            "version": string_value(metadata.get("version")),
            "previewOnly": bool(manifest.get("preview_only", False)),
            "capabilities": manifest_capabilities(manifest),
            "intents": manifest_intents(manifest),
        }

    def candidate_manifest(self, candidate_path: str) -> dict[str, Any]:
        if not candidate_path:
            return {}
        manifest_path = self.root / candidate_path / "specpm.yaml"
        try:
            return SpecYamlDocument(self.root, manifest_path).required_mapping()
        except StaticSpecRenderError:
            return {}


class CandidateSpecPackage:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def payload(self) -> dict[str, Any]:
        manifest_path = self.root / "specpm.yaml"
        manifest = SpecYamlDocument(self.root, manifest_path).required_mapping()
        spec_refs = ManifestSpecReferences(self.root, manifest).paths()
        specs = [BoundarySpecDocument(self.root, spec_path).payload() for spec_path in spec_refs]
        validation = CandidateValidationSummary(self.root).payload()
        validation_diagnostics = CandidateValidationSummary(self.root).diagnostics()
        producer = ProducerBundleEvidence(self.root).payload()
        diagnostics = validation_diagnostics + ProducerBundleEvidence(self.root).diagnostics()
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
            "producer": producer,
            "diagnostics": [diagnostic.as_dict() for diagnostic in diagnostics],
        }


class SpecYamlDocument:
    def __init__(self, root: Path, path: Path):
        self.root = root
        self.path = path

    def required_mapping(self) -> dict[str, Any]:
        self.ensure_readable_inside_root()
        try:
            text = self.path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise StaticSpecRenderError(
                [self.diagnostic("file_unreadable", f"Cannot read YAML file: {exc}")]
            ) from exc
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
        if value is None or isinstance(value, (str, bool, int)):
            return None
        if isinstance(value, float):
            return None if math.isfinite(value) else path
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
            spec_path = self.root / raw_path
            if not path_is_inside(spec_path.resolve(strict=False), self.root):
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
            loaded = json.loads(
                path.read_text(encoding="utf-8"),
                parse_constant=self.reject_non_finite_number,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            return self.invalid(path, f"Validation JSON could not be read: {exc}")
        if not isinstance(loaded, dict):
            return self.invalid(path, "Validation JSON must be an object.")
        json_issue = JsonCompatibleValue(loaded).issue_path()
        if json_issue is not None:
            return self.invalid(
                path,
                f"Validation JSON value is not JSON-compatible at {json_issue}.",
            )
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

    def invalid(self, path: Path, message: str) -> dict[str, Any]:
        return {
            "status": "invalid",
            "source": relative_display_path(self.root, path),
            "message": message,
        }

    def reject_non_finite_number(self, value: str) -> None:
        raise ValueError(f"non-finite JSON number is not supported: {value}")

    def path(self) -> Path | None:
        for name in ("specpm-validation.json", "validation.json"):
            candidate = self.root / name
            if candidate.is_file() and not candidate.is_symlink():
                return candidate
        return None


class ProducerBundleEvidence:
    def __init__(self, root: Path):
        self.root = root

    def payload(self) -> dict[str, Any]:
        receipt_artifact = JsonArtifact(self.root, "producer-receipt.json").payload()
        validation_artifact = JsonArtifact(self.root, "validation-report.json").payload()
        diagnostics_artifact = JsonArtifact(self.root, "diagnostics.json").payload()
        receipt = mapping_value(receipt_artifact.get("raw"))
        validation_report = mapping_value(validation_artifact.get("raw"))
        diagnostics_report = mapping_value(diagnostics_artifact.get("raw"))
        receipt_validation = mapping_value(receipt.get("validation"))
        receipt_diagnostics = mapping_value(receipt.get("diagnostics"))
        artifacts = [receipt_artifact, validation_artifact, diagnostics_artifact]
        if all(artifact["status"] == "not_provided" for artifact in artifacts):
            return {
                "status": "not_provided",
                "message": "Producer receipt artifacts were not found beside the candidate.",
                "trustBoundary": producer_trust_boundary(),
                "artifacts": artifacts,
            }
        return {
            "status": producer_status(artifacts),
            "trustBoundary": producer_trust_boundary(),
            "artifacts": artifacts,
            "receipt": {
                "apiVersion": string_value(receipt.get("apiVersion")),
                "kind": string_value(receipt.get("kind")),
                "schemaVersion": integer_value(receipt.get("schemaVersion")),
                "receiptProfile": string_value(receipt.get("receiptProfile")),
                "receiptId": string_value(receipt.get("receiptId")),
            },
            "producer": mapping_value(receipt.get("producer")),
            "subject": mapping_value(receipt.get("subject")),
            "inputs": object_list(receipt.get("inputs")),
            "outputs": object_list(receipt.get("outputs")),
            "validation": {
                "status": string_value(receipt_validation.get("status")),
                "warningCount": integer_value(receipt_validation.get("warningCount")),
                "errorCount": integer_value(receipt_validation.get("errorCount")),
                "reportPath": string_value(receipt_validation.get("reportPath")),
                "reportDigest": mapping_value(receipt_validation.get("reportDigest")),
                "report": {
                    "kind": string_value(validation_report.get("kind")),
                    "status": string_value(validation_report.get("status")),
                    "summary": mapping_value(validation_report.get("summary")),
                    "authority": string_value(validation_report.get("authority")),
                },
            },
            "diagnostics": {
                "status": string_value(receipt_diagnostics.get("status")),
                "path": string_value(receipt_diagnostics.get("path")),
                "digest": mapping_value(receipt_diagnostics.get("digest")),
                "entries": object_list(receipt_diagnostics.get("entries")),
                "report": {
                    "kind": string_value(diagnostics_report.get("kind")),
                    "status": string_value(diagnostics_report.get("status")),
                    "summary": mapping_value(diagnostics_report.get("summary")),
                    "privacy": mapping_value(diagnostics_report.get("privacy")),
                    "security": mapping_value(diagnostics_report.get("security")),
                    "review": mapping_value(diagnostics_report.get("review")),
                },
            },
            "humanReview": mapping_value(receipt.get("humanReview")),
        }

    def diagnostics(self) -> list[RendererDiagnostic]:
        diagnostics = []
        for name in ("producer-receipt.json", "validation-report.json", "diagnostics.json"):
            artifact = JsonArtifact(self.root, name).payload()
            if artifact["status"] == "invalid":
                diagnostics.append(
                    RendererDiagnostic(
                        severity="warning",
                        code="producer_artifact_unreadable",
                        message=artifact["message"],
                        path=name,
                    )
                )
        return diagnostics


class JsonArtifact:
    def __init__(self, root: Path, name: str):
        self.root = root
        self.name = name

    def payload(self) -> dict[str, Any]:
        path = self.root / self.name
        if not path.exists():
            return {"path": self.name, "status": "not_provided"}
        if path.is_symlink():
            return {
                "path": self.name,
                "status": "invalid",
                "message": "Producer artifact symlinks are not supported.",
            }
        if not path.is_file():
            return {
                "path": self.name,
                "status": "invalid",
                "message": "Producer artifact is not a regular file.",
            }
        try:
            loaded = json.loads(
                path.read_text(encoding="utf-8"),
                parse_constant=self.reject_non_finite_number,
            )
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            return {"path": self.name, "status": "invalid", "message": f"Cannot read JSON: {exc}"}
        if not isinstance(loaded, dict):
            return {"path": self.name, "status": "invalid", "message": "JSON must be an object."}
        json_issue = JsonCompatibleValue(loaded).issue_path()
        if json_issue is not None:
            return {
                "path": self.name,
                "status": "invalid",
                "message": f"JSON value is not JSON-compatible at {json_issue}.",
            }
        return {"path": self.name, "status": "available", "raw": loaded}

    def reject_non_finite_number(self, value: str) -> None:
        raise ValueError(f"non-finite JSON number is not supported: {value}")


class JsonRequiredDocument:
    def __init__(self, root: Path, name: str):
        self.root = root
        self.name = name

    def required_mapping(self) -> dict[str, Any]:
        artifact = JsonArtifact(self.root, self.name).payload()
        if artifact["status"] == "available":
            raw = artifact.get("raw")
            if isinstance(raw, dict):
                return raw
        message = artifact.get("message") or "Required package-set JSON artifact is missing."
        raise StaticSpecRenderError(
            [
                RendererDiagnostic(
                    severity="error",
                    code="package_set_artifact_unreadable",
                    message=str(message),
                    path=self.name,
                )
            ]
        )


class OptionalBundleSetPreflight:
    def __init__(self, root: Path):
        self.root = root

    def payload(self) -> dict[str, Any]:
        artifact = JsonArtifact(self.root, PACKAGE_SET_PREFLIGHT_FILENAME).payload()
        if artifact["status"] != "available":
            return {
                "status": "not_provided",
                "path": PACKAGE_SET_PREFLIGHT_FILENAME,
                "message": "Bundle-set preflight report was not found beside the package set.",
            }
        raw = mapping_value(artifact.get("raw"))
        if (
            raw.get("apiVersion") != BUNDLE_SET_PREFLIGHT_API_VERSION
            or raw.get("kind") != BUNDLE_SET_PREFLIGHT_KIND
        ):
            return {
                "status": "invalid",
                "path": PACKAGE_SET_PREFLIGHT_FILENAME,
                "message": "Bundle-set preflight report identity is invalid.",
            }
        summary = mapping_value(raw.get("summary"))
        return {
            "status": string_value(raw.get("status")),
            "path": PACKAGE_SET_PREFLIGHT_FILENAME,
            "candidateCount": integer_value(summary.get("candidateCount")),
            "relationCount": integer_value(summary.get("relationCount")),
            "errorCount": integer_value(summary.get("errorCount")),
            "warningCount": integer_value(summary.get("warningCount")),
            "candidateReports": object_list(raw.get("candidateReports")),
        }


class StaticSpecSite:
    def __init__(self, output: Path):
        self.output = output

    def write(self, payload: dict[str, Any], *, data_filename: str) -> list[str]:
        self.output.mkdir(parents=True, exist_ok=True)
        assets = self.output / "assets"
        if assets.exists():
            shutil.rmtree(assets)
        assets.mkdir(parents=True)
        serialized_payload = json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        files = {
            self.output / "index.html": INDEX_HTML.replace(
                "__SPEC_PACKAGE_JSON__",
                script_safe_json(serialized_payload),
            ).replace(
                "__SPEC_PACKAGE_JSON_HREF__",
                data_filename,
            ),
            assets / "spec-renderer.css": VIEWER_CSS,
            assets / "spec-renderer.js": VIEWER_JS,
            self.output / data_filename: serialized_payload + "\n",
        }
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
        return sorted(relative_display_path(self.output, path) for path in files)


def render_static_spec_site(options: StaticSpecRendererOptions) -> dict[str, Any]:
    return StaticSpecRenderer(options).render()


def render_static_package_set_site(options: StaticPackageSetRendererOptions) -> dict[str, Any]:
    return StaticPackageSetRenderer(options).render()


def write_static_spec_site(candidate: Path, output: Path) -> dict[str, Any]:
    return render_static_spec_site(StaticSpecRendererOptions(candidate=candidate, output=output))


def write_static_package_set_site(bundle_set: Path, output: Path) -> dict[str, Any]:
    return render_static_package_set_site(
        StaticPackageSetRendererOptions(bundle_set=bundle_set, output=output)
    )


def path_is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def relative_display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        pass
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def object_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def relation_payloads(relations: dict[str, Any]) -> list[dict[str, Any]]:
    records = list_value(relations.get("relations"))
    return sorted(
        [
            {
                "id": string_value(relation.get("id")),
                "type": string_value(relation.get("type")),
                "reviewStatus": string_value(relation.get("reviewStatus")),
                "authority": string_value(relation.get("authority")),
                "source": mapping_value(relation.get("source")),
                "target": mapping_value(relation.get("target")),
                "evidenceCount": len(list_value(relation.get("evidence"))),
            }
            for relation in records
            if isinstance(relation, dict)
        ],
        key=lambda item: item["id"],
    )


def manifest_capabilities(manifest: dict[str, Any]) -> list[str]:
    provides = mapping_value(mapping_value(manifest.get("index")).get("provides"))
    return string_list(provides.get("capabilities"))


def manifest_intents(manifest: dict[str, Any]) -> list[str]:
    provides = mapping_value(mapping_value(manifest.get("index")).get("provides"))
    return string_list(provides.get("intents"))


def string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted(item for item in value if isinstance(item, str) and item)


def integer_value(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def script_safe_json(serialized_payload: str) -> str:
    return (
        serialized_payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    )


def producer_status(artifacts: list[dict[str, Any]]) -> str:
    statuses = {artifact["status"] for artifact in artifacts}
    if "invalid" in statuses:
        return "invalid"
    if "not_provided" in statuses:
        return "partial"
    return "available"


def producer_trust_boundary() -> str:
    return (
        "Generated producer evidence is review material only; it is not SpecPM acceptance, "
        "maintainer approval, or public index publication authority."
    )
