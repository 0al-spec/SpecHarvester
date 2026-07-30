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
    assert provider.requests == [input_pack["request"]]
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

        def read(self) -> bytes:
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
        .complete({"candidateId": "demo"}, SemanticAuthorPassOptions())
        .payload
        == {}
    )
    assert command[0:2] == ["codex", "exec"]
    assert "read-only" in command and "gpt-5.3-codex-spark" in command
    assert "requiredProposalSchema" in inputs[0]
