from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

SCHEMA_NAME = "local-candidate-review-workbench-v0.schema.json"


def load_candidate_review_schema() -> dict[str, Any]:
    try:
        payload = (
            files("spec_harvester").joinpath("schemas", SCHEMA_NAME).read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        source_path = Path(__file__).resolve().parents[2] / "schemas" / SCHEMA_NAME
        try:
            payload = source_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"Cannot read candidate review schema: {exc}") from exc
    try:
        schema = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Cannot read candidate review schema: {exc}") from exc
    if not isinstance(schema, dict):
        raise ValueError("Candidate review schema must be an object")
    return schema
