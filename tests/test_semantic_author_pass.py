from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from spec_harvester.experimental_intent_policy import (
    load_experimental_intent_decision_policy,
)
from spec_harvester.relevant_intent_routing import build_relevant_intent_catalog
from spec_harvester.semantic_author_input_pack import build_semantic_author_input_pack
from spec_harvester.semantic_author_pass import (
    CodexSparkSemanticAuthorProvider,
    LMStudioSemanticAuthorProvider,
    ProviderCompletion,
    SemanticAuthorPassError,
    SemanticAuthorPassOptions,
    run_semantic_author_pass,
    validate_semantic_author_provider_receipt,
)
from spec_harvester.semantic_product_profile import build_semantic_product_profile

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/ai_semantic_author_schemas/p55-t2-valid.example.json"


class FakeProvider:
    provider_id = "test_provider"

    def __init__(self, proposal: dict) -> None:
        self.proposal = proposal
        self.requests: list[dict] = []

    def complete(self, request: dict, options: SemanticAuthorPassOptions) -> ProviderCompletion:
        self.requests.append(request)
        return ProviderCompletion(
            payload=copy.deepcopy(self.proposal),
            receipt={
                "providerKind": "test",
                "durationMs": 1,
                "rawPromptPersisted": False,
                "rawResponsePersisted": False,
                "chainOfThoughtPersisted": False,
            },
        )


def catalog(intent_id: str = "intent.ai.context_selection") -> dict:
    payload = {
        "sourcePath": "catalog/observed.json",
        "intents": [{"intentId": intent_id, "sha256": "a" * 64}],
    }
    return {
        **payload,
        "sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def routed_profile() -> dict:
    readme = b"Reduce AI context consumption by selecting relevant repository content."
    profile = build_semantic_product_profile(
        repository_id="demo",
        candidate_id="demo.package",
        harvest={
            "source": {
                "repository": "https://github.com/demo/package",
                "revision": "a" * 40,
                "target": {"path": "."},
            },
            "files": [
                {
                    "path": "package.json",
                    "package": {
                        "name": "demo-package",
                        "description": "Reduce AI context consumption by selecting content",
                    },
                }
            ],
        },
        root_document={
            "evidencePath": "README.md",
            "sourcePath": "README.md",
            "sha256": hashlib.sha256(readme).hexdigest(),
            "byteCount": len(readme),
            "harvestSha256": hashlib.sha256(b"{}").hexdigest(),
        },
        manifest_metadata={
            "sourcePath": "package.json",
            "sha256": "b" * 64,
            "description": "Reduce AI context consumption by selecting content",
            "keywords": ["context", "content", "selection"],
        },
    )
    return profile


def routed_catalog() -> dict:
    return build_relevant_intent_catalog(
        routed_profile(),
        current_intent_ids=["intent.package.javascript_library"],
    )


def pack(
    tmp_path: Path,
    intent_id: str = "intent.ai.context_selection",
    *,
    catalog_override: dict | None = None,
) -> dict:
    (tmp_path / "specs").mkdir()
    (tmp_path / "specpm.yaml").write_text(
        "kind: SpecPackage\nmetadata:\n  id: demo.package\npreview_only: true\n"
    )
    (tmp_path / "specs/core.spec.yaml").write_text("kind: BoundarySpec\n")
    (tmp_path / "harvest.json").write_text("{}")
    if catalog_override is not None and "routing" in catalog_override:
        (tmp_path / "README.md").write_bytes(
            b"Reduce AI context consumption by selecting relevant repository content."
        )
        (tmp_path / "semantic-product-profile.json").write_text(
            json.dumps(routed_profile(), sort_keys=True)
        )
    return build_semantic_author_input_pack(tmp_path, catalog_override or catalog(intent_id))


def proposal(input_pack: dict) -> dict:
    result = json.loads(FIXTURE.read_text())["proposal"]
    result["candidateId"] = input_pack["candidateId"]
    result["sourceBundleSha256"] = input_pack["sourceBundleSha256"]
    evidence = input_pack["request"]["evidence"][0]
    for claim in result["claims"]:
        claim["evidence"] = [dict(evidence)]
    reuse = result["intentDecisions"][0]
    reuse["intentId"] = input_pack["observedIntents"][0]["intentId"]
    reuse["observedIntentSha256"] = input_pack["observedIntents"][0]["observedIntentSha256"]
    result["intentDecisions"][1]["intentId"] = (
        f"intent.experimental.ai_context_optimization.{input_pack['sourceBundleSha256'][:8]}"
    )
    result["intentDecisions"][1]["nearbyIntentIds"] = [reuse["intentId"]]
    result["intentDecisions"][1]["nearbyIntentClaimIds"] = ["nearby_difference"]
    return result


def transport_proposal(input_pack: dict) -> dict:
    result = proposal(input_pack)
    result.pop("proposalSha256")
    result.pop("provider")
    return result


def provider_request(input_pack: dict) -> dict:
    request = {
        "request": input_pack["request"],
        "observedIntents": input_pack["observedIntents"],
        "evidence": input_pack["evidence"],
        "experimentalIntentDecisionPolicy": load_experimental_intent_decision_policy(),
        "requiredJsonShape": {"type": "object"},
        "allowedEvidencePaths": [item["sourcePath"] for item in input_pack["request"]["evidence"]],
    }
    if "intentRouting" in input_pack:
        request["intentRouting"] = input_pack["intentRouting"]
    return request


def test_provider_neutral_pass_normalizes_contract_and_discards_raw_data(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    provider = FakeProvider(proposal(input_pack))
    report = run_semantic_author_pass(input_pack, provider)
    assert provider.requests[0]["request"] == input_pack["request"]
    assert provider.requests[0]["observedIntents"] == input_pack["observedIntents"]
    assert provider.requests[0]["evidence"] == input_pack["evidence"]
    assert provider.requests[0]["evidence"][0]["content"]
    assert (
        report["experimentalIntentDecisionPolicy"]["policySha256"]
        == provider.requests[0]["experimentalIntentDecisionPolicy"]["policySha256"]
    )
    assert report["kind"] == "SpecHarvesterSemanticAuthorPass"
    assert report["proposal"]["provider"]["id"] == "test_provider"
    assert (
        report["proposal"]["provider"]["receiptSha256"]
        == report["providerReceipt"]["receiptSha256"]
    )
    assert all(
        value is False
        for key, value in report["executionBoundary"].items()
        if key != "providerInvoked"
    )
    assert report["providerReceipt"]["rawPromptPersisted"] is False
    assert report["providerReceipt"]["rawResponsePersisted"] is False
    assert report["providerReceipt"]["chainOfThoughtPersisted"] is False
    validate_semantic_author_provider_receipt(report["providerReceipt"])


def test_provider_payload_carries_bounded_semantic_focus(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    provider = FakeProvider(proposal(input_pack))
    run_semantic_author_pass(
        input_pack,
        provider,
        semantic_focus={
            "purposeConceptGroups": [["token", "context"], ["reduce", "save"]],
            "specificTerms": ["token", "command"],
        },
    )

    focus = provider.requests[0]["semanticFocus"]
    assert focus["purposeConceptGroups"] == [
        ["token", "context"],
        ["reduce", "save"],
    ]
    assert focus["authority"] == "review_rubric_only"
    assert (
        provider.requests[0]["authoringConstraints"]["capabilityMustUseCandidateNamespace"]
        == input_pack["candidateId"]
    )
    assert (
        provider.requests[0]["authoringConstraints"][
            "purposeMustUseExactSupportedTermFromEverySemanticFocusGroup"
        ]
        is True
    )
    assert (
        provider.requests[0]["authoringConstraints"]["capabilityMustUseExactSupportedSpecificTerm"]
        is True
    )
    assert provider.requests[0]["authoringConstraints"]["purposeRequiredExactTermGroups"] == [
        ["token", "context"],
        ["reduce", "save"],
    ]
    assert provider.requests[0]["authoringConstraints"]["capabilityRequiredExactTerms"] == [
        "token",
        "command",
    ]


def test_provider_payload_rejects_malformed_semantic_focus_before_invocation(
    tmp_path: Path,
) -> None:
    input_pack = pack(tmp_path)
    provider = FakeProvider(proposal(input_pack))
    with pytest.raises(ValueError, match="semantic focus is malformed"):
        run_semantic_author_pass(
            input_pack,
            provider,
            semantic_focus={"purposeConceptGroups": [], "specificTerms": []},
        )
    assert provider.requests == []


def test_decision_policy_is_validated_before_provider_invocation(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    provider = FakeProvider(proposal(input_pack))
    stale = load_experimental_intent_decision_policy()
    stale["policySha256"] = "f" * 64

    with pytest.raises(ValueError, match="policy digest is stale"):
        run_semantic_author_pass(input_pack, provider, decision_policy=stale)

    assert provider.requests == []


def test_generic_reuse_and_experimental_novelty_are_mutually_exclusive(
    tmp_path: Path,
) -> None:
    input_pack = pack(tmp_path, "intent.package.javascript_library")
    provider = FakeProvider(proposal(input_pack))

    with pytest.raises(SemanticAuthorPassError, match="cannot retain a generic observed intent"):
        run_semantic_author_pass(input_pack, provider)


def test_generic_reuse_is_allowed_with_explicit_comparison(tmp_path: Path) -> None:
    input_pack = pack(tmp_path, "intent.package.javascript_library")
    payload = proposal(input_pack)
    payload["intentDecisions"] = payload["intentDecisions"][:1]

    report = run_semantic_author_pass(input_pack, FakeProvider(payload))

    assert report["proposal"]["intentDecisions"][0]["state"] == "proposed_reuse"


def test_specific_purpose_cannot_use_only_routed_generic_intent(tmp_path: Path) -> None:
    input_pack = pack(tmp_path, catalog_override=routed_catalog())
    payload = proposal(input_pack)
    payload["intentDecisions"] = [
        item
        for item in payload["intentDecisions"]
        if item["state"] == "proposed_reuse"
        and item["intentId"] == "intent.package.javascript_library"
    ]
    provider = FakeProvider(payload)

    with pytest.raises(
        SemanticAuthorPassError,
        match="specific semantic purpose cannot use only a generic observed intent",
    ):
        run_semantic_author_pass(input_pack, provider)

    assert provider.requests[0]["intentRouting"] == input_pack["intentRouting"]
    assert (
        provider.requests[0]["authoringConstraints"]["specificPurposeCannotUseOnlyGenericIntent"]
        is True
    )


def test_routing_cannot_be_removed_from_digest_bound_catalog_pack(tmp_path: Path) -> None:
    input_pack = pack(tmp_path, catalog_override=routed_catalog())
    input_pack.pop("intentRouting")
    provider = FakeProvider(proposal(input_pack))

    with pytest.raises(ValueError, match="routing evidence is stale"):
        run_semantic_author_pass(input_pack, provider)

    assert provider.requests == []


def test_generic_reuse_without_comparison_fails_closed(tmp_path: Path) -> None:
    input_pack = pack(tmp_path, "intent.package.javascript_library")
    payload = proposal(input_pack)
    payload["intentDecisions"] = payload["intentDecisions"][:1]
    payload["intentDecisions"][0]["rationaleClaimId"] = next(
        claim["id"] for claim in payload["claims"] if claim["kind"] == "capability"
    )

    with pytest.raises(SemanticAuthorPassError, match="lacks an explicit comparison claim"):
        run_semantic_author_pass(input_pack, FakeProvider(payload))


def test_experimental_identifier_cannot_leak_candidate_namespace(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    payload = proposal(input_pack)
    payload["intentDecisions"][1]["intentId"] = (
        f"intent.experimental.demo_context.{input_pack['sourceBundleSha256'][:8]}"
    )

    with pytest.raises(SemanticAuthorPassError, match="leaks candidate namespace"):
        run_semantic_author_pass(input_pack, FakeProvider(payload))


def test_experimental_nearby_intent_must_be_observed(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    payload = proposal(input_pack)
    payload["intentDecisions"][1]["nearbyIntentIds"] = ["intent.ai.unknown"]

    with pytest.raises(SemanticAuthorPassError, match="unknown nearby observed intent"):
        run_semantic_author_pass(input_pack, FakeProvider(payload))


def test_experimental_nearby_intents_require_matching_comparison_claims(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    payload = proposal(input_pack)
    payload["intentDecisions"][1]["nearbyIntentClaimIds"] = ["capability"]

    with pytest.raises(SemanticAuthorPassError, match="matching comparison claims"):
        run_semantic_author_pass(input_pack, FakeProvider(payload))


@pytest.mark.parametrize("mutation", ("evidence", "intent", "candidate", "output"))
def test_pass_fails_closed_for_untrusted_provider_output(tmp_path: Path, mutation: str) -> None:
    input_pack = pack(tmp_path)
    invalid = proposal(input_pack)
    if mutation == "evidence":
        invalid["claims"][0]["evidence"][0]["sourcePath"] = "docs/forged.md"
    elif mutation == "intent":
        invalid["intentDecisions"][0]["observedIntentSha256"] = "b" * 64
    elif mutation == "candidate":
        invalid["candidateId"] = "other"
    else:
        invalid.pop("claims")
    with pytest.raises(SemanticAuthorPassError):
        run_semantic_author_pass(input_pack, FakeProvider(invalid))


def test_lm_studio_adapter_uses_local_schema_constrained_transport(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[dict] = []
    input_pack = pack(tmp_path)
    content = json.dumps(transport_proposal(input_pack))

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: object) -> None:
            pass

        def read(self, size: int = -1) -> bytes:
            return json.dumps(
                {"model": "local", "choices": [{"message": {"content": content}}]}
            ).encode()

    def fake_urlopen(request: object, timeout: float) -> Response:
        calls.append(json.loads(request.data.decode()))  # type: ignore[attr-defined]
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    provider = LMStudioSemanticAuthorProvider(base_url="http://127.0.0.1:1234/v1", model="local")
    completion = provider.complete(provider_request(input_pack), SemanticAuthorPassOptions())
    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert calls[0]["response_format"]["type"] == "json_schema"
    serialized_schema = json.dumps(calls[0]["response_format"]["json_schema"]["schema"])
    assert "$ref" not in serialized_schema
    assert all(
        keyword not in serialized_schema
        for keyword in ('"allOf"', '"contains"', '"oneOf"', '"uniqueItems"')
    )
    assert provider.base_url == "http://127.0.0.1:1234"


def test_lm_studio_rejects_remote_or_credentialed_urls() -> None:
    for url in ("https://example.com", "http://token@127.0.0.1:1234"):
        with pytest.raises(ValueError):
            LMStudioSemanticAuthorProvider(base_url=url, model="local")


def test_codex_adapter_is_bounded_and_uses_read_only_temporary_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    command: list[str] = []
    inputs: list[str] = []
    schemas: list[dict] = []
    input_pack = pack(tmp_path)

    def fake_run(args: list[str], **kwargs: object) -> object:
        command.extend(args)
        inputs.append(str(kwargs["input"]))
        schemas.append(json.loads(Path(args[args.index("--output-schema") + 1]).read_text()))
        Path(args[args.index("--output-last-message") + 1]).write_text(
            json.dumps(transport_proposal(input_pack))
        )
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    assert (
        CodexSparkSemanticAuthorProvider()
        .complete(
            provider_request(input_pack),
            SemanticAuthorPassOptions(),
        )
        .payload["candidateId"]
        == input_pack["candidateId"]
    )
    assert command[0:2] == ["codex", "exec"]
    assert "read-only" in command and "gpt-5.3-codex-spark" in command
    assert "--ephemeral" in command and "--output-schema" in command
    serialized_schema = json.dumps(schemas[0])
    assert "$ref" not in serialized_schema
    assert all(
        keyword not in serialized_schema
        for keyword in ('"allOf"', '"contains"', '"oneOf"', '"uniqueItems"')
    )
    assert "requiredJsonShape" in inputs[0]


def test_receipt_whitelist_discards_provider_supplied_sensitive_fields(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)

    class SensitiveReceiptProvider(FakeProvider):
        def complete(self, request: dict, options: SemanticAuthorPassOptions) -> ProviderCompletion:
            completion = super().complete(request, options)
            return ProviderCompletion(
                payload=completion.payload,
                receipt={
                    **completion.receipt,
                    "rawPrompt": "secret prompt",
                    "rawResponse": "secret response",
                    "credential": "secret token",
                    "privateMachinePath": "/private/workspace",
                },
            )

    report = run_semantic_author_pass(input_pack, SensitiveReceiptProvider(proposal(input_pack)))
    serialized = json.dumps(report["providerReceipt"])
    for forbidden in ("secret", 'rawPrompt"', 'rawResponse"', "credential", "/private"):
        assert forbidden not in serialized


def test_receipt_whitelist_normalizes_only_bounded_metadata(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)

    class MetadataProvider(FakeProvider):
        def complete(self, request: dict, options: SemanticAuthorPassOptions) -> ProviderCompletion:
            return ProviderCompletion(
                payload=copy.deepcopy(self.proposal),
                receipt={
                    "providerKind": "test",
                    "providerName": "test_provider",
                    "modelId": "test-model",
                    "durationMs": 2,
                    "baseUrl": "http://127.0.0.1:1234",
                    "endpoint": "/v1/chat/completions",
                    "usage": {"input_tokens": 10, "ignored": "unknown"},
                    "jsonRepairNeeded": True,
                    "jsonRepairAttemptCount": 1,
                    "jsonRepairStatus": "repaired",
                },
            )

    receipt = run_semantic_author_pass(input_pack, MetadataProvider(proposal(input_pack)))[
        "providerReceipt"
    ]
    assert receipt["modelId"] == "test-model"
    assert receipt["baseUrl"] == "http://127.0.0.1:1234"
    assert receipt["endpoint"] == "/v1/chat/completions"
    assert receipt["usage"] == {"input_tokens": 10}
    assert receipt["jsonRepairStatus"] == "repaired"


def test_receipt_whitelist_rejects_invalid_fixed_fields(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)

    class InvalidReceiptProvider(FakeProvider):
        def complete(self, request: dict, options: SemanticAuthorPassOptions) -> ProviderCompletion:
            return ProviderCompletion(
                payload=copy.deepcopy(self.proposal),
                receipt={"providerKind": "test", "durationMs": -1},
            )

    with pytest.raises(SemanticAuthorPassError, match="duration is invalid"):
        run_semantic_author_pass(input_pack, InvalidReceiptProvider(proposal(input_pack)))


def test_rejects_stale_pack_digest_before_provider_invocation(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    input_pack["sourceBundleSha256"] = "f" * 64
    provider = FakeProvider(proposal(input_pack))

    with pytest.raises(ValueError, match="request is malformed"):
        run_semantic_author_pass(input_pack, provider)

    assert provider.requests == []


@pytest.mark.parametrize(
    "field",
    ("rationaleClaimId", "userNeedClaimId", "nonGoalClaimIds"),
)
def test_rejects_intent_decisions_with_unknown_claims(tmp_path: Path, field: str) -> None:
    input_pack = pack(tmp_path)
    invalid = proposal(input_pack)
    decision = invalid["intentDecisions"][0 if field == "rationaleClaimId" else 1]
    decision[field] = ["missing_claim"] if field == "nonGoalClaimIds" else "missing_claim"

    with pytest.raises(SemanticAuthorPassError, match="unknown claim"):
        run_semantic_author_pass(input_pack, FakeProvider(invalid))


def test_codex_repairs_malformed_json_within_budget(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    outputs = iter(("not json", json.dumps(transport_proposal(input_pack))))

    def fake_run(args: list[str], **kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )
    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert completion.receipt["jsonRepairNeeded"] is True
    assert completion.receipt["jsonRepairAttemptCount"] == 1


def test_codex_unwraps_only_a_single_known_proposal_envelope(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)

    def fake_run(args: list[str], **_kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(
            json.dumps({"proposal": transport_proposal(input_pack)})
        )
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack), SemanticAuthorPassOptions()
    )
    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert completion.receipt["jsonRepairNeeded"] is False


def test_codex_repairs_invalid_known_proposal_envelope(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    outputs = iter(
        (
            json.dumps({"proposal": None}),
            json.dumps(transport_proposal(input_pack)),
        )
    )

    def fake_run(args: list[str], **_kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )
    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert completion.receipt["jsonRepairNeeded"] is True
    assert completion.receipt["jsonRepairAttemptCount"] == 1


def test_transport_state_discards_only_inactive_intent_branch_padding(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    padded = transport_proposal(input_pack)
    reuse = padded["intentDecisions"][0]
    reuse.update(
        {
            "userNeedClaimId": "inactive_value",
            "nearbyIntentIds": ["intent.inactive"],
            "nearbyIntentClaimIds": ["inactive_claim"],
            "nonGoalClaimIds": ["inactive_claim"],
        }
    )

    def fake_run(args: list[str], **_kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(json.dumps(padded))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack), SemanticAuthorPassOptions()
    )
    normalized = completion.payload["intentDecisions"][0]
    assert normalized["state"] == "proposed_reuse"
    assert normalized["rationaleClaimId"] == reuse["rationaleClaimId"]
    assert "userNeedClaimId" not in normalized
    assert "nearbyIntentIds" not in normalized
    assert "nearbyIntentClaimIds" not in normalized
    assert "nonGoalClaimIds" not in normalized


def test_codex_provider_pins_model_reasoning_effort(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    command: list[str] = []

    def fake_run(args: list[str], **_kwargs: object) -> object:
        command.extend(args)
        Path(args[args.index("--output-last-message") + 1]).write_text(
            json.dumps(transport_proposal(input_pack))
        )
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider(
        model="gpt-5.6-luna", reasoning_effort="low"
    ).complete(provider_request(input_pack), SemanticAuthorPassOptions())

    assert command[command.index("--model") + 1] == "gpt-5.6-luna"
    assert command[command.index("-c") + 1] == 'model_reasoning_effort="low"'
    assert completion.receipt["providerName"] == "gpt-5.6-luna"
    assert completion.receipt["reasoningEffort"] == "low"


@pytest.mark.parametrize(
    ("decision_index", "api_version", "kind"),
    (
        (
            0,
            "spec-harvester.ai-semantic-intent-reuse/v0",
            "SpecHarvesterAISemanticIntentReuse",
        ),
        (
            1,
            "spec-harvester.ai-semantic-experimental-intent/v0",
            "SpecHarvesterAISemanticExperimentalIntent",
        ),
    ),
)
def test_transport_state_normalizes_intent_branch_discriminators(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    decision_index: int,
    api_version: str,
    kind: str,
) -> None:
    input_pack = pack(tmp_path)
    malformed = transport_proposal(input_pack)
    decision = malformed["intentDecisions"][decision_index]
    decision.update({"apiVersion": "wrong", "kind": "Wrong", "schemaVersion": 99})

    def fake_run(args: list[str], **_kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(json.dumps(malformed))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack), SemanticAuthorPassOptions()
    )
    normalized = completion.payload["intentDecisions"][decision_index]
    assert normalized["apiVersion"] == api_version
    assert normalized["kind"] == kind
    assert normalized["schemaVersion"] == 1


def test_codex_repairs_schema_conformance_failure_with_diagnostic(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    malformed = transport_proposal(input_pack)
    malformed["apiVersion"] = "wrong-api"
    outputs = iter((json.dumps(malformed), json.dumps(transport_proposal(input_pack))))
    prompts: list[str] = []

    def fake_run(args: list[str], **kwargs: object) -> object:
        prompts.append(str(kwargs["input"]))
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )
    assert completion.receipt["jsonRepairNeeded"] is True
    assert completion.receipt["jsonRepairAttemptCount"] == 1
    assert "transport schema violation" in prompts[1]


def test_codex_repairs_cross_record_conformance_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    malformed = transport_proposal(input_pack)
    malformed["intentDecisions"][0]["rationaleClaimId"] = "missing_claim"
    outputs = iter((json.dumps(malformed), json.dumps(transport_proposal(input_pack))))
    prompts: list[str] = []

    def fake_run(args: list[str], **kwargs: object) -> object:
        prompts.append(str(kwargs["input"]))
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )
    assert completion.receipt["jsonRepairNeeded"] is True
    assert "references an unknown claim" in prompts[1]
    repair_messages = json.loads(prompts[1])
    assert [message["role"] for message in repair_messages] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert json.loads(repair_messages[1]["content"])["evidence"] == input_pack["evidence"]
    repair_request = json.loads(repair_messages[3]["content"])
    assert repair_request["allowedEvidenceBindings"] == input_pack["request"]["evidence"]
    assert repair_request["observedIntentBindings"] == [
        {
            "intentId": item["intentId"],
            "observedIntentSha256": item["observedIntentSha256"],
        }
        for item in input_pack["observedIntents"]
    ]


def test_codex_repairs_specific_purpose_generic_only_contradiction(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path, catalog_override=routed_catalog())
    malformed = transport_proposal(input_pack)
    malformed["intentDecisions"] = [malformed["intentDecisions"][0]]
    repaired = transport_proposal(input_pack)
    repaired["intentDecisions"] = [repaired["intentDecisions"][1]]
    outputs = iter((json.dumps(malformed), json.dumps(repaired)))
    prompts: list[str] = []

    def fake_run(args: list[str], **kwargs: object) -> object:
        prompts.append(str(kwargs["input"]))
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )

    assert completion.receipt["jsonRepairNeeded"] is True
    assert completion.payload["intentDecisions"][0]["state"] == "proposed_experimental"
    assert "specific semantic purpose cannot use only a generic" in prompts[1]


def test_codex_repairs_frozen_semantic_focus_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    malformed = transport_proposal(input_pack)
    repaired = transport_proposal(input_pack)
    repaired["claims"][0]["text"] = "Help users reduce token context."
    repaired["claims"][1]["text"] = "Compress command output."
    outputs = iter((json.dumps(malformed), json.dumps(repaired)))
    prompts: list[str] = []

    def fake_run(args: list[str], **kwargs: object) -> object:
        prompts.append(str(kwargs["input"]))
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    request = provider_request(input_pack)
    request["semanticFocus"] = {
        "purposeConceptGroups": [["token"], ["reduce"]],
        "specificTerms": ["command"],
    }
    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        request, SemanticAuthorPassOptions(json_repair_max_attempts=1)
    )

    assert completion.receipt["jsonRepairNeeded"] is True
    assert "purpose misses a required exact term group" in prompts[1]


def test_lm_studio_repairs_schema_fragment_value(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    malformed = transport_proposal(input_pack)
    malformed["candidateId"] = {"$ref": "#/$defs/candidateId"}
    contents = iter((json.dumps(malformed), json.dumps(transport_proposal(input_pack))))

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: object) -> None:
            pass

        def read(self, size: int = -1) -> bytes:
            return json.dumps(
                {
                    "model": "local",
                    "choices": [{"message": {"content": next(contents)}}],
                }
            ).encode()[:size]

    monkeypatch.setattr("urllib.request.urlopen", lambda *_args, **_kwargs: Response())
    completion = LMStudioSemanticAuthorProvider(
        base_url="http://127.0.0.1:1234", model="local"
    ).complete(
        provider_request(input_pack),
        SemanticAuthorPassOptions(json_repair_max_attempts=1),
    )
    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert completion.receipt["jsonRepairNeeded"] is True


def test_codex_rejects_output_before_unbounded_read(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(args: list[str], **kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_bytes(b"x" * 9)
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    with pytest.raises(SemanticAuthorPassError, match="byte budget exceeded"):
        CodexSparkSemanticAuthorProvider().complete(
            {}, SemanticAuthorPassOptions(max_output_bytes=8)
        )


def test_lm_studio_repairs_json_and_bounds_response_reads(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    input_pack = pack(tmp_path)
    bodies = iter(
        (
            b'{"model":"local","choices":[{"message":{"content":"bad"}}]}',
            json.dumps(
                {
                    "model": "local",
                    "choices": [
                        {"message": {"content": json.dumps(transport_proposal(input_pack))}}
                    ],
                }
            ).encode(),
        )
    )
    read_sizes: list[int] = []

    class Response:
        def __init__(self) -> None:
            self.body = next(bodies)

        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: object) -> None:
            pass

        def read(self, size: int = -1) -> bytes:
            read_sizes.append(size)
            return self.body[:size]

    monkeypatch.setattr("urllib.request.urlopen", lambda *_args, **_kwargs: Response())
    completion = LMStudioSemanticAuthorProvider(
        base_url="http://127.0.0.1:1234", model="local"
    ).complete(provider_request(input_pack), SemanticAuthorPassOptions(max_output_bytes=16_384))

    assert completion.payload["candidateId"] == input_pack["candidateId"]
    assert completion.receipt["jsonRepairAttemptCount"] == 1
    assert read_sizes == [16_385, 16_385]


def test_lm_studio_rejects_oversized_response_while_reading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: object) -> None:
            pass

        def read(self, size: int = -1) -> bytes:
            return b"x" * size

    monkeypatch.setattr("urllib.request.urlopen", lambda *_args, **_kwargs: Response())
    with pytest.raises(SemanticAuthorPassError, match="byte budget exceeded"):
        LMStudioSemanticAuthorProvider(base_url="http://127.0.0.1:1234", model="local").complete(
            {}, SemanticAuthorPassOptions(max_output_bytes=8)
        )
