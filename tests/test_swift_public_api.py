from __future__ import annotations

from pathlib import Path

import pytest

from spec_harvester.interface_index import validate_public_interface_index
from spec_harvester.swift_public_api import (
    SWIFT_PUBLIC_API_ANALYZER_ID,
    analyze_swift_public_api,
    swift_source_files,
)


def test_analyze_swift_public_api_extracts_public_and_open_declarations(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "swift-demo"
    source = repo / "Sources" / "SwiftDemo"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        """
        // swift-tools-version: 6.0
        import PackageDescription
        let package = Package(name: "SwiftDemo")
        """,
        encoding="utf-8",
    )
    (source / "API.swift").write_text(
        """
import Foundation

/// Builds a graph.
public func buildGraph(nodes: [String]) async throws -> Graph {
    Graph(id: "root")
}

public struct Graph: Sendable {
    public let id: String
    public var count: Int { 0 }
    let hidden: String

    public init(id: String) {
        self.id = id
        self.hidden = ""
    }

    public func connect(_ target: Graph) -> Edge {
        Edge()
    }

    private func hiddenMethod() {}

    public enum State {
        case idle
        case running(task: String), failed(Error)
    }
}

public struct Edge {}

open class GraphController {
    open func start() {}
    public var isRunning: Bool { false }
}

public protocol Graphing {
    associatedtype Node
    func connect(_ node: Node)
    var nodes: [Node] { get }
}

public enum ResultState {
    case success(String), failure(Error)
}

public typealias Handler = (Graph) -> Void
public actor GraphActor {}

internal struct Hidden {}
private func hidden()
let modulePrivate = 1

let example = "public func notADeclaration() {}"
// public func commentedOut() {}
""",
        encoding="utf-8",
    )

    index = analyze_swift_public_api(repo, source_revision="abc123")

    validate_public_interface_index(index)
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"] == [
        {
            "id": SWIFT_PUBLIC_API_ANALYZER_ID,
            "version": "0.1.0",
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "confidence": "medium",
        }
    ]
    assert index["packages"][0]["id"] == "SwiftDemo"
    assert index["packages"][0]["language"] == "swift"
    assert index["packages"][0]["entrypoints"][0]["path"] == "Sources/SwiftDemo/API.swift"

    symbols = {
        symbol["name"]: symbol for symbol in index["packages"][0]["entrypoints"][0]["symbols"]
    }
    assert sorted(symbols) == [
        "Edge",
        "Graph",
        "Graph.State",
        "Graph.State.failed",
        "Graph.State.idle",
        "Graph.State.running",
        "Graph.connect",
        "Graph.count",
        "Graph.id",
        "Graph.init",
        "GraphActor",
        "GraphController",
        "GraphController.isRunning",
        "GraphController.start",
        "Graphing",
        "Graphing.Node",
        "Graphing.connect",
        "Graphing.nodes",
        "Handler",
        "ResultState",
        "ResultState.failure",
        "ResultState.success",
        "buildGraph",
    ]
    assert symbols["buildGraph"]["kind"] == "function"
    assert symbols["buildGraph"]["doc"] == "Builds a graph."
    assert symbols["Graph"]["kind"] == "struct"
    assert symbols["Graph.id"]["kind"] == "constant"
    assert symbols["Graph.count"]["kind"] == "variable"
    assert symbols["Graph.State"]["kind"] == "enum"
    assert symbols["Graph.State.running"]["kind"] == "constant"
    assert symbols["GraphController"]["kind"] == "class"
    assert symbols["GraphController"]["visibility"] == "open"
    assert symbols["GraphController.start"]["visibility"] == "open"
    assert symbols["Graphing"]["kind"] == "interface"
    assert symbols["Handler"]["kind"] == "type"
    assert symbols["GraphActor"]["kind"] == "type"
    assert "Hidden" not in symbols
    assert "hidden" not in symbols
    assert "notADeclaration" not in symbols
    assert "commentedOut" not in symbols


def test_swift_public_api_handles_public_extensions_and_multiple_packages(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "monorepo"
    root_source = repo / "Sources" / "Root"
    nested_source = repo / "Packages" / "Feature" / "Sources" / "Feature"
    root_source.mkdir(parents=True)
    nested_source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "RootPackage")\n',
        encoding="utf-8",
    )
    (repo / "Packages" / "Feature" / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "FeaturePackage")\n',
        encoding="utf-8",
    )
    (root_source / "RootAPI.swift").write_text(
        """
public struct RootAPI {}
public extension RootAPI {
    func makeFeature() -> String { "feature" }
}
""",
        encoding="utf-8",
    )
    (nested_source / "FeatureAPI.swift").write_text(
        "public struct FeatureAPI {}\n",
        encoding="utf-8",
    )

    index = analyze_swift_public_api(repo)

    packages = {package["path"]: package for package in index["packages"]}
    assert sorted(packages) == [".", "Packages/Feature"]
    assert packages["."]["id"] == "RootPackage"
    assert packages["Packages/Feature"]["id"] == "FeaturePackage"
    root_symbols = {
        symbol["name"]
        for entrypoint in packages["."]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }
    nested_symbols = {
        symbol["name"]
        for entrypoint in packages["Packages/Feature"]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }
    assert root_symbols == {"RootAPI", "RootAPI.makeFeature"}
    assert nested_symbols == {"FeatureAPI"}


def test_swift_public_api_skips_manifests_tests_build_outputs_and_symlinks(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "swift-demo"
    source = repo / "Sources" / "SwiftDemo"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "SwiftDemo")\n',
        encoding="utf-8",
    )
    (source / "API.swift").write_text("public struct API {}\n", encoding="utf-8")
    tests = repo / "Tests" / "SwiftDemoTests"
    tests.mkdir(parents=True)
    (tests / "APITests.swift").write_text("public struct TestAPI {}\n", encoding="utf-8")
    build = repo / ".build" / "checkouts" / "Dependency"
    build.mkdir(parents=True)
    (build / "Dependency.swift").write_text("public struct Dependency {}\n", encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "Outside.swift").write_text("public struct Outside {}\n", encoding="utf-8")
    (repo / "LinkedSources").symlink_to(outside, target_is_directory=True)

    assert [path.relative_to(repo).as_posix() for path in swift_source_files(repo)] == [
        "Sources/SwiftDemo/API.swift"
    ]

    index = analyze_swift_public_api(repo)
    symbols = {
        symbol["name"]
        for entrypoint in index["packages"][0]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }
    assert symbols == {"API"}


def test_swift_public_api_reuses_cached_file_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "swift-demo"
    source = repo / "Sources" / "SwiftDemo"
    cache_dir = tmp_path / "cache"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "SwiftDemo")\n',
        encoding="utf-8",
    )
    (source / "API.swift").write_text("public struct API {}\n", encoding="utf-8")

    first = analyze_swift_public_api(repo, cache_dir=cache_dir)

    def fail_swift_symbols(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("cache miss")

    monkeypatch.setattr("spec_harvester.swift_public_api.swift_symbols", fail_swift_symbols)

    second = analyze_swift_public_api(repo, cache_dir=cache_dir)

    assert second == first


def test_swift_public_api_reports_no_source_and_bad_source_root(tmp_path: Path) -> None:
    repo = tmp_path / "swift-demo"
    repo.mkdir()
    (repo / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "SwiftDemo")\n',
        encoding="utf-8",
    )

    index = analyze_swift_public_api(repo)

    assert index["summary"]["status"] == "failed"
    assert index["packages"] == []
    assert index["diagnostics"] == [
        {
            "level": "warning",
            "message": "No Swift source files were found.",
        }
    ]
    with pytest.raises(ValueError, match="Swift source root does not exist"):
        analyze_swift_public_api(tmp_path / "missing")


def test_swift_public_api_records_unreadable_source_and_continues(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "swift-demo"
    source = repo / "Sources" / "SwiftDemo"
    source.mkdir(parents=True)
    (repo / "Package.swift").write_text(
        'import PackageDescription\nlet package = Package(name: "SwiftDemo")\n',
        encoding="utf-8",
    )
    valid = source / "Valid.swift"
    unreadable = source / "Unreadable.swift"
    valid.write_text("public struct Valid {}\n", encoding="utf-8")
    unreadable.write_text("public struct Unreadable {}\n", encoding="utf-8")
    original_read_bytes = Path.read_bytes

    def read_bytes_or_fail(path: Path) -> bytes:
        if path == unreadable:
            raise OSError("permission denied")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes_or_fail)

    index = analyze_swift_public_api(repo)

    assert index["summary"] == {
        "status": "partial",
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 1,
        "diagnosticCount": 1,
    }
    assert index["packages"][0]["entrypoints"][0]["path"] == "Sources/SwiftDemo/Valid.swift"
    assert index["diagnostics"][0]["level"] == "error"
    assert index["diagnostics"][0]["path"] == "Sources/SwiftDemo/Unreadable.swift"
    assert "Unable to read Swift source file" in index["diagnostics"][0]["message"]


def test_swift_public_api_handles_split_scopes_subscripts_and_masked_text(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "source-only"
    repo.mkdir()
    (repo / "API.swift").write_text(
        '''
/* public struct HiddenBlock {} */
let stringLiteral = "public struct HiddenString {}"
let multilineLiteral = """
public struct HiddenMultiline {}
"""

/**
 * Split API docs.
 */
public struct SplitAPI
{
    public subscript(index: Int) -> String { "value" }
}

public func makeSplit(
    name: String,
    count: Int
) -> SplitAPI {
    SplitAPI()
}

private typealias HiddenAlias = String
internal enum InternalState {
    case hidden
}
''',
        encoding="utf-8",
    )

    index = analyze_swift_public_api(repo, package_id="demo.swift")

    assert index["packages"][0]["id"] == "demo.swift"
    symbols = {
        symbol["name"]: symbol for symbol in index["packages"][0]["entrypoints"][0]["symbols"]
    }
    assert sorted(symbols) == ["SplitAPI", "SplitAPI.subscript", "makeSplit"]
    assert symbols["SplitAPI"]["doc"] == "Split API docs."
    assert symbols["SplitAPI.subscript"]["kind"] == "function"
    assert symbols["makeSplit"]["signature"] == (
        "public func makeSplit( name: String, count: Int ) -> SplitAPI"
    )
    assert "HiddenBlock" not in symbols
    assert "HiddenString" not in symbols
    assert "HiddenMultiline" not in symbols
    assert "HiddenAlias" not in symbols
    assert "InternalState.hidden" not in symbols


def test_swift_public_api_falls_back_when_manifest_has_no_name_or_is_unreadable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "fallback-demo"
    source = repo / "Sources" / "Fallback"
    source.mkdir(parents=True)
    manifest = repo / "Package.swift"
    manifest.write_text("// no Package(name:) metadata\n", encoding="utf-8")
    (source / "API.swift").write_text("public struct API {}\n", encoding="utf-8")

    assert analyze_swift_public_api(repo)["packages"][0]["id"] == "fallback-demo"

    original_read_text = Path.read_text

    def read_text_or_fail(path: Path, *args, **kwargs):  # type: ignore[no-untyped-def]
        if path == manifest:
            raise OSError("permission denied")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text_or_fail)

    assert analyze_swift_public_api(repo)["packages"][0]["id"] == "fallback-demo"
