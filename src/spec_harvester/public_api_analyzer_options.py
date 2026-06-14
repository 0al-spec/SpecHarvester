from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spec_harvester.analyzer_cache import AnalyzerCache

PUBLIC_API_ANALYZER_OPTION_KEYS = frozenset(
    {"package_id", "source_revision", "cache_dir", "parser_profile_id"}
)


@dataclass(frozen=True)
class PublicApiAnalyzerOptions:
    source: Path
    package_id: str | None = None
    source_revision: str | None = None
    cache_dir: Path | None = None
    parser_profile_id: str | None = None

    @classmethod
    def from_call(
        cls,
        source: Path | PublicApiAnalyzerOptions,
        **kwargs: Any,
    ) -> PublicApiAnalyzerOptions:
        if isinstance(source, cls):
            if kwargs:
                raise TypeError(
                    "PublicApiAnalyzerOptions cannot be combined with analyzer keyword options"
                )
            return source

        unexpected = sorted(set(kwargs) - PUBLIC_API_ANALYZER_OPTION_KEYS)
        if unexpected:
            names = ", ".join(unexpected)
            raise TypeError(f"Unexpected public API analyzer option(s): {names}")
        return cls(
            source=source,
            package_id=kwargs.get("package_id"),
            source_revision=kwargs.get("source_revision"),
            cache_dir=kwargs.get("cache_dir"),
            parser_profile_id=kwargs.get("parser_profile_id"),
        )

    def root(self, language: str) -> Path:
        root = self.source.resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError(
                f"{language} source root does not exist or is not a directory: {self.source}"
            )
        return root

    def cache(self) -> AnalyzerCache | None:
        return AnalyzerCache(self.cache_dir) if self.cache_dir is not None else None

    def package_id_or(self, fallback: str) -> str:
        return self.package_id or fallback
