"""Caller-side evidence accounting and output storage, not a worker sandbox."""

from __future__ import annotations

import copy
import hashlib
import os
import re
import stat
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


class AuthoringIOError(ValueError):
    """A portable terminal or request-level I/O diagnostic."""


@dataclass(frozen=True)
class EvidenceLimits:
    calls: int = 100
    evidence_bytes: int = 96 * 1024
    source_file_bytes: int = 24 * 1024


def _portable_path(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(char) < 32 for char in value)
        or PurePosixPath(value).is_absolute()
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise AuthoringIOError("invalid_path")
    return value


def _union(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def _size(ranges: list[tuple[int, int]]) -> int:
    return sum(end - start for start, end in ranges)


class AuthoringEvidence:
    """One unit's shared budget; keep this object across repair and retry."""

    def __init__(
        self, root: Path, allowlist: dict[str, str], limits: EvidenceLimits | None = None
    ) -> None:
        limits = limits if limits is not None else EvidenceLimits()
        if any(type(value) is not int or value <= 0 for value in vars(limits).values()):
            raise AuthoringIOError("invalid_limits")
        for path, digest in allowlist.items():
            _portable_path(path)
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise AuthoringIOError("invalid_digest")
        self._root = root
        self._allowlist = dict(allowlist)
        self._limits = limits
        self._ranges: dict[str, list[tuple[int, int]]] = {}
        self._generated: dict[str, tuple[str, int]] = {}
        self._ledger: list[dict[str, Any]] = []
        self._calls = 0
        self._exhausted = False

    def read(self, path: str, start: int, end: int) -> dict[str, Any]:
        row: dict[str, Any] = {
            "sequence": len(self._ledger) + 1,
            "operation": "source_read",
            "path": None,
            "sourceSha256": None,
            "requestedRange": None,
            "returnedRange": None,
            "returnedBytes": 0,
            "startedMonotonic": time.monotonic(),
        }
        self._calls += 1
        try:
            self._check_budget(self._calls > self._limits.calls)
            safe = _portable_path(path)
            # Do not retain a denied caller-supplied host path in portable receipts.
            if safe not in self._allowlist:
                raise AuthoringIOError("source_not_allowlisted")
            row["path"] = safe
            row["sourceSha256"] = self._allowlist[safe]
            if (
                type(start) is not int
                or type(end) is not int
                or start < 0
                or end <= start
                or end - start > self._limits.source_file_bytes
            ):
                raise AuthoringIOError("invalid_range")
            row["requestedRange"] = [start, end]
            data, total = self._verified_slice(safe, start, end)
            actual_start, actual_end, text = self._utf8_slice(data, start, end, total)
            previous = self._ranges.get(safe, [])
            merged = _union([*previous, (actual_start, actual_end)])
            extra = _size(merged) - _size(previous)
            summary = self.summary()
            self._check_budget(
                _size(merged) > self._limits.source_file_bytes
                or summary["sourceBytes"] + summary["generatedBytes"] + extra
                > self._limits.evidence_bytes
            )
            self._ranges[safe] = merged
            row.update(
                returnedRange=[actual_start, actual_end],
                returnedBytes=actual_end - actual_start,
                status="returned",
            )
            return {
                "path": safe,
                "sourceSha256": self._allowlist[safe],
                "requestedRange": [start, end],
                "returnedRange": [actual_start, actual_end],
                "truncated": (start, end) != (actual_start, actual_end),
                "text": text,
            }
        except AuthoringIOError as exc:
            row.update(status="denied", code=str(exc))
            raise
        finally:
            row["endedMonotonic"] = time.monotonic()
            self._ledger.append(row)

    def generated(self, item: str, serialized_text: str) -> None:
        """Charge a stable generated evidence item, including projected arm-A text."""
        self._check_budget(False)
        _portable_path(item)
        data = serialized_text.encode("utf-8")
        record = (hashlib.sha256(data).hexdigest(), len(data))
        if item in self._generated:
            if self._generated[item] != record:
                raise AuthoringIOError("generated_item_changed")
            return
        summary = self.summary()
        self._check_budget(
            summary["sourceBytes"] + summary["generatedBytes"] + len(data)
            > self._limits.evidence_bytes
        )
        self._generated[item] = record

    def summary(self) -> dict[str, Any]:
        return {
            "readCalls": self._calls,
            "sourceBytes": sum(_size(ranges) for ranges in self._ranges.values()),
            "generatedBytes": sum(size for _, size in self._generated.values()),
            "exhausted": self._exhausted,
        }

    def ledger(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._ledger)

    def _check_budget(self, exceeds: bool) -> None:
        self._exhausted = self._exhausted or exceeds
        if self._exhausted:
            raise AuthoringIOError("budget_exhausted")

    def _verified_slice(self, path: str, start: int, end: int) -> tuple[bytes, int]:
        descriptors: list[int] = []
        try:
            directory = os.open(self._root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            descriptors.append(directory)
            parts = path.split("/")
            for part in parts[:-1]:
                directory = os.open(
                    part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory
                )
                descriptors.append(directory)
            file = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            descriptors.append(file)
            metadata = os.fstat(file)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise AuthoringIOError("unsafe_source")
            digest = hashlib.sha256()
            data = bytearray()
            position = 0
            # Hash the full pinned file but retain only the requested bounded slice.
            while chunk := os.read(file, 64 * 1024):
                digest.update(chunk)
                left, right = max(start - position, 0), min(end - position, len(chunk))
                if right > left:
                    data.extend(chunk[left:right])
                position += len(chunk)
            if digest.hexdigest() != self._allowlist[path]:
                raise AuthoringIOError("source_digest_mismatch")
            return bytes(data), position
        except OSError as exc:
            raise AuthoringIOError("unsafe_source") from exc
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)

    def _utf8_slice(self, data: bytes, start: int, end: int, total: int) -> tuple[int, int, str]:
        actual_start = min(start, total)
        actual_end = min(end, total)
        while data and data[0] & 0xC0 == 0x80:
            data = data[1:]
            actual_start += 1
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            if exc.reason != "unexpected end of data" or end >= total:
                raise AuthoringIOError("source_not_utf8") from exc
            data = data[: exc.start]
            actual_end = actual_start + len(data)
            text = data.decode("utf-8")
        return actual_start, actual_end, text


class CandidateOutput:
    """Create one immutable-attempt directory; never follow worker-chosen paths."""

    def __init__(self, root: Path, max_bytes: int = 256 * 1024) -> None:
        self._root = root
        self._max_bytes = max_bytes

    def write(self, files: dict[str, str]) -> dict[str, Any]:
        if not files or type(self._max_bytes) is not int or self._max_bytes <= 0:
            raise AuthoringIOError("invalid_output")
        encoded = {_portable_path(path): text.encode("utf-8") for path, text in files.items()}
        if sum(map(len, encoded.values())) > self._max_bytes:
            raise AuthoringIOError("output_budget_exhausted")
        for path in encoded:
            if any(str(parent) in encoded for parent in PurePosixPath(path).parents):
                raise AuthoringIOError("output_path_collision")
        try:
            self._root.mkdir(mode=0o700)
        except FileExistsError as exc:
            raise AuthoringIOError("output_exists") from exc
        for path, data in encoded.items():
            target = self._root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
        return {
            "bytes": sum(map(len, encoded.values())),
            "files": {path: hashlib.sha256(data).hexdigest() for path, data in encoded.items()},
        }
