from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "specnode_live_retry_smoke.py"
SPEC = importlib.util.spec_from_file_location("specnode_live_retry_smoke", SCRIPT)
assert SPEC is not None
live_smoke = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = live_smoke
SPEC.loader.exec_module(live_smoke)


def test_live_smoke_config_requires_explicit_environment() -> None:
    with pytest.raises(live_smoke.LiveSmokeConfigError, match="SPECHARVESTER"):
        live_smoke.LiveSmokeConfig.from_env({})

    with pytest.raises(live_smoke.LiveSmokeConfigError, match="RUN_LIVE"):
        live_smoke.LiveSmokeConfig.from_env(
            {
                live_smoke.BASE_URL_ENV: "http://127.0.0.1:1234",
                live_smoke.MODEL_ENV: "openai/gpt-oss-20b",
            },
            require_run_flag=True,
        )

    config = live_smoke.LiveSmokeConfig.from_env(
        {
            live_smoke.RUN_FLAG_ENV: "1",
            live_smoke.BASE_URL_ENV: "http://127.0.0.1:1234",
            live_smoke.MODEL_ENV: "openai/gpt-oss-20b",
            live_smoke.TIMEOUT_ENV: "7",
        },
        require_run_flag=True,
    )
    assert config.base_url == "http://127.0.0.1:1234"
    assert config.model == "openai/gpt-oss-20b"
    assert config.timeout_seconds == 7


def test_openai_compatible_chat_client_parses_gpt_oss_wrapped_json(monkeypatch) -> None:
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self) -> bytes:
            return json.dumps(
                {
                    "model": "openai/gpt-oss-20b",
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": (
                                    "<|channel|>final <|constrain|>json<|message|>"
                                    '{"status":"ok","purpose":"parser"}'
                                )
                            },
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 3,
                        "completion_tokens": 5,
                        "total_tokens": 8,
                    },
                }
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        assert request.full_url == "http://127.0.0.1:1234/v1/chat/completions"
        assert timeout == 11
        return FakeResponse()

    monkeypatch.setattr(live_smoke.urllib.request, "urlopen", fake_urlopen)
    client = live_smoke.OpenAICompatibleChatClient(
        live_smoke.LiveSmokeConfig(
            base_url="http://127.0.0.1:1234",
            model="openai/gpt-oss-20b",
            timeout_seconds=11,
        )
    )

    result = client.chat_json(
        purpose="parser-test",
        messages=[{"role": "user", "content": "return json"}],
    )

    assert result.payload == {"status": "ok", "purpose": "parser"}
    assert result.model == "openai/gpt-oss-20b"
    assert result.usage["total_tokens"] == 8


def test_live_retry_smoke_runs_two_attempts_without_network(monkeypatch) -> None:
    class FakeClient:
        def __init__(self, config):
            self.config = config
            self.calls = []

        def chat_json(self, *, purpose, messages):
            self.calls.append({"purpose": purpose, "messages": messages})
            if purpose == "semantic-review":
                payload = {
                    "verdict": "needs_revision" if len(self.calls) <= 2 else "approve",
                    "summary": f"{purpose} summary",
                }
            else:
                payload = {
                    "decision": "propose",
                    "summary": f"{purpose} summary {len(self.calls)}",
                }
            return live_smoke.ChatJSONResult(
                payload=payload,
                raw_content=json.dumps(payload),
                model=self.config.model,
                finish_reason="stop",
                usage={
                    "prompt_tokens": 10,
                    "completion_tokens": 4,
                    "total_tokens": 14,
                },
                duration_ms=1,
            )

    monkeypatch.setattr(live_smoke, "OpenAICompatibleChatClient", FakeClient)

    summary = live_smoke.run_live_retry_smoke(
        live_smoke.LiveSmokeConfig(
            base_url="http://127.0.0.1:1234",
            model="openai/gpt-oss-20b",
            timeout_seconds=5,
        )
    )

    assert summary["status"] == "approved"
    assert summary["attemptCount"] == 2
    assert summary["attemptStatuses"] == ["retry_scheduled", "approved"]
    assert summary["reviewVerdicts"] == ["needs_revision", "approve"]
    assert summary["retryContextSeenByProvider"] == [False, True]
    assert summary["tokenUsage"] == {
        "promptTokens": 40,
        "completionTokens": 16,
        "totalTokens": 56,
    }


@pytest.mark.skipif(
    os.environ.get(live_smoke.RUN_FLAG_ENV) != "1",
    reason="set SPECHARVESTER_RUN_LIVE_LM_STUDIO_SMOKE=1 to run live LM Studio smoke",
)
def test_live_lm_studio_retry_smoke() -> None:
    config = live_smoke.LiveSmokeConfig.from_env(require_run_flag=True)
    summary = live_smoke.run_live_retry_smoke(config)
    assert summary["attemptCount"] == 2
    assert summary["retryContextSeenByProvider"] == [False, True]
    assert summary["reviewVerdicts"] == ["needs_revision", "approve"]
    assert summary["status"] == "approved"
