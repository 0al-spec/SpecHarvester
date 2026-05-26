from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PublicApiPayloadPath:
    path: str

    def matches_entrypoint(self, value: Any) -> bool:
        if not isinstance(value, dict) or value.get("path") != self.path:
            return False
        symbols = value.get("symbols")
        if not isinstance(symbols, list):
            return False
        return all(self.matches_symbol(symbol) for symbol in symbols)

    def matches_symbol(self, value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        evidence = value.get("evidence")
        return isinstance(evidence, dict) and evidence.get("path") == self.path

    def matches_diagnostic(self, value: Any) -> bool:
        if not isinstance(value, dict) or value.get("path") != self.path:
            return False
        evidence = value.get("evidence")
        return isinstance(evidence, dict) and evidence.get("path") == self.path
