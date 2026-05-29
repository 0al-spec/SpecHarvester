from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.cli import main
from spec_harvester.static_spec_renderer import write_static_spec_site


def test_static_spec_renderer_writes_browser_safe_site(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    write_candidate(candidate, summary="<script>alert(1)</script>")
    output = tmp_path / "site"

    result = write_static_spec_site(candidate, output)

    assert result["status"] == "ok"
    assert result["packageId"] == "demo.core"
    assert result["specCount"] == 1
    assert (output / "index.html").is_file()
    assert (output / "assets/spec-renderer.js").is_file()
    assert (output / "assets/spec-renderer.css").is_file()
    assert (output / "spec-package.json").is_file()

    payload = json.loads((output / "spec-package.json").read_text(encoding="utf-8"))
    assert payload["kind"] == "SpecHarvesterStaticSpecPackage"
    assert payload["package"]["id"] == "demo.core"
    assert payload["package"]["capabilities"] == ["demo.core.render"]
    assert payload["package"]["intents"] == ["intent.spec.render_static_preview"]
    assert payload["validation"]["status"] == "ok"
    assert payload["specs"][0]["interfaces"]["inbound"][0]["name"] == "renderSpecSite"
    assert payload["specs"][0]["evidence"][0]["id"] == "manifest_evidence"

    html = (output / "index.html").read_text(encoding="utf-8")
    javascript = (output / "assets/spec-renderer.js").read_text(encoding="utf-8")
    css = (output / "assets/spec-renderer.css").read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in html
    assert "\\u003cscript" in html
    assert "__SPEC_PACKAGE_JSON__" not in html
    assert "spec-package-data" in html
    assert "escapeHtml" in javascript
    assert "textContent" in javascript
    assert "bindReadingControls" in javascript
    assert "filterSpecs" in javascript
    assert "specs.length <= 1" in javascript
    assert "min-width: 0;" in css
    assert "overflow-wrap: anywhere;" in css
    assert ".outline:empty" in css
    assert "spec-outline" in html
    assert "spec-search" in html


def test_render_spec_site_cli_writes_site_and_prints_result(tmp_path: Path, capsys) -> None:
    candidate = tmp_path / "candidate"
    write_candidate(candidate)
    output = tmp_path / "site"

    exit_code = main(["render-spec-site", "--candidate", str(candidate), "--output", str(output)])

    printed = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert printed["status"] == "ok"
    assert printed["written"] == [
        "assets/spec-renderer.css",
        "assets/spec-renderer.js",
        "index.html",
        "spec-package.json",
    ]


def test_render_spec_site_cli_returns_error_for_missing_manifest(tmp_path: Path, capsys) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()

    exit_code = main(
        ["render-spec-site", "--candidate", str(candidate), "--output", str(tmp_path / "site")]
    )

    printed = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert printed["status"] == "error"
    assert printed["diagnostics"][0]["code"] == "file_missing"
    assert not (tmp_path / "site" / "index.html").exists()


def test_static_spec_renderer_rejects_missing_referenced_spec(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "specpm.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: SpecPackage",
                "metadata:",
                "  id: demo.core",
                "  name: Demo",
                "  version: 0.1.0",
                "  summary: Demo",
                "  license: MIT",
                "specs:",
                "  - path: specs/missing.spec.yaml",
                "index:",
                "  provides:",
                "    capabilities: []",
                "    intents: []",
                "  requires:",
                "    capabilities: []",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = write_static_spec_site(candidate, tmp_path / "site")

    assert result["status"] == "error"
    assert result["diagnostics"][0]["code"] == "file_missing"
    assert result["diagnostics"][0]["path"] == "specs/missing.spec.yaml"


def test_static_spec_renderer_rejects_yaml_aliases(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "specpm.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: SpecPackage",
                "metadata: &metadata",
                "  id: demo.core",
                "  name: Demo",
                "  version: 0.1.0",
                "  summary: Demo",
                "  license: MIT",
                "copiedMetadata: *metadata",
                "specs: []",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = write_static_spec_site(candidate, tmp_path / "site")

    assert result["status"] == "error"
    assert result["diagnostics"][0]["code"] == "yaml_anchor_unsupported"


def test_static_spec_renderer_rejects_referenced_spec_symlink(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    write_candidate(candidate)
    link = candidate / "specs/linked.spec.yaml"
    link.symlink_to(candidate / "specs/demo.spec.yaml")
    (candidate / "specpm.yaml").write_text(
        (candidate / "specpm.yaml")
        .read_text(encoding="utf-8")
        .replace("specs/demo.spec.yaml", "specs/linked.spec.yaml"),
        encoding="utf-8",
    )

    result = write_static_spec_site(candidate, tmp_path / "site")

    assert result["status"] == "error"
    assert result["diagnostics"][0]["code"] == "symlink_unsupported"
    assert result["diagnostics"][0]["path"] == "specs/linked.spec.yaml"


def test_static_spec_renderer_rejects_non_finite_yaml_float(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    write_candidate(candidate)
    spec_path = candidate / "specs/demo.spec.yaml"
    spec_path.write_text(
        spec_path.read_text(encoding="utf-8") + "\ncustomScore: .nan\n",
        encoding="utf-8",
    )

    result = write_static_spec_site(candidate, tmp_path / "site")

    assert result["status"] == "error"
    assert result["diagnostics"][0]["code"] == "yaml_non_json_value"


def write_candidate(candidate: Path, *, summary: str = "Static renderer demo") -> None:
    specs = candidate / "specs"
    specs.mkdir(parents=True)
    (candidate / "specpm.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: SpecPackage",
                "metadata:",
                "  id: demo.core",
                "  name: Demo Core",
                "  version: 0.1.0",
                f"  summary: {json.dumps(summary)}",
                "  license: MIT",
                "preview_only: true",
                "specs:",
                "  - path: specs/demo.spec.yaml",
                "index:",
                "  provides:",
                "    capabilities:",
                "      - demo.core.render",
                "    intents:",
                "      - intent.spec.render_static_preview",
                "  requires:",
                "    capabilities: []",
                "compatibility:",
                "  specpm: ^0.2.0",
                "foreignArtifacts:",
                "  - id: source_repository",
                "    uri: https://github.com/example/demo",
                "keywords:",
                "  - generated",
                "  - specharvester",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (specs / "demo.spec.yaml").write_text(
        "\n".join(
            [
                "apiVersion: specpm.dev/v0.1",
                "kind: BoundarySpec",
                "metadata:",
                "  id: demo.core",
                "  title: Demo Static Renderer Boundary",
                "  version: 0.1.0",
                "  status: draft",
                "intent:",
                "  summary: Render generated SpecPM YAML as a static review site.",
                "scope:",
                "  boundedContext: static_spec_review",
                "  includes:",
                "    - Load generated candidate package YAML.",
                "  excludes:",
                "    - Execute harvested package code.",
                "provides:",
                "  capabilities:",
                "    - id: demo.core.render",
                "      role: primary",
                "      summary: Render static review output.",
                "requires:",
                "  capabilities: []",
                "interfaces:",
                "  inbound:",
                "    - name: renderSpecSite",
                "      summary: Render a candidate package into static HTML.",
                "  outbound: []",
                "effects:",
                "  sideEffects:",
                "    - kind: filesystem_write",
                "      summary: Writes static site files.",
                "constraints:",
                "  - id: no_package_execution",
                "    level: MUST",
                "    statement: Do not execute harvested package code.",
                "evidence:",
                "  - id: manifest_evidence",
                "    kind: package_manifest",
                "    path: specpm.yaml",
                "provenance:",
                "  generatedBy: tests",
                "keywords:",
                "  - static-preview",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (candidate / "specpm-validation.json").write_text(
        json.dumps({"error_count": 0, "warning_count": 1, "warnings": []}),
        encoding="utf-8",
    )
