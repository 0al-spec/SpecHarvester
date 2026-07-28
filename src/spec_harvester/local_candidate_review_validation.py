from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def validate_decision_reason_compatibility(
    decisions: Iterable[dict[str, Any]], reasons: dict[str, Any]
) -> None:
    """Reject decisions whose reason code is absent from or incompatible with the taxonomy."""

    codes = reasons.get("codes")
    if not isinstance(codes, list):
        raise ValueError("Review reason taxonomy must contain a codes array")

    allowed_by_code: dict[str, set[str]] = {}
    for record in codes:
        if not isinstance(record, dict):
            raise ValueError("Review reason taxonomy contains an invalid code record")
        code = record.get("code")
        dispositions = record.get("allowedDispositions")
        if not isinstance(code, str) or not isinstance(dispositions, list):
            raise ValueError("Review reason taxonomy contains invalid code metadata")
        if code in allowed_by_code:
            raise ValueError(f"Review reason taxonomy duplicates code: {code}")
        allowed_by_code[code] = set(dispositions)

    for decision in decisions:
        code = decision.get("reasonCode")
        disposition = decision.get("disposition")
        if code not in allowed_by_code:
            raise ValueError(f"Review decision uses unknown reason code: {code}")
        if disposition not in allowed_by_code[code]:
            raise ValueError(
                f"Review decision disposition is not allowed for reason code: {code}/{disposition}"
            )
