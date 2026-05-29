from __future__ import annotations

from typing import Any

from spec_harvester.analyzer_cache import AnalyzerCache
from spec_harvester.public_api_payload_records import PublicApiPayloadPath


def read_cached_public_api_entrypoint(
    cache: AnalyzerCache | None,
    *,
    analyzer_id: str,
    analyzer_version: str,
    path: str,
    digest: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]] | None:
    if cache is None:
        return None
    payload = cache.read(
        analyzer_id=analyzer_id,
        analyzer_version=analyzer_version,
        file_digest=digest,
    )
    if not isinstance(payload, dict):
        return None
    entrypoint = payload.get("entrypoint")
    diagnostics = payload.get("diagnostics")
    if not isinstance(diagnostics, list):
        return None
    payload_path = PublicApiPayloadPath(path)
    if entrypoint is not None and not payload_path.matches_entrypoint(entrypoint):
        return None
    for diagnostic in diagnostics:
        if not payload_path.matches_diagnostic(diagnostic):
            return None
    return entrypoint, diagnostics


def write_cached_public_api_entrypoint(
    cache: AnalyzerCache | None,
    *,
    analyzer_id: str,
    analyzer_version: str,
    digest: str,
    entrypoint: dict[str, Any] | None,
    diagnostics: list[dict[str, Any]],
) -> None:
    if cache is None:
        return
    cache.write(
        analyzer_id=analyzer_id,
        analyzer_version=analyzer_version,
        file_digest=digest,
        payload={"entrypoint": entrypoint, "diagnostics": diagnostics},
    )
