from __future__ import annotations

import json

from spec_harvester.analyzer_cache import AnalyzerCache, analyzer_cache_key


def test_analyzer_cache_key_is_deterministic_and_metadata_scoped() -> None:
    digest = "a" * 64

    assert analyzer_cache_key("python-ast-public-api", "0.1.0", digest) == analyzer_cache_key(
        "python-ast-public-api", "0.1.0", digest
    )
    assert analyzer_cache_key("python-ast-public-api", "0.1.0", digest) != analyzer_cache_key(
        "python-ast-public-api", "0.2.0", digest
    )
    assert analyzer_cache_key("python-ast-public-api", "0.1.0", digest) != analyzer_cache_key(
        "other-analyzer", "0.1.0", digest
    )
    assert analyzer_cache_key("python-ast-public-api", "0.1.0", digest) != analyzer_cache_key(
        "python-ast-public-api", "0.1.0", "b" * 64
    )


def test_analyzer_cache_round_trips_matching_payload(tmp_path) -> None:  # type: ignore[no-untyped-def]
    cache = AnalyzerCache(tmp_path)
    digest = "a" * 64
    payload = {"path": "api.py", "symbols": [{"name": "build", "kind": "function"}]}

    cache.write(
        analyzer_id="python-ast-public-api",
        analyzer_version="0.1.0",
        file_digest=digest,
        payload=payload,
    )

    assert (
        cache.read(
            analyzer_id="python-ast-public-api",
            analyzer_version="0.1.0",
            file_digest=digest,
        )
        == payload
    )
    cache_files = sorted(tmp_path.glob("*.json"))
    assert len(cache_files) == 1
    assert json.loads(cache_files[0].read_text(encoding="utf-8"))["fileDigest"] == digest


def test_analyzer_cache_ignores_metadata_mismatch_and_malformed_entries(tmp_path) -> None:  # type: ignore[no-untyped-def]
    cache = AnalyzerCache(tmp_path)
    digest = "a" * 64
    cache.write(
        analyzer_id="python-ast-public-api",
        analyzer_version="0.1.0",
        file_digest=digest,
        payload={"symbols": []},
    )

    assert (
        cache.read(
            analyzer_id="python-ast-public-api",
            analyzer_version="0.2.0",
            file_digest=digest,
        )
        is None
    )
    assert (
        cache.read(
            analyzer_id="python-ast-public-api",
            analyzer_version="0.1.0",
            file_digest="b" * 64,
        )
        is None
    )

    cache.path_for(
        analyzer_id="broken",
        analyzer_version="0.1.0",
        file_digest=digest,
    ).write_text("{", encoding="utf-8")
    assert (
        cache.read(
            analyzer_id="broken",
            analyzer_version="0.1.0",
            file_digest=digest,
        )
        is None
    )
