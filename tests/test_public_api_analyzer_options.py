from pathlib import Path

import pytest

from spec_harvester.analyzer_cache import AnalyzerCache
from spec_harvester.public_api_analyzer_options import PublicApiAnalyzerOptions


def test_public_api_analyzer_options_resolve_root_cache_and_package_id(
    tmp_path: Path,
) -> None:
    cache_dir = tmp_path / "cache"
    options = PublicApiAnalyzerOptions(
        source=tmp_path,
        package_id="demo.package",
        source_revision="abc123",
        cache_dir=cache_dir,
    )

    assert options.root("Python") == tmp_path.resolve()
    assert isinstance(options.cache(), AnalyzerCache)
    assert options.package_id_or("fallback") == "demo.package"
    assert options.source_revision == "abc123"


def test_public_api_analyzer_options_use_package_fallback(tmp_path: Path) -> None:
    options = PublicApiAnalyzerOptions(source=tmp_path)

    assert options.cache() is None
    assert options.package_id_or("fallback") == "fallback"


def test_public_api_analyzer_options_preserve_legacy_call_keywords(tmp_path: Path) -> None:
    options = PublicApiAnalyzerOptions.from_call(
        tmp_path,
        package_id="demo.package",
        source_revision="abc123",
        cache_dir=tmp_path / "cache",
    )

    assert options.source == tmp_path
    assert options.package_id == "demo.package"
    assert options.source_revision == "abc123"
    assert options.cache_dir == tmp_path / "cache"


def test_public_api_analyzer_options_accept_options_instance(tmp_path: Path) -> None:
    options = PublicApiAnalyzerOptions(source=tmp_path)

    assert PublicApiAnalyzerOptions.from_call(options) is options


def test_public_api_analyzer_options_reject_unexpected_keywords(tmp_path: Path) -> None:
    with pytest.raises(TypeError, match="Unexpected public API analyzer option"):
        PublicApiAnalyzerOptions.from_call(tmp_path, unknown=True)


def test_public_api_analyzer_options_reject_mixed_object_and_keywords(tmp_path: Path) -> None:
    options = PublicApiAnalyzerOptions(source=tmp_path)

    with pytest.raises(TypeError, match="cannot be combined"):
        PublicApiAnalyzerOptions.from_call(options, package_id="demo.package")


def test_public_api_analyzer_options_reject_non_directory_source(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text("def ok():\n    return True\n", encoding="utf-8")
    options = PublicApiAnalyzerOptions(source=source)

    with pytest.raises(ValueError, match="Python source root does not exist"):
        options.root("Python")
