from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ANALYZER_CACHE_SCHEMA_VERSION = 1


def analyzer_cache_key(analyzer_id: str, analyzer_version: str, file_digest: str) -> str:
    key_material = "\0".join((analyzer_id, analyzer_version, file_digest))
    return hashlib.sha256(key_material.encode("utf-8")).hexdigest()


class AnalyzerCache:
    def __init__(self, root: Path) -> None:
        self.root = root

    def path_for(
        self,
        *,
        analyzer_id: str,
        analyzer_version: str,
        file_digest: str,
    ) -> Path:
        key = analyzer_cache_key(analyzer_id, analyzer_version, file_digest)
        return self.root / f"{key}.json"

    def read(
        self,
        *,
        analyzer_id: str,
        analyzer_version: str,
        file_digest: str,
    ) -> Any | None:
        path = self.path_for(
            analyzer_id=analyzer_id,
            analyzer_version=analyzer_version,
            file_digest=file_digest,
        )
        if not path.exists() or not path.is_file():
            return None
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(record, dict):
            return None
        if record.get("schemaVersion") != ANALYZER_CACHE_SCHEMA_VERSION:
            return None
        if record.get("analyzerId") != analyzer_id:
            return None
        if record.get("analyzerVersion") != analyzer_version:
            return None
        if record.get("fileDigest") != file_digest:
            return None
        if "payload" not in record:
            return None
        return record["payload"]

    def write(
        self,
        *,
        analyzer_id: str,
        analyzer_version: str,
        file_digest: str,
        payload: Any,
    ) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        record = {
            "schemaVersion": ANALYZER_CACHE_SCHEMA_VERSION,
            "analyzerId": analyzer_id,
            "analyzerVersion": analyzer_version,
            "fileDigest": file_digest,
            "payload": payload,
        }
        path = self.path_for(
            analyzer_id=analyzer_id,
            analyzer_version=analyzer_version,
            file_digest=file_digest,
        )
        temp_path = path.with_suffix(".json.tmp")
        temp_path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temp_path.replace(path)
