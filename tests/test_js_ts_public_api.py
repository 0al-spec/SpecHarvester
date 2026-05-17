from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.interface_index import validate_public_interface_index
from spec_harvester.js_ts_public_api import analyze_js_ts_public_api


def test_analyze_js_ts_public_api_extracts_manifest_entrypoints_and_exports(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps(
            {
                "name": "@scope/demo",
                "main": "./dist/index.js",
                "types": "./dist/index.d.ts",
                "exports": {
                    ".": "./src/index.ts",
                    "./feature": {
                        "import": "./src/feature.js",
                        "types": "./src/feature.d.ts",
                    },
                },
                "bin": {"demo": "./bin/cli.js"},
                "scripts": {"postinstall": "node ./scripts/postinstall.js"},
            }
        ),
        encoding="utf-8",
    )
    for directory in ("dist", "src", "bin"):
        (package / directory).mkdir()
    (package / "dist" / "index.js").write_text(
        """
export { buildGraph as createGraph } from "../src/index.js";
export default class Demo {}
""",
        encoding="utf-8",
    )
    (package / "dist" / "index.d.ts").write_text(
        "export interface DistOptions {}\n",
        encoding="utf-8",
    )
    (package / "src" / "index.ts").write_text(
        """
export function buildGraph(nodes, edges = []) {
  return nodes;
}
export async function loadGraph(source) {
  return source;
}
export class Graph {}
export interface GraphOptions {}
export type GraphId = string;
export enum Mode { Fast }
export const VERSION = "1", RUNTIME = true;
export let mutableValue = 1;
export var legacyValue = 2;
const internal = 1;
export { internal as exposedInternal, type GraphId as PublicGraphId };
export default function createDefault() {}
""",
        encoding="utf-8",
    )
    (package / "src" / "feature.js").write_text(
        "export class Feature {}\n",
        encoding="utf-8",
    )
    (package / "src" / "feature.d.ts").write_text(
        "export type FeatureOptions = { enabled: boolean };\n",
        encoding="utf-8",
    )
    (package / "bin" / "cli.js").write_text(
        "#!/usr/bin/env node\nconsole.log('demo')\n",
        encoding="utf-8",
    )

    index = analyze_js_ts_public_api(
        package,
        package_id="demo.js",
        source_revision="abc123",
    )

    validate_public_interface_index(index)
    assert json.dumps(index, sort_keys=True) == json.dumps(index, sort_keys=True)
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"] == [
        {
            "id": "js-ts-manifest-export-analyzer",
            "version": "0.1.0",
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "confidence": "medium",
        }
    ]
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 6,
        "symbolCount": 18,
        "diagnosticCount": 0,
    }

    package_record = index["packages"][0]
    assert package_record["id"] == "demo.js"
    assert package_record["path"] == "."
    assert package_record["language"] == "javascript-typescript"

    entrypoints = {
        entrypoint["path"]: {symbol["name"]: symbol for symbol in entrypoint["symbols"]}
        for entrypoint in package_record["entrypoints"]
    }
    assert sorted(entrypoints) == [
        "bin/cli.js",
        "dist/index.d.ts",
        "dist/index.js",
        "src/feature.d.ts",
        "src/feature.js",
        "src/index.ts",
    ]
    assert entrypoints["bin/cli.js"] == {}
    assert entrypoints["dist/index.js"]["createGraph"]["kind"] == "unknown"
    assert entrypoints["dist/index.js"]["default"]["kind"] == "class"
    assert entrypoints["dist/index.d.ts"]["DistOptions"]["kind"] == "interface"
    assert entrypoints["src/feature.js"]["Feature"]["kind"] == "class"
    assert entrypoints["src/feature.d.ts"]["FeatureOptions"]["kind"] == "type"

    source_symbols = entrypoints["src/index.ts"]
    assert sorted(source_symbols) == [
        "Graph",
        "GraphId",
        "GraphOptions",
        "Mode",
        "PublicGraphId",
        "RUNTIME",
        "VERSION",
        "buildGraph",
        "default",
        "exposedInternal",
        "legacyValue",
        "loadGraph",
        "mutableValue",
    ]
    assert source_symbols["buildGraph"]["kind"] == "function"
    assert source_symbols["buildGraph"]["signature"] == "buildGraph(nodes, edges = [])"
    assert source_symbols["loadGraph"]["kind"] == "function"
    assert source_symbols["Graph"]["kind"] == "class"
    assert source_symbols["GraphOptions"]["kind"] == "interface"
    assert source_symbols["GraphId"]["kind"] == "type"
    assert source_symbols["Mode"]["kind"] == "enum"
    assert source_symbols["VERSION"]["kind"] == "constant"
    assert source_symbols["RUNTIME"]["kind"] == "constant"
    assert source_symbols["mutableValue"]["kind"] == "variable"
    assert source_symbols["legacyValue"]["kind"] == "variable"
    assert source_symbols["exposedInternal"]["kind"] == "unknown"
    assert source_symbols["PublicGraphId"]["kind"] == "type"
    assert source_symbols["default"]["kind"] == "function"

    for symbols in entrypoints.values():
        for symbol in symbols.values():
            assert len(symbol["evidence"]["sha256"]) == 64


def test_analyze_js_ts_public_api_records_manifest_and_missing_entrypoint_diagnostics(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "package.json").write_text(
        '{"name": "broken", "main": "./missing.js", "exports": {"."',
        encoding="utf-8",
    )
    nested = package / "packages" / "valid"
    nested.mkdir(parents=True)
    (nested / "package.json").write_text(
        json.dumps({"name": "valid", "main": "./missing.js", "bin": "./cli.js"}),
        encoding="utf-8",
    )
    (nested / "cli.js").write_text("export default function main() {}\n", encoding="utf-8")
    node_modules = package / "node_modules" / "ignored"
    node_modules.mkdir(parents=True)
    (node_modules / "package.json").write_text(
        json.dumps({"name": "ignored", "main": "./index.js"}),
        encoding="utf-8",
    )

    index = analyze_js_ts_public_api(package)

    validate_public_interface_index(index)
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 1,
        "diagnosticCount": 2,
    }
    assert index["packages"][0]["id"] == "valid"
    assert index["packages"][0]["path"] == "packages/valid"
    assert index["packages"][0]["entrypoints"][0]["path"] == "packages/valid/cli.js"
    assert index["packages"][0]["entrypoints"][0]["symbols"][0]["name"] == "default"

    diagnostics = {diagnostic["path"]: diagnostic for diagnostic in index["diagnostics"]}
    assert sorted(diagnostics) == ["package.json", "packages/valid/missing.js"]
    assert diagnostics["package.json"]["level"] == "error"
    assert "Invalid package.json" in diagnostics["package.json"]["message"]
    assert diagnostics["packages/valid/missing.js"]["level"] == "warning"
    assert "does not exist" in diagnostics["packages/valid/missing.js"]["message"]


def test_analyze_js_ts_public_api_records_default_expression_exports(tmp_path: Path) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "default-expression", "main": "./index.js"}),
        encoding="utf-8",
    )
    (package / "index.js").write_text(
        """
const createClient = () => ({});
export default createClient;
""",
        encoding="utf-8",
    )

    index = analyze_js_ts_public_api(package)

    validate_public_interface_index(index)
    symbols = {
        symbol["name"]: symbol
        for entrypoint in index["packages"][0]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }
    assert sorted(symbols) == ["default"]
    assert symbols["default"]["kind"] == "unknown"


def test_analyze_js_ts_public_api_resolves_directory_entrypoints_to_index_files(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "package.json").write_text(
        json.dumps({"name": "directory-entrypoint", "main": "./dist", "exports": "./src"}),
        encoding="utf-8",
    )
    (package / "dist").mkdir()
    (package / "dist" / "index.js").write_text(
        "export function fromMain() {}\n",
        encoding="utf-8",
    )
    (package / "src").mkdir()
    (package / "src" / "index.ts").write_text(
        "export class FromExport {}\n",
        encoding="utf-8",
    )

    index = analyze_js_ts_public_api(package)

    validate_public_interface_index(index)
    assert index["diagnostics"] == []
    entrypoints = {
        entrypoint["path"]: {symbol["name"]: symbol for symbol in entrypoint["symbols"]}
        for entrypoint in index["packages"][0]["entrypoints"]
    }
    assert sorted(entrypoints) == ["dist/index.js", "src/index.ts"]
    assert entrypoints["dist/index.js"]["fromMain"]["kind"] == "function"
    assert entrypoints["src/index.ts"]["FromExport"]["kind"] == "class"


def test_analyze_js_ts_public_api_records_unreadable_manifest_and_continues(
    tmp_path: Path,
    monkeypatch,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    unreadable_manifest = package / "packages" / "bad" / "package.json"
    unreadable_manifest.parent.mkdir(parents=True)
    unreadable_manifest.write_text(json.dumps({"name": "bad"}), encoding="utf-8")
    valid = package / "packages" / "valid"
    valid.mkdir(parents=True)
    (valid / "package.json").write_text(
        json.dumps({"name": "valid", "main": "./index.js"}),
        encoding="utf-8",
    )
    (valid / "index.js").write_text("export function ok() {}\n", encoding="utf-8")
    original_read_bytes = Path.read_bytes

    def read_bytes_or_fail(path: Path) -> bytes:
        if path == unreadable_manifest:
            raise OSError("permission denied")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes_or_fail)

    index = analyze_js_ts_public_api(package)

    validate_public_interface_index(index)
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 1,
        "diagnosticCount": 1,
    }
    assert index["packages"][0]["id"] == "valid"
    assert index["packages"][0]["entrypoints"][0]["symbols"][0]["name"] == "ok"
    diagnostic = index["diagnostics"][0]
    assert diagnostic["level"] == "error"
    assert diagnostic["path"] == "packages/bad/package.json"
    assert "Unable to read package.json" in diagnostic["message"]


def test_analyze_js_ts_public_api_records_unreadable_entrypoint_diagnostics(
    tmp_path: Path,
    monkeypatch,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    entrypoint = package / "index.js"
    (package / "package.json").write_text(
        json.dumps({"name": "unreadable", "main": "./index.js"}),
        encoding="utf-8",
    )
    entrypoint.write_text("export function ok() {}\n", encoding="utf-8")
    original_read_bytes = Path.read_bytes

    def read_bytes_or_fail(path: Path) -> bytes:
        if path == entrypoint:
            raise OSError("permission denied")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes_or_fail)

    index = analyze_js_ts_public_api(package)

    validate_public_interface_index(index)
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 0,
        "symbolCount": 0,
        "diagnosticCount": 1,
    }
    diagnostic = index["diagnostics"][0]
    assert diagnostic["level"] == "error"
    assert diagnostic["path"] == "index.js"
    assert "Unable to read manifest entrypoint" in diagnostic["message"]
    assert diagnostic["evidence"]["path"] == "package.json"


def test_analyze_js_ts_public_api_rejects_non_directory_source(tmp_path: Path) -> None:
    source = tmp_path / "package.json"
    source.write_text("{}", encoding="utf-8")

    try:
        analyze_js_ts_public_api(source)
    except ValueError as exc:
        assert "does not exist or is not a directory" in str(exc)
    else:
        raise AssertionError("expected ValueError")
