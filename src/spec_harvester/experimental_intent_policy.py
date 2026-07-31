from __future__ import annotations

import hashlib
import json
import re
from importlib.resources import files
from pathlib import Path
from typing import Any

POLICY_FILENAME = "experimental-intent-decision-policy-v0.json"
POLICY_SOURCE_PATH = (
    "tests/fixtures/experimental_intent_decision_policy/"
    "p55-t10a-experimental-intent-decision-policy.example.json"
)

GENERIC_OBSERVED_INTENT_IDS = frozenset(
    {
        "intent.package.javascript_library",
        "intent.package.public_repository_metadata",
        "intent.repository.package_workspace",
    }
)
EXPERIMENTAL_INTENT_ID_PATTERN = re.compile(
    r"^intent\.experimental\.[a-z0-9]+(?:_[a-z0-9]+){1,5}\.[0-9a-f]{8}$"
)


def load_experimental_intent_decision_policy() -> dict[str, Any]:
    """Load the bounded P55-T10A reuse-versus-novelty policy."""
    try:
        raw = (
            files("spec_harvester")
            .joinpath("policies", POLICY_FILENAME)
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        source = Path(__file__).resolve().parents[2] / POLICY_SOURCE_PATH
        try:
            raw = source.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"cannot read experimental intent decision policy: {exc}") from exc
    try:
        policy = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"cannot read experimental intent decision policy: {exc}") from exc
    validate_experimental_intent_decision_policy(policy)
    return policy


def validate_experimental_intent_decision_policy(policy: dict[str, Any]) -> None:
    if not isinstance(policy, dict):
        raise ValueError("experimental intent decision policy must be an object")
    if (
        policy.get("apiVersion") != "spec-harvester.experimental-intent-decision-policy/v0"
        or policy.get("kind") != "SpecHarvesterExperimentalIntentDecisionPolicy"
        or policy.get("schemaVersion") != 1
        or policy.get("authority") != "maintainer_bounded_proposal_policy"
        or policy.get("frozenByTask") != "P55-T10A"
        or policy.get("genericObservedIntentIds") != sorted(GENERIC_OBSERVED_INTENT_IDS)
    ):
        raise ValueError("experimental intent decision policy identity is invalid")
    expected_rules = {
        "existingIntentReusePreferredWhenSufficient": True,
        "genericIntentRequiresExplicitComparison": True,
        "maxExperimentalIntentCount": 1,
        "experimentalNamespace": "intent.experimental.*",
        "identifierPattern": EXPERIMENTAL_INTENT_ID_PATTERN.pattern,
        "identifierSuffixSource": "sourceBundleSha256:first8",
        "nearbyIntentMustBeObserved": True,
        "userNeedClaimKind": "purpose",
        "nearbyDifferenceClaimKind": "nearby_intent_difference",
        "minimumNonGoalClaims": 1,
        "falseNoveltyDisposition": "calibration_failure",
        "proposalOnly": True,
        "canonicalizationAllowed": False,
    }
    if policy.get("decisionRules") != expected_rules:
        raise ValueError("experimental intent decision policy rules are invalid")
    digest = policy.get("policySha256")
    if not isinstance(digest, str) or digest != _digest_without(policy, "policySha256"):
        raise ValueError("experimental intent decision policy digest is stale")


def experimental_intent_suffix(source_bundle_sha256: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", source_bundle_sha256):
        raise ValueError("source bundle digest is invalid")
    return source_bundle_sha256[:8]


def candidate_namespace_tokens(candidate_id: str) -> set[str]:
    """Return package-specific tokens that must not enter portable intent IDs."""
    ignored = {"api", "app", "cli", "core", "library", "package", "tool", "workspace"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", candidate_id.casefold())
        if len(token) >= 3 and token not in ignored
    }


def _digest_without(value: dict[str, Any], key: str) -> str:
    payload = {name: item for name, item in value.items() if name != key}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
