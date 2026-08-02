from __future__ import annotations

import re
from typing import Any

import yaml

REPAIR_FIELD = "capabilityNamespaceRepairs"


def capability_namespace_violations(evidence: list[Any], candidate_id: str) -> list[str]:
    """Return distinct static capability IDs outside the candidate namespace."""
    expected_prefix = f"{candidate_id}."
    capability_ids: set[str] = set()
    for item in evidence:
        if not isinstance(item, dict) or item.get("class") != "validated_candidate_yaml":
            continue
        try:
            document = yaml.safe_load(item.get("content"))
        except yaml.YAMLError as exc:
            raise ValueError("candidate YAML evidence is malformed") from exc
        if not isinstance(document, dict):
            raise ValueError("candidate YAML evidence is malformed")
        source_path = item.get("sourcePath")
        if source_path == "specpm.yaml":
            index = document.get("index")
            provides = index.get("provides") if isinstance(index, dict) else None
            capability_ids.update(
                _string_list(provides.get("capabilities") if isinstance(provides, dict) else None)
            )
        elif isinstance(source_path, str) and source_path.endswith(".spec.yaml"):
            provides = document.get("provides")
            capabilities = provides.get("capabilities") if isinstance(provides, dict) else None
            for capability in capabilities if isinstance(capabilities, list) else []:
                if isinstance(capability, dict) and isinstance(capability.get("id"), str):
                    capability_ids.add(capability["id"])
    return sorted(
        capability_id
        for capability_id in capability_ids
        if not capability_id.startswith(expected_prefix)
    )


def capability_namespace_repair_constraints(candidate_id: str) -> dict[str, str]:
    escaped = re.escape(candidate_id)
    return {
        "candidateNamespace": candidate_id,
        "requiredPrefix": f"{candidate_id}.",
        "replacementIdPattern": f"^{escaped}\\.[a-z][a-z0-9_]{{0,79}}$",
    }


def validate_capability_namespace_repairs(
    repairs: Any,
    *,
    candidate_id: str,
    violations: list[str],
) -> list[dict[str, str]]:
    """Validate bounded, proposal-only replacements for static namespace violations."""
    if not violations:
        if repairs in (None, []):
            return []
        raise ValueError("capability namespace repairs are unexpected")
    if not isinstance(repairs, list):
        raise ValueError("capability namespace repairs are missing")
    expected = set(violations)
    replacements: dict[str, str] = {}
    constraints = capability_namespace_repair_constraints(candidate_id)
    pattern = re.compile(constraints["replacementIdPattern"])
    for repair in repairs:
        if not isinstance(repair, dict):
            raise ValueError("capability namespace repair is malformed")
        prohibited = repair.get("prohibitedCapabilityId")
        replacement = repair.get("replacementCapabilityId")
        if not isinstance(prohibited, str) or not isinstance(replacement, str):
            raise ValueError("capability namespace repair is malformed")
        if prohibited in replacements or not pattern.fullmatch(replacement):
            raise ValueError("capability namespace repair is invalid")
        replacements[prohibited] = replacement
    if set(replacements) != expected or len(set(replacements.values())) != len(replacements):
        raise ValueError("capability namespace repairs do not match violations")
    return [
        {
            "prohibitedCapabilityId": prohibited,
            "replacementCapabilityId": replacements[prohibited],
        }
        for prohibited in sorted(replacements)
    ]


def _string_list(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []
