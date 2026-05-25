from __future__ import annotations

from pathlib import Path

import pytest

from spec_harvester.specpm_manifest import SpecPackageManifest


def write_manifest(path: Path, text: str) -> Path:
    path.write_text(text.strip() + "\n", encoding="utf-8")
    return path


def test_spec_package_manifest_reads_identity_namespace_and_metadata(tmp_path: Path) -> None:
    manifest = SpecPackageManifest.from_path(
        write_manifest(
            tmp_path / "specpm.yaml",
            """
metadata:
  id: example.core
  version: 1.2.3
  namespace: example
  license: MIT
""",
        )
    )

    assert manifest.package_id() == "example.core"
    assert manifest.package_version() == "1.2.3"
    assert manifest.namespace() == "example"
    assert manifest.metadata_strings()["license"] == "MIT"


def test_spec_package_manifest_rejects_missing_identity(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="metadata.id and metadata.version"):
        SpecPackageManifest.from_path(
            write_manifest(
                tmp_path / "specpm.yaml",
                """
metadata:
  id: missing.version
""",
            )
        )


def test_spec_package_manifest_reads_foreign_artifacts(tmp_path: Path) -> None:
    manifest = SpecPackageManifest.from_path(
        write_manifest(
            tmp_path / "specpm.yaml",
            """
metadata:
  id: example.core
  version: 1.0.0
foreignArtifacts:
  - id: upstream_repository
    uri: https://github.com/example/project
    role: source
    revision: abc123
  - artifact: docs
    uri: docs/README.md
""",
        )
    )

    assert [artifact.as_dict() for artifact in manifest.artifacts] == [
        {
            "id": "upstream_repository",
            "uri": "https://github.com/example/project",
            "role": "source",
            "revision": "abc123",
        },
        {
            "id": "docs",
            "uri": "docs/README.md",
        },
    ]


def test_spec_package_manifest_reads_index_claims(tmp_path: Path) -> None:
    manifest = SpecPackageManifest.from_path(
        write_manifest(
            tmp_path / "specpm.yaml",
            """
metadata:
  id: example.core
  version: 1.0.0
index:
  intents:
    - intent.package.utility
  provides:
    capabilities:
      - cap.one
      - cap.two
    intents:
      - intent.provided
""",
        )
    )

    assert manifest.intents == ("intent.package.utility", "intent.provided")
    assert manifest.capabilities == ("cap.one", "cap.two")


def test_spec_package_manifest_reads_license_evidence_paths(tmp_path: Path) -> None:
    manifest = SpecPackageManifest.from_path(
        write_manifest(
            tmp_path / "specpm.yaml",
            """
metadata:
  id: example.core
  version: 1.0.0
  license: UNKNOWN
  licenseEvidence:
    source: ambiguous_license_file
    confidence: low
    paths:
      - LICENSE.txt
      - COPYING.rst
""",
        )
    )

    assert manifest.license_evidence() == {
        "source": "ambiguous_license_file",
        "confidence": "low",
        "paths": ["LICENSE.txt", "COPYING.rst"],
    }


def test_spec_package_manifest_supports_inline_license_evidence_path(tmp_path: Path) -> None:
    manifest = SpecPackageManifest.from_path(
        write_manifest(
            tmp_path / "specpm.yaml",
            """
metadata:
  id: example.core
  version: 1.0.0
  licenseEvidence:
    paths: LICENSE
""",
        )
    )

    assert manifest.license_evidence() == {"paths": ["LICENSE"]}
