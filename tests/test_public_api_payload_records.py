from __future__ import annotations

from spec_harvester.public_api_payload_records import PublicApiPayloadPath


def test_public_api_payload_path_matches_entrypoint_symbols_and_diagnostics() -> None:
    payload_path = PublicApiPayloadPath("package/module.py")

    assert payload_path.matches_entrypoint(
        {
            "path": "package/module.py",
            "symbols": [
                {"name": "PublicClass", "evidence": {"path": "package/module.py"}},
                {"name": "public_function", "evidence": {"path": "package/module.py"}},
            ],
        }
    )
    assert payload_path.matches_symbol(
        {"name": "PublicClass", "evidence": {"path": "package/module.py"}}
    )
    assert payload_path.matches_diagnostic(
        {
            "path": "package/module.py",
            "level": "error",
            "evidence": {"path": "package/module.py"},
        }
    )


def test_public_api_payload_path_rejects_wrong_or_missing_paths() -> None:
    payload_path = PublicApiPayloadPath("package/module.py")

    assert not payload_path.matches_entrypoint(
        {
            "path": "package/module.py",
            "symbols": [
                {"name": "PublicClass", "evidence": {"path": "other.py"}},
            ],
        }
    )
    assert not payload_path.matches_entrypoint({"path": "other.py", "symbols": []})
    assert not payload_path.matches_entrypoint({"path": "package/module.py"})
    assert not payload_path.matches_symbol({"name": "PublicClass"})
    assert not payload_path.matches_diagnostic(
        {
            "path": "package/module.py",
            "level": "error",
            "evidence": {"path": "other.py"},
        }
    )
