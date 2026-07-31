from __future__ import annotations

import copy

import pytest

from spec_harvester.experimental_intent_policy import (
    EXPERIMENTAL_INTENT_ID_PATTERN,
    GENERIC_OBSERVED_INTENT_IDS,
    experimental_intent_suffix,
    load_experimental_intent_decision_policy,
    validate_experimental_intent_decision_policy,
)


def test_policy_is_digest_bound_and_preserves_proposal_only_authority() -> None:
    policy = load_experimental_intent_decision_policy()

    validate_experimental_intent_decision_policy(policy)
    assert policy["genericObservedIntentIds"] == sorted(GENERIC_OBSERVED_INTENT_IDS)
    assert policy["decisionRules"]["maxExperimentalIntentCount"] == 1
    assert policy["decisionRules"]["falseNoveltyDisposition"] == "calibration_failure"
    assert policy["decisionRules"]["proposalOnly"] is True
    assert policy["decisionRules"]["canonicalizationAllowed"] is False


def test_policy_rejects_rule_or_digest_drift() -> None:
    policy = load_experimental_intent_decision_policy()
    changed_rule = copy.deepcopy(policy)
    changed_rule["decisionRules"]["maxExperimentalIntentCount"] = 2
    with pytest.raises(ValueError, match="rules are invalid"):
        validate_experimental_intent_decision_policy(changed_rule)

    changed_digest = copy.deepcopy(policy)
    changed_digest["policySha256"] = "f" * 64
    with pytest.raises(ValueError, match="digest is stale"):
        validate_experimental_intent_decision_policy(changed_digest)


def test_identifier_contract_is_collision_bound_without_package_namespace() -> None:
    source_digest = "a1b2c3d4" + "0" * 56
    intent_id = f"intent.experimental.reduce_ai_context.{experimental_intent_suffix(source_digest)}"

    assert EXPERIMENTAL_INTENT_ID_PATTERN.fullmatch(intent_id)
    assert intent_id.endswith(".a1b2c3d4")


@pytest.mark.parametrize("digest", ("", "A" * 64, "0" * 63, "not-a-digest"))
def test_identifier_suffix_rejects_invalid_source_digest(digest: str) -> None:
    with pytest.raises(ValueError, match="source bundle digest is invalid"):
        experimental_intent_suffix(digest)
