from __future__ import annotations

import json
from pathlib import Path

from spec_harvester.interface_index import validate_public_interface_index
from spec_harvester.python_public_api import analyze_python_public_api


def test_analyze_python_public_api_extracts_public_symbols_deterministically(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    module = package / "api.py"
    module.write_text(
        '''
"""API module."""

__all__ = ["build_graph", "Graph", "_explicit_export"]

CONSTANT = 1
runtime_value = 2
_hidden_value = 3

def build_graph(nodes, edges=None, *extras, strict=False, **metadata):
    """Build graph docs."""
    return nodes

def _explicit_export():
    return "exported by __all__"

def _hidden_function():
    return None

class Graph:
    """Graph docs."""

    def connect(self, source, target):
        return source, target

    def _private_method(self):
        return None
''',
        encoding="utf-8",
    )

    index = analyze_python_public_api(
        package,
        package_id="demo.python",
        source_revision="abc123",
    )

    validate_public_interface_index(index)
    assert json.dumps(index, sort_keys=True) == json.dumps(index, sort_keys=True)
    assert index["sourceRevision"] == "abc123"
    assert index["analyzers"] == [
        {
            "id": "python-ast-public-api",
            "version": "0.1.0",
            "execution": "none",
            "networkAccess": "none",
            "packageScripts": "not_run",
            "confidence": "high",
        }
    ]
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 4,
        "diagnosticCount": 0,
    }

    package_record = index["packages"][0]
    assert package_record["id"] == "demo.python"
    assert package_record["path"] == "."
    assert package_record["language"] == "python"

    entrypoint = package_record["entrypoints"][0]
    assert entrypoint["path"] == "api.py"
    symbols = {symbol["name"]: symbol for symbol in entrypoint["symbols"]}
    assert sorted(symbols) == ["Graph", "Graph.connect", "_explicit_export", "build_graph"]
    assert symbols["build_graph"]["kind"] == "function"
    assert (
        symbols["build_graph"]["signature"]
        == "build_graph(nodes, edges=None, *extras, strict=False, **metadata)"
    )
    assert symbols["build_graph"]["doc"] == "Build graph docs."
    assert symbols["Graph"]["kind"] == "class"
    assert symbols["Graph"]["doc"] == "Graph docs."
    assert symbols["Graph.connect"]["kind"] == "function"
    assert symbols["_explicit_export"]["visibility"] == "public"

    for symbol in symbols.values():
        assert symbol["evidence"]["path"] == "api.py"
        assert len(symbol["evidence"]["sha256"]) == 64


def test_analyze_python_public_api_extracts_default_public_names_without_all(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "__init__.py").write_text(
        """
PUBLIC = 1
public_value = object()
_private_value = object()

def public_func(a: int, b: str = "x") -> str:
    return b

def _private_func():
    return None

class PublicClass:
    def method(self, item):
        return item

class _PrivateClass:
    pass
""",
        encoding="utf-8",
    )

    index = analyze_python_public_api(package)
    symbols = {
        symbol["name"]: symbol
        for entrypoint in index["packages"][0]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }

    assert sorted(symbols) == [
        "PUBLIC",
        "PublicClass",
        "PublicClass.method",
        "public_func",
        "public_value",
    ]
    assert symbols["PUBLIC"]["kind"] == "constant"
    assert symbols["public_value"]["kind"] == "variable"
    assert symbols["public_func"]["signature"] == "public_func(a: int, b: str = 'x') -> str"


def test_analyze_python_public_api_honors_final_all_assignment(tmp_path: Path) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "api.py").write_text(
        """
__all__ = ["old_export"]

def old_export():
    return "old"

def final_export():
    return "final"

__all__ = ["final_export"]
""",
        encoding="utf-8",
    )

    index = analyze_python_public_api(package)
    symbols = {
        symbol["name"]: symbol
        for entrypoint in index["packages"][0]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }

    assert sorted(symbols) == ["final_export"]


def test_analyze_python_public_api_preserves_positional_only_signature_marker(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "api.py").write_text(
        """
def callable_shape(a, b=1, /, c: int = 2, *, d, e=3):
    return a, b, c, d, e
""",
        encoding="utf-8",
    )

    index = analyze_python_public_api(package)
    symbols = {
        symbol["name"]: symbol
        for entrypoint in index["packages"][0]["entrypoints"]
        for symbol in entrypoint["symbols"]
    }

    assert (
        symbols["callable_shape"]["signature"] == "callable_shape(a, b=1, /, c: int = 2, *, d, e=3)"
    )


def test_analyze_python_public_api_records_parse_diagnostics_and_skips_cache_dirs(
    tmp_path: Path,
) -> None:
    package = tmp_path / "demo"
    package.mkdir()
    (package / "valid.py").write_text("def ok():\n    return True\n", encoding="utf-8")
    (package / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    (package / "null_byte.py").write_bytes(b"\x00")
    cache = package / "__pycache__"
    cache.mkdir()
    (cache / "ignored.py").write_text("def ignored():\n    pass\n", encoding="utf-8")

    index = analyze_python_public_api(package, package_id="demo.python")

    validate_public_interface_index(index)
    assert index["summary"] == {
        "packageCount": 1,
        "entrypointCount": 1,
        "symbolCount": 1,
        "diagnosticCount": 2,
    }
    assert [entrypoint["path"] for entrypoint in index["packages"][0]["entrypoints"]] == [
        "valid.py"
    ]
    assert index["packages"][0]["entrypoints"][0]["symbols"][0]["name"] == "ok"

    diagnostics = {diagnostic["path"]: diagnostic for diagnostic in index["diagnostics"]}
    assert sorted(diagnostics) == ["broken.py", "null_byte.py"]
    assert diagnostics["broken.py"]["level"] == "error"
    assert "invalid syntax" in diagnostics["broken.py"]["message"]
    assert diagnostics["broken.py"]["evidence"]["path"] == "broken.py"
    assert len(diagnostics["broken.py"]["evidence"]["sha256"]) == 64
    assert diagnostics["null_byte.py"]["level"] == "error"
    assert "null bytes" in diagnostics["null_byte.py"]["message"]
    assert diagnostics["null_byte.py"]["evidence"]["path"] == "null_byte.py"
    assert len(diagnostics["null_byte.py"]["evidence"]["sha256"]) == 64


def test_analyze_python_public_api_rejects_non_directory_source(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text("def ok():\n    return True\n", encoding="utf-8")

    try:
        analyze_python_public_api(source)
    except ValueError as exc:
        assert "does not exist or is not a directory" in str(exc)
    else:
        raise AssertionError("expected ValueError")
