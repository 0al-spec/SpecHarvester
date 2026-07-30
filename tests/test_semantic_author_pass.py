from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

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


def catalog() -> dict:
    payload = {
        "sourcePath": "catalog/observed.json",
        "intents": [{"intentId": "intent.package.javascript_library", "sha256": "a" * 64}],
    }
    return {
        **payload,
        "sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def pack(tmp_path: Path) -> dict:
    (tmp_path / "specs").mkdir()
    (tmp_path / "specpm.yaml").write_text(
        "kind: SpecPackage\nmetadata:\n  id: demo.package\npreview_only: true\n"
    )
    (tmp_path / "specs/core.spec.yaml").write_text("kind: BoundarySpec\n")
    (tmp_path / "harvest.json").write_text("{}")
    return build_semantic_author_input_pack(tmp_path, catalog())


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
    return result


def test_provider_neutral_pass_normalizes_contract_and_discards_raw_data(tmp_path: Path) -> None:
    input_pack = pack(tmp_path)
    provider = FakeProvider(proposal(input_pack))
    report = run_semantic_author_pass(input_pack, provider)
    assert provider.requests[0]["request"] == input_pack["request"]
    assert provider.requests[0]["observedIntents"] == input_pack["observedIntents"]
    assert provider.requests[0]["evidence"] == input_pack["evidence"]
    assert provider.requests[0]["evidence"][0]["content"]
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict] = []

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *_: object) -> None:
            pass

        def read(self, size: int = -1) -> bytes:
            return b'{"model":"local","choices":[{"message":{"content":"{}"}}]}'

    def fake_urlopen(request: object, timeout: float) -> Response:
        calls.append(json.loads(request.data.decode()))  # type: ignore[attr-defined]
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    provider = LMStudioSemanticAuthorProvider(base_url="http://127.0.0.1:1234/v1", model="local")
    assert provider.complete({"candidateId": "demo"}, SemanticAuthorPassOptions()).payload == {}
    assert calls[0]["response_format"]["type"] == "json_schema"
    assert provider.base_url == "http://127.0.0.1:1234"


def test_lm_studio_rejects_remote_or_credentialed_urls() -> None:
    for url in ("https://example.com", "http://token@127.0.0.1:1234"):
        with pytest.raises(ValueError):
            LMStudioSemanticAuthorProvider(base_url=url, model="local")


def test_codex_adapter_is_bounded_and_uses_read_only_temporary_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command: list[str] = []
    inputs: list[str] = []

    def fake_run(args: list[str], **kwargs: object) -> object:
        command.extend(args)
        inputs.append(str(kwargs["input"]))
        Path(args[args.index("--output-last-message") + 1]).write_text("{}")
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    assert (
        CodexSparkSemanticAuthorProvider()
        .complete(
            {"candidateId": "demo", "requiredJsonShape": {"type": "object"}},
            SemanticAuthorPassOptions(),
        )
        .payload
        == {}
    )
    assert command[0:2] == ["codex", "exec"]
    assert "read-only" in command and "gpt-5.3-codex-spark" in command
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


def test_codex_repairs_malformed_json_within_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    outputs = iter(("not json", "{}"))

    def fake_run(args: list[str], **kwargs: object) -> object:
        Path(args[args.index("--output-last-message") + 1]).write_text(next(outputs))
        return type("Completed", (), {"returncode": 0})()

    monkeypatch.setattr("spec_harvester.semantic_author_pass.subprocess.run", fake_run)
    completion = CodexSparkSemanticAuthorProvider().complete(
        {"requiredJsonShape": {}}, SemanticAuthorPassOptions(json_repair_max_attempts=1)
    )
    assert completion.payload == {}
    assert completion.receipt["jsonRepairNeeded"] is True
    assert completion.receipt["jsonRepairAttemptCount"] == 1


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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bodies = iter(
        (
            b'{"model":"local","choices":[{"message":{"content":"bad"}}]}',
            b'{"model":"local","choices":[{"message":{"content":"{}"}}]}',
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
    ).complete({}, SemanticAuthorPassOptions(max_output_bytes=1024))

    assert completion.payload == {}
    assert completion.receipt["jsonRepairAttemptCount"] == 1
    assert read_sizes == [1025, 1025]


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
