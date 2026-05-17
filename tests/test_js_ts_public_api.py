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


def test_analyze_js_ts_public_api_rejects_non_directory_source(tmp_path: Path) -> None:
    source = tmp_path / "package.json"
    source.write_text("{}", encoding="utf-8")

    try:
        analyze_js_ts_public_api(source)
    except ValueError as exc:
        assert "does not exist or is not a directory" in str(exc)
    else:
        raise AssertionError("expected ValueError")
